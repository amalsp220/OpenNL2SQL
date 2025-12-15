"""FastAPI Backend for OpenNL2SQL
Author: Amal SP
Created: December 2025
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import logging

from app.services.schema_service import SchemaService
from app.services.nl2sql_service import NL2SQLService
from app.services.sql_validator import SQLValidator
from app.services.query_executor import QueryExecutor
from app.services.explanation_service import ExplanationService
from app.services.memory_service import MemoryService
from app.db.database import get_database_path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="OpenNL2SQL API",
    description="AI-powered Natural Language to SQL Analytics System",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class QueryRequest(BaseModel):
    question: str
    session_id: Optional[str] = None
    db_path: Optional[str] = None

class QueryResponse(BaseModel):
    success: bool
    sql: Optional[str] = None
    results: Optional[List[Dict[str, Any]]] = None
    sql_explanation: Optional[str] = None
    results_explanation: Optional[str] = None
    error: Optional[str] = None
    session_id: str

# Initialize services
schema_service = SchemaService()
nl2sql_service = NL2SQLService()
sql_validator = SQLValidator()
query_executor = QueryExecutor()
explanation_service = ExplanationService()
memory_service = MemoryService()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "OpenNL2SQL API",
        "version": "1.0.0"
    }

@app.get("/schema")
async def get_schema(db_path: Optional[str] = None):
    """Get database schema"""
    try:
        db = db_path or get_database_path()
        schema = schema_service.get_schema(db)
        return {
            "success": True,
            "schema": schema
        }
    except Exception as e:
        logger.error(f"Schema error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process natural language query with auto-recovery"""
    session_id = request.session_id or memory_service.create_session()
    
    try:
        # Get database path
        db_path = request.db_path or get_database_path()
        
        # Get schema
        schema = schema_service.get_schema(db_path)
        
        # Get conversation context
        context = memory_service.get_context(session_id)
        
        # Generate SQL
        logger.info(f"Generating SQL for: {request.question}")
        sql = nl2sql_service.generate_sql(
            question=request.question,
            schema=schema,
            context=context
        )
        
        # Validate SQL
        validation = sql_validator.validate(sql)
        if not validation["valid"]:
            return QueryResponse(
                success=False,
                error=f"Invalid SQL: {validation['error']}",
                session_id=session_id
            )
        
        # Execute with auto-recovery
        results = None
        error_occurred = False
        
        try:
            results = query_executor.execute(sql, db_path)
        except Exception as exec_error:
            logger.warning(f"SQL execution failed: {str(exec_error)}")
            error_occurred = True
            
            # Auto-recovery: regenerate SQL with error feedback
            logger.info("Attempting auto-recovery...")
            corrected_sql = nl2sql_service.fix_sql(
                original_sql=sql,
                error=str(exec_error),
                schema=schema
            )
            
            # Validate corrected SQL
            corrected_validation = sql_validator.validate(corrected_sql)
            if not corrected_validation["valid"]:
                return QueryResponse(
                    success=False,
                    error=f"Auto-recovery failed: {corrected_validation['error']}",
                    session_id=session_id
                )
            
            # Retry execution
            try:
                results = query_executor.execute(corrected_sql, db_path)
                sql = corrected_sql  # Use corrected SQL
                logger.info("Auto-recovery successful!")
            except Exception as retry_error:
                return QueryResponse(
                    success=False,
                    error=f"Query failed after auto-recovery: {str(retry_error)}",
                    session_id=session_id
                )
        
        # Generate explanations
        sql_explanation = explanation_service.explain_sql(sql, request.question)
        results_explanation = explanation_service.explain_results(results, request.question)
        
        # Store in memory
        memory_service.add_interaction(
            session_id=session_id,
            question=request.question,
            sql=sql,
            results=results
        )
        
        return QueryResponse(
            success=True,
            sql=sql,
            results=results,
            sql_explanation=sql_explanation,
            results_explanation=results_explanation,
            session_id=session_id
        )
        
    except Exception as e:
        logger.error(f"Query processing error: {str(e)}")
        return QueryResponse(
            success=False,
            error=str(e),
            session_id=session_id
        )

@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Get session history"""
    try:
        context = memory_service.get_context(session_id)
        return {
            "success": True,
            "session_id": session_id,
            "history": context
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail="Session not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
