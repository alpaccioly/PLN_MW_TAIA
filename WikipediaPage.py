class WikipediaPage:

    links = []
    categories = set()
    candidates = []

    def __init__(self, title, html, links, categories):
        self.title = title
        self.html = html
        self.links = links
        self.categories = categories

    #geters and seters
