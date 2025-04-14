


import asyncio
import os
import shutil
import json
from typing import List, Any



import google.generativeai as genai

from agents import Agent, Runner
from agents.message import Message
from agents.models.base import ChatModel, ChatModelResponse
from agents.model_settings import ModelSettings
from agents.mcp import MCPServerSse, MCPServer

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
mcp_host = os.getenv("MCP_HOST")


genai.configure(api_key=api_key) 

class GeminiChatModel(ChatModel):
    def __init__(self, model="gemini-pro"):
        self.model = genai.GenerativeModel(model)

    async def chat(self, messages: List[Message]) -> ChatModelResponse:
        prompt = "\n".join([f"{m.role}: {m.content}" for m in messages])
        response = self.model.generate_content(prompt)

        return ChatModelResponse(
            message=response.text,
            raw=response.text
        )


async def run(mcp_server: MCPServer):
    agent = Agent(
        name="Gemini Assistant",
        model=GeminiChatModel(), 
        instructions="You are an intelligent assistant. Use tools when needed.",
        mcp_servers=[mcp_server],
        model_settings=ModelSettings(tool_choice="auto"),
    )

    message = "What is the temperature in Hanoi?"
    print(f"\n\n🧪 Running: {message}")
    result = await Runner.run(
        starting_agent=agent,
        input=[{"role": "user", "content": message}],
        max_turns=10
    )
    print("🧠 Final Answer:", result.final_output)
    print("📦 Raw responses:", result.raw_responses)


async def main():
    async with MCPServerSse(
        name="SSE Python Server",
        params={
            "url": f"{mcp_host}/sse",  
        },
    ) as server:
        await run(server)


if __name__ == "__main__":
    if not shutil.which("uv"):
        raise RuntimeError(
            "uv is not installed. Please install it: https://docs.astral.sh/uv/getting-started/installation/"
        )

    asyncio.run(main())
