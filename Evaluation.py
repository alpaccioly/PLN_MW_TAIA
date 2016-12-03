#!-*- coding: utf8 -*-
import wikipedia
import string

import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *

from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# print wikipedia.summary("Dii Consentes", sentences = 2);

stemmer = PorterStemmer()

def process(text):
    # make it string
    text = str(text)
    # lower case
    lowers = text.lower()
    # remove punctuations
    no_punctuation = lowers.translate(None, string.punctuation)
    return no_punctuation


# tokenize and stemming
def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed


# {'page':'Pagina atual', 'term': 'Termo a ser linkado', 'position':'Posicao do termo na pagina', 'candidates':['Lista de paginas candidatas a link']}

# for (f,w,i,j,ind) in cand:
# 	#f  similaridade entre texto e titulo do link , w o termo sem stopword, i posição no array das palavras , j quantas palavras a partir do inicio, ind indice do link
# 	print str(f)+" || "+w+" || "+wikipediaPageList[ind].title+" | "+str(i)+" "+str(j)
# print "------------------------------------------------------------"




data = [
    {'page':'Dii Consentes', 'candidates':['Mercury (element)','Mercury (planet)', 'Mercury (Marvel Comics)','Mercury (mythology)']},
    {'page':'Gallium', 'candidates':['Mercury (element)','Mercury (planet)', 'Mercury (Marvel Comics)','Mercury (mythology)']},
    {'page':'Crust (geology)', 'candidates':['Mercury (element)','Mercury (planet)', 'Mercury (Marvel Comics)','Mercury (mythology)']},
    {'page':'Euchre', 'candidates':['Joker (playing card)', 'Joker (character)', 'Joker (2012 film)', 'Joker (musician)']},
    {'page':'Mark Hamill', 'candidates':['Joker (playing card)', 'Joker (character)', 'Joker (2012 film)', 'Joker (musician)']},
    {'page':'Dimensionality reduction', 'candidates':['Vector (mathematics)', 'Vector (epidemiology)', 'Vector (comics)', 'Array data structure']},
    {'page':'Ixodes scapularis', 'candidates':['Vector (mathematics)', 'Vector (epidemiology)', 'Vector (comics)', 'Array data structure']},
    {'page':'Chemical equation', 'candidates':['Chemical decomposition', 'Matrix decomposition', 'Decomposition (computer science)']},
    {'page':'Urban planning', 'candidates':['Population density', 'Probability density function', 'Density']},
    {'page':'Iridium', 'candidates':['Population density', 'Probability density function', 'Density']},
    {'page':'Brothers Grimm', 'candidates':['Aurora', 'Aurora, Florence County, Wisconsin', 'Aurora (Spencer, Virginia)', 'Aurora (mythology)', 'Aurora (given name)', 'Aurora (Disney character)']},
    {'page':'U.S. state', 'candidates':['Aurora', 'Aurora, Florence County, Wisconsin', 'Aurora (Spencer, Virginia)', 'Aurora (mythology)', 'Aurora (given name)', 'Aurora (Disney character)']},
    {'page':'Brothers Grimm', 'candidates':['Aurora', 'Aurora, Florence County, Wisconsin', 'Aurora (Spencer, Virginia)', 'Aurora (mythology)', 'Aurora (given name)', 'Aurora (Disney character)']},
    {'page':'Self-concept', 'candidates':['Identity (social science)', 'Identity document', 'Identity (philosophy)', 'Identity matrix']},
    {'page':'Unit vector', 'candidates':['Identity (social science)', 'Identity document', 'Identity (philosophy)', 'Identity matrix']},
    {'page':'Arecaceae', 'candidates':['Family of curves', 'Family', 'Family (periodic table)', 'Family (biology)']},
    {'page':'Atomic nucleus', 'candidates':['Family of curves', 'Family', 'Family (periodic table)', 'Family (biology)']},

]

# data = [{'page':'Dii Consentes', 'candidates':['Mercury (element)','Mercury (planet)', 'Mercury (Marvel Comics)','Mercury (mythology)']}]

for dat in data:
    page = dat['page']
    candidates = dat['candidates']

    corpus = []

    ## le a pagina e coloca no corpus
    text = wikipedia.page(page).content
    text = process(text)
    corpus.append(text)

    for candidate in candidates:
        candidatetext = wikipedia.page(candidate).content
        candidatetext = process(candidatetext)
        corpus.append(candidatetext)

    ## tentar fazer o tfidf so pras comparacoes dois a dois

    tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
    tfs = tfidf.fit_transform(corpus)
    matrix = tfs.toarray()

    pagefeat = matrix[0,:]

    print "\n", page
    for i in range(0,len(candidates)):
        feat = matrix[i+1,:]
        print candidates[i], ": ", cosine(pagefeat, feat)
