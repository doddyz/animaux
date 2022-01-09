# Next Dataframe function
# Then scrape from Live Webpage any african country first
# Remove unused vars & funs once main functions built
# See if possible to remove past uncessary commits from version history
# Translate BS manual into French + Spanish (Linguee)
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
    continent = 'africa'
    r = requests.get(BASE_URL + 'location/' + continent + '/' + country + '/')
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def get_animals_data_from_file(filename):
    page_urls, image_urls, names, descriptions = [], [], [], []
    data = {}
    with open(filename) as f:
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
            
            # print(f'{name}, {page_url}, {image_url}, {description}')
            page_urls.append(page_url)
            image_urls.append(image_url)
            names.append(name)
            descriptions.append(description)

        data['page_urls'] = page_urls
        data['image_urls'] = image_urls
        data['names'] = names
        data['descriptions'] = descriptions
        
    return pd.DataFrame(data)


# @st.cache        
def get_animals_data(country):
    page_urls, image_urls, names, descriptions = [], [], [], []
    data = {}
    
    soup = get_page_soup(country)
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
                
            # print(f'{name}, {page_url}, {image_url}, {description}')
        page_urls.append(page_url)
        image_urls.append(image_url)
        names.append(name)
        descriptions.append(description)

    data['page_urls'] = page_urls
    data['image_urls'] = image_urls
    data['names'] = names
    data['descriptions'] = descriptions
        
    return pd.DataFrame(data)

            
def draw_images_grid_from_df(df):
    st.images(df['image_urls'].to_list(), df['Names'].to_list())
