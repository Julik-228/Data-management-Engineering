from bs4 import BeautifulSoup
import requests
import pandas as pd

SOURCE = 'https://shop.ritual.ru/catalog/groby/elitnye_groby/'

get_source = requests.get(SOURCE)
get_source.raise_for_status()
print('Status code:', get_source.status_code)
# print(len(get_source.text))

soup = BeautifulSoup(get_source.text, 'html.parser')
# print(soup.title.text)

coffin = []
items = soup.select('div.catalog_item.main_item_wrapper.item_wrap')
# print(items)

for item in items:
    name_item = item.select_one('.item-title')
    name = name_item.get_text(strip = True) if name_item else None

    price_item = item.select_one('.price_matrix_wrapper')
    price = price_item.get_text(strip = True) if price_item else None

    article_item = item.select_one('.article_block')
    article = article_item.get_text(strip = True) if article_item else None 

    image_wrapper = item.select_one('.image_wrapper_block')
    image = None
    if image_wrapper:
        img_tag = image_wrapper.find('img')  
        if img_tag:
            image = img_tag.get('src')
            image = 'https://shop.ritual.ru/' + image

    if name:
        coffin.append(
            {
                'name': name,
                'price': price,
                'article': article,
                'image': image,
            }
        )
# print(coffin)

data = pd.DataFrame(coffin)
print(data)
