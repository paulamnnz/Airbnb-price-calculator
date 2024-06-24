# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 23:41:26 2024

@author: pamum
"""

import streamlit as st

def app():
    st.title("Welcome to the Airbnb Price Analyzer")
    st.markdown("""
    Welcome to the Airbnb rental price prediction application! 🎉
    
    This tool will help you estimate the price of a rental property based on various factors, such as location, type of room, distance from the center, and more. By leveraging data and analytics, you can make informed decisions to optimize your rental pricing strategy.
    
    **Quick Start Guide:**
    1. **Select a City**: Choose a city from the dropdown menu to see detailed maps and data.
    2. **Analyze Data**: Explore the visualizations to understand how different factors impact rental prices.
    3. **Get Recommendations**: Use the insights provided to set competitive and attractive rental prices for your property.

    Use the sidebar to navigate through the different sections of the application:
  
    - **Cities Analysis**: Learn about the factors that influence rental prices. Select a city to view detailed maps and data.
    - **Calculator**: Select your city and your property specifications.
    
    **Let's get started!** Use the sidebar to begin exploring the application.
    """)

    st.image("images/airbnb-logo.jpeg", use_column_width=True)

    # Call to Action Button
    if st.button("Go to Calculator"):
        st.session_state.page = "Calculator"
        st.experimental_rerun()
