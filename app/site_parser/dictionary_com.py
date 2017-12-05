from app.site_parser.site_parser import SiteParser

class DictionaryCom(SiteParser):
    def __init__(self):
        SiteParser.__init__(self)
        self.is_recording = False
        self.results = []

    def handle_starttag(self, tag, attrs):
        for one_attr in attrs:
            if 'id' in one_attr and one_attr[1] == 'clipboard-text':
                self.is_recording = True

    def handle_data(self, data):
        if self.is_recording:
            self.results.append(data)

    def handle_endtag(self, tag):
        if self.is_recording:
            self.is_recording = False
