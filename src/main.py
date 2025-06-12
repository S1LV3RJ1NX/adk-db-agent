from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.agents.call_agent import run_conversation
from src.shared_libraries.logger import logger

# Initialize FastAPI app
app = FastAPI(
    title="DB Agent API", description="API service for the DB Agent", version="1.0.0"
)


# Request models
class ConversationRequest(BaseModel):
    session_id: str
    query: str


class ConversationResponse(BaseModel):
    session_id: str
    response: str


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "DB Agent API is running"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/conversation", response_model=ConversationResponse)
async def create_conversation(request: ConversationRequest):
    """
    Process a conversation query and return the agent's response

    Args:
        request: ConversationRequest containing query, user_id, and optional session_id

    Returns:
        ConversationResponse with the agent's response
    """
    try:
        logger.info(f"Processing conversation request for session {request.session_id}")

        # Call the agent
        # Every new session is assumed as a new user conversation
        response = await run_conversation(
            session_id=request.session_id,
            user_id=request.session_id,
            query=request.query,
        )

        logger.info(
            f"Successfully processed conversation for session {request.session_id}"
        )

        return ConversationResponse(
            session_id=request.session_id,
            response=response,
        )

    except Exception as e:
        logger.error(f"Error processing conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "src.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
    )
