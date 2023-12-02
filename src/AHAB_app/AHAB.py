#imports

import streamlit as st
import folium
import json
from streamlit_folium import st_folium

from IPython.display import HTML
from collections import Counter

import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz, process

from PIL import Image


#DFs

with open('../../data/CLEAN/audio_df.json', 'r') as audio:
    audio_products = json.load(audio)

with open('../../data/CLEAN/camera_df.json', 'r') as cameras:
    camera_products = json.load(cameras)

with open('../../data/CLEAN/lens_df.json', 'r') as lenses:
    lens_products = json.load(lenses)

with open('../../data/CLEAN/lights_df.json', 'r') as lights:
    light_products = json.load(lights)

with open('../../data/CLEAN/rental_places.json', 'r') as places:
    rental_places = json.load(places)

audiodf = pd.DataFrame(audio_products)
camerasdf = pd.DataFrame(camera_products)
lensesdf = pd.DataFrame(lens_products)
lightsdf = pd.DataFrame(light_products)
rentaldf = pd.DataFrame(rental_places)


data_frames = {'audio': audiodf, 'cameras': camerasdf, 'lenses': lensesdf, 'lights': lightsdf}


#Streamlit AHAB

class AHABFinder:
    def __init__(self, audiodf, camerasdf, lensesdf, lightsdf, rentaldf):
        
        self.audiodf = audiodf
        self.camerasdf = camerasdf
        self.lensesdf = lensesdf
        self.lightsdf = lightsdf
        self.rentaldf = rentaldf

    def find_products_in_dataframes(self, products):
        found_products_dict = {category: [] for category in ['Audio', 'Cameras', 'Lenses', 'Lights']}
        
        for category, df in zip(['Audio', 'Cameras', 'Lenses', 'Lights'], [self.audiodf, self.camerasdf, self.lensesdf, self.lightsdf]):
            found_products = []
            
            for product in products:
                # Filter by similarity and retrieve name and rental_place_id
                found = df[df['name'].apply(lambda x: fuzz.partial_ratio(x, product)) > 95][['name', 'rental_place_id']]
                found_products.extend(found.to_dict('records'))
            
            found_products_dict[category] = found_products
        
        return found_products_dict


    # Function to find the most common rental place ID

    def find_most_common_place_id(self, found_products_dict):
        all_ids = [item['rental_place_id'] for sublist in found_products_dict.values() for item in sublist]
        count_ids = Counter(all_ids)
        
        most_common_id = None
        if count_ids:  # Check if count_ids is not empty
            most_common_id = count_ids.most_common(1)[0][0]
        
        return most_common_id

    def get_rental_place_info(self, rental_place_id):
        
        return self.rentaldf[self.rentaldf['rental_place_id'] == str(rental_place_id)]#[['rental_place_name', 'address', 'email', 'phone', 'website']]


    def display_map(self, df):
            
            df_2 = pd.DataFrame(df)
            mp = folium.Map(location=[df_2['latitude'], df_2['longitude']], zoom_start=13)  # Initial map centered at a location

            # Add marker for rental shop location
            
            lat = df_2.latitude
            lon = df_2.longitude
            name = df_2.rental_place_name[0]
            address = df_2.address[0]
            phone = df_2.phone[0]
            
            popup = folium.Popup(f"Company: {name} <br> Address: {address} <br> Phone: {phone}", min_width=300, max_width=300)
            folium.Marker([lat, lon], popup = popup).add_to(mp)

            return mp          

#image

img = Image.open('images/AHAB_logo.png')
st.image(img)

state = 'home'

def main():
    #st.subheader('The film gear finder')
    st.markdown('Welcome to AHAB the Captain of the vessel that would help you find your gear'
            '\namong the ocean of rental shops. \n\nDo not hesitate to feed me your gear needs as I will not stop until I find'
            '\nwhat you are looking for.' 
            '\n\nOr you can filter the seven seas to find an arrange of gear that might fill'
            '\nyour needs. AAAARRRRG"')
    
    st.write("##")
    
    # Create AHABFinder instance
    finder = AHABFinder(audiodf, camerasdf, lensesdf, lightsdf, rentaldf)

    st.subheader('Enter a list of film gear items')
    user_input = st.text_input('(comma-separated)', 'Arri alexa 35, Arri/zeiss masterprime 18mm t1.3, Zoom h6, Nanlite pavotube 15c')

    if user_input:
        input_products = [prod.strip() for prod in user_input.lower().split(',')]
        
        found_products_dict = finder.find_products_in_dataframes(input_products)
        most_common_id = finder.find_most_common_place_id(found_products_dict)
        rental_place_info = finder.get_rental_place_info(most_common_id)
        rental_mp = finder.display_map(rental_place_info)

        # Display results
        st.subheader("Found Products in Each Category:")
        st.write(found_products_dict)

        st.subheader("Rental Place Information:")
        st.write(HTML(rental_place_info[['rental_place_name', 'address', 'email', 'phone', 'website']].to_html(render_links=True, escape=False)))
        
        # Display the map in Streamlit
        st.title('Rental Shop Locations')   
        st_folium(rental_mp, width = 1000)
        

if state == 'home':
    main()


# Function to display filter page
def show_filter_page():
    st.subheader("Filter Page")
    # Sidebar selection
    category = st.sidebar.selectbox("Select Category", options=['audio', 'cameras', 'lenses', 'lights'])

    if category:
        df = data_frames[category]
        selected_brand = st.sidebar.selectbox("Select Brand", options=df['brand'].unique())
        
        if selected_brand:
            filtered_data = df[df['brand'] == selected_brand]
            st.write(filtered_data[['name', 'price_a_day', 'link']])
        else:
            st.write(df[['name', 'price_a_day', 'link']])

st.write("##")

st.subheader('Or simply navigate through your options by clicking here:')
# Display navigation and filter option
if state == 'home':
    filter_option = st.checkbox("Filter Data")
    if filter_option:
        state = 'filter'

# Display content based on state
if state == 'home':
    st.text('')

else:
    show_filter_page()


