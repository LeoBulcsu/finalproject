#imports

import streamlit as st
import folium
import json



def main():
    st.title('AHAB - Film Gear Finder')
    
    # Text input for users to enter their list of items
    items_input = st.text_input('Enter a list of film gear items (comma-separated)', 'Camera, Lens, Lighting')
    
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




# Load rental_places.json with latitudes and longitudes
with open('../data/CLEAN/rental_places.json', 'r') as file:
    rental_places = json.load(file)

def display_map():
    m = folium.Map(location=[40.45456508369153, -3.7239992747135258], zoom_start=11)  # Initial map centered at a location

    # Add markers for rental shop locations
    for place in rental_places:
        lat = place['latitude']
        lon = place['longitude']
        name = place['rental_place_name']
        folium.Marker([lat, lon], popup=name).add_to(m)

    # Display the map in Streamlit
    folium_static(m)

if __name__ == '__main__':
    st.title('Rental Shop Locations')
    display_map()
