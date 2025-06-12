from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from src.agents.db_agent.agent import root_agent
from src.shared_libraries.constants import APP_NAME
from src.shared_libraries.logger import logger

# TODO: later replace with a session service factory
SESSION_SERVICE = InMemorySessionService()


async def create_runner(user_id: str, session_id: str):
    # Check if the session exists
    session = await SESSION_SERVICE.get_session(
        app_name=APP_NAME, user_id=user_id, session_id=session_id
    )

    if session is None:
        # Create the specific session where the conversation will happen
        logger.info(f"Creating new session {session_id} for user {user_id}")
        session = await SESSION_SERVICE.create_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )
    else:
        logger.info(f"Session {session_id} already exists for user {user_id}")

    runner = Runner(
        agent=root_agent,  # The agent we want to run
        app_name=APP_NAME,  # Associates runs with our app
        session_service=SESSION_SERVICE,  # Uses our session manager
    )
    logger.info(f"Runner created for {root_agent.name} successfully.")
    return runner
