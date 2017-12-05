from app.site_parser.site_parser import SiteParser

class Weblio(SiteParser):
    def __init__(self, result_mode):
        SiteParser.__init__(self)
        self.is_in_result_tag = False
        self.is_recording = False

        self.results = []
        self.one_result = ''

        # This records the language of result.
        self.result_mode = result_mode

    def handle_starttag(self, tag, attrs):
        # If the flow is going throught the li tag of result.
        if self.is_in_result_tag and tag == 'span':
            if self.result_mode == 'ja':
                self.is_recording = True

            else:
                for one_attr in attrs:
                    if 'class' in one_attr and one_attr[1] == 'popupW':
                        self.is_recording = True

        # This searches the li tag of result.
        else:
            for one_attr in attrs:
                if 'class' in one_attr and one_attr[1] == 'translatedTextAreaLn':
                    self.is_in_result_tag = True

    def handle_data(self, data):
        if self.is_recording:
            self.one_result += data + ' '
            self.is_recording = False



    def handle_endtag(self, tag):
        if self.is_in_result_tag and tag == 'li':
            self.results.append(self.one_result.rstrip(' '))
            self.one_result = ''
            self.is_recording = False
            self.is_in_result_tag = False
