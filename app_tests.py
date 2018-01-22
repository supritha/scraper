from scraper import Scraper, URLLoadError, BasicExtractor
from downloader import NameAttribute

import pytest

def test_get_details_wrong_url():
	"""
	Test case: When given wrong url
	"""
	url = 'https://nbgdhckkdoo.com'
	with pytest.raises(URLLoadError):
		product = Scraper(url, BasicExtractor()).get_details([NameAttribute])


def test_get_details():
	url = 'https://bestchoiceproducts.com/products/portable-ip67-waterproof-wireless-bluetooth-speaker-shower-fm-radio-built-in-speakerphone-led-lights-orange'
	product = Scraper(url, BasicExtractor()).get_details([NameAttribute])

	assert product[0].value is not None





