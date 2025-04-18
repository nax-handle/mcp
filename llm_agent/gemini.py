import asyncio
import os
from mcp import ClientSession
from mcp.client.sse import sse_client  
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI

async def run_agent():
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", 
        temperature=0,
        api_key=os.environ["GEMINI_API_KEY"],
        max_tokens=512,
    )
    
    async with sse_client("http://192.168.1.218:8000/sse") as streams:
        async with ClientSession(streams[0], streams[1]) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent = create_react_agent(llm, tools, debug=True)
            response = await agent.ainvoke({"messages": "Tên của tôi là gì?"})
            return response

if __name__ == "__main__":
    result = asyncio.run(run_agent())
    print("Kết quả phản hồi từ MCP agent sử dụng Google Gemini:")
    print(result)
