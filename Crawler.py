import urlparse
import urllib2
import ssl
from bs4 import BeautifulSoup
import re
import os.path
import Util
import pickle
import datetime
import sys
from WikipediaPage import WikipediaPage

now = datetime.datetime.now()

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://en.wikipedia.org/wiki/Small-world_network"
path = os.path.dirname(os.path.abspath(__file__)) + '/files/'

urls = [url]
visited = [url]

count = 1
stop_expanding = False
max_pages = 500


Util.deleteFilesFromFolder()

while ((len(urls) != 0) & (count <= max_pages)):
	print("LEN",len(urls))
	print("COUNT",count)
	
	try:
		print(urls[0])
		html_text = urllib2.urlopen(urls[0],context=ctx).read()

		# Removes saved html link from queue

		print("URL --------> ",urls.pop(0))


		soup = BeautifulSoup(html_text, "html.parser")

		# Expands actual url to find more non-visited urls

		#Body links
		bodyLinks = []
		paragraphs = soup.findAll('p')
		for paragraph in paragraphs:
			tags = paragraph.findAll('a', href=True)
			for tag in tags:
				tag['href'] = urlparse.urljoin(url, tag['href'])
				if "cite_note" not in tag['href']:
					bodyLinks.append({(tag['href']),tag.text})
		 			print tag['href'] , tag.text

					# not visited
					if tag['href'] not in visited:
						urls.append(tag['href'])
						visited.append(tag['href'])

		#Categories assigned links
		print 'Categories'
		categories = set()
		links = soup.findAll('a', href = re.compile('^/wiki/Category'))
		for link in links:
			categories.add(str(links))

		print categories

		wikipediaPage = WikipediaPage(html_text,bodyLinks,categories)

		#Saving the file
		file = path + str(count) + ".pkl"
		with open(file, 'wb') as output:
			pickle.dump(wikipediaPage,output, pickle.HIGHEST_PROTOCOL)
			count = count + 1


	except Exception, e:
		print("Error: " + urls[0])
		print(e)
		urls.pop(0)
		

now2 = datetime.datetime.now()
print("Time",str(now2-now))




