"""SQL Validator - Security layer to prevent unsafe SQL operations"""

import re
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class SQLValidator:
    """Validates SQL queries for security and safety"""
    
    # Dangerous keywords that should be blocked
    BLOCKED_KEYWORDS = [
        'DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE',
        'TRUNCATE', 'REPLACE', 'MERGE', 'GRANT', 'REVOKE',
        'EXEC', 'EXECUTE', 'PRAGMA', 'ATTACH', 'DETACH'
    ]
    
    # Maximum number of rows to return
    MAX_ROWS = 1000
    
    def validate(self, sql: str) -> Dict[str, any]:
        """Validate SQL query for security and safety
        
        Returns:
            Dict with 'valid' (bool) and 'error' (str) keys
        """
        try:
            # Remove extra whitespace
            sql = ' '.join(sql.split())
            
            # Check if SQL is empty
            if not sql.strip():
                return {
                    "valid": False,
                    "error": "Empty SQL query"
                }
            
            # Check for blocked keywords
            sql_upper = sql.upper()
            for keyword in self.BLOCKED_KEYWORDS:
                if re.search(r'\b' + keyword + r'\b', sql_upper):
                    logger.warning(f"Blocked keyword detected: {keyword}")
                    return {
                        "valid": False,
                        "error": f"Blocked operation: {keyword} is not allowed. Only SELECT queries are permitted."
                    }
            
            # Ensure it's a SELECT query
            if not sql_upper.strip().startswith('SELECT'):
                return {
                    "valid": False,
                    "error": "Only SELECT queries are allowed"
                }
            
            # Check for comment-based injection attempts
            if '--' in sql or '/*' in sql or '*/' in sql:
                logger.warning("SQL comment detected")
                return {
                    "valid": False,
                    "error": "SQL comments are not allowed"
                }
            
            # Check for semicolon-based multi-statement attempts
            if sql.count(';') > 1:
                return {
                    "valid": False,
                    "error": "Multiple SQL statements not allowed"
                }
            
            # Add LIMIT if not present (safety measure)
            if 'LIMIT' not in sql_upper:
                sql = sql.rstrip(';')
                sql = f"{sql} LIMIT {self.MAX_ROWS};"
                logger.info(f"Added LIMIT clause: LIMIT {self.MAX_ROWS}")
            
            logger.info("SQL validation passed")
            return {
                "valid": True,
                "sql": sql
            }
            
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return {
                "valid": False,
                "error": f"Validation failed: {str(e)}"
            }
    
    def sanitize_input(self, value: str) -> str:
        """Sanitize user input to prevent injection
        
        Args:
            value: User input string
            
        Returns:
            Sanitized string
        """
        # Remove potential SQL injection characters
        dangerous_chars = ['--', ';', '/*', '*/', 'xp_', 'sp_']
        sanitized = value
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        return sanitized
