from pydantic import BaseModel, Field
from typing import List, Literal, Annotated

class Configuration(BaseModel):
    """The configuration for the agent"""

    system_prompt: str = Field(
        default="You are a helpful AI assistant",
        description="The system prompt to use for the agent's interactions"
        "This prompt sets the context and behavior of the agent.",
    )
    model: Annotated[
        Literal["openai/gpt-3.5-turbo", "openai/gpt-4-o"],
        {"__template_metadata__": {"kind": "llm"}}
    ] = Field(
        default="openai/gpt-3.5-turbo",
        description="The name of the language model to use for the agents main interactions"
        "should be in the format 'provider/model-id', e.g., 'openai/gpt-3.5-turbo', 'google/gemini-pro', 'mistral/mistral-7b'.",
    )
    
    selected_tools: List[
        Literal["search", "calculator", "code_interpreter", "web_scraper", "add"]
    ] = Field(
        default=["calculator"],
        description="The list of tools to use for the agent's interactions"
        "this list should contain the names of the tools that the agent can use to assist with tasks.",
    )



