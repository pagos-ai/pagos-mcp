from typing import Optional
import os
from mcp.server.fastmcp import FastMCP
from pagos_client import PagosClient, BinDataResponse

mcp = FastMCP("bin-data")


def format_bin_data(bin_data: Optional[BinDataResponse]) -> str:
    if not bin_data:
        return "No BIN data available"

    card = bin_data.card
    return f"""
Card Details:
-------------
Brand: {card.card_brand}
Type: {card.type}
Prepaid: {'Yes' if card.prepaid else 'No'}
Product: {card.product.product_name} ({card.product.product_id})

Bank Information:
----------------
Bank: {card.bank.name}

Country Information:
------------------
Country: {card.country.name}
Country Code: {card.country.alpha2}
Numeric Code: {card.country.numeric}

Technical Details:
----------------
BIN Range: {card.bin_min} - {card.bin_max}
Card Number Length: {card.number.length}
Correlation ID: {card.correlation_id}
"""


@mcp.tool()
async def get_bin_data_tool(bin: str) -> str:
    """
    Get BIN data for a given BIN number.

    Args:
        bin (str): The BIN number to get data for.
        ctx (Context): The MCP context containing the PagosClient.
    Returns:
        str: A formatted string containing the BIN data.
    """
    api_key = os.getenv("PAGOS_API_KEY")
    pagos_client = PagosClient(api_key=api_key)
    data = await pagos_client.get_bin_data(bin)
    if not data:
        return "Unable to retrieve BIN data or no BIN data found"
    return format_bin_data(data)


if __name__ == "__main__":
    mcp.run(transport="stdio")
