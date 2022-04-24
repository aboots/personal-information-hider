from parsi_io.modules.address_extractions import AddressExtraction


class EmailDetection:
    hiding_text = "<#email_address#>"

    def __init__(self):
        self.extractor = AddressExtraction()

    def hide_emails(self, text):
        email_list = self.extractor.run(text)['email']
        for email in email_list:
            text = text.replace(email, self.hiding_text, 1)
        return text
