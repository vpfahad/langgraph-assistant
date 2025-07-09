from typing import Any
from langchain.tools import BaseTool


class AddTool(BaseTool):
    name: str = "add"
    description: str = "Adds two numbers together."

    def _run(self, a: float, b: float) -> float:
        return a + b

    async def _arun(self, a: float, b: float) -> float:
        return self._run(a, b)
# Example usage:
# model = load_chat_model("openai/gpt-4.1-mini")
def load_tool(tool_name: str = None, **kwargs) -> Any:
    """
    Load a tool by name.
    Args:
        tool_name (str, optional): Name of the tool, e.g., "add".
    Returns:
        Any: An instance of the loaded tool.
    """
    if tool_name is None:
        raise ValueError(
            "No tool_name specified. Please provide a tool_name, e.g., 'add'."
        )

    tool_name = tool_name.lower()
    if tool_name == "add":
        return AddTool(**kwargs)
    else:
        raise ValueError(f"Unknown tool '{tool_name}'.")


def get_tools(tool_names: list[str]):
    """Returns a list of tools based on the tool names."""
    tools = [load_tool(tool_name) for tool_name in tool_names]
    return tools