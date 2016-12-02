import Util
import urlparse
from bs4 import BeautifulSoup
import re
from WikiCore import WikiCore


wikipediaPageList = Util.getWikipediaPages()

core = WikiCore(wikipediaPageList)

print wikipediaPageList[18].title
cand = core.generateCandidates(wikipediaPageList[18])
print "--"
for (f,w,j) in cand:
	print str(f)+" || "+w+" || "+wikipediaPageList[j].title
	print "------------------------------------------------------------"
