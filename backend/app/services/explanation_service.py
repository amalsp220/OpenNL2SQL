"""Explanation Service - Generates plain English explanations"""

import os
from typing import List, Dict, Any
import logging
from groq import Groq

logger = logging.getLogger(__name__)

class ExplanationService:
    """Generates human-readable explanations using LLM"""
    
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found")
        self.client = Groq(api_key=api_key)
        self.model = "mixtral-8x7b-32768"
    
    def explain_sql(self, sql: str, question: str) -> str:
        """Explain what the SQL query does in plain English"""
        
        prompt = f"""You are a SQL expert explaining queries to non-technical users.

User asked: "{question}"

Generated SQL:
{sql}

Explain in 2-3 simple sentences what this SQL query does. Be clear and concise.

Explanation:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=200
            )
            
            explanation = response.choices[0].message.content.strip()
            logger.info("Generated SQL explanation")
            return explanation
            
        except Exception as e:
            logger.error(f"Explanation generation failed: {str(e)}")
            return "This query retrieves data from the database based on your question."
    
    def explain_results(self, results: List[Dict[str, Any]], question: str) -> str:
        """Explain query results in natural language"""
        
        if not results:
            return "No results found for your query."
        
        row_count = len(results)
        
        if row_count == 1 and len(results[0]) == 1:
            # Single value result (e.g., COUNT)
            value = list(results[0].values())[0]
            return f"The answer is: {value}"
        
        prompt = f"""Summarize these query results in 2-3 simple sentences.

User asked: "{question}"

Results ({row_count} rows):
{str(results[:5])}

Provide a clear summary:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=250
            )
            
            explanation = response.choices[0].message.content.strip()
            logger.info("Generated results explanation")
            return explanation
            
        except Exception as e:
            logger.error(f"Results explanation failed: {str(e)}")
            return f"Found {row_count} result(s) matching your query."
