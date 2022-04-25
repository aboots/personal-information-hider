from parstdex import Parstdex


class BirthdayDateDetection:
    abbvr = '000_000'
    hiding_text = "<#birthday_date#>"

    def __init__(self):
        self.model = Parstdex()
        self.before_keywords = ['ولادت', 'تولد', 'متولد']
        self.after_keywords = ['به دنیا', 'زاده', 'متولد شد']

    def is_any_keyword_in_text(self, text, keywords):
        for keyword in keywords:
            if keyword in text:
                return True
        return False

    def extract_birthday_spans(self, text, spans):
        final_spans = []
        for span in spans:
            start = max(0, span[0] - 20)
            end = min(len(text), span[1] + 20)
            if self.is_any_keyword_in_text(text[start:span[0]], self.before_keywords) or self.is_any_keyword_in_text(
                    text[span[1]: end], self.after_keywords):
                final_spans.append(span)
        return final_spans

    def convert_text(self, text, spans):
        final_text = ""
        last_span = 0
        for span in spans:
            if text[span[0]:span[1]] == self.abbvr:
                continue
            final_text += text[last_span:span[0]] + self.abbvr
            last_span = span[1]
        return final_text + text[last_span:]

    def hide_date_names(self, text):
        spans = self.model.extract_span(text)['datetime']
        birthday_spans = self.extract_birthday_spans(text, spans)
        text = self.convert_text(text, birthday_spans)
        return text.replace(self.abbvr, self.hiding_text)
