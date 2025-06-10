from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset

from db_agent.config import settings
from db_agent.prompt import DB_MCP_PROMPT

root_agent = LlmAgent(
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
