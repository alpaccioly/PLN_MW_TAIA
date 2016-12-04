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

# entrada: lista de lista
def removeDuplicatesListofList(a):
    b = [set(aa) for aa in a]
    c = [tuple(bb) for bb in b]
    d = list(set(c))
    e = [list(dd) for dd in d]
    return e

def evalCandidate(pagelist, page, similarity, term, termidx, nwords, candidx):
# f: similaridade entre texto e titulo do link
# w: o termo sem stopword
# i: posição no array das palavras
# j: quantas palavras a partir do inicio
# ind: indice do link
    # page = pagelist[curridx]
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
    # ta vindo um erro de deprecation da funcao "rank" daqui
    tfs = tfidf.fit_transform([pagetext, candtext])
    tfidfmatrix = tfs.toarray()
    pagefeat = tfidfmatrix[0,:]
    candfeat = tfidfmatrix[1,:]

    cos = cosine(pagefeat, candfeat)
    dist = getMinimumDistance(page, cand)

    return cos, dist


def groupCandidates(cand):
    group = []
    for i in cand:
        group.append([])

    for i1 in range(len(cand)):
        (f1, w1, idx1, siz1, candidx1) = cand[i1]
        group[i1].append(i1)
        for i2 in range(len(cand)):
            (f2, w2, idx2, siz2, candidx2) = cand[i2]
            # if w1 == w2 and idx1 == idx2 and siz1 == siz2:
            if w1 == w2 and idx1 == idx2:
                if not (i1 == i2):
                    group[i1].append(i2)
    return removeDuplicatesListofList(group)


def removeLoopsAndDuplicates(links, page_index):
    filtered = []
    for (w1,idx1,size1,cos1,dist1,pageidx1) in links:
        found = False
        for (w2,idx2,size2,cos2,dist2,pageidx2) in filtered:
            if w1 == w2 and pageidx1 == pageidx2:
                # tem uma repeticao
                found = True
                if idx1 < idx2:
                    # o indice novo eh menor do que o indice antigo
                    filtered.remove((w2,idx2,size2,cos2,dist2,pageidx2))
                    filtered.append((w1,idx1,size1,cos1,dist1,pageidx1))
        if not found:
            filtered.append((w1,idx1,size1,cos1,dist1,pageidx1))

        ## remove loops aqui
        if pageidx1 == page_index:
            filtered.remove((w1,idx1,size1,cos1,dist1,pageidx1))

    return filtered


def chooseLinks(cand, group, score, page_index):
    bestof = []
    for g in group:
        group_cos = []
        group_dist = []
        for gg in g:
            (cos, dist, f) = score[gg]
            group_cos.append(cos)
            group_dist.append(dist)
        bestcosidx = group_cos.index(min(group_cos))
        bestdistidx = group_dist.index(min(group_dist))
        if (bestcosidx == bestdistidx):
            # print "temos um melhor", min(group_cos), min(group_dist)
            bestof.append((g[bestcosidx],group_cos[bestcosidx],group_dist[bestcosidx]))
        else:
            # print "empate"
            ### no empate eu to escolhendo o menor cosseno
            bestof.append((g[bestcosidx],group_cos[bestcosidx],group_dist[bestcosidx]))

    links = []
    for (candidx,cos,dist) in bestof:
        (f,w,idx,size,pageidx) = cand[candidx]
        # w: termo a ser linkado sem stop word
        # idx: indice da primeira palavra a ser linkada
        # size: quantas palavras a partir da primeira
        # cos: cosseno entre as paginas
        # dist: distancia entre as paginas
        # pageidx: index do link
        links.append((w,idx,size,cos,dist,pageidx))


    links = removeLoopsAndDuplicates(links, page_index)

    return links

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
