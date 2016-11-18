class WikipediaPage:

    links = []
    categories = set()
    candidates = []

    def __init__(self, html, links, categories):
        self.html = html
        self.links = links
        self.categories = categories

    #geters and seters
