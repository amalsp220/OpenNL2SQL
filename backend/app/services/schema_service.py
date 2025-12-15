"""Schema Service - Extracts database schema for AI context"""

import sqlite3
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class SchemaService:
    """Extracts and formats database schema"""
    
    def get_schema(self, db_path: str) -> Dict[str, Any]:
        """Extract schema from SQLite database
        
        Returns:
            Dict with tables, columns, and relationships
        """
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            schema = {}
            
            for table in tables:
                # Get column info
                cursor.execute(f"PRAGMA table_info({table})")
                columns = []
                for row in cursor.fetchall():
                    col_info = {
                        "name": row[1],
                        "type": row[2],
                        "nullable": not row[3],
                        "primary_key": bool(row[5])
                    }
                    columns.append(col_info)
                
                # Get sample data (first 3 rows)
                cursor.execute(f"SELECT * FROM {table} LIMIT 3")
                sample_data = cursor.fetchall()
                
                schema[table] = {
                    "columns": columns,
                    "sample_count": len(sample_data)
                }
            
            conn.close()
            
            logger.info(f"Extracted schema for {len(schema)} tables")
            return schema
            
        except Exception as e:
            logger.error(f"Schema extraction failed: {str(e)}")
            raise Exception(f"Failed to extract schema: {str(e)}")
