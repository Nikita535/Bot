"""
parser.py
====================================
The module for parse web document to json file
"""
import json
import requests
import lxml
from bs4 import BeautifulSoup
from DataBase import sqlite_db

def get_first_menu_item():
    """
    Parsing divs from site into dictionary,then convert it into json file
    """
    headers = {
        "user-agent": "user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Mobile Safari/537.36"
    }
    url = "https://xn--80aaac2aiu7bg5b9c.xn--p1ai/menu"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    menu = soup.find_all("div", class_="menu-items-holder")

    menu_dict = {}
    for item in menu:
        item = item.find_all("div", class_="catalogue__item")
        for i in item:
            i_name = i.find("div", class_="catalogue__item-title").text.strip()
            i_price = str(i.find("div", class_="catalogue__item-price").text.strip()).replace("₽", "руб.")

            i_photo_link_ = str(i.find("div", class_="catalogue__item-pic"))

            i_photo_link = "https://xn--80aaac2aiu7bg5b9c.xn--p1ai" + i_photo_link_[i_photo_link_.find('(') + 1:i_photo_link_.find(')')]

            i_photo_name= i_photo_link_[i_photo_link_.find('(') + 1:i_photo_link_.find(')')]
            i_photo_name =i_photo_name[i_photo_name.rfind('/')+1:]

            img_data = requests.get(i_photo_link, verify=False).content

            with open('ParserMenu/pics/' + i_photo_name,'wb') as handler:
                handler.write(img_data)

            i_link_photo_id = i_photo_link.split("/")[-1]
            i_link_photo_id = i_link_photo_id[:-5]

            # print(f"{i_name} | {i_price} | {i_photo_link} | {i_link_photo_id}")
            # print(f"{i_price}")
            menu_dict[i_link_photo_id] = {
                "name": i_name,
                "price": i_price,
                "photo_link": i_photo_link,
                "photo_name":i_photo_name
            }
        # print(menu_dict)
    print(menu_dict)

    with open("./ParserMenu/menu_dict.json", "w", encoding='utf-8') as file:
        json.dump(menu_dict, file, indent=4, ensure_ascii=False)
    sqlite_db.sql_add_from_json()

def main():
    """
    Running parse function
    """
    get_first_menu_item()


if __name__ == '__main__':
    main()
