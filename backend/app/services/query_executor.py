"""Query Executor - Executes SQL with timeout and safety"""

import sqlite3
import signal
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class TimeoutError(Exception):
    pass

class QueryExecutor:
    """Executes SQL queries safely"""
    
    def __init__(self, timeout_seconds: int = 30):
        self.timeout = timeout_seconds
    
    def execute(self, sql: str, db_path: str) -> List[Dict[str, Any]]:
        """Execute SQL query with timeout protection
        
        Args:
            sql: SQL query to execute
            db_path: Path to SQLite database
            
        Returns:
            List of dictionaries with results
        """
        try:
            conn = sqlite3.connect(db_path, timeout=self.timeout)
            conn.row_factory = sqlite3.Row  # Enable column name access
            cursor = conn.cursor()
            
            logger.info(f"Executing: {sql}")
            cursor.execute(sql)
            
            # Fetch all results
            rows = cursor.fetchall()
            
            # Convert to list of dicts
            results = [dict(row) for row in rows]
            
            conn.close()
            
            logger.info(f"Query returned {len(results)} rows")
            return results
            
        except sqlite3.OperationalError as e:
            logger.error(f"SQL execution error: {str(e)}")
            raise Exception(f"Query execution failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise Exception(f"Failed to execute query: {str(e)}")
