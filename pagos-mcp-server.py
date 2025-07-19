from typing import Optional
import os
from mcp.server.fastmcp import FastMCP
from pagos_client import PagosClient, EnhancedBinApiResponse

mcp = FastMCP("bin-data")


def format_bin_data(bin_data: Optional[EnhancedBinApiResponse]) -> str:
    if not bin_data or not bin_data.card:
        return "No BIN data available"

    card = bin_data.card
    result = []

    # Basic card information
    result.append("Card Details:")
    result.append("-------------")
    if card.card_brand:
        result.append(f"Brand: {card.card_brand}")
    if card.type:
        result.append(f"Type: {card.type}")
    if card.prepaid is not None:
        result.append(f"Prepaid: {'Yes' if card.prepaid else 'No'}")
    if card.virtual_card is not None:
        result.append(f"Virtual Card: {'Yes' if card.virtual_card else 'No'}")
    if card.funding_source:
        result.append(f"Funding Source: {card.funding_source}")
    if card.card_segment_type:
        result.append(f"Card Segment Type: {card.card_segment_type}")
    if card.combo_card:
        result.append(f"Combo Card: {card.combo_card}")

    # Product information
    if card.product:
        result.append("")
        result.append("Product Information:")
        result.append("-------------------")
        if card.product.product_name:
            result.append(f"Product: {card.product.product_name}")
        if card.product.product_id:
            result.append(f"Product ID: {card.product.product_id}")

    # Bank information
    if card.bank:
        result.append("")
        result.append("Bank Information:")
        result.append("----------------")
        if card.bank.name:
            result.append(f"Bank: {card.bank.name}")
        if card.bank.clean_name:
            result.append(f"Clean Name: {card.bank.clean_name}")
        if card.bank.phone:
            result.append(f"Phone: {card.bank.phone}")
        if card.bank.url:
            result.append(f"URL: {card.bank.url}")

    # Country information
    if card.country:
        result.append("")
        result.append("Country Information:")
        result.append("-------------------")
        if card.country.name:
            result.append(f"Country: {card.country.name}")
        if card.country.alpha2:
            result.append(f"Country Code: {card.country.alpha2}")
        if card.country.numeric:
            result.append(f"Numeric Code: {card.country.numeric}")

    # Authentication information
    if card.authentication:
        result.append("")
        result.append("Authentication:")
        result.append("---------------")
        result.append(
            f"Authentication Required: {'Yes' if card.authentication.authentication_required else 'No'}"
        )
        if card.authentication.authentication_name:
            result.append(
                f"Authentication Name: {card.authentication.authentication_name}"
            )

    # Technical details
    result.append("")
    result.append("Technical Details:")
    result.append("-----------------")
    if card.bin_min and card.bin_max:
        result.append(f"BIN Range: {card.bin_min} - {card.bin_max}")
    if card.bin_length:
        result.append(f"BIN Length: {card.bin_length}")
    if card.pagos_bin_length:
        result.append(f"Pagos BIN Length: {card.pagos_bin_length}")
    if card.number and card.number.length:
        result.append(f"Card Number Length: {card.number.length}")
    if card.pan_or_token:
        result.append(f"PAN or Token: {card.pan_or_token}")
    if card.correlation_id:
        result.append(f"Correlation ID: {card.correlation_id}")

    # Additional features
    if any(
        [
            card.level2,
            card.level3,
            card.alm,
            card.account_updater,
            card.domestic_only,
            card.gambling_blocked,
            card.reloadable,
            card.issuer_supports_tokenization,
            card.shared_bin,
        ]
    ):
        result.append("")
        result.append("Additional Features:")
        result.append("-------------------")
        if card.level2 is not None:
            result.append(f"Level 2: {'Yes' if card.level2 else 'No'}")
        if card.level3 is not None:
            result.append(f"Level 3: {'Yes' if card.level3 else 'No'}")
        if card.alm is not None:
            result.append(f"ALM: {'Yes' if card.alm else 'No'}")
        if card.account_updater is not None:
            result.append(f"Account Updater: {'Yes' if card.account_updater else 'No'}")
        if card.domestic_only is not None:
            result.append(f"Domestic Only: {'Yes' if card.domestic_only else 'No'}")
        if card.gambling_blocked is not None:
            result.append(
                f"Gambling Blocked: {'Yes' if card.gambling_blocked else 'No'}"
            )
        if card.reloadable is not None:
            result.append(f"Reloadable: {'Yes' if card.reloadable else 'No'}")
        if card.issuer_supports_tokenization is not None:
            result.append(
                f"Issuer Supports Tokenization: {'Yes' if card.issuer_supports_tokenization else 'No'}"
            )
        if card.shared_bin is not None:
            result.append(f"Shared BIN: {'Yes' if card.shared_bin else 'No'}")

    # Currency and access information
    if card.issuer_currency or card.multi_account_access_indicator:
        result.append("")
        result.append("Currency & Access:")
        result.append("------------------")
        if card.issuer_currency:
            result.append(f"Issuer Currency: {card.issuer_currency}")
        if card.multi_account_access_indicator:
            result.append(
                f"Multi Account Access: {card.multi_account_access_indicator}"
            )

    # Additional card brands
    if card.additional_card_brands:
        result.append("")
        result.append("Additional Card Brands:")
        result.append("----------------------")
        for brand in card.additional_card_brands:
            if brand.card_brand:
                result.append(f"- {brand.card_brand}")
                if brand.card_brand_product:
                    result.append(f"  Product: {brand.card_brand_product}")
                if brand.card_brand_bank_name:
                    result.append(f"  Bank: {brand.card_brand_bank_name}")
                if brand.ecom_enabled is not None:
                    result.append(
                        f"  E-commerce Enabled: {'Yes' if brand.ecom_enabled else 'No'}"
                    )
                if brand.billpay_enabled is not None:
                    result.append(
                        f"  Bill Pay Enabled: {'Yes' if brand.billpay_enabled else 'No'}"
                    )

    # Cost information
    if card.cost and card.cost.interchange:
        result.append("")
        result.append("Cost Information:")
        result.append("-----------------")
        interchange = card.cost.interchange
        result.append(f"Regulated: {'Yes' if interchange.regulated else 'No'}")
        if interchange.regulated_name:
            result.append(f"Regulated Name: {interchange.regulated_name}")
        if interchange.notes:
            result.append(f"Notes: {interchange.notes}")

    return "\n".join(result)


@mcp.tool()
async def get_bin_data_tool(bin: str) -> str:
    """
    Get BIN data for a given BIN number.

    Args:
        bin (str): The BIN number to get data for.
    Returns:
        str: A formatted string containing the BIN data (enhanced or basic based on ENHANCED_BIN_DATA config).
    """
    api_key = os.getenv("PAGOS_API_KEY")
    pagos_client = PagosClient(api_key=api_key)
    data = await pagos_client.get_bin_data(bin)
    if not data:
        return "Unable to retrieve BIN data or no BIN data found"
    return format_bin_data(data)


if __name__ == "__main__":
    mcp.run(transport="stdio")
