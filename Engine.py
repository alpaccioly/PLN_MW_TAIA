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
for (w,j) in cand:
	print w+" || "+wikipediaPageList[j].title
	print "------------------------------------------------------------"
