import streamlit as st

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