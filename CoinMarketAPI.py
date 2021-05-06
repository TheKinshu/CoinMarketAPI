import requests, os
from pprint import pprint

API_KEY = os.getenv("MARKET_CAP_API")

# Create a class of CoinMarket
class CoinMarketAPI():
    # Initializing the variables
    def __init__(self) -> None:
        self.crypto_data_endpoint = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        self.crypto_info_endpoint = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/info"
        self.header = {
            'Accepts': 'application/json',
            "X-CMC_PRO_API_KEY": API_KEY
        }
        self.info_parameter = {
            "slug": None
        }
        self.crypto_info = {}

    # The search function creates an API request to the Coin Market Cap server and search for -
    # a specific crypto currency base on what it recieves from the UI function
    def search(self, name):
        self.info_parameter["slug"] = name
        coin_market_data_response = requests.get(self.crypto_data_endpoint, params=self.info_parameter, headers=self.header)
        coin_market_data_response.raise_for_status()
        cryto_market_data = coin_market_data_response.json()['data']
        id = cryto_market_data.keys()

        for i in id:
            new_id = i
        seven_day_graph = "https://s3.coinmarketcap.com/generated/sparklines/web/7d/usd/{}.png".format(new_id)

        cryto_market_data = cryto_market_data[new_id]

        self.crypto_info = {
            "id": new_id,
            "name": cryto_market_data["name"],
            "price": cryto_market_data["quote"]["USD"]["price"],
            "percent_change_24h": cryto_market_data["quote"]["USD"]["percent_change_24h"],
            "market_cap": cryto_market_data["quote"]["USD"]["market_cap"],
            "last_updated": cryto_market_data["quote"]["USD"]["last_updated"],
            "seven_day_graph": seven_day_graph
        }


        # Second
        coin_market_info_response = requests.get(self.crypto_info_endpoint, params=self.info_parameter, headers=self.header)
        coin_market_info_response.raise_for_status()

        information = (coin_market_info_response.json()['data'][new_id])

        self.crypto_info["type"] = information['category']
        self.crypto_info["website"] = information["urls"]["website"]

        pprint(self.crypto_info)
