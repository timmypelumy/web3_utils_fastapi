from email.policy import default
from pydantic import BaseModel, Field,  validator
from typing import Set, Dict, Union


class FiatToFiatInputModel(BaseModel):
    base_currency: str = Field(
        default='USD', max_length=4, min_length=3, alias='baseCurrency', description="Fiat currency to convert from.")
    output_currencies: Union[Set[str], None] = Field(default={'GBP', 'EUR', 'NGN', 'JPY', 'INR'},
                                                     alias='outputCurrencies', min_items=1, description="List of fiat currencies to convert to.")

    @validator('base_currency', 'output_currencies')
    def is_valid_currency_code(cls, v):
        return v

    class Config:
        allow_population_by_field_name = True


class FiatToFiatOutputModel(BaseModel):
    base_currency: str = Field(
        max_length=4, min_length=3, alias='baseCurrency', description="Fiat currency converted from.")
    rates: Dict[str, float] = Field(
        description="Conversion rates")
    date: str

    class Config:
        allow_population_by_field_name = True


class AllAvailableFiatCurrencyOutputModel(BaseModel):
    symbols: Dict[str, str] = Field()


class FetchCoinDataInputModel(BaseModel):
    coin_ids: Set[str] = Field(
        default=['bitcoin',  'celo', 'litecoin'], alias='coinIds')
    output_fiat_currencies: Set[str] = Field(default={'NGN', 'USD'},
                                             alias='outputFiatCurrencies', min_items=1, description="List of fiat currencies to convert to.")

    @validator('coin_ids')
    def is_valid_coin_id(cls, v):
        return v

    @validator('output_fiat_currencies')
    def is_valid_currency_code(cls, v):
        return v

    class Config:
        allow_population_by_field_name = True


class CoinData(BaseModel):
    price: float = Field(ge=0)
    market_cap: float = Field(alias='marketCap', ge=0)
    vol_24h: float = Field(alias="24h_vol", ge=0)
    change_24h: float = Field(alias='24h_change')
    date: int = Field(gt=0)

    class Config:
        allow_population_by_field_name = True


class FetchCoinDataOutputModel(BaseModel):
    coins: Dict[str, Dict[str, CoinData]] = Field()

    class Config:
        allow_population_by_field_name = True
