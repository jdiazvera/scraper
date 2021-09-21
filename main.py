# -*- coding: utf-8 -*-

from time import sleep
from bs4 import BeautifulSoup
from helpers.item import Item
from helpers.amazon import Amazon
from tqdm import tqdm
#file = open('source.csv', 'w', encoding='utf-8')

#file.writelines('id,asin,url,title, price, status\n')
amazon = Amazon()


def write(product, item):
    file.writelines(f'{product.id},{product.asin},{product.url},{item.title},{item.price},{status}\n')
    return True

def write2file(product, item):
    with open('output/'+product.asin, 'w') as f:
        f.writelines(f'{product.id},{product.asin},{product.url},{item.title},{item.price},{status}\n')
    return True

def write2console(product, item):
    print(f'{product.asin}, {item.title}, {item.description}\n')

# for product in tqdm(amazon.build_urls()):
#    sleep(10)
#    soup = amazon.get(product)
#    item = Item(soup)
#    status = 1 if item.price != 0 else 0
#    write(product, item)

with open('asins', 'r') as file:
    for line in file.readlines():
        product = amazon.build_url(line)
        soup = amazon.get(product)
        item = Item(soup)
        print(item)
        status = 1 if item.price != 0 else 0
        write2console(product, item)
        
#file.close()