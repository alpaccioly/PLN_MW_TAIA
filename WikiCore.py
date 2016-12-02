import nltk
from nltk.corpus import stopwords
import sys

reload(sys)
sys.setdefaultencoding('utf8')

class WikiCore:
	def __init__(self, pages):
		
		self.index = {}
		self.inverted_index = {}
		self.pages = pages
		
		self.stop_words = set(stopwords.words('english'))

		for i in range(len(pages)):
			wikipediaPage = pages[i]
			title = wikipediaPage.title.upper()
			self.index[title] = i

			title_words = title.split(' ')
			for w in title_words:
				if w.lower() not in self.stop_words:
					w_upper = w.upper()
					if w_upper in self.inverted_index:
						
						self.inverted_index[w_upper].add(i)
					else:
						self.inverted_index[w_upper] = {i}


	def generateCandidates(self , page):
		cand = set()
		i = 0
		words = page.content.split(' ')
		n = len(words)
		while(i<n):
			w = words[i].upper()
			j = 1;
			verbets = self.search(w.split(' '))
			while(len(verbets) != 0 and (i+j)<len(words)):
				t = self.check_candidates(verbets, w)
				cand = set.union(cand,t)
				if(i+j<len(words) and words[i+j] not in self.stop_words):
					w = w+" "+words[i+j].upper()
					q = w.split(' ')	
					verbets = self.search(q)
				j = j+1
			i = i+1
		return cand

	def search(self, words):
		key = words[0].upper()
		if key in self.inverted_index :
			rst = self.inverted_index[key]
			for w in  words:
				w_upper = w.upper()
				if(w_upper in self.inverted_index):
					rst = set.intersection(rst, self.inverted_index[w_upper])
			return rst
		return set()

	def check_candidates(self, articles_ids, w):
		sel = set()
		for ind in articles_ids:
			title = self.pages[ind].title.upper()
			title_words = set(title.split(' '))
			w_words = set(w.split(' '))
			title_words = title_words - self.stop_words
			w_words = w_words - self.stop_words

			inter_size = len(w_words & title_words)
			union_size = len(w_words | title_words)
			
			if(float(inter_size)/union_size > 0.6):
				sel = set.union(sel,set({(w,ind)}))
		return sel

	def minimumEditDistance(self, s1,s2):
	    if len(s1) > len(s2):
	        s1,s2 = s2,s1
	    distances = range(len(s1) + 1)
	    for index2,char2 in s2:
	        newDistances = [index2+1]
	        for index1,char1 in s1:
	            if char1 == char2:
	                newDistances.append(distances[index1])
	            else:
	                newDistances.append(1 + min((distances[index1],
	                                             distances[index1+1],
	                                             newDistances[-1])))
	        distances = newDistances
	    return distances[-1]
