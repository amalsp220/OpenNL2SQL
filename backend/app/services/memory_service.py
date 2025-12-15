"""Memory Service - Manages conversation context"""

import uuid
from typing import List, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MemoryService:
    """Manages conversation history and context"""
    
    def __init__(self):
        self.sessions = {}  # In-memory storage (use Redis/DB for production)
    
    def create_session(self) -> str:
        """Create a new session"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "created_at": datetime.now(),
            "interactions": []
        }
        logger.info(f"Created session: {session_id}")
        return session_id
    
    def add_interaction(self, session_id: str, question: str, sql: str, results: List[Dict[str, Any]]):
        """Add interaction to session history"""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "created_at": datetime.now(),
                "interactions": []
            }
        
        self.sessions[session_id]["interactions"].append({
            "timestamp": datetime.now(),
            "question": question,
            "sql": sql,
            "results": results
        })
        
        logger.info(f"Added interaction to session {session_id}")
    
    def get_context(self, session_id: str) -> List[Dict[str, Any]]:
        """Get conversation context for a session"""
        if session_id not in self.sessions:
            return []
        
        return self.sessions[session_id]["interactions"]
