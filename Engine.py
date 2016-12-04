#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Util
import urlparse
from bs4 import BeautifulSoup
import re
from WikiCore import WikiCore
from Evaluation import evalCandidate
from Evaluation import groupCandidates
from Evaluation import chooseLinks

import sys

reload(sys)
sys.setdefaultencoding('utf8')

############################################

wikipediaPageList = Util.wikipediaPageList
core = WikiCore(wikipediaPageList)

for page_index in range(3):
	print "\n",page_index, wikipediaPageList[page_index].title
	print "------------------------"

	cand = core.generateCandidates(wikipediaPageList[page_index])

	# pra poder trabalhar com indices
	cand = list(cand)

	# agrupar em candidatos concorrentes de acordo com o indice de 'cand'
	group = groupCandidates(cand)
	score = []

	for (f,w,i,j,ind) in cand:
		#f  similaridade entre texto e titulo do link
		#w o termo sem stopword
		#i posição no array das palavras
		#j quantas palavras a partir do inicio
		#ind indice do link
		cos, dist = evalCandidate(wikipediaPageList, page_index, f, w, i, j, ind)
		score.append((cos,dist,f))
		# print str(f)+" || "+w+" || "+wikipediaPageList[ind].title+" | ", i, j, " | ", cos, dist
		# print "------------------------------------------------------------"

	links = chooseLinks(cand, group, score)

	# printing the links
	print "LINKS GERADOS DA PAGINA"
	for (w,idx,size,cos,dist,pageidx) in links:
		link = wikipediaPageList[pageidx]
		print "\t", w, idx, " -> ", link.title
