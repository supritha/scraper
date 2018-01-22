from bs4 import BeautifulSoup


import requests


class BasicExtractor(object):

	def get(self, content, rules):
		beautiful_soup = BeautifulSoup(content, 'html.parser')

		for rule in rules:
			i = 0
			data = beautiful_soup
			while i < len(rule):
				if hasattr(data, rule[i]):
					data = getattr(data, rule[i])
					i += 1
				else:
					break

			if i == len(rule):
				return data


class Scraper(object):

	def __init__(self, url, extractor):
		self.url = url
		self.extractor = extractor
		self.url_content = None

	@property
	def content(self):
		if not self.url_content:
			self.url_content = get_content(self.url)

		return self.url_content

	def get_details(self, attributes):
		content  = self.content
		details = []
		for attribute_cls in attributes:
			attribute = attribute_cls()
			attribute.value = self.extractor.get(content, attribute.rules)
			details.append(attribute)

		return details


class URLLoadError(Exception):
	''' Error when loading url '''
	pass


def get_content(url):
	try:
		response = requests.get(url)
	except Exception as e:
		raise URLLoadError

	if response.status_code == 200:
		return response.content

	raise response.content
