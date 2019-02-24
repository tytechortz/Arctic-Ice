import requests
import lxml
from lxml import html
import pandas as pd

response = requests.get('https://www.esrl.noaa.gov/gmd/ccgg/trends/monthly.html')

tree = lxml.html.fromstring(response.text)
title_elem = tree.xpath('//td')[1]

print(title_elem.text_content())