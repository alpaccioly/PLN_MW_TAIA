import Util
import urlparse
from bs4 import BeautifulSoup
import re
from WikiCore import WikiCore


wikipediaPageList = Util.getWikipediaPages()

core = WikiCore(wikipediaPageList)

for page_index in range(40):
	print wikipediaPageList[page_index].title
	cand = core.generateCandidates(wikipediaPageList[page_index])
	print "--"
	for (f,w,i,j,ind) in cand:
		print str(f)+" || "+w+" || "+wikipediaPageList[ind].title+" | "+str(i)+" "+str(j)
	print "------------------------------------------------------------"
