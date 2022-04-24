import inspect
import os
import re

from hazm import POSTagger, word_tokenize
from nltk import RegexpParser


def open_file(filename):
    pkg_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    return open(pkg_dir + "/" + filename, 'r', encoding="utf-8")


class CompanyDetection:
    hiding_text = "<#company_name#>"
    abbvr = '0000'

    def __init__(self, use_pos):
        self.use_pos = use_pos
        if use_pos:
            self.tagger = POSTagger(model='personal_information_hider/resources/postagger.model')

        file = open_file('resources/iranian_companies.txt')
        self.companies = file.read().split('\n')
        file.close()

        file = open_file('resources/national_companies.txt')
        self.companies.extend(file.read().split('\n'))
        file.close()

        self.before_companies_words = 'شرکت|موسسه|سازمان|کمپانی'

    def nn_ext(self, sentence):
        grammar = r"""
        NNN: {<N|Ne><N|Ne>}
      """
        cp = RegexpParser(grammar)
        return (cp.parse(sentence))

    def find_NNs(self, text):
        NNs = []
        tree = self.nn_ext(self.tagger.tag(word_tokenize(text)))
        for subtree in tree.subtrees():
            if subtree.label() == 'NNN':
                NNs.append(" ".join([lf[0] for lf in subtree.leaves()]))
        return NNs

    def find_companies_names(self, text):
        companies_pattern = f"({'|'.join(self.companies)})"
        spans = []
        for obj in re.finditer(companies_pattern, text):
            spans.append(obj.span(1))
        return spans

    def find_other_companies(self, text):
        NNs = self.find_NNs(text) if self.use_pos else None
        pattern = f"({self.before_companies_words})\W+(\w+)"
        spans = []
        for obj in re.finditer(pattern, text):
            if self.use_pos:
                if obj.group() in NNs:
                    spans.append(obj.span(2))
            else:
                spans.append(obj.span(2))
        return spans

    def convert_text(self, text, spans):
        final_text = ""
        last_span = 0
        for span in spans:
            if text[span[0]:span[1]] == self.abbvr:
                continue
            final_text += text[last_span:span[0]] + self.abbvr
            last_span = span[1]
        return final_text + text[last_span:]

    def hide_companies_names(self, text):
        text = self.convert_text(text, self.find_companies_names(text))
        text = self.convert_text(text, self.find_other_companies(text))
        return text.replace(self.abbvr, self.hiding_text)
