import Util
import urlparse
from bs4 import BeautifulSoup
import re

wikipediaPageList = Util.getWikipediaPages()

print(len(wikipediaPageList))

wikipediaPage = wikipediaPageList[20]
print wikipediaPage.title
print wikipediaPage.html
print wikipediaPage.categories
print wikipediaPage.links
