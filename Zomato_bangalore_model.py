import streamlit as st
import pandas as pd

# URLs to datasets
url1 = "https://raw.githubusercontent.com/anishkatoch/Zomato-Recommendation-Model/main/Datasets/zomatoCleanData.csv"
url2 = "https://raw.githubusercontent.com/anishkatoch/Zomato-Recommendation-Model/main/Datasets/zomatoNewRestaurant.csv"
url3 = "https://raw.githubusercontent.com/anishkatoch/Zomato-Recommendation-Model/main/Datasets/feedback.csv"

# Load datasets
zomatoData = pd.read_csv(url1)
zomatoNewRestaurant = pd.read_csv(url2)

# Feedback data handling
feedback_file_path = url3
feedback_data = pd.DataFrame(columns=["name", "feedback"])

def save_feedback(name, feedback):
    global feedback_data
    if not isinstance(feedback_data, pd.DataFrame):
        st.error("Error: feedback_data is not a pandas DataFrame.")
        return
    try:
        feedback_data = feedback_data.append({"name": name, "feedback": feedback}, ignore_index=True)
        feedback_data.to_csv(feedback_file_path, index=False)
        st.success("Feedback submitted successfully.")
    except Exception as e:
        st.error(f"An error occurred while saving feedback: {e}")

def load_feedback_data():
    global feedback_data
    try:
        feedback_data = pd.read_csv(feedback_file_path)
    except FileNotFoundError:
        st.warning("Feedback file not found. Creating a new DataFrame.")
        feedback_data = pd.DataFrame(columns=["name", "feedback"])

# Load existing feedback data if available
load_feedback_data()

# Set dark theme
page_bg_img = '''
    <style>
    body {
        background-color: #1F1F1F;
        color: #FFFFFF;
    }
    </style>
    ''' 
st.markdown(page_bg_img, unsafe_allow_html=True)

# Welcome page function
def welcome_page():
    st.markdown("<h1 style='text-align: center; color: gold;'>Welcome to Zomato Recommendation System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: justify; color: white; font-size: 18px;'>Welcome to our Zomato Recommendation System! Explore the best restaurants in Bangalore with our powerful recommendation engine. Click the Explore button below to get started.</p>", unsafe_allow_html=True)

    # Centering the Explore button
    st.markdown("<div style='display: flex; justify-content: center; margin-top: 20vh;'>", unsafe_allow_html=True)
    if st.button("Explore", key='explore_button'):
        st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Function to display Cuisine and Location tab content
def display_cuisine_location():
    st.markdown("<h2 style='text-align: center; color: red;'>Find Restaurants by Cuisine and Location</h2>", unsafe_allow_html=True)
    selectedCuisine = zomatoData['cuisine'].unique()
    Cuisine = st.selectbox("Select Cuisine:", selectedCuisine)

    filterZomatoData = zomatoData[zomatoData['cuisine'] == Cuisine]
    filterLocation = filterZomatoData['location'].unique()
    Location = st.selectbox("Select Location:", filterLocation)

    if st.button("Predict"):
        filtered_data = filterZomatoData[filterZomatoData['location'] == Location]
        if filtered_data.empty:
            st.warning("No restaurants found for the selected cuisine and location.")
        else:
            avg_price = round(filtered_data['price_for_one'].mean())
            best_restaurant = filtered_data.loc[filtered_data['price_for_one'].idxmin()]

            st.markdown(f"**Standard Rate:** {avg_price}")
            st.markdown(f"**Restaurant Name:** {best_restaurant['restaurant_name']}")
            st.markdown(f"**Timings:** {best_restaurant['timings']}")
            st.markdown(f"**Surf To:** [{best_restaurant['links']}]({best_restaurant['links']})")

# Function to display New Restaurants tab content
def display_new_restaurants():
    st.markdown("<h2 style='text-align: center; color: teal;'>Newly Open Restaurants</h2>", unsafe_allow_html=True)
    
    filterLocation = zomatoNewRestaurant['locations'].unique()
    Location = st.selectbox("Select Location:", filterLocation)

    showRestaurant = zomatoNewRestaurant[zomatoNewRestaurant['locations'] == Location]
    showRestaurantName = showRestaurant['restaurant_name'].unique()
    selectedRestaurant = st.selectbox("Select Restaurant:", showRestaurantName)

    if st.button("Confirm"):
        restaurantInfo = showRestaurant[showRestaurant['restaurant_name'] == selectedRestaurant]
        st.markdown(f"**Estimate Price:** {restaurantInfo['price_for_one'].values[0]}")
        st.markdown(f"**Cuisine:** {restaurantInfo['cuisins'].values[0]}")
        st.markdown(f"**Navigate To:** [{restaurantInfo['links'].values[0]}]({restaurantInfo['links'].values[0]})")

# Function to display Feedback tab content
def display_feedback():
    st.markdown("<h2 style='text-align: center; color: red;'>Feedback</h2>", unsafe_allow_html=True)
    name = st.text_input("Name")
    feedback = st.text_area("Feedback")
    
    if st.button("Submit"):
        if name.strip() == "" or feedback.strip() == "":
            st.warning("Please enter both name and feedback.")
        else:
            save_feedback(name, feedback)

# Main function to run the application
def main():
    welcome_page()

    # Check if Explore button has been clicked
    if st.session_state.get('explore_clicked', False):
        # Create tabs
        tab_selection = st.radio("Select a tab:", ["Cuisine and Location", "New Restaurants", "Feedback"])

        if tab_selection == "Cuisine and Location":
            display_cuisine_location()

        elif tab_selection == "New Restaurants":
            display_new_restaurants()

        elif tab_selection == "Feedback":
            display_feedback()

if __name__ == "__main__":
    main()

      
   



 
           




   
    
  
   

    

