from dotenv import load_dotenv

load_dotenv()
from typing import Annotated
from typing_extensions import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
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

# Try using 'gemini-1.5-flash-latest' or 'gemini-2.5-flash'
# Change this line in graph_builder_agent.py:
llm = ChatGoogleGenerativeAI(model="lyria-3-pro-preview")

# Tell the LLM which tools it can call
llm_with_tools = llm.bind_tools(tools, tool_choice="auto")

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

# Visualize your graph
graph

for chunk in graph.stream(
    {"messages": [{"role": "user", "content": "Tell me about Apple Inc."}]}
):
    # Iterate over node outputs in each stream event
    for node_name, node_output in chunk.items():
        print(f"\n--- Output from node: {node_name} ---")
        for message in node_output.get("messages", []):
            print(f"[{message.type.upper()}]: {message.content}")