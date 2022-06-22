from models.conversion import FiatToFiatInputModel, FiatToFiatOutputModel, AllAvailableFiatCurrencyOutputModel
from fastapi import APIRouter, HTTPException
from requests import request
from config import settings


router = APIRouter(
    prefix='/conversions',
    responses={
        404: {"description": "Resource does not exist"}
    }
)


@router.get('/available-currencies-with-symbol',  description="Get all available currencies with their respective symbol", response_model=AllAvailableFiatCurrencyOutputModel)
def available_currencies_with_symbol():
    headers = {
        'apiKey': settings.api_layer_key
    }
    url = "https://api.apilayer.com/fixer/symbols"

    response = request("GET", url, headers=headers)

    status_code = response.status_code

    if status_code != 200:
        raise HTTPException(
            status_code=500, detail="Unable to process request")

    else:
        data = response.json()
        return {
            "symbols": data["symbols"]
        }


@router.post('/fiat-to-fiat',  description="Convert any valid fiat currency to its equivalent value in any other valid fiat currency.", response_model=FiatToFiatOutputModel)
def fiat_to_fiat_conversions(body: FiatToFiatInputModel):

    headers = {
        'apiKey': settings.api_layer_key
    }
    url = "https://api.apilayer.com/fixer/latest?symbols={0}&base={1}".format(
        ','.join(body.output_currencies), body.base_currency)

    response = request("GET", url, headers=headers)

    status_code = response.status_code

    if status_code != 200:
        raise HTTPException(
            status_code=500, detail="Unable to process request")

    else:
        data = response.json()
        return {
            "base_currency": data["base"],
            "date": data["date"],
            "rates": data["rates"]
        }


@ router.post('/coin-to-fiat', description="Convert any valid coin asset to its equivalent value in any valid fiat currency.")
def coin_to_fiat_conversions():
    pass


@ router.post('/token-to-fiat', description="Convert any valid token asset to its equivalent value in any valid fiat currency.")
def token_to_fiat_conversions():
    pass
