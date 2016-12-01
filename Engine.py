import Util
import urlparse
from bs4 import BeautifulSoup
import re
from WikiCore import WikiCore


wikipediaPageList = Util.getWikipediaPages()

core = WikiCore(wikipediaPageList)

for i in range(20):
	print wikipediaPageList[i].title
	cand = core.generateCandidates(wikipediaPageList[i])
	print "--"
	for j in cand:
		print wikipediaPageList[j].title
	print cand
	print "------------------------------------------------------------"
