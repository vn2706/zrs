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
        print("Error: feedback_data is not a pandas DataFrame.")
        return
    try:
        feedback_data = feedback_data.append({"name": name, "feedback": feedback}, ignore_index=True)
        feedback_data.to_csv(feedback_file_path, index=False)
        st.write("Feedback saved successfully.")
    except Exception as e:
        st.write("An error occurred while saving feedback:", e)

def load_feedback_data():
    global feedback_data
    try:
        feedback_data = pd.read_csv(feedback_file_path)
    except FileNotFoundError:
        st.write("Feedback file not found. Creating a new DataFrame.")
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

def predict_function(cuisine, location):
    filtered_data = zomatoData[(zomatoData['cuisine'] == cuisine) & (zomatoData['location'] == location)]
    if filtered_data.empty:
        return "No restaurants found for the selected cuisine and location."

    avg_price = round(filtered_data['price_for_one'].mean())
    best_restaurant = filtered_data.loc[filtered_data['price_for_one'].idxmin()]
    
    result = {
        "Standard Rate": avg_price,
        "Restaurant Name": best_restaurant['restaurant_name'],
        "Timings": best_restaurant['timings'],
        "Surf To": best_restaurant['links']
    }
    return result

# Function to display Cuisine and Location tab content
def display_cuisine_location():
    st.markdown("<h2 style='text-align: center; color: red;'>Find Restaurants by Cuisine and Location</h2>", unsafe_allow_html=True)
    selectedCuisine = zomatoData['cuisine'].unique()
    Cuisine = st.selectbox("Select Cuisine:", selectedCuisine)

    filterZomatoData = zomatoData[zomatoData['cuisine'] == Cuisine]
    filterLocation = filterZomatoData['location'].unique()
    Location = st.selectbox("Select Location:", filterLocation)

    if st.button("Predict"):
        prediction_result = predict_function(Cuisine, Location)
        
        if isinstance(prediction_result, dict):
            st.markdown("<h3>Standard Rate:</h3>")
            st.write(prediction_result["Standard Rate"])
            st.markdown("<h3>Restaurant Name:</h3>")
            st.write(prediction_result["Restaurant Name"])
            st.markdown("<h3>Timings:</h3>")
            st.write(prediction_result["Timings"])
            st.markdown("<h3>Surf To:</h3>")
            st.write(prediction_result["Surf To"])
        else:
            st.write(prediction_result)

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
        st.markdown("<h3>Estimate Price:</h3>")
        st.write(restaurantInfo['price_for_one'].values[0])
        st.markdown("<h3>Cuisine:</h3>")
        st.write(restaurantInfo['cuisins'].values[0])
        st.markdown("<h3>Navigate To:</h3>")
        st.write(restaurantInfo['links'].values[0])

# Function to display Feedback tab content
def display_feedback():
    st.markdown("<h2 style='text-align: center; color: red;'>Feedback</h2>", unsafe_allow_html=True)
    name = st.text_input("Name")
    feedback = st.text_area("Feedback")
    
    if st.button("Submit"):
        save_feedback(name, feedback)
        st.success("Thank you for your feedback!")

# Main function to run the application
def main():
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


