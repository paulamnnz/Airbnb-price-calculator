# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 23:43:21 2024

@author: pamum
"""
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import lime
import lime.lime_tabular
import joblib

def app():
    st.header("Price calculator")
    st.markdown("""
    ### How to Use This Tool

    1. **Select a City**: Use the dropdown menu to choose a city you are interested in.
    2. **Adjust Filters**: Customize the filters on the sidebar to match the characteristics of your property, such as number of bedrooms, distance to city center, and tourist attraction index.
    3. **View Results**: Explore the generated graphs to understand how different variables impact rental prices in your selected city.
    4. **Get Price Estimates**: Use the tool to predict the optimal rental price for your property based on the selected criteria.

    """)
    def df_combinado(ruta_weekdays_df, ruta_weekends_df):
        weekdays_df = pd.read_csv(ruta_weekdays_df)
        weekends_df = pd.read_csv(ruta_weekends_df)
        weekdays_df['weekend'] = 0
        weekends_df['weekend'] = 1
        combined_df = pd.concat([weekdays_df, weekends_df], ignore_index=True)
        feature_names = ['realSum', 'room_type', 'person_capacity', 'host_is_superhost', 'biz', 'cleanliness_rating', 'bedrooms', 'dist', 'metro_dist', 'weekend', 'attr_index_norm', 'rest_index_norm']
        combined_df = combined_df[feature_names]
        qualitative_columns = combined_df.select_dtypes(include=['object']).columns
        combined_df = pd.get_dummies(combined_df, columns=qualitative_columns)
        combined_df = combined_df.applymap(lambda x: 1 if x is True else (0 if x is False else x))
        combined_df = combined_df[combined_df['realSum'] < 1500]
        return combined_df

    def grafico(df, inst_df, modelo):
        df = df.drop(columns=['realSum'])
        explainer = lime.lime_tabular.LimeTabularExplainer(df.values, mode="regression", feature_names=df.columns.tolist(), random_state=42)
        instance_idx = 0
        exp = explainer.explain_instance(inst_df.iloc[instance_idx], modelo.predict, num_features=7, top_labels=1)
        fig = exp.as_pyplot_figure()
        fig.set_size_inches(10, 6)
        fig.suptitle('Contribution to the prediction', fontsize=16)
        st.pyplot(fig)

    def grafico_distribucion(df, ciudad, pred):
        value_counts = df['realSum'].value_counts()
        filtered_values = value_counts[value_counts >= 3].index
        filtered_df = df[df['realSum'].isin(filtered_values)]
        plt.figure(figsize=(10, 6))
        sns.histplot(filtered_df['realSum'], bins=30, kde=True)
        plt.axvline(pred, color='red', linestyle='--', linewidth=2)
        plt.title(f'Price distribution in {ciudad}')
        plt.xlabel('Price (realSum)')
        plt.ylabel('Frecuency')
        plt.grid(True)
        return plt.gcf()

    st.write("This app enables you to establish the price of any propertiby based in specific metrics.")
    st.sidebar.header("Filters")
    ciudad = st.sidebar.selectbox('Choose your city', ['Amsterdam', 'Athens', 'Barcelona', 'Berlin', 'Budapest', 'Lisbon', 'London', 'Paris', 'Rome', 'Vienna'])
    num_habitaciones = st.sidebar.slider("Number of Bedrooms in the Property", 1, 10, 3)
    distancia_centro = st.sidebar.slider("Distance to City Center (km)", 0.00, 30.00, 1.00)
    distancia_metro = st.sidebar.slider("Distance to Nearest Metro (km)", 0.00, 10.00, 1.00)
    turistico = st.sidebar.slider("Tourist Attraction of the Area", 0.00, 100.00, 50.00)
    restaurante = st.sidebar.slider("Gastronomic Attraction of the Area", 0.00, 100.00, 50.00)
    fin_de_semana = st.sidebar.checkbox("Is it a weekend?", False)
    num_personas = st.sidebar.slider("Maximum Number of People in the Property", 1, 10, 4)
    tipo_habitacion = st.sidebar.selectbox("Select Your Type of Property", ["Entire home", "Shared Room", "Private Room"])
    superhost = st.sidebar.checkbox("Are you a Superhost in our App?", False)
    biz = st.sidebar.checkbox("Is the property rented for business purposes?", False)
    clean = st.sidebar.slider("Cleanliness Rating of the Property", 1, 10, 7)
    index = ['registro_1']
    
    data = {
        'person_capacity': num_personas, 'host_is_superhost': superhost, 'biz': biz,
        'cleanliness_rating': clean, 'bedrooms': num_habitaciones, 'dist': distancia_centro,
        'metro_dist': distancia_metro, 'weekend': fin_de_semana, 'attr_index_norm': turistico,
        'rest_index_norm': restaurante
    }
    
    room_type_map = {
        "Entire home": [1, 0, 0],
        "Shared Room": [0, 0, 1],
        "Private Room": [0, 1, 0]
    }
    
    data.update(dict(zip(['room_type_Entire home/apt', 'room_type_Private room', 'room_type_Shared room'], room_type_map[tipo_habitacion])))
    
    df_final = pd.DataFrame(data, index=index).applymap(lambda x: 1 if x is True else (0 if x is False else x))
    
    ciudad_modelo_map = {
        'Amsterdam': ('DATOS20/amsterdam_weekdays.csv', 'DATOS20/amsterdam_weekends.csv', 'MODELOS/trained_model_amsterdam.pkl'),
        'Athens': ('DATOS20/athens_weekdays.csv', 'DATOS20/athens_weekends.csv', 'MODELOS/trained_model_athens.pkl'),
        'Barcelona': ('DATOS20/barcelona_weekdays.csv', 'DATOS20/barcelona_weekends.csv', 'MODELOS/trained_model_barcelona.pkl'),
        'Berlin': ('DATOS20/berlin_weekdays.csv', 'DATOS20/berlin_weekends.csv', 'MODELOS/trained_model_berlin.pkl'),
        'Budapest': ('DATOS20/budapest_weekdays.csv', 'DATOS20/budapest_weekends.csv', 'MODELOS/trained_model_budapest.pkl'),
        'Lisbon': ('DATOS20/lisbon_weekdays.csv', 'DATOS20/lisbon_weekends.csv', 'MODELOS/trained_model_lisbon.pkl'),
        'London': ('DATOS20/london_weekdays.csv', 'DATOS20/london_weekends.csv', 'MODELOS/trained_model_london.pkl'),
        'Paris': ('DATOS20/paris_weekdays.csv', 'DATOS20/paris_weekends.csv', 'MODELOS/trained_model_paris.pkl'),
        'Roma': ('DATOS20/rome_weekdays.csv', 'DATOS20/rome_weekends.csv', 'MODELOS/trained_model_rome.pkl'),
        'Vienna': ('DATOS20/vienna_weekdays.csv', 'DATOS20/vienna_weekends.csv', 'MODELOS/trained_model_vienna.pkl')
    }
    
    if ciudad in ciudad_modelo_map:
        ruta_weekdays, ruta_weekends, modelo_path = ciudad_modelo_map[ciudad]
        df = df_combinado(ruta_weekdays, ruta_weekends)
        modelo = joblib.load(modelo_path)
        pred = modelo.predict(df_final)
        
        # Format the price for better visual appeal
        formatted_price = f"{round(pred[0], 2):,} €"
        st.markdown(f"""
        <div style="background-color:#fafafa; padding:20px; border-radius:10px; text-align:center; margin:20px 0;">
            <h2 style="color:#4CAF50;"> Estimated price:</h2>
            <h1 style="font-size:48px; color:#4CAF50;"><b>{formatted_price}</b></h1>
        </div>
        """, unsafe_allow_html=True)
        
        fig_distribucion = grafico_distribucion(df, ciudad, pred)
        grafico(df, df_final, modelo)
        st.pyplot(fig_distribucion)
