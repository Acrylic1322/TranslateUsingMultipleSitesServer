from html.parser import HTMLParser
class SiteParser(HTMLParser):
    result = []

    def __init__(self):
        HTMLParser.__init__(self)
