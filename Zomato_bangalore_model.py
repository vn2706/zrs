import streamlit as st
import pandas as pd
import time

# Function to simulate loading animation (optional)
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

# Function to navigate to Zomato recommendation system with tabs
def navigate_to_tabs():
    st.experimental_rerun()

# Welcome page function
def welcome_page():
    st.markdown("<h1 style='text-align: center; color: gold;'>Welcome to Zomato Recommendation System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white; font-size: 18px;'>Explore the best restaurants in Bangalore with our Zomato Recommendation System. Select a tab to get started.</p>", unsafe_allow_html=True)

    # Centering the Explore button
    st.markdown("<div style='display: flex; justify-content: center; margin-top: 20vh;'>", unsafe_allow_html=True)
    if st.button("Explore", key='explore_button'):
        navigate_to_tabs()
    st.markdown("</div>", unsafe_allow_html=True)

# Function to display Zomato recommendation system with tabs
def display_tabs():
    st.markdown("<h1 style='text-align: center; color: gold;'>Zomato Recommendation System</h1>", unsafe_allow_html=True)

    # Create tabs
    tab_selection = st.radio("Select a tab:", ["Cuisine and Location", "New Restaurants", "Feedback"])

    if tab_selection == "Cuisine and Location":
        st.markdown("<h2 style='text-align: center; color: red;'>Find Restaurants by Cuisine and Location</h2>", unsafe_allow_html=True)
        # Your code for Cuisine and Location tab

    elif tab_selection == "New Restaurants":
        st.markdown("<h2 style='text-align: center; color: teal;'>Newly Open Restaurants</h2>", unsafe_allow_html=True)
        # Your code for New Restaurants tab

    elif tab_selection == "Feedback":
        st.markdown("<h2 style='text-align: center; color: red;'>Feedback</h2>", unsafe_allow_html=True)
        # Your code for Feedback tab

# Main function to run the application
def main():
    welcome_page()
    display_tabs()

if __name__ == "__main__":
    main()

