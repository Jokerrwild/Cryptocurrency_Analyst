import urllib.request
import xml.etree.ElementTree as ET
import hashlib
import logging
from datetime import datetime
from typing import List, Dict, Any, Tuple

from .db import get_db_connection

logger = logging.getLogger("crypto_analyst.news_feed")

# Configure news sources
RSS_FEEDS = {
    "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "CoinTelegraph": "https://cointelegraph.com/rss",
    "The Block": "https://www.theblock.co/rss/all"
}

# Keyword-based categorization weights
EVENT_WEIGHTS = {
    "regulatory_cleared": 0.18,
    "regulatory_threat": -0.18,
    "macro_tightening": -0.15,
    "macro_easing": 0.15,
    "utility_threat": -0.25
}

# Categorization Keyword mappings
KEYWORD_MAPS = {
    "regulatory_cleared": ["approved", "cleared", "dismissed", "settled", "dropped", "victory", "ends investigation"],
    "regulatory_threat": ["probe", "lawsuit", "subpoena", "enforcement", "warns", "sues", "charges", "banned", "restrict"],
    "macro_tightening": ["fed rate hike", "hawkish", "rate hike", "inflation high", "tightening", "yields spike"],
    "macro_easing": ["rate cut", "dovish", "easing", "inflation cools", "yields drop"],
    "utility_threat": ["labeled", "deanonymized", "exploit", "hack", "breach", "vulnerability", "deanonymize", "tracing", "heuristics"]
}

def generate_headline_hash(title: str, source: str) -> str:
    """Generates a unique MD5 hash for deduplication."""
    raw_str = f"{title.strip().lower()}|{source.strip().lower()}"
    return hashlib.md5(raw_str.encode('utf-8')).hexdigest()

def parse_rss_feed(source_name: str, feed_url: str) -> List[Dict[str, str]]:
    """Fetches and parses a public RSS feed using standard library only."""
    logger.info(f"Fetching RSS feed from {source_name}: {feed_url}")
    articles = []
    try:
        # Set a standard User-Agent to avoid HTTP 403 Forbidden errors
        req = urllib.request.Request(
            feed_url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            
            for item in root.findall(".//item"):
                title = item.findtext("title", "").strip()
                link = item.findtext("link", "").strip()
                pub_date = item.findtext("pubDate", "").strip()
                description = item.findtext("description", "").strip()
                
                if title:
                    articles.append({
                        "title": title,
                        "source": source_name,
                        "published_at": pub_date,
                        "description": description
                    })
    except Exception as e:
        logger.warning(f"Failed to fetch RSS from {source_name}: {e}")
    return articles

def classify_headline(title: str, description: str) -> Tuple[str, float]:
    """Classifies a headline into an event type based on keyword matches."""
    text = f"{title} {description}".lower()
    
    # Priority match
    for category, keywords in KEYWORD_MAPS.items():
        for kw in keywords:
            if kw in text:
                return category, EVENT_WEIGHTS[category]
                
    return "neutral", 0.0

def ingest_and_score_news() -> Tuple[float, List[Dict[str, Any]]]:
    """Runs the ingestion pipeline for all feeds. Deduplicates and returns aggregate score."""
    logger.info("Starting RSS news ingestion and scoring cycle.")
    new_events = []
    aggregate_score = 0.0
    total_impactful_news = 0
    
    # Phase 1: Fetch and parse all feeds
    all_articles = []
    for name, url in RSS_FEEDS.items():
        all_articles.extend(parse_rss_feed(name, url))
        
    # Phase 2: Process and deduplicate against database
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for art in all_articles:
            title = art["title"]
            source = art["source"]
            h_hash = generate_headline_hash(title, source)
            
            # Check for duplicates
            cursor.execute("SELECT 1 FROM news_events WHERE headline_hash = ?", (h_hash,))
            if cursor.fetchone():
                continue # Already processed, skip
                
            # Classify event
            event_type, score = classify_headline(title, art["description"])
            
            # Insert into SQLite
            cursor.execute("""
                INSERT INTO news_events (headline_hash, title, source, event_type, score, published_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (h_hash, title, source, event_type, score, art["published_at"]))
            
            if event_type != "neutral":
                aggregate_score += score
                total_impactful_news += 1
                
            new_events.append({
                "title": title,
                "source": source,
                "event_type": event_type,
                "score": score,
                "published_at": art["published_at"]
            })
            
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Database transaction failed during news ingestion: {e}")
        raise e
        
    # Clamp aggregate sentiment score between [-1.0, 1.0]
    clamped_score = max(-1.0, min(1.0, aggregate_score))
    logger.info(f"Processed {len(new_events)} new news items. Clamped sentiment score: {clamped_score:.2f}")
    
    return clamped_score, new_events
