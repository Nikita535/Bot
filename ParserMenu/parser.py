import requests
import lxml
from bs4 import BeautifulSoup

def get_first_menu_item():
    headers = {
        "user-agent" : "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Mobile Safari/537.36"
    }
    url = "https://cafe-anderson.ru/cakes/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    catalog_list = soup.find_all("ul", class_="catalog-list catalog-col-4")

    # print(catalog_list[0])

    for card in catalog_list:
        cake = card.find_all("li", class_="catalog-list__item")
        for c in cake:
            card_name = c.find("div", class_="c-card-catalog-3__title js-show-pie-order").text
            card_desc = c.find("div", class_="c-card-catalog-3__weight").text
            card_price = c.find("div", class_="").text[12:-1]
            card_link_photo_ = str(c.find("div", class_="c-card-catalog-3__img"))
            card_link_photo = card_link_photo_[card_link_photo_.find('(')+1:card_link_photo_.find(')')]

            print(f"{card_name} | {card_desc} | {card_price} | {card_link_photo}")

get_first_menu_item()