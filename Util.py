import os.path
import WikiPage
import pickle

import sys

reload(sys)
sys.setdefaultencoding('utf8')

notFound = True
i = 1
limit = 10

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


def getMinimumDistance(wikiPage1, wikiPage2):
    global notFound
    global i

    if wikiPage1.url == wikiPage2.url:
        distance = 0
    else:
        notFound = True
        i = 1
        distance = calculateGraphDistance(wikiPage1, wikiPage2)
        notFound = True
        i = 1
        distance2 = calculateGraphDistance(wikiPage2, wikiPage1)
        if distance > distance2:
            distance = distance2

    return distance


def calculateGraphDistance(wikiPage1, wikiPage2):
    global notFound
    global i

    links = [j[1]for j in wikiPage1.links]
    url = wikiPage2.url

    if notFound | i <= limit:
        if url in links:
            notFound = False
        else:
            linksToBeVisited = []
            for link in links:
                if notFound:
                    wikiPageNeighbor = getWikiPageFromUrl(link)
                    if wikiPageNeighbor is not None:
                        linksToBeVisited.append(wikiPageNeighbor)
            i = i + 1
            for wiki in linksToBeVisited:
                calculateGraphDistance(wiki, wikiPage2)

    return i


wikipediaPageList = getWikipediaPages()