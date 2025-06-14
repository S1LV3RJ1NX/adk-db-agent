from google.adk.agents.llm_agent import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset

from src.agents.db_agent.prompt import DB_MCP_PROMPT
from src.shared_libraries.config import settings
from src.shared_libraries.logger import logger


def create_root_agent():
    """Creates the root agent with MCP tools."""

    agent = LlmAgent(
        model=LiteLlm(
            model=f"openai/{settings.LLM_MODEL}",
            api_base=settings.LLM_API_BASE,
            api_key=settings.LLM_API_KEY,
            extra_headers={
                "Authorization": f"Bearer {settings.LLM_API_KEY}",
                "X-TFY-METADATA": '{"tfy_log_request":"true"}',
            },
        ),
        name="db_agent",
        instruction=DB_MCP_PROMPT,
        tools=[
            MCPToolset(
                connection_params=StreamableHTTPServerParams(
                    url=settings.MCP_SERVER_URL,
                    timeout=20,
                ),
            )
        ],
    )
    logger.info(f"Agent {agent.name} created successfully.")
    return agent


root_agent = create_root_agent()
