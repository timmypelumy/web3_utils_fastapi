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


class CoinToFiatInputModel(BaseModel):
    base_currency: str = Field(
        default='USD', max_length=4, min_length=3, alias='baseCurrency', description="Fiat currency to convert from.")
    output_currencies: Set[str] = Field(default={'GBP', 'EUR', 'NGN', 'JPY', 'INR'},
                                        alias='outputCurrencies', min_items=1, description="List of fiat currencies to convert to.")

    @validator('base_currency', 'output_currencies')
    def is_valid_currency_code(cls, v):
        return v

    class Config:
        allow_population_by_field_name = True


class CoinToFiatOutputModel(BaseModel):
    base_currency: str = Field(
        max_length=4, min_length=3, alias='baseCurrency', description="Fiat currency converted from.")
    rates: Dict[str, float] = Field(
        description="Conversion rates")
    date: str

    class Config:
        allow_population_by_field_name = True
