from parsi_io.modules.address_extractions import AddressExtraction


class AddressDetection:
    abbvr = '000_000'
    hiding_text = "<#address#>"

    def __init__(self):
        self.extractor = AddressExtraction()

    def convert_text(self, text, data):
        final_text = ""
        last_span = 0
        spans = data['address_span']
        for i, address in enumerate(data['address']):
            span = (spans[2 * i], spans[(2 * i) + 1])
            if text[span[0]:span[1]] == self.abbvr:
                continue
            final_text += text[last_span:span[0]] + self.abbvr
            last_span = span[1]
        return final_text + text[last_span:]

    def hide_address(self, text):
        data = self.extractor.run(text)
        text = self.convert_text(text, data)
        return text.replace(self.abbvr, self.hiding_text)
