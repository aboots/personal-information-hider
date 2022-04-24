import requests
from bs4 import BeautifulSoup
from hazm import Normalizer

normalizer = Normalizer()


def clean_data(name):
    normalized_name = normalizer.normalize(name).replace('\n', '').strip()
    if normalized_name.startswith('گروه'):
        return normalized_name.replace('گروه ', '')
    else:
        return normalized_name


url = f"https://fa.wikipedia.org/wiki/%D9%81%D9%87%D8%B1%D8%B3%D8%AA_%D8%A8%D8%B2%D8%B1%DA%AF%D8%AA%D8%B1%DB%8C%D9%86_%D8%B4%D8%B1%DA%A9%D8%AA%E2%80%8C%D9%87%D8%A7%DB%8C_%D8%AA%D9%88%D9%84%DB%8C%D8%AF%DB%8C_%D8%A8%D8%B1_%D9%BE%D8%A7%DB%8C%D9%87_%D8%AF%D8%B1%D8%A2%D9%85%D8%AF"
brands_names = []

f = requests.get(url)
soup = BeautifulSoup(f.content, 'lxml')
rows = soup.findAll("tbody")[0].findAll('tr')
for i in range(1, len(rows)):
    row = rows[i]
    brands_names.append(row.findAll('td')[0].text)
normalized_brands = []
for brand in brands_names:
    normalized_brands.append(clean_data(brand))
print(normalized_brands)
with open(f"national_companies.txt", "w", encoding="utf-8") as file:
    file.write('\n'.join(normalized_brands))
