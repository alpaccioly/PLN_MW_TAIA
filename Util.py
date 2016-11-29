import os.path
import WikiPage
import pickle


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
               with open(file_path,'rb') as input:
                   wikipediaPage = pickle.load(input)
               wikipediaPageList.append(wikipediaPage)
        except Exception as e:
            print(e)
    return wikipediaPageList

