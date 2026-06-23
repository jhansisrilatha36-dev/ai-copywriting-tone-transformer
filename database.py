import sqlite3
from datetime import datetime
import os

DB_NAME = "copywriting_history.db"

def get_db_connection(db_path=None):
    """
    Establish a connection to the SQLite database.
    """
    if db_path is None:
        # Default to copywriting-transformer folder database location
        dir_path = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(dir_path, DB_NAME)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def init_db(db_path=None):
    """
    Initialize the database and create the history table if it doesn't exist.
    """
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS generation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            product_name TEXT NOT NULL,
            description TEXT NOT NULL,
            platform TEXT NOT NULL,
            tone TEXT NOT NULL,
            prompt_version TEXT NOT NULL,
            prompt_compiled TEXT NOT NULL,
            generated_copy TEXT NOT NULL,
            temperature REAL NOT NULL,
            top_p REAL NOT NULL,
            quality_score REAL DEFAULT 0.0
        )
    """)
    conn.commit()
    conn.close()

def save_history(product_name, description, platform, tone, prompt_version, prompt_compiled, 
                 generated_copy, temperature, top_p, quality_score=0.0, db_path=None):
    """
    Save a generated copywriting record into the database.
    Returns the ID of the newly inserted row.
    """
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        INSERT INTO generation_history (
            timestamp, product_name, description, platform, tone, 
            prompt_version, prompt_compiled, generated_copy, temperature, top_p, quality_score
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp, product_name, description, platform, tone, 
        prompt_version, prompt_compiled, generated_copy, temperature, top_p, quality_score
    ))
    
    conn.commit()
    inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id

def get_history(limit=50, db_path=None):
    """
    Retrieve past generations from the database, ordered by timestamp descending.
    """
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, timestamp, product_name, description, platform, tone, 
               prompt_version, prompt_compiled, generated_copy, temperature, top_p, quality_score
        FROM generation_history
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    # Convert Row objects to dicts
    return [dict(row) for row in rows]

def update_quality_score(record_id, score, db_path=None):
    """
    Update the user quality score for a specific history record.
    """
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE generation_history
        SET quality_score = ?
        WHERE id = ?
    """, (score, record_id))
    
    conn.commit()
    conn.close()

def clear_history(db_path=None):
    """
    Clear all records from the history table.
    """
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM generation_history")
    conn.commit()
    conn.close()
