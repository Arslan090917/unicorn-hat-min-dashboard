import random
import logging
import asyncio
import json
import time
import sys
import math
import asyncio

from datetime import datetime
from colorsys import hsv_to_rgb

import requests
from PIL import Image, ImageDraw, ImageFont
from unicornhatmini import UnicornHATMini

from config import Config
from crypto_data import Coinmarketcup

class Main:
    def __init__(self) -> None:
        self.unicorn = UnicornHATMini()
        self.unicorn.set_brightness(0.1)
        self.display_width, self.display_height = self.unicorn.get_shape()
        self.text_width, self.text_height = (0 ,0)
        self.font = ImageFont.truetype("/home/pi/unicorn-hat-min-dashboard/5x7.ttf", 8)
        self.coin = Coinmarketcup()
        self.coin.update_crypto_data() # update price before start
        self.date = datetime.now()
        self.text = 'DEFAULT'
        self.image = None
        self.count = 0

    def create_text(self) -> None:
        self.text = f'{datetime.strftime(self.date, "%H:%M")} || BTC:{self.coin.data["BTC"]} || HFT:{self.coin.data["HFT"]}'
        print('update text')
    
    def create_image(self) -> None:
        self.create_text()
        self.text_width, self.text_height = self.font.getsize(self.text)
        # Create a new PIL image big enough to fit the text
        self.image = Image.new('P', (
            self.text_width + self.display_width + self.display_width, self.display_height), 0)
        self.draw = ImageDraw.Draw(self.image)
        # self.set_rotation()
        # Draw the text into the image
        self.draw.text((self.display_width, -1), self.text, font=self.font, fill=255)
        print('create images')

    #print text on led panel       
    async def display_info(self) -> None:
        print('Start')
        self.create_image()
        offset_x = 0
        a = True
        while a:
            # self.create_text()
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
            await asyncio.sleep(0.05)

    async def minute_pass(self):
        while True:
            if self.date.minute != datetime.now().minute:
                self.date = datetime.now()
                print('Updated text SUCCESS')
                print(f'{self.text}')
                self.create_image()
                self.count += 1
            else:
                await asyncio.sleep(0)

    async def update_cryptocurrency_data(self):
        while True:
            if self.count == 25:
                self.coin.update_crypto_data()
                print('print updated price')
                logging.warning('INFO system get data from coinmarketcup every 20 minutes')
                self.count = 0
            else:
                await asyncio.sleep(0)


if __name__ == "__main__":
    dash = Main()
    io_loops = asyncio.get_event_loop()
    task = [
        io_loops.create_task(dash.display_info()),
        io_loops.create_task(dash.minute_pass()),
        io_loops.create_task(dash.update_cryptocurrency_data()),
    ]
    io_loops.run_until_complete(asyncio.wait(task))
    io_loops.close()
    