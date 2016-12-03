#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Util
import urlparse
from bs4 import BeautifulSoup
import re
import sys

reload(sys)
sys.setdefaultencoding('utf8')

wikipediaPageList = Util.wikipediaPageList

print(len(wikipediaPageList))

wikipediaPage = wikipediaPageList[0]
vizinho = Util.getWikiPageFromUrl(u"https://en.wikipedia.org/wiki/Social_network")


dist=-1
if vizinho is not None:
    dist = Util.getMinimumDistance(wikipediaPage, vizinho)
print dist


# print wikipediaPage.url
# print wikipediaPage.title
# print wikipediaPage.html
# print wikipediaPage.content
# print wikipediaPage.categoriesd
# print wikipediaPage.links