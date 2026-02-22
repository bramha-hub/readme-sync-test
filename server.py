from mcp.server.fastmcp import FastMCP
# Create an MCP server
mcp = FastMCP("Demo")

print("Hello from server!")

@mcp.tool()
def usd_to_gbp(amount: float) -> float:
    """Convert USD(dollars) to GBP(pounds sterling)"""
    print("Hello from server!")
    EXCHANGE_RATE = 0.79
    return round (amount * EXCHANGE_RATE, 2)