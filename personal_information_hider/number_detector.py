import re
from hazm import *


def join_patterns(items):
    return '(?:' + '|'.join(list(items)) + ')'


class NumberDetection:
    ENGLISH_NON_ZERO_DIGITS = '123456789'
    PERSIAN_NON_ZERO_DIGITS = '۱۲۳۴۵۶۷۸۹'
    ENGLISH_ZERO_DIGIT = '0'
    PERSIAN_ZERO_DIGIT = '۰'
    PATTERN_DIGIT = join_patterns(
        list(ENGLISH_NON_ZERO_DIGITS + PERSIAN_NON_ZERO_DIGITS + ENGLISH_ZERO_DIGIT + PERSIAN_ZERO_DIGIT))
    PATTERN_NUMBER_WITH_DIGITS = f'{PATTERN_DIGIT}+'

    def find_num(self, inp):
        matches = []
        for keyword_count in range(10, 0, -1):
            count_pattern = self.PATTERN_NUMBER_WITH_DIGITS.format()
            for matched in re.finditer(count_pattern, inp):
                start, end = matched.span()
                inp = inp[:start] + '#' * (end - start) + inp[end:]
                matched_dict = {}
                matched_dict['phrase'] = matched.group()
                matched_dict['span'] = (matched.start(), matched.end())
                matches.append(matched_dict)
        return matches

    def hide_personal_numbers(self, text):
        word_tokens = word_tokenize(text)
        extracted_numbers = self.find_num(text)
        iter_index = 0
        iter_text_words = 0
        if len(extracted_numbers):
            while iter_index < len(extracted_numbers):
                if word_tokens[iter_text_words] == extracted_numbers[iter_index]['phrase']:
                    for i in range(-3, 2):
                        type_recognized = False
                        if iter_text_words + i >= 0 and iter_text_words + i < len(word_tokens):
                            if word_tokens[iter_text_words + i] in ['تماس', 'تلفن', 'زنگ', 'موبایل', 'شماره منزل']:
                                extracted_numbers[iter_index]['type'] = 'phone_number'
                                type_recognized = True
                                text = text.replace(extracted_numbers[iter_index]['phrase'], "<#phone#>")
                                break
                            elif word_tokens[iter_text_words + i] in ['حساب', 'بانک']:
                                extracted_numbers[iter_index]['type'] = 'account_number'
                                type_recognized = True
                                text = text.replace(extracted_numbers[iter_index]['phrase'], "<#account_number#>")
                                break
                            elif word_tokens[iter_text_words + i] in ['ملی', 'کدملی']:
                                if iter_text_words + i - 1 >= 0:
                                    bigram = word_tokens[iter_text_words + i - 1] + " " + word_tokens[
                                        iter_text_words + i]
                                    if bigram in ['کد ملی', 'شماره ملی']:
                                        extracted_numbers[iter_index]['type'] = 'national_number'
                                        type_recognized = True
                                        text = text.replace(extracted_numbers[iter_index]['phrase'],
                                                            "<#national_number#>")
                                        break
                        if not type_recognized:
                            extracted_numbers[iter_index]['type'] = 'None'
                    iter_index += 1
                iter_text_words += 1
        return text