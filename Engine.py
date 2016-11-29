import Util
import urlparse
from bs4 import BeautifulSoup
import re

wikipediaPageList = Util.getWikipediaPages()

print(len(wikipediaPageList))

wikipediaPage = wikipediaPageList[0]
print wikipediaPage.title
print wikipediaPage.html
print wikipediaPage.content
print wikipediaPage.categories
print wikipediaPage.links
