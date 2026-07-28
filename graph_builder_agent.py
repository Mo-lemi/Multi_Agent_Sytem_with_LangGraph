from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode, tools_condition
from agent_tools import wikipedia_tool, stock_data_tool, python_repl_tool

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

# Add three tools to the list: wikipedia_tool, stock_data_tool, and python_repl_tool
tools = [wikipedia_tool, stock_data_tool, python_repl_tool]

llm = ChatOpenAI(model="gpt-4o-mini")

# Tell the LLM which tools it can call
llm_with_tools = llm.bind_tools(tools)

def llm_node(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# Create the llm and tools nodes
graph_builder.add_node("llm", llm_node)
tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

# Add the edges
graph_builder.add_edge(START, "llm")
#The condition passes the llm neh, then triggers the right tool, executes that tool, then ends
#The add_conditional_edges tool returns a boolean. It checks the last response from the llm,to see if the tool was executed and if go byao, then it returns true.
# Power of Langchain 😝😝
graph_builder.add_conditional_edges("llm", tools_condition, ["tools", END])
graph_builder.add_edge("tools", "llm")

graph = graph_builder.compile()