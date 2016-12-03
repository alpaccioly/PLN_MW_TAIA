#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Util
import urlparse
from bs4 import BeautifulSoup
import re
from WikiCore import WikiCore
from Evaluation import evalCandidate


import sys

reload(sys)
sys.setdefaultencoding('utf8')

wikipediaPageList = Util.wikipediaPageList

core = WikiCore(wikipediaPageList)

for page_index in range(2):
	print wikipediaPageList[page_index].title
	cand = core.generateCandidates(wikipediaPageList[page_index])
	print "--"
	print type(cand)
	for (f,w,i,j,ind) in cand:
		#f  similaridade entre texto e titulo do link , w o termo sem stopword, i posição no array das palavras , j quantas palavras a partir do inicio, ind indice do link
		words = wikipediaPageList[page_index].content.split(' ')
		cos, dist = evalCandidate(wikipediaPageList, page_index, f, w, i, j, ind)
		print str(f)+" || "+w+" || "+wikipediaPageList[ind].title+" | "+str(i)+" "+str(j)
		print w, " | ", words[i], " | ", j, " | ", words[i:i+j], " | ", cos, dist
		print "------------------------------------------------------------"


# Teste Graph Distance Manuela
# wikipediaPage = wikipediaPageList[0]
# dictionary = Util.dictionary
#
# vizinho = dictionary.get(u"https://en.wikipedia.org/wiki/Discrete_mathematics")
#
# dist=-1
# if vizinho is not None:
#     dist = Util.getMinimumDistance(wikipediaPage, vizinho)
# print "Distancia : ",dist
