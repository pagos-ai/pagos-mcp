from typing import Optional
from dataclasses import dataclass
import httpx
import os


@dataclass
class CardProduct:
    product_id: str
    product_name: str


@dataclass
class Bank:
    name: str


@dataclass
class Country:
    alpha2: str
    numeric: str
    name: str


@dataclass
class CardNumber:
    length: int


@dataclass
class Card:
    number: CardNumber
    bin_min: str
    bin_max: str
    card_brand: str
    type: str
    prepaid: bool
    product: CardProduct
    bank: Bank
    country: Country
    correlation_id: str


@dataclass
class BinDataResponse:
    card: Card


class PagosClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("PAGOS_API_KEY")
        if not self.api_key:
            raise ValueError("PAGOS_API_KEY environment variable is required")
        self.base_url = "https://parrot.prod.pagosapi.com/bins"
        self.headers = {"x-api-key": self.api_key}

    async def get_bin_data(self, bin: str) -> Optional[BinDataResponse]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}?bin={bin}", headers=self.headers
                )
                response.raise_for_status()
                data = response.json()
                return BinDataResponse(
                    card=Card(
                        number=CardNumber(**data["card"]["number"]),
                        bin_min=data["card"]["bin_min"],
                        bin_max=data["card"]["bin_max"],
                        card_brand=data["card"]["card_brand"],
                        type=data["card"]["type"],
                        prepaid=data["card"]["prepaid"],
                        product=CardProduct(**data["card"]["product"]),
                        bank=Bank(**data["card"]["bank"]),
                        country=Country(**data["card"]["country"]),
                        correlation_id=data["card"]["correlation_id"],
                    )
                )
            except (httpx.HTTPStatusError, KeyError) as e:
                return None
