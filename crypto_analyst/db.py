import os
import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger("crypto_analyst.db")

DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "market_pulse.db")

def get_db_connection() -> sqlite3.Connection:
    """Establishes an active SQLite database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """Initializes all mandatory database schemas defined by the operational blueprint."""
    logger.info(f"Initializing persistent SQLite database at: {DB_PATH}")
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # 1. snapshots table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT UNIQUE NOT NULL,
                btc_price REAL NOT NULL,
                eth_price REAL NOT NULL,
                rsi REAL,
                trend_score REAL,
                momentum_score REAL,
                macro_support REAL,
                macro_risk REAL,
                raw_json TEXT NOT NULL
            )
        """)
        
        # 2. news_events table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS news_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                headline_hash TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                source TEXT NOT NULL,
                event_type TEXT NOT NULL,
                score REAL NOT NULL,
                published_at TEXT NOT NULL
            )
        """)
        
        # 3. regime_outcomes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS regime_outcomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT UNIQUE NOT NULL,
                predicted_regime TEXT NOT NULL,
                predicted_prob REAL NOT NULL,
                actual_regime TEXT,
                resolved INTEGER DEFAULT 0
            )
        """)
        
        # 4. weight_priors table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weight_priors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                feature_name TEXT NOT NULL,
                regime_name TEXT NOT NULL,
                weight_mean REAL NOT NULL,
                weight_variance REAL NOT NULL,
                last_updated TEXT NOT NULL,
                UNIQUE(feature_name, regime_name)
            )
        """)
        
        # 5. delivery_audit table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS delivery_audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                attempt_number INTEGER NOT NULL,
                response_code INTEGER,
                response_body_hash TEXT,
                confirmed_message_id TEXT,
                status TEXT NOT NULL
            )
        """)
        
        # 6. pipeline_runs / checkpoint_events table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pipeline_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                stage TEXT NOT NULL,
                status TEXT NOT NULL,
                message TEXT,
                UNIQUE(run_id, stage)
            )
        """)
        
        # 7. system_state table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_state (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        
        # Insert default state if absent
        cursor.execute("""
            INSERT OR IGNORE INTO system_state (key, value) 
            VALUES ('pipeline_frozen', 'false')
        """)
        
        conn.commit()
    logger.info("All 7 persistence tables initialized successfully.")

def is_pipeline_frozen() -> bool:
    """Reads the persistent freeze state of the orchestrator."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM system_state WHERE key = 'pipeline_frozen'")
            row = cursor.fetchone()
            return row is not None and row["value"].lower() == "true"
    except Exception:
        return False

def set_pipeline_frozen(frozen: bool) -> None:
    """Persists the orchestrator freeze state to prevent runaway executions."""
    val_str = "true" if frozen else "false"
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO system_state (key, value) 
            VALUES ('pipeline_frozen', ?) 
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """, (val_str,))
        conn.commit()

def log_checkpoint(run_id: str, stage: str, status: str, message: str = "") -> None:
    """Records stage-by-stage boundary checkpoint metrics for observability."""
    utc_now = datetime.utcnow().isoformat() + "Z"
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO pipeline_runs (run_id, timestamp, stage, status, message)
            VALUES (?, ?, ?, ?, ?)
        """, (run_id, utc_now, stage, status, message))
        conn.commit()

def prune_old_data(days_limit: int = 30) -> None:
    """Prunes database records older than the limit and reclaims space via VACUUM."""
    logger.info(f"Running data pruning routine (Retention Limit: {days_limit} days)")
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cutoff_query = f"-{days_limit} days"
            
            cursor.execute("DELETE FROM snapshots WHERE timestamp < datetime('now', ?)", (cutoff_query,))
            snapshots_deleted = cursor.rowcount
            
            cursor.execute("DELETE FROM news_events WHERE published_at < datetime('now', ?)", (cutoff_query,))
            news_deleted = cursor.rowcount
            
            cursor.execute("DELETE FROM pipeline_runs WHERE timestamp < datetime('now', ?)", (cutoff_query,))
            
            cursor.execute("DELETE FROM delivery_audit WHERE timestamp < datetime('now', ?)", (cutoff_query,))
            
            conn.commit()
            conn.isolation_level = None
            cursor.execute("VACUUM")
            conn.isolation_level = 'DEFERRED'
            conn.commit()
            
            # Prune physical report files older than days_limit
            reports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports")
            if os.path.exists(reports_dir):
                import time
                now = time.time()
                cutoff_sec = days_limit * 86400
                reports_deleted = 0
                for f in os.listdir(reports_dir):
                    if f.startswith("report_") and f.endswith(".md"):
                        fpath = os.path.join(reports_dir, f)
                        if now - os.path.getmtime(fpath) > cutoff_sec:
                            try:
                                os.remove(fpath)
                                reports_deleted += 1
                            except Exception as fe:
                                logger.warning(f"Could not delete stale local report file {f}: {fe}")
                if reports_deleted > 0:
                    logger.info(f"Pruned {reports_deleted} stale local report files from disk.")
                    
            logger.info(f"Pruned {snapshots_deleted} snapshots and {news_deleted} news events. Vacuum complete.")
    except Exception as e:
        logger.error(f"Failed to prune database: {e}")
        raise e
