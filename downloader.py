from scheduler import Scheduler
from bs4 import BeautifulSoup
from scraper import Scraper, BasicExtractor
from app import Product

import json
import requests
import uuid





class NameAttribute(object):

	def __init__(self):
		self.name = 'name'
		self.value = None
		self.rules = [('h1', 'text')]

class DescriptionAttribute(object):

	def __init__(self):
		self.name = 'description'
		self.value = None
		self.rules = [('product-description', 'div', 'text')]


class ImageAttribute(object):

	def __init__(self):
		self.name = 'image_url'
		self.value = None
		self.rules = [('img', 'text')]


class Downloader(object):

	@staticmethod
	def start():
		self = Downloader()
		Scheduler.recieve('load_url', self.load_url)

	def load_url(self, channel, method, properties, body):
		body = json.loads(body)
		url = body.get('url', '')
		print(url)
		if url:
			details = Scraper(url, BasicExtractor()).get_details([NameAttribute])
			product = Product()
			for attribute in details:
				setattr(product, attribute.name, attribute.value)

			print(product.name)
			channel.basic_ack(delivery_tag = method.delivery_tag)
			data = product.__dict__
			Scheduler.add('extract_meta', data)


if __name__ == '__main__':
	Downloader.start()