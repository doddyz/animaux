# Il faudra regler l'alignement des largeurs de tables de modes distincts avec contraintes existantes sur les tables st.columns

from animaux import *
import streamlit as st

st.set_page_config('Animaux', page_icon=':zebra_face:', layout='wide', initial_sidebar_state='expanded')

st.title('Animaux')


# CSS used to hide dataframes indexes
hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """

# This code will hide the dataframes indexes, see where to place it
st.markdown(hide_table_row_index, unsafe_allow_html=True)


# Sidebar widgets
# pays = st.sidebar.text_input('Tapez ici le pays à rechercher')
pays = st.sidebar.selectbox('Choisissez un pays', COUNTRIES, 2)

if not (pays is None):
    
    st.markdown(f'### {pays.title()}')

    st.write('#####')

    df = get_animals_data(pays.lower())
    
    # df
    
    draw_images_grid_from_df(df)

