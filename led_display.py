import random
import asyncio
import json
import datetime
import time
import sys
import math
import asyncio

from colorsys import hsv_to_rgb

import requests
from PIL import Image, ImageDraw, ImageFont
from unicornhatmini import UnicornHATMini

from config import Config


class UnicornDashboard:
    def __init__(self) -> None:
        self.text = 'DEFAULT'
        self.rotation = 0
        self.unicorn = UnicornHATMini()
        self.display_width, self.display_height = self.unicorn.get_shape()
        self.unicorn.set_brightness(0.1)
        self.font = ImageFont.truetype("/home/pi/unicorn-hat-min-dashboard/5x7.ttf", 8)
        self.text_width, self.text_height = (0 ,0)
        self.image = None
        self.draw = None
        self.price = 0
        self.response = None
        self.date = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M')
        self.minuts_start = datetime.datetime.now().minute
        self.counters = 0
        self.crypto_data = {
            'BTC': 0,
            'HFT' : 0
        }

    
    def set_rotation(self) -> None:
        if len(sys.argv) > 1:
            try:
                self.rotation = int(sys.argv[1])
            except ValueError:
                print("Usage: {} <rotation>".format(sys.argv[0]))
                sys.exit(1)
        self.unicorn.set_rotation(self.rotation)
        
    
    # https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest

    def _fake_get_coin_price_from_coin_master_cap(self) -> None:
        '''
        set fake response for test 
        '''
        self.response = Config.FAKE_RESPONSE


    def _get_coin_price_from_coin_master_cap(self) -> None:
        '''
        Get crypto price from https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest
        '''
        session = requests.Session()
        endpoint = '/v1/cryptocurrency/listings/latest'
        headers = {
            "X-CMC_PRO_API_KEY" : Config.COINT_MARKET_API_KEY,
            "Content-type": "application/json"
        }
        params = {'start': 1, 'limit': 1000, 'convert': 'USD'}
        try:
            self.response = session.get(Config.COINT_MARKET_URL + endpoint, headers= headers, params=params).text
        except Exception:
            raise Exception
        

    def _get_from_json_response_cryptocurrency_price(self, *crypto_name) -> dict:
        '''
        Function for geting price from json response
        :params *crypto_name: dict - take list of crypto currency 
        Example: ['BTC', 'ETH', 'HFT']
        '''
        # price = json.loads(self.response)['data'][0]['quote']['USD']['price']
        json_data = json.loads(self.response)
        for name in crypto_name:
            for currency in json_data['data']:
                if name == currency['symbol']:
                    self.crypto_data[name] = str(currency['quote']['USD']['price'])[:6]
       
        # try:
        #     self.price = math.floor(price)
        # except Exception:
        #     raise TypeError
        
    
    def _get_time_kz_almaty_now(self) -> None:
        self.date = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M')

    
    def create_text(self) -> None:
        '''
        create text which will be displaying on led panel
        '''
        self.text = f'{self.date} || BTC:{self.crypto_data["BTC"]} || HFT:{self.crypto_data["HFT"]}'


    def create_image(self) -> None:
        self.create_text()
        self.text_width, self.text_height = self.font.getsize(self.text)
        # Create a new PIL image big enough to fit the text
        self.image = Image.new('P', (self.text_width + self.display_width + self.display_width, self.display_height), 0)
        self.draw = ImageDraw.Draw(self.image)
        self.set_rotation()
        # Draw the text into the image
        self.draw.text((self.display_width, -1), self.text, font=self.font, fill=255)

    
    def update_time(self) -> None:
        '''
        update time every minuts
        '''
        self._get_time_kz_almaty_now()
        self.create_image()

    
    def update_price(self) -> None:
        '''
        update price crypto curency
        '''
        self._get_coin_price_from_coin_master_cap()
        self._get_from_json_response_cryptocurrency_price('BTC', 'HFT')
        self.create_image()


    def _track_minuts(self) -> None:
        if self.minuts_start != datetime.datetime.now().minute:
            self.minuts_start = datetime.datetime.now().minute
            print('minute number changed')
            self.counters += 1
            self.update_time()
        else:
            print('minuts wasn\'t changed')


    def _get_price_every_twenty_minuts(self):
        if self.counters == 20:
            self.update_price()
            self.counters = 0
        else:
            print('wait until 20 minutes pass')


    #print text on led panel       
    async def display_info(self) -> None:
        self._get_coin_price_from_coin_master_cap()
        self._get_from_json_response_cryptocurrency_price('BTC', 'HFT')
        self.create_image()
        offset_x = 0
        a = True
        while a:
            # self.create_text()
            print('running')
            for y in range(self.display_height):
                for x in range(self.display_width):
                    # if end of image set zero offset
                    # hue = (time.time() / 10.0) + (x / float(self.display_width * 2))
                    # r, g, b = [int(c * 255) for c in hsv_to_rgb(hue, 1.0, 1.0)]
                    r, g, b = (255, 255, 255)
                    try:
                        self.image.getpixel((x + offset_x, y))
                    except Exception:
                        offset_x = 0
                    if self.image.getpixel((x + offset_x, y)) == 255:
                        test = self.image
                        self.unicorn.set_pixel(x, y, r, g, b)
                    else:
                        self.unicorn.set_pixel(x, y, 0, 0, 0)
            
            offset_x += 1
            # if end of image set zero offset
            if offset_x + self.display_height + 1 >= self.image.size[0]:
                offset_x = 0
            self.unicorn.show()
            # a = False
            time.sleep(0.5)
            await asyncio.sleep(0)
            print('check time')

    
    async def get_event_changed_minuts(self):
        while True:
            self._track_minuts()
            self._get_price_every_twenty_minuts()
            print('Time checked')
            await asyncio.sleep(1)


if __name__ == "__main__":
    dash = UnicornDashboard()
    dash.display_info()
    io_loops = asyncio.get_event_loop()
    task = [
        io_loops.create_task(dash.get_event_changed_minuts()),
        io_loops.create_task(dash.display_info())
    ]
    io_loops.run_until_complete(asyncio.wait(task))