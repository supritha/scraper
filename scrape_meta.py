from scheduler import Scheduler
from bs4 import BeautifulSoup
from scraper import Scraper, BasicExtractor
from app import Product


import json


class AdvancedExtractor(BasicExtractor):

	def get(self, content, rules):
		beautiful_soup = BeautifulSoup(content, 'html.parser')

		for rule in rules:
			i = 0
			data = beautiful_soup
			while i < len(rule) and data:

				print(rule[i])
				try:
					a_type, a_value = rule[i].split(':')
				except:
					a_value = rule[i]
					a_type = None

				print(a_type, a_value)

				if a_type and a_type == 'id':
					data = data.find(id=a_value)
					i += 1

				elif a_type and a_type == 'class_':
					data = data.find(class_=a_value)
					i += 1

				elif hasattr(data, rule[i]):
					data = getattr(data, rule[i])
					i += 1
				else:
					break

			if i == len(rule):
				return data 


class AmazonRatings(object):
	
	def __init__(self):
		self.name = 'amazon-ratings'
		self.value = None
		self.rules = [('id:averageCustomerReviews', 'id:acrPopover', 'class_:a-icon-star', 'text')]

	def __repr__(self):
		return '%s=%s' % (self.name, self.value)


class ScrapeMeta(object):

	@staticmethod
	def start():
		self = ScrapeMeta()
		Scheduler.recieve('extract_meta', self.extract_meta)

	def extract_meta(self, channel, method, properties, body):
		product = json.loads(body)
		print(body)

		amazon_url = 'https://www.amazon.com/Portable-Waterproof-Wireless-Bluetooth-Speakerphone/dp/B07458JJPB?th=1'
		meta = Scraper(amazon_url, AdvancedExtractor()).get_details([AmazonRatings])
		# for each in details:
		# 	setattr(product, each.name, each.value)

		Product.save_meta(product['id'], meta)
		channel.basic_ack(delivery_tag = method.delivery_tag)




if __name__ == '__main__':
	ScrapeMeta.start()