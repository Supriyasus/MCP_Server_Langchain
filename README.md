# MCP Server with LangChain

A Model Context Protocol (MCP) server implementation using LangChain with math and weather tools.

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv/Scripts/activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

5. Add your Groq API key to `.env`:
   ```
   GROQ_API_KEY=your_actual_api_key_here
   ```

## Usage

Run the client:
```bash
python client.py
```

## Features

- Math operations (add, subtract, multiply, divide)
- Weather information (mock data)
- LangChain integration with Groq LLM