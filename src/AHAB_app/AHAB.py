#imports

import streamlit as st
import folium
import json
from streamlit_folium import st_folium



def main():
    st.title('AHAB - Film Gear Finder')
    
    # Text input for users to enter their list of items
    items_input = st.text_input('Enter a list of film gear items (comma-separated)', 'Arri Alexa 35, ArriZeiss 28mm, SkyPanel')
    
    if st.button('Find Rental Place'):
        items_list = [item.strip() for item in items_input.split(',')]
        # Process the list and find the rental place offering most items
        recommended_place = find_rental_place(items_list)
        st.write(f"Recommended Rental Place: {recommended_place}")

def find_rental_place(items_list):
    # Logic to find the rental place offering most items from the list
    # You'll use the items list and your DataFrames to perform this matching
    
    # Sample logic (you'll need to adjust this based on your data structure)
    recommended_place = "Sample Rental Place"
    
    return recommended_place

if __name__ == '__main__':
    main()


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

