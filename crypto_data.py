'''
Get data from coinmarketcup
'''
import json
import logging
import requests

from config import Config

logging.basicConfig(
    filename='error.log',
    format='%(asctime)s %(levelname)s:%(message)s',
      encoding='utf-8',
        level=logging.WARNING)

class Coinmarketcup:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.endpoint = '/v1/cryptocurrency/listings/latest'
        self.params = {'start': 1, 'limit': 1000, 'convert': 'USD'}
        self.headers = {
            "X-CMC_PRO_API_KEY" : Config.COINT_MARKET_API_KEY,
            "Content-type": "application/json"
        }
        self.data = None
        self.crypto_names = ['BTC', 'HFT']
    
    def get_pirce(self, response) -> dict:
        '''
        Function for geting price from json response
        :params *crypto_name: dict - take list of crypto currency 
        Example: ['BTC', 'ETH', 'HFT']
        '''
        # price = json.loads(self.response)['data'][0]['quote']['USD']['price']
        crypto_data = dict()
        json_data = json.loads(response)
        for name in self.crypto_names:
            for currency in json_data['data']:
                if name == currency['symbol']:
                    crypto_data[name] = str(currency['quote']['USD']['price'])[:6]
        return crypto_data

    def update_crypto_data(self) -> dict:
        try:
            self.response = self.session.get(
                Config.COINT_MARKET_URL + self.endpoint, headers= self.headers, params=self.params)
            logging.info(f'Send request {Config.COINT_MARKET_URL}', extra= {'Status code': self.response.status_code})
            if self.response.status_code in [200, 201]:
                try:
                    self.data = self.get_pirce(self.response.text)
                    logging.info('Update crypto data', extra={'BTC': self.data['BTC'], 'HFT': self.data['HFT']})
                except Exception as exp:
                    logging.error(exp)
                    raise exp
                logging.info(f'Finish updating crypto currency data')
            else:
                logging.error(f'ERROR Request to {Config.COINT_MARKET_URL} Staus code: {self.response.status_code}')
        except Exception as exp:
            logging.error(f'{exp} error')
            raise exp        
