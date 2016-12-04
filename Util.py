import os.path
import WikiPage
import pickle

import sys

reload(sys)
sys.setdefaultencoding('utf8')

notFound = True
limit = 10
minimumDepthFound = 11
parent = None
parentLinks = None

path = os.path.dirname(os.path.abspath(__file__)) + '/files/'


def deleteFilesFromFolder():
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


def getWikipediaPages():
    wikipediaPageList = []
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as input:
                    wikipediaPage = pickle.load(input)
                wikipediaPageList.append(wikipediaPage)
        except Exception as e:
            print(e)
    return wikipediaPageList


def getWikiPageFromUrl(url):
    for wikiPage in wikipediaPageList:
        if wikiPage.url == url:
            return wikiPage
    return None

def getWikiPagesFromUrlDictionary():
    dictionary = dict()
    for wikiPage in wikipediaPageList:
        dictionary[wikiPage.url] = wikiPage
    return dictionary

def getMinimumDistance(wikiPage1, wikiPage2):
    global notFound
    global minimumDepthFound

    minimumDepthFound = 11

    if wikiPage1.url == wikiPage2.url:
        minimumDepthFound = 0
    else:
        notFound = True
        calculateGraphDistance(wikiPage1, wikiPage2,0)
        notFound = True
        calculateGraphDistance(wikiPage2, wikiPage1,0)
        #just to check the method is ok...
        # print "Parent",parent
        # print parentLinks
    return minimumDepthFound


def calculateGraphDistance(wikiPage1, wikiPage2, depth):
    global notFound
    global minimumDepthFound
    global parent
    global parentLinks

    depth = depth + 1
    links = [j[1]for j in wikiPage1.links]
    url = wikiPage2.url

    if notFound | depth <= limit:
        if url in links:
            notFound = False
            if depth < minimumDepthFound:
                minimumDepthFound = depth
                parent = wikiPage1.url
                parentLinks = wikiPage1.links
            return depth
        else:
            linksToBeVisited = []
            for link in links:
                if notFound:
                    wikiPageNeighbor = dictionary.get(link)
                    if wikiPageNeighbor is not None:
                        linksToBeVisited.append(wikiPageNeighbor)
            for wiki in linksToBeVisited:
                calculateGraphDistance(wiki, wikiPage2, depth)
    return depth


wikipediaPageList = getWikipediaPages()
dictionary = getWikiPagesFromUrlDictionary()
