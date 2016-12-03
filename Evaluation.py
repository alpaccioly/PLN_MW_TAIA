#!-*- coding: utf8 -*-
import wikipedia
import string

import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *

from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine

from Util import getMinimumDistance

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')


#####################################################

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
    stemmer = PorterStemmer()
    tokens = nltk.word_tokenize(text)
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def getExcerpt(words, idx, nwords):
    totalwords = 10
    begin = max(0, idx - totalwords/2)
    nw1 = idx - begin - 1
    nw2 = totalwords - nw1
    end = idx + nwords + nw2
    return string.join(words[begin:end])

def evalCandidate(pagelist, curridx, similarity, term, termidx, nwords, candidx):
# f: similaridade entre texto e titulo do link
# w: o termo sem stopword
# i: posição no array das palavras
# j: quantas palavras a partir do inicio
# ind: indice do link
    page = pagelist[curridx]
    pagewords = page.content.split(' ')
    pageexcerpt = getExcerpt(pagewords, termidx, nwords)
    pagetext = process(pageexcerpt)
    # print term, " | ", pageexcerpt

    cand = pagelist[candidx]
    candwords = cand.content.split(' ')
    candtext = process(cand.content)

    # tirando os tokens e os stop words dentro da funcao do scikit
    # porque a do nltk eh mais lenta
    tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
    tfs = tfidf.fit_transform([pagetext, candtext])
    tfidfmatrix = tfs.toarray()
    pagefeat = tfidfmatrix[0,:]
    candfeat = tfidfmatrix[1,:]

    cos = cosine(pagefeat, candfeat)
    dist = getMinimumDistance(page, cand)

    return cos, dist

# data = [
#     {'page':'Dii Consentes', 'candidates':['Mercury (element)','Mercury (planet)', 'Mercury (Marvel Comics)','Mercury (mythology)']},
#     {'page':'Gallium', 'candidates':['Mercury (element)','Mercury (planet)', 'Mercury (Marvel Comics)','Mercury (mythology)']},
#     {'page':'Crust (geology)', 'candidates':['Mercury (element)','Mercury (planet)', 'Mercury (Marvel Comics)','Mercury (mythology)']},
#     {'page':'Euchre', 'candidates':['Joker (playing card)', 'Joker (character)', 'Joker (2012 film)', 'Joker (musician)']},
#     {'page':'Mark Hamill', 'candidates':['Joker (playing card)', 'Joker (character)', 'Joker (2012 film)', 'Joker (musician)']},
#     {'page':'Dimensionality reduction', 'candidates':['Vector (mathematics)', 'Vector (epidemiology)', 'Vector (comics)', 'Array data structure']},
#     {'page':'Ixodes scapularis', 'candidates':['Vector (mathematics)', 'Vector (epidemiology)', 'Vector (comics)', 'Array data structure']},
#     {'page':'Chemical equation', 'candidates':['Chemical decomposition', 'Matrix decomposition', 'Decomposition (computer science)']},
#     {'page':'Urban planning', 'candidates':['Population density', 'Probability density function', 'Density']},
#     {'page':'Iridium', 'candidates':['Population density', 'Probability density function', 'Density']},
#     {'page':'Brothers Grimm', 'candidates':['Aurora', 'Aurora, Florence County, Wisconsin', 'Aurora (Spencer, Virginia)', 'Aurora (mythology)', 'Aurora (given name)', 'Aurora (Disney character)']},
#     {'page':'U.S. state', 'candidates':['Aurora', 'Aurora, Florence County, Wisconsin', 'Aurora (Spencer, Virginia)', 'Aurora (mythology)', 'Aurora (given name)', 'Aurora (Disney character)']},
#     {'page':'Brothers Grimm', 'candidates':['Aurora', 'Aurora, Florence County, Wisconsin', 'Aurora (Spencer, Virginia)', 'Aurora (mythology)', 'Aurora (given name)', 'Aurora (Disney character)']},
#     {'page':'Self-concept', 'candidates':['Identity (social science)', 'Identity document', 'Identity (philosophy)', 'Identity matrix']},
#     {'page':'Unit vector', 'candidates':['Identity (social science)', 'Identity document', 'Identity (philosophy)', 'Identity matrix']},
#     {'page':'Arecaceae', 'candidates':['Family of curves', 'Family', 'Family (periodic table)', 'Family (biology)']},
#     {'page':'Atomic nucleus', 'candidates':['Family of curves', 'Family', 'Family (periodic table)', 'Family (biology)']},
# ]
#
# for dat in data:
#     page = dat['page']
#     candidates = dat['candidates']
#
#     corpus = ['',''];
#
#     ## le a pagina e coloca no corpus
#     text = wikipedia.page(page).content
#     text = process(text)
#     corpus[0] = text
#
#     tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
#
#     for candidate in candidates:
#         candidatetext = wikipedia.page(candidate).content
#         candidatetext = process(candidatetext)
#         corpus[1] = candidatetext
#
#         tfs = tfidf.fit_transform(corpus)
#         matrix = tfs.toarray()
#
#         pagefeat = matrix[0,:]
#         candfeat = matrix[1,:]
#         print page, " | ", candidate, ": ", cosine(pagefeat, candfeat)
