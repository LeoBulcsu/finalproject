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
        
        product_dict = {}
        
        for category, df in zip(['Audio', 'Cameras', 'Lenses', 'Lights'], [self.audiodf, self.camerasdf, self.lensesdf, self.lightsdf]):
            
            found_products = []
            
            for product in products:
                found = df[df['name'].apply(lambda x: fuzz.partial_ratio(x, product)) > 95]['rental_place_id'].tolist()
                found_products.extend(found)
            
            product_dict[category] = found_products
        
        return product_dict

    def find_most_common_place_id(self, found_products_dict):
        
        all_ids = [item for sublist in found_products_dict.values() for item in sublist]
        count_ids = Counter(all_ids)
        most_common_id = count_ids.most_common(1)[0][0]
        
        return most_common_id

    def get_rental_place_info(self, rental_place_id):
        
        return self.rentaldf[self.rentaldf['rental_place_id'] == str(rental_place_id)][['rental_place_name', 'address', 'email', 'phone', 'website']]


    def find_rental_place_for_products(self):
        
        user_input = input("Enter a list of products separated by commas: ")
        input_products = [prod.strip() for prod in user_input.lower().split(',')]
        
        found_products_dict = self.find_products_in_dataframes(input_products)
        most_common_id = self.find_most_common_place_id(found_products_dict)
        rental_place_info = self.get_rental_place_info(most_common_id)
        
        return found_products_dict, most_common_id, rental_place_info

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

    # Text input for users to enter their list of items
    # st.subheader('Enter a list of film gear items')
    # items_input = st.text_input('(comma-separated)', 'ex: Arri Alexa 35, ArriZeiss 28mm, SkyPanel')
    
    # Create AHABFinder instance
    finder = AHABFinder(audiodf, camerasdf, lensesdf, lightsdf, rentaldf)

    st.subheader('Enter a list of film gear items')
    user_input = st.text_input('(comma-separated)', 'Arri alexa 35, Arri/zeiss masterprime 18mm t1.3, Zoom h6, Nanlite pavotube 15c')

    if user_input:
        input_products = [prod.strip() for prod in user_input.lower().split(',')]
        
        found_products_dict = finder.find_products_in_dataframes(input_products)
        most_common_id = finder.find_most_common_place_id(found_products_dict)
        rental_place_info = finder.get_rental_place_info(most_common_id)

        # Display results
        st.subheader("Found Products in Each Category:")
        st.write(found_products_dict)

        st.subheader("Rental Place Information:")
        st.write(HTML(rental_place_info.to_html(render_links=True, escape=False)))


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



# Locations map

# Load rental_places.json with latitudes and longitudes
with open('../../data/CLEAN/rental_places.json', 'r') as file:
    rental_places = json.load(file)

def display_map():
    
    map = folium.Map(location=[40.471981, -3.704809], zoom_start=10.5)  # Initial map centered at a location

    # Add markers for rental shop locations
    for place in rental_places:
        lat = place['latitude']
        lon = place['longitude']
        name = place['rental_place_name']
        address = place['address']
        phone = place['phone']
        popup = folium.Popup(f"Company: {name} <br> Address: {address} <br> Phone: {phone}", min_width=300, max_width=300)
        folium.Marker([lat, lon], popup = popup).add_to(map)

    # Display the map in Streamlit
    st.title('Rental Shop Locations')
    st_folium(map, width = 1000)  # Display the Folium map in Streamlit

if __name__ == '__main__':
    display_map()

