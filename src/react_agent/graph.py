"""Define a custom Reasoning and Action agent.

Works with a chat model with tool calling support.
"""

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
graph = create_agent(model, tools=[])