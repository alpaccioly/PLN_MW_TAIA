#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import Util
from WikiCore import WikiCore
from Evaluation import evalCandidate
from Evaluation import groupCandidates
from Evaluation import chooseLinks
from Evaluation import removeCandLoopsAndDuplicates

reload(sys)
sys.setdefaultencoding('utf8')

############################################

wikipediaPageList = Util.wikipediaPageList
core = WikiCore(wikipediaPageList)

def searchPage(page):
	idx = 0
	for i in range(len(wikipediaPageList)):
		pg = wikipediaPageList[i]
		if pg.url == page.url:
			idx = i
			break
	return idx

def process(page):
	page_index = searchPage(page)
	cand = core.generateCandidates(page)
	# convertendo pra lista pra poder trabalhar com indices
	cand = list(cand)
	cand = removeCandLoopsAndDuplicates(cand, page_index)

	score = []
	for (f,w,i,j,ind) in cand:
		#f  similaridade entre texto e titulo do link
		#w o termo sem stopword
		#i posição no array das palavras
		#j quantas palavras a partir do inicio
		#ind indice do link
		cos, dist = evalCandidate(wikipediaPageList, page, f, w, i, j, ind)
		score.append((cos,dist,f))
		# print str(f)+" || "+w+" || "+wikipediaPageList[ind].title+" | ", i, j, " | ", cos, dist
		# print "------------------------------------------------------------"
		# print (f,w,i,j,ind)," | ", cos, dist, " | ", wikipediaPageList[ind].title

	# agrupar em candidatos concorrentes de acordo com o indice de 'cand'
	group = groupCandidates(cand)
	links = chooseLinks(cand, group, score, page_index)
	return links




# for page_index in range(3):
# 	page = wikipediaPageList[page_index]
#
# 	print "\n",page_index, page.title
# 	print "------------------------"
#
# 	page = wikipediaPageList[page_index]
# 	links = process(page)
#
# 	# printing the links
# 	print "LINKS GERADOS DA PAGINA: ", len(links)
# 	for (w,idx,size,cos,dist,pageidx) in links:
# 		link = wikipediaPageList[pageidx]
# 		print "\t", w, idx, " -> ", link.title
