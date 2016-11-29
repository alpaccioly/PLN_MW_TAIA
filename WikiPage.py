class WikiPage:

    links = []
    categories = set()
    candidates = []

    def __init__(self, title, html, content, links, categories):
        self.title = title
        self.html = html
        self.content = content
        self.links = links
        self.categories = categories

