# from mcp.server.fastmcp import FastMCP

# mcp = FastMCP("Demo")


# @mcp.tool()
# def add(a: int, b: int) -> int:
#     """Add two numbers"""
#     print('add tools')
#     return a - b

# @mcp.tool()
# def get_greeting(name: str) -> str:
#     """Get a personalized greeting"""
#     return f"Hello cl, {name}!"

# @mcp.resource("greeting://{name}")
# def get_greeting(name: str) -> str:
#     return f"Hello cc, {name}!"


# if __name__ == "__main__":
#     mcp.run(transport="sse")

# example_mcp.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ExampleServer")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Tool: Cộng hai số"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Tool: Nhân hai số"""
    return a * b

@mcp.tool()
def get_data() -> dict:
    """Resource: Trả về dữ liệu mẫu"""
    return {"status": "active", "data": [10, 20, 30]}

@mcp.tool()
def my_name() -> str:
    """Tool: Trả về tên của tôi"""
    return "Minh Nguyen - Nax"

@mcp.tool()
def welcome_prompt(name: str) -> str:
    """Prompt: Tạo lời chào mừng dựa trên tên người dùng"""
    return f"Xin chào {name}! Chào mừng bạn đến với ExampleServer."

if __name__ == "__main__":
    mcp.run(transport="sse")
