from os import remove
from abebooks import AbeBooks
import requests, json, re
from bs4 import BeautifulSoup
from abebooks import AbeBooks

ab = AbeBooks()
url = 'https://hpb.com/products/black-cat-15-9781421516066'
result = requests.get(url).text
soup = BeautifulSoup(result, "html.parser")
soup_tag = str(soup.find("div", {"class": "big-blue-header-area mbn"}))
print(soup_tag)
if soup_tag != 'None':
    print('Broken Link')
else: print('Good Link')
