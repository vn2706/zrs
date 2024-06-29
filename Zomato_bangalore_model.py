import streamlit as st
import pandas as pd
import time

# Function to simulate loading animation
def loading_animation():
    st.markdown(
        """
        <div style='display: flex; justify-content: center; align-items: center; height: 80vh;'>
            <img src='https://media.giphy.com/media/7LsZmLKs3YbRO/giphy.gif' alt='loading' style='width: 40%;'>
        </div>
        """,
        unsafe_allow_html=True
    )
    time.sleep(3)  # Simulate a delay for loading animation

# Main function for Zomato recommendation system
def main():
    # Display welcome page
    st.markdown("<h1 style='text-align: center; color: gold;'>Welcome to Zomato Recommendation System</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: white;'>Discover the Best Food in Bangalore</h2>", unsafe_allow_html=True)
    
    # Show loading animation
    loading_animation()

    # Continue to the main functionality
    import_zomato_recommendation_system()

# Function to import Zomato recommendation system
def import_zomato_recommendation_system():
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
        nonlocal feedback_data
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
        nonlocal feedback_data
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

    # Main UI
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
            prediction_result = predict_function(Cuisine, Location)

            if isinstance(prediction_result, dict):
                st.markdown("<span style='color: Olivedrab; font-family: \"Times New Roman\", Times, serif; font-weight: bold; font-size: 32px; margin-right: 10px;'>Standard Rate:</span><span style='color: purple; font-family: \"Georgia\", serif; font-weight: bold; font-size: 30px;'>{}</span>".format(prediction_result["Standard Rate"]), unsafe_allow_html=True)
                st.markdown("<span style='color: Olivedrab; font-family: \"Times New Roman\", Times, serif; font-weight: bold; font-size: 32px; margin-right: 10px;'>Restaurant Name:</span><span style='color: purple; font-family: \"Georgia\", serif; font-weight: bold; font-size: 27px;'>{}</span>".format(prediction_result["Restaurant Name"]), unsafe_allow_html=True)
                st.markdown("<span style='color: Olivedrab; font-family: \"Times New Roman\", Times, serif; font-weight: bold; font-size: 32px; margin-right: 10px;'>Timings:</span><span style='color: purple; font-family: \"Georgia\", serif; font-weight: bold; font-size: 27px;'>{}</span>".format(prediction_result["Timings"]), unsafe_allow_html=True)
                st.markdown("<span style='color: Olivedrab; font-family: \"Times New Roman\", Times, serif; font-weight: bold; font-size: 32px; margin-right: 10px;'>Surf To:</span><span style='color: purple; font-family: \"Georgia\", serif; font-weight: bold; font-size: 27px;'><a href='{0}' style='color: purple;'>{0}</a></span>".format(prediction_result["Surf To"]), unsafe_allow_html=True)
            else:
                st.markdown("<span style='color: red;'>{}</span>".format(prediction_result), unsafe_allow_html=True)

    with tab2:
        st.markdown("<h2 style='text-align: center; color: teal;'>Newly Open Restaurants</h2>", unsafe_allow_html=True)

        filterLocation = zomatoNewRestaurant['locations'].unique()
        st.markdown("<h2 style='font-size: 24px;'><span style='color: red;'><b>Location:</b></span></h2>", unsafe_allow_html=True)
        Location = st.selectbox("", filterLocation)

        showRestaurant = zomatoNewRestaurant[zomatoNewRestaurant['locations'] == Location]
        showRestaurantName = showRestaurant['restaurant_name'].unique()
        st.markdown("<h2 style='font-size: 24px;'><span style='color: red;'><b>Restaurant Name:</b></span></h2>", unsafe_allow_html=True)
        selectedRestaurant = st.selectbox("", showRestaurantName)

        if st.button("Confirm"):
            restaurantInfo = showRestaurant[showRestaurant['restaurant_name'] == selectedRestaurant]
            Estimate = restaurantInfo['price_for_one'].values[0]
            dishes = restaurantInfo['cuisins'].values[0]
            navigateTo = restaurantInfo['links'].values[0]

            st.markdown("<span style='color: Olivedrab; font-family: \"Times New Roman\", Times, serif; font-weight: bold; font-size: 32px; margin-right: 10px;'>Estimate Price:</span><span style='color: purple; font-family: \"Georgia\", serif; font-weight: bold; font-size: 30px;'>{}</span>".format(Estimate), unsafe_allow_html=True)
            st.markdown("<span style='color: Olivedrab; font-family: \"Times New Roman\", Times, serif; font-weight: bold; font-size: 32px; margin-right: 10px;'>Cuisine:</span><span style='color: purple; font-family: \"Georgia\", serif; font-weight: bold; font-size: 27px;'>{}</span>".format(dishes), unsafe_allow_html=True)
            st.markdown("<span style='color: Olivedrab; font-family: \"Times New Roman\", Times, serif; font-weight: bold; font-size: 32px; margin-right: 10px;'>Navigate To:</span><span style='color: purple; font-family: \"Georgia\", serif; font-weight: bold; font-size: 27px;'><a href='{0}' style='color: purple;'>{0}</a></span>".format(navigateTo), unsafe_allow_html=True)

    with tab3:
        st.markdown("<h2 style='text-align: center; color: red;'>Feedback</h2>", unsafe_allow_html=True)
        name = st.text_input("Name")
        feedback = st.text_area("Feedback")

        if st.button("Submit"):
            save_feedback(name, feedback)
            st.success("Thank you for your feedback!")

if __name__ == "__main__":
    main()


