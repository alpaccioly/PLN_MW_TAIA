#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Util
import urlparse
from bs4 import BeautifulSoup
import re
from WikiCore import WikiCore

import sys

reload(sys)
sys.setdefaultencoding('utf8')

wikipediaPageList = Util.wikipediaPageList

core = WikiCore(wikipediaPageList)

for page_index in range(40):
	print wikipediaPageList[page_index].title
	cand = core.generateCandidates(wikipediaPageList[page_index])
	print "--"
	for (f,w,i,j,ind) in cand:
		#f  similaridade entre texto e titulo do link , w o termo sem stopword, i posição no array das palavras , j quantas palavras a partir do inicio, ind indice do link
		print str(f)+" || "+w+" || "+wikipediaPageList[ind].title+" | "+str(i)+" "+str(j)
	print "------------------------------------------------------------"



# Teste Graph Distance Manuela
# wikipediaPage = wikipediaPageList[0]
# vizinho = Util.getWikiPageFromUrl(u"https://en.wikipedia.org/wiki/Social_network")
#
# dist=-1
# if vizinho is not None:
#     dist = Util.getMinimumDistance(wikipediaPage, vizinho)
# print dist


# print wikipediaPage.url
# print wikipediaPage.title
# print wikipediaPage.html
# print wikipediaPage.content
# print wikipediaPage.categoriesd
# print wikipediaPage.links