# TestAgentAI
First AgentAI
# AgentAI – CLI AI Agent with LangGraph

A simple AI Agent built with **LangGraph + LangChain**, supporting:
- Tool calling
- Semantic search
- Calculator
- CLI interaction

## Features
- CLI-based AI agent
- Tool routing with LangGraph
- Modular tool system
- OpenAI-compatible LLM integration

## Tools
- **Search Tool**: Returns popular Python libraries for semantic search
- **Calculator Tool**: Evaluates math expressions

## Requirements
- Python 3.10+
- OpenAI API key

## Setup

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

export OPENAI_API_KEY="your_api_key"
# Windows PowerShell:
$env:OPENAI_API_KEY="your_api_key"
run >> python agent.py
