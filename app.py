
from scheduler import Scheduler


import uuid


class Product(object):

	def __init__(self):
		self.id = uuid.uuid4().hex
		self.name = None

	def set_description(self, description):
		self.description = description

	def set_specification(self, specification):
		self.specification = specification

	@staticmethod
	def save_meta(id, meta):
		print(meta)


class Crawler(object):

	@staticmethod
	def process_request(url):
		Scheduler.add('load_url', {'url': url})



if __name__ == '__main__':
	
	while True:
		Crawler.process_request(input())

