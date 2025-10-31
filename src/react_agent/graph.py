"""Define a custom Reasoning and Action agent.

Works with a chat model with tool calling support.
"""

from datetime import datetime

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from react_agent import tools
from react_agent.prompts import SYSTEM_PROMPT


def graph():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    system_prompt = SYSTEM_PROMPT.format(
        system_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    agent = create_agent(model, tools=tools.TOOLS, system_prompt=system_prompt)
    return agent
