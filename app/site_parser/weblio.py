from app.site_parser.site_parser import SiteParser

class Weblio(SiteParser):
    def __init__(self):
        SiteParser.__init__(self)
        self.is_result_parent = False
        self.is_result = False
        self.result = []

    def handle_starttag(self, tag, attrs):
        if self.is_result_parent == True and tag == 'span':
            self.is_result = True
            self.is_result_parent = False
        else:
            for one_attr in attrs:
                if 'class' in one_attr and one_attr[1] == 'translatedTextAreaLn':
                    self.is_result_parent = True

    def handle_data(self, data):
        if self.is_result:
            self.result.append(data)
            self.is_result = False

    def handle_endtag(self, tag):
        if self.is_result_parent and tag == 'li':
            self.is_result_parent = False
