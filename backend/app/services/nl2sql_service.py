"""NL2SQL Service - Converts natural language to SQL using Groq API"""

import os
import json
import re
from typing import Dict, List, Any, Optional
import logging
from groq import Groq

logger = logging.getLogger(__name__)

class NL2SQLService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        self.client = Groq(api_key=api_key)
        self.model = "mixtral-8x7b-32768"  # Using Mixtral for better SQL generation
    
    def generate_sql(self, question: str, schema: Dict[str, Any], context: List[Dict] = None) -> str:
        """Generate SQL from natural language question"""
        
        # Build context from conversation history
        context_str = ""
        if context:
            context_str = "\n\nPrevious conversation:\n"
            for i, interaction in enumerate(context[-3:]):  # Last 3 interactions
                context_str += f"Q{i+1}: {interaction['question']}\n"
                context_str += f"SQL{i+1}: {interaction['sql']}\n"
        
        # Create prompt
        prompt = f"""You are a SQL expert. Convert the natural language question to a valid SQL query.

Database Schema:
{json.dumps(schema, indent=2)}
{context_str}

Rules:
1. Generate ONLY SELECT queries
2. Use proper JOIN syntax when needed
3. Include appropriate WHERE clauses
4. Add LIMIT clause for large result sets
5. Use aggregate functions (COUNT, SUM, AVG) when appropriate
6. Return ONLY the SQL query, no explanations
7. Do not use markdown code blocks

Question: {question}

SQL Query:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,  # Low temperature for consistent SQL
                max_tokens=500
            )
            
            sql = response.choices[0].message.content.strip()
            
            # Clean up the SQL
            sql = self._clean_sql(sql)
            
            logger.info(f"Generated SQL: {sql}")
            return sql
            
        except Exception as e:
            logger.error(f"SQL generation failed: {str(e)}")
            raise Exception(f"Failed to generate SQL: {str(e)}")
    
    def fix_sql(self, original_sql: str, error: str, schema: Dict[str, Any]) -> str:
        """Auto-recovery: Fix SQL based on error message"""
        
        prompt = f"""You are a SQL debugging expert. The following SQL query failed with an error.

Database Schema:
{json.dumps(schema, indent=2)}

Original SQL:
{original_sql}

Error:
{error}

Please provide a corrected SQL query that fixes this error.
Return ONLY the corrected SQL query, no explanations or markdown.

Corrected SQL Query:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=500
            )
            
            corrected_sql = response.choices[0].message.content.strip()
            corrected_sql = self._clean_sql(corrected_sql)
            
            logger.info(f"Corrected SQL: {corrected_sql}")
            return corrected_sql
            
        except Exception as e:
            logger.error(f"SQL correction failed: {str(e)}")
            raise Exception(f"Failed to correct SQL: {str(e)}")
    
    def _clean_sql(self, sql: str) -> str:
        """Clean up SQL query"""
        # Remove markdown code blocks
        sql = re.sub(r'```sql\s*', '', sql)
        sql = re.sub(r'```\s*', '', sql)
        
        # Remove comments
        sql = re.sub(r'--.*$', '', sql, flags=re.MULTILINE)
        
        # Remove extra whitespace
        sql = ' '.join(sql.split())
        
        # Ensure ends with semicolon
        sql = sql.rstrip(';') + ';'
        
        return sql
