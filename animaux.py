# Regler probleme pays avec espace dans leur nonm (uk, usa, ...)
# Ajouter description et lien page animal en meme temps
# merge get_animals_data_from_file and get_animals_data
# Traduire pays, names et description en français 
# See if possible to remove past uncessary commits from version history
# Translate BS manual into French + Spanish (Linguee)
# Images et description par pays (afrique puis Europe)
# On peut creer une librairie simple utilisant les fonctions de base (généralité de ce que lon compose) 

import pandas as pd
import pycountry
import requests
import streamlit as st
from bs4 import BeautifulSoup
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2

CONTINENTS = {'AF': 'africa', 'EU': 'europe', 'SA': 'south-america', 'NA': 'north-america', 'OC': 'oceania'}

COUNTRIES = [country.name for country in list(pycountry.countries)]

BASE_URL = 'https://a-z-animals.com/animals/'

def get_country_continent(country):
    try:
        country_code =  country_name_to_country_alpha2(country, cn_name_format='lower')
    except:
        country_code = 'Inconnu' 
    try:
        country_continent = country_alpha2_to_continent_code(country_code)
    except:
        country_continent = 'Inconnu' 
    return country_continent

def get_page_soup(country):
    continent_code = get_country_continent(country)
    # st.write(continent_code)
    continent = CONTINENTS[continent_code]
    # st.write(continent)
    r = requests.get(BASE_URL + 'location/' + continent + '/' + country.replace(' ', '-') + '/')
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
            
            page_urls.append(page_url)
            image_urls.append(image_url)
            names.append(name)
            descriptions.append(description)

        data['page_urls'] = page_urls
        data['image_urls'] = image_urls
        data['names'] = names
        data['descriptions'] = descriptions
        
    return pd.DataFrame(data)


@st.cache
def get_animals_data(country):
    data = {}
    page_urls, image_urls, names, descriptions = [], [], [], []    
    soup = get_page_soup(country)
    card_divs = soup.find_all('div', class_='card')
    for card_div in card_divs:
        page_url = card_div.a['href']
        image_url = card_div.img['src']
        if image_url == '':
            image_url = 'https://via.placeholder.com/400x300'
        name = card_div.h5.a.get_text()
        description = card_div.find(class_='card-fun-fact')
        if description is None:
            description = 'Dummy empty description here'
        else:
            description = description.get_text()
            
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

    captions_series = df['names'] + ' - ' + df['descriptions']
    
    st.image(df['image_urls'].to_list(), captions_series.to_list(), 400)
