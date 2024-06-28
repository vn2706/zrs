import pandas as pd
import streamlit as st

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
        print("Error: feedback_data is not a pandas DataFrame.")
        return
    try:
        feedback_data = feedback_data.append({"name": name, "feedback": feedback}, ignore_index=True)
        feedback_data.to_csv(feedback_file_path, index=False)
        print("Feedback saved successfully.")
    except Exception as e:
        print("An error occurred while saving feedback:", e)

def load_feedback_data():
    global feedback_data
    try:
        feedback_data = pd.read_csv(feedback_file_path)
    except FileNotFoundError:
        print("Feedback file not found. Creating a new DataFrame.")
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

def main():
    # Add heading and tagline
    st.markdown("<h1 style='text-align: center; color: gold;'>Zomato Recommendation System</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: white;'>Discover the Best Food in Bangalore</h2>", unsafe_allow_html=True)

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Cuisine and Location", "New Restaurants", "Feedback"])

    with tab1:
        st.markdown("<h2 style='text-align: center; color: red;'>Find Restaurants by Cuisine and Location</h2>", unsafe_allow_html=True)
        selectedCuisine = zomatoData['cuisine'].unique()
        st.markdown("<h2 style='font-size: 24px;'><span style='color: red;'><b>Cuisine:</b></span></h2>", unsafe_allow_html=True)
        Cuisine = st.selectbox("", selectedCuisine)

        filterZomatoData = zomatoData[zomatoData['cuisine'] == Cuisine]
        filterLocation = filterZomatoData['location'].unique()
        st.markdown("<h2 style='font-size: 24px;'><span style='color: red;'>Location:</span></h2>", unsafe_allow_html=True)
        Location = st.selectbox("", filterLocation)

        if st.button("Predict"):
            st.write("Button clicked")

    with tab2:
        st.markdown("<h2 style='text-align: center; color: teal;'>Newly Open Restaurants</h2>", unsafe_allow_html=True)
        
        filterLocation = zomatoNewRestaurant['locations'].unique()
        st.markdown("<h2 style='font-size: 24px;'><span style='color: red;'><b>Location:</b></span></h2>", unsafe_allow_html=True)
        Location = st.selectbox("", filterLocation)

        showRestaurant = zomatoNewRestaurant[zomatoNewRestaurant['locations'] == Location]
        showRestaurantName = showRestaurant['restaurant_name'].unique()
        st.markdown("<h2 style='font-size: 24px;'><span style='color: red;'><b>Restaurant Name:</b></span></h2>", unsafe_allow_html=True)
        selectedRestaurant = st.selectbox("", showRestaurantName)

    with tab3:
        st.markdown("<h2 style='text-align: center; color: blue;'>Feedback</h2>", unsafe_allow_html=True)
        
        name = st.text_input("Enter your name:")
        feedback = st.text_area("Enter your feedback:")
        
        if st.button("Submit Feedback"):
            save_feedback(name, feedback)
            st.write("Feedback submitted successfully!")

if __name__ == "__main__":
    main()

       
