import Util
import urlparse
from bs4 import BeautifulSoup
import re

wikipediaPageList = Util.getWikipediaPages()

print(len(wikipediaPageList))

wikipediaPage = wikipediaPageList[0]
print wikipediaPage.html
print wikipediaPage.links