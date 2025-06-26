from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get weather for a particular location."""
    return f"The weather in {location} is sunny with 22°C temperature"

if __name__ == "__main__":
    # Run using streamable HTTP transport
    mcp.run(transport="streamable-http")
