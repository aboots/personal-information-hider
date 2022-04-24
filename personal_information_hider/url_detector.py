import re
from parsi_io.modules.address_extractions import AddressExtraction


class UrlDetection:
    hiding_text = "<#url_address#>"

    def __init__(self):
        self.extractor = AddressExtraction()

    def hide_url(self, text):
        data = self.extractor.run(text)
        url_list = []
        email_regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        for url in data['url']:
            if not (re.search(email_regex, url)):
                url_list.append(url)
        for url in url_list:
            text = text.replace(url, self.hiding_text, 1)
        return text
