import os
import json
import urllib.request
import urllib.parse
import hashlib
import logging
import re
from datetime import datetime
from typing import List

from .db import get_db_connection

logger = logging.getLogger("crypto_analyst.telegram_notifier")

# Path to Agent Zero core Telegram integration plugin settings
TELEGRAM_PLUGIN_CONFIG = "/a0/usr/plugins/_telegram_integration/config.json"

def get_telegram_credentials() -> tuple[str, str]:
    """
    Resolves Telegram bot token and chat ID. 
    First checks environmental variables, then falls back to direct parsing of the active 
    framework Telegram integration plugin config, then falls back to empty defaults.
    """
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    
    if (not token or not chat_id) and os.path.exists(TELEGRAM_PLUGIN_CONFIG):
        try:
            with open(TELEGRAM_PLUGIN_CONFIG, "r") as f:
                plugin_data = json.load(f)
                bots = plugin_data.get("bots", [])
                if bots:
                    bot = bots[0]
                    if not token:
                        token = bot.get("token", "")
                    if not chat_id and bot.get("allowed_users"):
                        chat_id = bot["allowed_users"][0]
                    logger.info(f"Successfully auto-loaded Telegram configurations from system plugin settings (Bot: {bot.get('name')})")
        except Exception as e:
            logger.warning(f"Could not auto-load system plugin configuration: {e}")
            
    return token, chat_id

def markdown_to_html(md_text: str) -> str:
    """
    Converts basic Markdown formatting to Telegram-compatible HTML tags.
    Escapes HTML entities first to prevent parse errors from special characters like < or &.
    Uses alphanumeric placeholders to avoid collision with formatting regexes.
    """
    # 1. Escape raw HTML entities to prevent parser crashes
    html = md_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    # 2. Convert preformatted code blocks: ```text ... ``` or ``` ... ``` to <pre>...</pre>
    # We use a purely alphanumeric placeholder with NO underscores or special characters
    code_blocks = []
    def save_block(match):
        code_blocks.append(match.group(1))
        return f"HTMLPLACEHOLDER{len(code_blocks)-1}BLOCK"
    
    html = re.sub(r"```(?:\w+)?\n(.*?)\n```", save_block, html, flags=re.DOTALL)
    
    # 3. Convert inline code spans `code` to <code>code</code>
    html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)
    
    # 4. Convert bold marks **text** to <b>text</b>
    html = re.sub(r"\*\*([^\*]+)\*\*", r"<b>\1</b>", html)
    
    # 5. Convert italic marks _text_ to <i>text</i>
    html = re.sub(r"_([^_]+)_", r"<i>\1</i>", html)
    
    # 6. Convert headers ### Header or ## Header or # Header to bold lines
    html = re.sub(r"^(?:###|##|#)\s+(.*?)$", r"<b>\1</b>", html, flags=re.MULTILINE)
    
    # Restore preformatted code blocks
    for i, block in enumerate(code_blocks):
        html = html.replace(f"HTMLPLACEHOLDER{i}BLOCK", f"<pre>{block}</pre>")
        
    return html

def split_report(report_text: str, max_chars: int = 4000) -> List[str]:
    """
    Intelligently splits a Markdown report into multiple messages without truncating words
    or breaking Markdown blocks, separating cleanly at section boundary headings.
    """
    if len(report_text) <= max_chars:
        return [report_text]
        
    chunks = []
    current_chunk = []
    current_length = 0
    
    lines = report_text.split('\n')
    
    for line in lines:
        is_header = line.strip().startswith('## ') or line.strip().startswith('# ') or line.strip().startswith('### ')
        line_len = len(line) + 1
        
        if (current_length + line_len > max_chars) or (is_header and current_length > max_chars * 0.6):
            if current_chunk:
                chunks.append('\n'.join(current_chunk).strip())
                current_chunk = []
                current_length = 0
        
        current_chunk.append(line)
        current_length += line_len
        
    if current_chunk:
        chunks.append('\n'.join(current_chunk).strip())
        
    return chunks

def log_delivery_audit(attempt: int, code: int, body_hash: str, msg_id: str, status: str) -> None:
    """Persists send statistics directly to the delivery_audit database table for verification."""
    utc_now = datetime.utcnow().isoformat() + "Z"
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO delivery_audit (timestamp, attempt_number, response_code, response_body_hash, confirmed_message_id, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (utc_now, attempt, code, body_hash, msg_id, status))
            conn.commit()
    except Exception as e:
        logger.error(f"Failed to log delivery audit checkpoint: {e}")

def send_telegram_report(report_text: str) -> List[str]:
    """
    Splits the structured analysis report, converts to HTML, and dispatches it to Telegram.
    Enforces strict API response verification, 3-retry exponential backoff,
    and records every attempt in the SQLite delivery_audit table.
    """
    token, chat_id = get_telegram_credentials()
    if not token or not chat_id:
        logger.warning("Telegram configurations not loaded. Skipping active network dispatch.")
        return []
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    delivered_message_ids = []
    
    # Split raw report into compliant chunks FIRST before converting to HTML
    chunks = split_report(report_text)
    logger.info(f"Report split into {len(chunks)} chunks for Telegram distribution.")
    
    for idx, chunk in enumerate(chunks):
        # Convert Markdown formatting to HTML safely
        html_chunk = markdown_to_html(chunk)
        
        payload = {
            "chat_id": chat_id,
            "text": html_chunk,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data)
        req.add_header('Content-Type', 'application/json')
        req.add_header('User-Agent', 'CryptoAnalystTelegramNotifier/1.2')
        
        success = False
        last_error = None
        for attempt in range(1, 4):
            try:
                with urllib.request.urlopen(req, timeout=15) as response:
                    status_code = response.getcode()
                    raw_resp = response.read()
                    resp_str = raw_resp.decode('utf-8')
                    body_hash = hashlib.md5(raw_resp).hexdigest()
                    
                    res_json = json.loads(resp_str)
                    
                    if res_json.get("ok") and "result" in res_json and "message_id" in res_json["result"]:
                        msg_id = str(res_json["result"]["message_id"])
                        delivered_message_ids.append(msg_id)
                        success = True
                        
                        log_delivery_audit(attempt, status_code, body_hash, msg_id, "success")
                        logger.info(f"Chunk {idx+1}/{len(chunks)} successfully dispatched (ID: {msg_id})")
                        break
                    else:
                        log_delivery_audit(attempt, status_code, body_hash, None, "missing_message_id")
                        raise RuntimeError(f"API response missing mandatory message_id: {resp_str}")
            except Exception as e:
                last_error = e
                logger.warning(f"Telegram dispatch attempt {attempt}/3 failed: {e}")
                log_delivery_audit(attempt, getattr(e, 'code', 500), "", None, "failed_attempt")
                if attempt < 3:
                    import time
                    time.sleep(attempt * 5)
                    
        if not success:
            raise last_error or RuntimeError(f"Failed to deliver Telegram chunk {idx+1} after 3 attempts.")
            
    return delivered_message_ids
