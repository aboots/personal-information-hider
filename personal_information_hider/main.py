from hazm import Normalizer

from personal_information_hider import UrlDetection, EmailDetection, CompanyDetection, BirthdayDateDetection, \
    NameDetection, NumberDetection, AddressDetection


def run(address, use_pos=True):
    file = open(address, 'r', encoding="utf-8")
    text = file.read()
    file.close()
    text = EmailDetection().hide_emails(text)
    text = UrlDetection().hide_url(text)
    normalizer = Normalizer()
    text = normalizer.normalize(text)
    text = CompanyDetection(use_pos).hide_companies_names(text)
    text = BirthdayDateDetection().hide_date_names(text)
    text = AddressDetection().hide_address(text)
    text = NameDetection().hide_person_name(text)
    text = NumberDetection().hide_personal_numbers(text)
    return text
