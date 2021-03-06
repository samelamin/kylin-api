from api.sources import source_config
from api.sources.generic_source import GenericSource
import requests
from datetime import datetime

class CryptoWatch(GenericSource):
    def __init__(self):
        self.url = source_config.sources["cryptowatch"]['url']
        self.source_name = source_config.sources["cryptowatch"]['source_name']
        super().__init__(self.url,self.source_name)

    def get_prices(self,currency_pairs):
        url = self.template_url
        all_markets = requests.get(url).json()
        full_response = {}
        full_response[self.source_name] = {}
        for currency_pair in currency_pairs.split(","):
            filtered_currencies = {key:value for (key,value) in all_markets['result'].items() if  currency_pair.replace("_","") in key }
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_response[self.source_name][currency_pair] = {"processed_at":current_timestamp,"source":self.source_name, "payload":filtered_currencies}
        return full_response