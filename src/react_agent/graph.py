from src.react_agent.tools import get_tools
from langgraph.prebuilt import create_react_agent
from src.agentwrap.easy_llm import load_chat_model
from src.react_agent.config import Configuration
from langchain_core.runnables import RunnableConfig
import asyncio
from src.agentwrap.logger import function_logger
from langchain.prompts import ChatPromptTemplate


# FIXME: tools are not working , need to fix it.
@function_logger()
def make_graph(config: RunnableConfig):
    from src.agentwrap.env import set_environment_variables

    status = set_environment_variables(langchain_project="langgraph-assistant")
    print(status)

    configurable = config.get("configurable", {})

    llm = configurable.get("model", "google/gemini-2.0-flash-001")
    selected_tools = configurable.get("selected_tools", ["add"])

    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. Use the add tool to add numbers when needed.",
            ),
            ("user", "{messages}"),
        ]
    )
    prompt = configurable.get("system_prompt", prompt_template)

    name = configurable.get("name", "ready_agent")

    graph = create_react_agent(
        name=name,
        model=load_chat_model(llm),
        tools=get_tools(selected_tools),
        prompt=prompt,
        config_schema=Configuration,
    )

    return graph
