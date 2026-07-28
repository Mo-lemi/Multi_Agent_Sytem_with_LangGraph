# Multi_Agent_Sytem_with_LangGraph
A practice project for the building multi-agent system with LangGraph course. I'll be creating/building an agentic assistant to help retrieve and summarize information on Fortune 500 companies.

Tool 1 : wikipedia agent
Tool 2 : stock data agent
Tool 3 : visualisation agent
agent_tools.py = tool 1 + tool 2 + tool 3

graphy_bulder_agent.py = This module builds graphs .... eish, I am not sure. Still learning. ohh, I understand now. So we are building conditional edges. We are implementing them. So, I will rename the file. Anyway, the code I added, is catering for conditional edges.At first ( I forgot to push the code that has the version I am about to explain, but I'll explain it well so that you can visualize it.) there was code not catering for conditional edges neh. Korr when a user entered a message, the LLM would take the input but just return it without checking or without executing any of the tools to cater and answer the user. 🤔🤔 I hope I am on the right track . Still learning.