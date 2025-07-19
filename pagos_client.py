from typing import Optional, List
from dataclasses import dataclass
import httpx
import os


@dataclass
class Number:
    """Card number information from the Pagos Parrot API."""

    length: Optional[int] = None


@dataclass
class Product:
    """Product information from the Pagos Parrot API."""

    product_id: Optional[str] = None
    product_name: Optional[str] = None


@dataclass
class Bank:
    """Bank information from the Pagos Parrot API."""

    name: Optional[str] = None
    phone: Optional[str] = None
    url: Optional[str] = None
    clean_name: Optional[str] = None


@dataclass
class Country:
    """Country information from the Pagos Parrot API."""

    alpha2: Optional[str] = None
    numeric: Optional[str] = None
    name: Optional[str] = None


@dataclass
class Authentication:
    """Authentication information from the Pagos Parrot API."""

    authentication_required: bool
    authentication_name: Optional[str] = None


@dataclass
class CostDto:
    """Cost DTO information from the Pagos Parrot API."""

    cap_region_shortname: Optional[str] = None
    cap_advalorem_amount: Optional[str] = None
    cap_type_name: Optional[str] = None
    cap_fixed_amount: Optional[str] = None
    cap_type_qualifier_currency: Optional[str] = None
    cap_type_qualifier_text: Optional[str] = None
    cap_type_qualifier_lower: Optional[str] = None
    cap_type_qualifier_upper: Optional[str] = None


@dataclass
class Interchange:
    """Interchange information from the Pagos Parrot API."""

    regulated: bool
    regulated_name: Optional[str] = None
    domestic: Optional[CostDto] = None
    inter: Optional[CostDto] = None
    intra: Optional[CostDto] = None
    notes: Optional[str] = None


@dataclass
class Cost:
    """Cost information from the Pagos Parrot API."""

    interchange: Optional[Interchange] = None


@dataclass
class Networkfees:
    """Network fees information from the Pagos Parrot API."""

    pass


@dataclass
class AdditionalNetwork:
    """Additional network information from the Pagos Parrot API."""

    card_brand: Optional[str] = None
    bin_max: Optional[str] = None
    bin_min: Optional[str] = None
    card_brand_product: Optional[str] = None
    card_brand_bank_name: Optional[str] = None
    ecom_enabled: Optional[bool] = None
    billpay_enabled: Optional[bool] = None


@dataclass
class EnhancedCard:
    """Enhanced card information from the Pagos Parrot API."""

    number: Optional[Number] = None
    bin_length: Optional[int] = None
    pagos_bin_length: Optional[int] = None
    bin_min: Optional[str] = None
    bin_max: Optional[str] = None
    pan_or_token: Optional[str] = None
    virtual_card: Optional[bool] = None
    level2: Optional[bool] = None
    level3: Optional[bool] = None
    alm: Optional[bool] = None
    account_updater: Optional[bool] = None
    domestic_only: Optional[bool] = None
    gambling_blocked: Optional[bool] = None
    issuer_currency: Optional[str] = None
    reloadable: Optional[bool] = None
    additional_card_brands: Optional[List[AdditionalNetwork]] = None
    card_brand: Optional[str] = None
    card_segment_type: Optional[str] = None
    combo_card: Optional[str] = None
    type: Optional[str] = None
    funding_source: Optional[str] = None
    prepaid: Optional[bool] = None
    product: Optional[Product] = None
    bank: Optional[Bank] = None
    country: Optional[Country] = None
    authentication: Optional[Authentication] = None
    cost: Optional[Cost] = None
    networkfees: Optional[Networkfees] = None
    correlation_id: Optional[str] = None
    issuer_supports_tokenization: Optional[bool] = None
    multi_account_access_indicator: Optional[str] = None
    shared_bin: Optional[bool] = None


@dataclass
class EnhancedBinApiResponse:
    """Enhanced BIN API response from the Pagos Parrot API."""

    card: Optional[EnhancedCard] = None


