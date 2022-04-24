import requests
from bs4 import BeautifulSoup
from hazm import Normalizer

normalizer = Normalizer()


def clean_data(name):
    normalized_name = normalizer.normalize(name).replace('\n', '').strip()
    second_name = None
    if 'شرکت' in normalized_name:
        normalized_name = " ".join(normalized_name.split(' ')[1:])
    if '(' in normalized_name:
        second_name = normalized_name.split('(')[1].strip(')')
        normalized_name = normalized_name.split('(')[0].strip()
    return [normalized_name, second_name] if second_name else [normalized_name]


url = f"http://ircreative.isti.ir/contents.php?cntid=112"

brands_names = []

f = requests.get(url)
soup = BeautifulSoup(f.content, 'lxml')
rows = soup.findAll("tbody")[0].findAll('tr')
for i in range(2, len(rows)):
    row = rows[i]
    brands_names.append(row.findAll('td')[1].text)
normalized_brands = []
for brand in brands_names:
    normalized_brands.extend(clean_data(brand))
print(normalized_brands)
with open(f"iranian_companies.txt", "w", encoding="utf-8") as file:
    file.write('\n'.join(normalized_brands))
