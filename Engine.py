import Util
import urlparse
from bs4 import BeautifulSoup
import re

wikipediaPageList = Util.getWikipediaPages()


index = {}
for i in Range(len(wikipediaPageList)):
	wikipediaPage = wikipediaPageList[i]
	index[wikipediaPage.title] = i





print wikipediaPage.title
print wikipediaPage.html
print wikipediaPage.categories
print wikipediaPage.links