class PagosClient:
    """
    Client for the Pagos Parrot API.

    Based on the Swagger specification at:
    https://parrot.prod.pagosapi.com/swagger/parrot-api/swagger.json
    """

    def __init__(self, api_key: Optional[str] = None, enhanced: Optional[bool] = None):
        """
        Initialize the Pagos client.

        Args:
            api_key: API key for authentication. If not provided, will use PAGOS_API_KEY environment variable.
            enhanced: Whether to use enhanced data. If not provided, will use ENHANCED_BIN_DATA environment variable.

        Raises:
            ValueError: If no API key is provided or found in environment variables.
        """
        self.api_key = api_key or os.getenv("PAGOS_API_KEY")
        if not self.api_key:
            raise ValueError("PAGOS_API_KEY environment variable is required")

        # Get enhanced setting from environment variable if not provided
        if enhanced is None:
            env_value = os.getenv("ENHANCED_BIN_DATA", "false")
            self.enhanced = str(env_value).lower() == "true"
        else:
            self.enhanced = enhanced

        self.base_url = "https://parrot.prod.pagosapi.com/bins"
        self.headers = {"x-api-key": self.api_key}

    async def get_bin_data(
        self, bin: str, enhanced: Optional[bool] = None
    ) -> Optional[EnhancedBinApiResponse]:
        """
        Get BIN data for a given BIN number.

        Based on the GET /bins endpoint from the Pagos Parrot API.

        Args:
            bin: The BIN number to lookup (Bank Identification Number)
            enhanced: Whether to return enhanced data (default: True)

        Returns:
            EnhancedBinApiResponse if successful, None if not found or error occurs

        Raises:
            httpx.HTTPStatusError: For HTTP errors (4xx, 5xx)
            httpx.RequestError: For network/connection errors
        """
        # Use instance setting if enhanced parameter is None
        enhanced_value = enhanced if enhanced is not None else self.enhanced
        params = {"bin": bin, "enhanced": str(enhanced_value).lower()}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.base_url, params=params, headers=self.headers
                )
                response.raise_for_status()
                data = response.json()

                # Parse the card data with all enhanced fields
                card_data = data.get("card", {})

                # Parse nested objects
                number_data = card_data.get("number", {})
                number = Number(**number_data) if number_data else None

                product_data = card_data.get("product", {})
                product = Product(**product_data) if product_data else None

                bank_data = card_data.get("bank", {})
                bank = Bank(**bank_data) if bank_data else None

                country_data = card_data.get("country", {})
                country = Country(**country_data) if country_data else None

                auth_data = card_data.get("authentication", {})
                authentication = Authentication(**auth_data) if auth_data else None

                # Parse cost structure
                cost_data = card_data.get("cost", {})
                cost = None
                if cost_data:
                    interchange_data = cost_data.get("interchange", {})
                    interchange = None
                    if interchange_data:
                        domestic_data = interchange_data.get("domestic", {})
                        domestic = CostDto(**domestic_data) if domestic_data else None

                        inter_data = interchange_data.get("inter", {})
                        inter = CostDto(**inter_data) if inter_data else None

                        intra_data = interchange_data.get("intra", {})
                        intra = CostDto(**intra_data) if intra_data else None

                        interchange = Interchange(
                            regulated=interchange_data.get("regulated", False),
                            regulated_name=interchange_data.get("regulated_name"),
                            domestic=domestic,
                            inter=inter,
                            intra=intra,
                            notes=interchange_data.get("notes"),
                        )
                    cost = Cost(interchange=interchange)

                # Parse additional card brands
                additional_brands_data = card_data.get("additional_card_brands", [])
                additional_card_brands = None
                if additional_brands_data:
                    additional_card_brands = [
                        AdditionalNetwork(**brand) for brand in additional_brands_data
                    ]

                # Parse networkfees
                networkfees_data = card_data.get("networkfees", {})
                networkfees = Networkfees() if networkfees_data else None

                enhanced_card = EnhancedCard(
                    number=number,
                    bin_length=card_data.get("bin_length"),
                    pagos_bin_length=card_data.get("pagos_bin_length"),
                    bin_min=card_data.get("bin_min"),
                    bin_max=card_data.get("bin_max"),
                    pan_or_token=card_data.get("pan_or_token"),
                    virtual_card=card_data.get("virtual_card"),
                    level2=card_data.get("level2"),
                    level3=card_data.get("level3"),
                    alm=card_data.get("alm"),
                    account_updater=card_data.get("account_updater"),
                    domestic_only=card_data.get("domestic_only"),
                    gambling_blocked=card_data.get("gambling_blocked"),
                    issuer_currency=card_data.get("issuer_currency"),
                    reloadable=card_data.get("reloadable"),
                    additional_card_brands=additional_card_brands,
                    card_brand=card_data.get("card_brand"),
                    card_segment_type=card_data.get("card_segment_type"),
                    combo_card=card_data.get("combo_card"),
                    type=card_data.get("type"),
                    funding_source=card_data.get("funding_source"),
                    prepaid=card_data.get("prepaid"),
                    product=product,
                    bank=bank,
                    country=country,
                    authentication=authentication,
                    cost=cost,
                    networkfees=networkfees,
                    correlation_id=card_data.get("correlation_id"),
                    issuer_supports_tokenization=card_data.get(
                        "issuer_supports_tokenization"
                    ),
                    multi_account_access_indicator=card_data.get(
                        "multi_account_access_indicator"
                    ),
                    shared_bin=card_data.get("shared_bin"),
                )

                return EnhancedBinApiResponse(card=enhanced_card)

            except httpx.HTTPStatusError as e:
                # Log the error for debugging
                print(f"HTTP error {e.response.status_code}: {e.response.text}")
                return None
            except httpx.RequestError as e:
                # Log network/connection errors
                print(f"Request error: {e}")
                return None
            except KeyError as e:
                # Log data parsing errors
                print(f"Data parsing error: {e}")
                return None
