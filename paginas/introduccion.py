# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 23:42:42 2024

@author: pamum
"""
import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import contextily as cx
import seaborn as sns

def app():


    st.header("Analysis")
    st.markdown("""
    Welcome to the analysis section of our Airbnb price prediction application. Here, you can explore how various factors influence rental prices in different cities.

    ### How to Use This Tool

    1. **Select a City**: Use the dropdown menu to choose the city you are interested in.
    2. **View Maps**: Once you select a city, the maps will display the rental prices and the attraction indices (tourism and gastronomy) for different areas within the city.

    These visualizations will help you understand the market dynamics and identify the most influential factors for setting competitive rental prices.

    ### Select a City to Begin
    """)
    
    ciudades = pd.read_csv('ciudades.csv').drop(['Unnamed: 0'], axis=1)

    # preprocesado datos
    for city in ciudades['city'].unique():
        city_data = ciudades[ciudades['city'] == city]
        realSum_quantile = city_data['realSum'].quantile(0.992)
        attr_index_norm_quantile = city_data['attr_index_norm'].quantile(0.99)
        rest_index_norm_quantile = city_data['rest_index_norm'].quantile(0.99)
        is_outlier = (
            (city_data['realSum'] > realSum_quantile) |
            (city_data['attr_index_norm'] > attr_index_norm_quantile) |
            (city_data['rest_index_norm'] > rest_index_norm_quantile)
        )
        ciudades.loc[ciudades['city'] == city, 'outliers'] = is_outlier

    ciudades['outliers'] = ciudades['outliers'].astype(bool)
    geometry = [Point(xy) for xy in zip(ciudades.query("outliers == False")['lng'], ciudades.query("outliers == False")['lat'])]
    geo_df = gpd.GeoDataFrame(ciudades.query("outliers == False"), geometry=geometry, crs='EPSG:4326').to_crs(epsg=3857)
    geo_df['max_index'] = geo_df[['attr_index_norm', 'rest_index_norm']].max(axis=1)

    def plot_city_map(city, column, title):
        subset = geo_df.query("city == @city")
        norm = mcolors.LogNorm(vmin=subset[column].min(), vmax=subset[column].max()) if column == 'realSum' else mcolors.Normalize(vmin=subset[column].min(), vmax=subset[column].max())
        fig, ax = plt.subplots(figsize=(10, 10))
        subset.plot(column=column, markersize=5, legend=True, legend_kwds={'shrink': 0.3, 'label': ''}, norm=norm, ax=ax)
        cx.add_basemap(ax, source=cx.providers.CartoDB.Positron)
        ax.set_axis_off()
        ax.set_title(title)
        return fig

    def plot_average_distances(ciudades):
        fig, ax = plt.subplots(figsize=(15, 8))
        
        # Define the colors to match your page
        center_color = '#4CAF50'  # Green color for distance from center
        metro_color = '#2196F3'  # Blue color for distance from metro
        
        sns.barplot(data=ciudades, x="city", y="dist", ci=None, color=center_color, label='Distance from Center', ax=ax)
        sns.barplot(data=ciudades, x="city", y="metro_dist", ci=None, color=metro_color, label='Distance from Metro', ax=ax)
        
        ax.set_ylabel('Kilometers')
        ax.set_xlabel(None)
        ax.set_title('Average Distance per City')
        ax.legend()
    
        return fig

   
    city_options = ['Amsterdam', 'Athens', 'Barcelona', 'Berlin', 'Budapest', 'Lisbon', 'London', 'Paris', 'Rome', 'Vienna']
    selected_city = st.selectbox("Select a city to display its maps", city_options)

    st.write(f"### {selected_city}")
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(plot_city_map(selected_city.lower(), 'realSum', f'Price, EUR in {selected_city}'))
    with col2:
        st.pyplot(plot_city_map(selected_city.lower(), 'max_index', f'Max Attraction Index (Tourism and Restaurant) in {selected_city}'))

    
    st.subheader('Recommendations for Setting Your Rental Price')
    st.write('Based on the data visualizations and market analysis, here are some key insights and recommendations to help you set the optimal rental price for your apartment:')

    st.markdown("""
        **1. Prioritize Central Locations**:
        Apartments located in the city center consistently command higher rental prices across all cities. If your apartment is centrally located, highlight this feature in your listing. Emphasize its proximity to key attractions, business districts, and amenities.
        
        **2. Leverage Nearby Restaurants**:
        The presence of quality restaurants in the vicinity significantly boosts rental prices. The restaurant index provides a measure of the quality and quantity of dining options available in the area. Mention nearby dining options and popular restaurants in your listing. If your area has a high restaurant index, it can be a strong selling point for potential tenants.
        
        **3. Highlight Accessibility to Public Transport**:
        Apartments close to metro stations and public transportation hubs are more attractive and can demand higher rental prices. Easy access to public transportation is essential, especially for tourists and short-term renters. If your apartment is near a metro station or major public transport route, be sure to emphasize this in your listing.
        
        **4. Showcase Local Attractions**:
        Proximity to tourist attractions increases the attractiveness of your apartment. Areas with higher attraction indices often see increased rental demand and higher prices. Highlight any nearby tourist attractions, parks, or cultural sites in your listing.
        
        **5. Optimize Your Listing with Visuals**:
        Use maps and visuals in your listing to show the proximity to city centers, metro stations, restaurants, and attractions. Visual aids can make your listing stand out and provide clear, attractive information to potential renters.
        """)

    st.subheader('Average Distances to City Center and Metro Stations')
    st.write('In the graph below, you can see the average distance of rental properties in each city to the city center and the nearest metro station. This comparison helps highlight the balance between centrality and accessibility to public transportation, which are key considerations for setting rental prices.')

    average_distances_plot = plot_average_distances(ciudades)
    st.pyplot(average_distances_plot)

    st.write('For cities where rental properties are, on average, further from the center, the distance to the nearest metro station is generally shorter, reducing the inconvenience for tenants.')

