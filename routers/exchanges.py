from models.exchange import FiatToFiatInputModel, FiatToFiatOutputModel, AllAvailableFiatCurrencyOutputModel, FetchCoinDataInputModel, FetchCoinDataOutputModel
from fastapi import APIRouter, HTTPException
from requests import request
from config import settings


router = APIRouter(
    prefix='/exchange-and-conversion',
    responses={
        404: {"description": "Resource does not exist"}
    }
)


@router.get('/available-fiat-currencies',  description="Get all available currencies with their respective symbol", response_model=AllAvailableFiatCurrencyOutputModel)
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
    url = None

    if body.output_currencies:

        url = "https://api.apilayer.com/fixer/latest?symbols={0}&base={1}".format(
            ','.join(body.output_currencies), body.base_currency)

    else:
        url = "https://api.apilayer.com/fixer/latest?base={0}".format(
            body.base_currency)

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


@router.post('/coin-data', description="Fetch coin market data ", response_model=FetchCoinDataOutputModel)
def fetch_coin_data(body: FetchCoinDataInputModel):

    headers = {
        'apiKey': settings.coingecko_key
    }

    url = "https://api.coingecko.com/api/v3/simple/price?ids={0}&vs_currencies={1}&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true".format(
        ','.join(body.coin_ids), ','.join(body.output_fiat_currencies))

    response = request("GET", url, headers=headers)

    status_code = response.status_code

    if status_code != 200:
        raise HTTPException(
            status_code=500, detail="Unable to process request")

    else:
        data = response.json()
        # print(data)
        client_data = {}

        for coin_id in body.coin_ids:

            client_data[coin_id.lower()] = {}

            for currency in body.output_fiat_currencies:

                client_data[coin_id.lower()][currency.lower()] = {
                    'price': data[coin_id.lower()][currency.lower()],
                    "market_cap": data[coin_id.lower()]["{0}_market_cap".format(currency.lower())],
                    "vol_24h": data[coin_id.lower()]["{0}_24h_vol".format(currency.lower())],
                    "change_24h": data[coin_id.lower()]["{0}_24h_change".format(currency.lower())],
                    "date": data[coin_id.lower()]["last_updated_at"]
                }

        return {"coins": client_data}


@router.post('/token-data', description="Fetch token market data")
def fetch_token_data(body: FetchCoinDataInputModel):
    pass
