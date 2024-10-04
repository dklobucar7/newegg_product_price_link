from bs4 import BeautifulSoup
import requests
import re

search_term = input("What product do you want to search for? ")

url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

# How many pages in results we have
page_text = doc.find(class_="list-tool-pagination-text").strong

pages = int(page_text.text.split("/")[-1])
print(pages)

items_found = {}

# Loop thru all result pages
for page in range(1, pages + 1):
    url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131&page={page}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")
    div = doc.find(
        class_="item-cells-wrap border-cells short-video-box items-list-view is-list"
    )

    items = div.find_all(string=re.compile(search_term))

    # Loop through all items
    for item in items:
        parent = item.parent  # ovo je a
        if parent.name != "a":
            continue

        link = parent["href"]
        next_parent = item.find_parent(class_="item-container")
        try:
            price = next_parent.find(class_="price-current").find("strong").string
            items_found[item] = {"price": int(price.replace(",", "")), "link": link}
        except:
            pass


sorted_items = sorted(items_found.items(), key=lambda x: x[1]["price"])

for item in sorted_items:
    print(item[0])
    print(f"${item[1]['price']}")
    print(item[1]["link"])
    print("--------------------------------------------")
