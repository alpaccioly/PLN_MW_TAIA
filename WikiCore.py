class WikiCore:
	def __init__(self, pages):
		
		self.index = {}
		self.inverted_index = {}
		self.pages = pages
		
		for i in range(len(pages)):
			wikipediaPage = pages[i]
			self.index[wikipediaPage.title] = i

			title_words = wikipediaPage.title.split(' ')
			for w in title_words:
				if w in self.inverted_index:
					self.inverted_index[w].add(i)
				else:
					self.inverted_index[w] = {i}

	def generateCandidates(self , page):
		cand = set()
		i = 0
		words = page.content.split(' ')
		n = len(words)
		while(i<n):
			w = words[i]
			j = 1;
			verbets = self.search(w)
			while(len(verbets) != 0):
				t = self.check_candidates(verbets, w)
				cand = set.union(cand,t)
				if(i+j<len(words)):
					w = w+" "+words[i+j]
					q = w.split(' ')	
					verbets = self.search(q)
				j = j+1
			i = i+1
		return cand

	def search(self, words):
		if(words[0] in self.inverted_index):
			rst = self.inverted_index[words[0]]
			for w in  words:
				if(w in self.inverted_index):
					rst = set.intersection(rst, self.inverted_index[w])
			return rst
		return set()

	def check_candidates(self, articles_ids, w):
		cand = set()
		for ind in articles_ids:
			#if( self.minimumEditDistance(self.pages[ind].title, w)  < 5):
			cand = set.union(cand,set({ind}))

		return cand

	def minimumEditDistance(self, s1,s2):
	    if len(s1) > len(s2):
	        s1,s2 = s2,s1
	    distances = range(len(s1) + 1)
	    for index2,char2 in enumerate(s2):
	        newDistances = [index2+1]
	        for index1,char1 in enumerate(s1):
	            if char1 == char2:
	                newDistances.append(distances[index1])
	            else:
	                newDistances.append(1 + min((distances[index1],
	                                             distances[index1+1],
	                                             newDistances[-1])))
	        distances = newDistances
	    return distances[-1]
