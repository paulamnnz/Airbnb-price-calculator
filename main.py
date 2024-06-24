# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 23:39:37 2024

@author: pamum
"""

import streamlit as st
import importlib

# Set the page configuration
st.set_page_config(
    page_title="Airbnb Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.streamlit.io/help',
        'Report a bug': 'https://github.com/streamlit/streamlit/issues',
        'About': "This is a Streamlit app to predict Airbnb prices."
    }
)

# Custom CSS for additional styling
st.markdown("""
    <style>
    .css-18e3th9 {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    .css-1d391kg {
        padding: 0;
    }
    .css-hxt7ib {
        font-size: 1.5rem;
    }
    .css-12ttj6m {
        background-color: #f0f2f6;
        color: #0c0c0c;
    }
    .css-1aumxhk {
        background-color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to load a page from the paginas folder
def load_page(page_name):
    module = importlib.import_module(f"paginas.{page_name}")
    module.app()

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select ", ["Home", "Cities analysis", "Calculator"], index=["Home", "Cities analysis", "Calculator"].index(st.session_state.page))

# Update session state based on sidebar selection
st.session_state.page = page

# Page loading logic
if page == "Home":
    load_page("home")
elif page == "Cities analysis":
    load_page("introduccion")
elif page == "Calculator":
    load_page("analisis")