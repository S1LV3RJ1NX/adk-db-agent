from google.adk.runners import Runner
from google.genai import types

from src.agents.create_runner import create_runner
from src.shared_libraries.constants import DEFAULT_RESPONSE
from src.shared_libraries.logger import logger


async def call_agent_async(query: str, runner: Runner, user_id: str, session_id: str):
    """Sends a query to the agent and prints the final response."""
    logger.debug(f"User Query: {query}")

    content = types.Content(role="user", parts=[types.Part(text=query)])

    # TODO: add a default response
    final_response_text = DEFAULT_RESPONSE

    # Key Concept: run_async executes the agent logic and yields Events.
    # We iterate through events to find the final answer.
    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=content
    ):
        # You can uncomment the line below to see *all* events during execution
        # print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

        # Key Concept: is_final_response() marks the concluding message for the turn.
        if event.is_final_response():
            if event.content and event.content.parts:
                # Assuming text response in the first part
                final_response_text = event.content.parts[0].text
            elif (
                event.actions and event.actions.escalate
            ):  # Handle potential errors/escalations
                final_response_text = (
                    f"Agent escalated: {event.error_message or 'No specific message.'}"
                )
            # Add more checks here if needed (e.g., specific error codes)
            break  # Stop processing events once the final response is found

    logger.debug(f"Agent Response: {final_response_text}")
    return final_response_text


async def run_conversation(session_id: str, user_id: str, query: str):
    runner = await create_runner(user_id=user_id, session_id=session_id)
    response = await call_agent_async(
        query=query,
        runner=runner,
        user_id=user_id,
        session_id=session_id,
    )
    return response
