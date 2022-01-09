# Next Dataframe function
# Then scrape from Live Webpage any african country first
# Images et description par pays (afrique puis Europe)
# On peut creer une librairie simple utilisant les fonctions de base (généralité de ce que lon compose) 

import pandas as pd
import re
import requests
import streamlit as st
from bs4 import BeautifulSoup
from bs4 import NavigableString, Tag

BASE_URL = 'https://a-z-animals.com/animals/'

# Use for both name and page url
NAME_PATTERN = re.compile(r'^<a href="https://a-z-animals.com/animals/(.+)/">')
IMAGE_URL_PATTERN = re.compile(r'src="https://a-z-animals.com/media/animals/images/original/([a-z]+-\d+x\d+.jpg)"')
DESCRIPTION_PATTERN = re.compile(r'<p class="card-fun-fact">(.+)</p>')



def get_page_local_soup(country):
    with open(country + 'location/' + '.html') as f:
        soup = BeautifulSoup(f, 'html.parser')
    return soup


def get_page_soup(country):
    r = requests.get(BASE_URL + country + '/')
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def get_animals_data_from_file():
    data = {}
    with open('togo.html') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        card_divs = soup.find_all('div', class_='card')
        for card_div in card_divs:
            page_url = card_div.a['href']
            image_url = card_div.img['src']
            name = card_div.h5.a.get_text()
            description = card_div.find(class_='card-fun-fact')
            if description is None:
                description = 'Dummy empty description here'
            else:
                description = description.get_text()
            
            print(f'{name}, {page_url}, {image_url}, {description}')
    

def get_animals_data(country):
    data = {}
    soup = get_page_soup(country)
    card_divs = soup.find_all('div', class_='card')
    for result in card_divs:
        for child in result.children:
            if isinstance(child, NavigableString):
                continue
            if isinstance(child, Tag):
                page_url_tag = child.a
                image_url_tag = child.img
                print(f'{page_url_tag}, {image_url_tag}')
                
                # page_url = page_url_tag['href']
                # image_url = image_url_tag['src']
        # name = card.img.div.div.h5.content
        # description = DESCRIPTION_PATTERN.search(card).groups()[0]
        
            # data[page_url_tag.contents] = {'image_url': image_url_tag.contents}

    # return data

            
        

# @st.cache
def df_from_content(country):
    pass
