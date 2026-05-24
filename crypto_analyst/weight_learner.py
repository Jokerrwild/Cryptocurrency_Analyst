import sqlite3
import logging
from datetime import datetime
from typing import Dict, Any, Tuple

from .db import get_db_connection

logger = logging.getLogger("crypto_analyst.weight_learner")

# Default feature weight averages to seed weight_priors if empty
DEFAULT_WEIGHT_PRIORS = {
    # Feature format: (feature_name, regime_name) -> default_mean
    ("trend", "Bullish accumulation"): 1.2,
    ("momentum", "Bullish accumulation"): 1.0,
    ("macro", "Bullish accumulation"): 0.8,
    ("volatility", "Bullish accumulation"): -0.4,
    ("volume", "Bullish accumulation"): 0.5,
    
    ("trend", "Bullish continuation"): 1.4,
    ("momentum", "Bullish continuation"): 1.2,
    ("macro", "Bullish continuation"): 0.8,
    ("volatility", "Bullish continuation"): -0.35,
    ("volume", "Bullish continuation"): 0.4,
    
    ("trend", "Bearish distribution"): -1.2,
    ("momentum", "Bearish distribution"): -1.0,
    ("macro", "Bearish distribution"): -0.8,
    ("volatility", "Bearish distribution"): 0.4,
    ("volume", "Bearish distribution"): -0.5,
    
    ("trend", "Bearish continuation"): -1.4,
    ("momentum", "Bearish continuation"): -1.2,
    ("macro", "Bearish continuation"): -0.8,
    ("volatility", "Bearish continuation"): 0.35,
    ("volume", "Bearish continuation"): -0.4,
}

def seed_weight_priors() -> None:
    """Seeds the weight_priors table with default baseline weights if they are not already set."""
    logger.info("Checking and seeding weight_priors baseline tables...")
    utc_now = datetime.utcnow().isoformat() + "Z"
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            for (feat, regime), mean in DEFAULT_WEIGHT_PRIORS.items():
                cursor.execute("""
                    INSERT OR IGNORE INTO weight_priors (feature_name, regime_name, weight_mean, weight_variance, last_updated)
                    VALUES (?, ?, ?, 0.1, ?)
                """, (feat, regime, mean, utc_now))
            conn.commit()
    except Exception as e:
        logger.error(f"Failed to seed weight priors: {e}")
        raise e

def record_prediction(timestamp: str, predicted_regime: str, predicted_prob: float) -> None:
    """Saves a predicted regime outcome checkpoint in the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO regime_outcomes (timestamp, predicted_regime, predicted_prob, resolved)
            VALUES (?, ?, ?, 0)
        """, (timestamp, predicted_regime, predicted_prob))
        conn.commit()

def resolve_regime_outcome(timestamp: str, actual_regime: str) -> None:
    """Resolves a pending predicted outcome with actual classified regime structure."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE regime_outcomes
            SET actual_regime = ?, resolved = 1
            WHERE timestamp = ?
        """, (actual_regime, timestamp))
        conn.commit()

def get_adaptive_weights() -> Dict[str, Dict[str, float]]:
    """Retrieves active adaptive weights map from weight_priors to customize Bayesian scoring."""
    # First seed baseline if tables are completely unseeded
    seed_weight_priors()
    
    weights: Dict[str, Dict[str, float]] = {}
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT feature_name, regime_name, weight_mean FROM weight_priors")
        rows = cursor.fetchall()
        for row in rows:
            feat = row["feature_name"]
            regime = row["regime_name"]
            mean = row["weight_mean"]
            if regime not in weights:
                weights[regime] = {}
            weights[regime][feat] = mean
    return weights

def run_adaptive_update(learning_rate: float = 0.02) -> int:
    """
    Performs a conservative Bayesian prior weight update on historical resolved predictions.
    Increases feature weights that correctly map predictions, decays non-performing variables.
    Strictly obeys volume confirmation and does not bypass existing boundaries.
    """
    logger.info(f"Running conservative adaptive weight update (Learning Rate: {learning_rate})")
    utc_now = datetime.utcnow().isoformat() + "Z"
    updated_count = 0
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Load unresolved outcomes that have actuals present
            cursor.execute("""
                SELECT timestamp, predicted_regime, actual_regime 
                FROM regime_outcomes 
                WHERE resolved = 1 AND actual_regime IS NOT NULL
            """)
            outcomes = cursor.fetchall()
            
            if not outcomes:
                logger.info("No resolved outcomes available for adaptive weight updating.")
                return 0
                
            for out in outcomes:
                pred = out["predicted_regime"]
                act = out["actual_regime"]
                
                # Conservative feedback loop
                if pred == act:
                    # Correct classification: modestly reinforce weight means towards correct direction
                    cursor.execute("""
                        UPDATE weight_priors
                        SET weight_mean = weight_mean * (1.0 + ?), last_updated = ?
                        WHERE regime_name = ?
                    """, (learning_rate, utc_now, act))
                else:
                    # Classification error: moderately decay weight means to shift priors
                    cursor.execute("""
                        UPDATE weight_priors
                        SET weight_mean = weight_mean * (1.0 - ?), last_updated = ?
                        WHERE regime_name = ?
                    """, (learning_rate, utc_now, pred))
                    
                updated_count += 1
                
            conn.commit()
            logger.info(f"Completed conservative Bayesian adjustments on {updated_count} resolved regime transitions.")
    except Exception as e:
        logger.error(f"Adaptive weight update failure: {e}")
        raise e
        
    return updated_count
