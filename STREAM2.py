#!/usr/bin/env python
# coding: utf-8

# In[1]:
#importeren packages
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly as plt
from PIL import Image
import geopandas as gpd
import numpy as np
import os
from streamlit_folium import st_folium
from streamlit_folium import folium_static
import folium
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import streamlit_folium as st_folium
from streamlit_folium import folium_static
from folium import plugins
from folium.plugins import MarkerCluster
from folium.plugins import TimeSliderChoropleth
import branca
import branca.colormap as cm
import folium.plugins

st.set_page_config(layout='wide', initial_sidebar_state = 'expanded')

# In[2]: #INLADEN DATA
circuits = pd.read_csv("circuits.csv")
races = pd.read_csv('races.csv')
pitstop = pd.read_csv('pit_stops.csv')
dff = pd.read_csv('Voorspelling.csv')
Pitpit = pd.read_csv('Pitpit.csv')
df2 = pd.read_csv('df2.csv')
races1 = pd.read_csv('races1.csv')
aantalraces = pd.read_csv('Aantalraces.csv')

# In[4]: #Pitstop een
pitstop['TF'] = pitstop['duration'].str.len() > 7
pitstop = pitstop[pitstop['TF'] == False]
pitstop['duration']= pd.to_numeric(pitstop['duration'])
#fig = px.scatter(pitstop, x='lap', y='duration', color='stop',trendline='ols', trendline_color_override='red', title='Duur pitstop per ronde')
#fig.update_xaxes(title='Ronde')
#fig.update_yaxes(title='Duur pitstop (s)')


# In[5]: #Pitstop twee
fig2 = px.bar(Pitpit, x='year', y='aantal pitstops(pitstop)', title='Aantal stops per jaar', color='stop')
fig2.update_xaxes(title='Jaar')
fig2.update_yaxes(title='Aantal pitstops')

fig2.add_annotation(
        x=2011,
        y=1100,
        xref="x",
        yref="y",
        text="Pirelli fabrikant",
        showarrow=True,
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="#ffffff"
            ),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        ax=20,
        ay=-30,
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=4,
        bgcolor="#ff7f0e",
        opacity=0.8
)


fig2.add_annotation(
        x=2016.1,
        y=950,
        xref="x",
        yref="y",
        text="Invoering compounds",
        showarrow=True,
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="#ffffff"
            ),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        ax=20,
        ay=-30,
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=4,
        bgcolor="#ff7f0e",
        opacity=0.8
)

fig2.add_annotation(
        x=2017.3,
        y=800,
        xref="x",
        yref="y",
        text="Breedere banden",
        showarrow=True,
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="#ffffff"
            ),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        ax=20,
        ay=-30,
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=4,
        bgcolor="#ff7f0e",
        opacity=0.8
)

fig2.add_annotation(
        x=2019.3,
        y=700,
        xref="x",
        yref="y",
        text="5 dry compounds",
        showarrow=True,
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="#ffffff"
            ),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        ax=20,
        ay=-30,
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=4,
        bgcolor="#ff7f0e",
        opacity=0.8
)
fig2.update_layout(showlegend=False)

# In[6]: #Pitstop drie
fig3 = px.box(races1, x='year', y='duration', color='year', title='Verdeling pitstops over de jaren heen')
fig3.update_xaxes(title='Jaar')
fig3.update_yaxes(title='Duur pitstop (s)')

# In[6]: #Pitstop vier
fig4= px.scatter(races1, x='round', y='fastest pitstop', animation_frame="year", color='circuitId',  labels={
                     "naam_x": "Naam grote prijs",
                     "year": "Jaar",
                     "fastest pitstop": "Snelste pitstop",
                     "round": "Ronde"
                 })
fig4["layout"].pop("updatemenus")
fig4.update_layout(yaxis_range=[0,40], legend_title="Circuit ID", title='Tijd pitstops per jaar')
fig4.update_layout(xaxis_range=[0,25])
fig4.update_xaxes(title='Ronde')
fig4.update_yaxes(title='Tijd pitstop (s)')

# In[7]: #Circuits
fig5= px.bar(df2, x='name', y='1', title='Aantal races per GP', color='year')
fig5.update_xaxes(title='Grote prijs')
fig5.update_yaxes(title='Aantal races')

# In[8]: #Races


figaantal = px.bar(aantalraces, x='year', y='aantal', title='Aantal races per jaar')
figaantal.update_xaxes(title='Jaar')
figaantal.update_yaxes(title='Aantal races')


fig_voorspelling = px.bar(dff, x='year', y=['aantal', 'voorspelling'], title='Aantal races voorspelling')
fig_voorspelling.update_xaxes(title='Jaar')
fig_voorspelling.update_yaxes(title="Aantal GP's")

# In[6]: #DATAFRAME'S KAART Circuits

races2009 = races1[races1['year'] == 2009]
races2010 = races1[races1['year'] == 2010]
races2011 = races1[races1['year'] == 2011]
races2012 = races1[races1['year'] == 2012]
races2013 = races1[races1['year'] == 2013]
races2014 = races1[races1['year'] == 2014]
races2015 = races1[races1['year'] == 2015]
races2016 = races1[races1['year'] == 2016]
races2017 = races1[races1['year'] == 2017]
races2018 = races1[races1['year'] == 2018]
races2019 = races1[races1['year'] == 2019]
races2020 = races1[races1['year'] == 2020]
races2021 = races1[races1['year'] == 2021]
races2022 = races1[races1['year'] == 2022]

# In[6]: #KAART Circuits
m = folium.Map(location=[41.87194,12.56738], zoom_start=2, width="%100",height="%100")
#races1.apply(lambda row:folium.Marker(location = [row["lat"], 
                                                 # row["lng"]], popup=row['name_x']).add_to(m),axis=1)

#races1.apply(lambda row: folium.CircleMarker(location=[row["lat"], 
                                                 # row["lng"]], popup=row['name_x'], fill=True).add_to(m), axis=1)


#jaar_2009 = folium.FeatureGroup(name="2009").add_to(m)
#jaar_2010 = folium.FeatureGroup(name="2010",show=False).add_to(m)
jaar_2011 = folium.FeatureGroup(name="2011", show=False).add_to(m)
jaar_2012 = folium.FeatureGroup(name="2012", show=False).add_to(m)
jaar_2013 = folium.FeatureGroup(name="2013", show=False).add_to(m)
jaar_2014 = folium.FeatureGroup(name="2014", show=False).add_to(m)
jaar_2015 = folium.FeatureGroup(name="2015", show=False).add_to(m)
jaar_2016 = folium.FeatureGroup(name="2016", show=False).add_to(m)
jaar_2017 = folium.FeatureGroup(name="2017", show=False).add_to(m)
jaar_2018 = folium.FeatureGroup(name="2018", show=False).add_to(m)
jaar_2019 = folium.FeatureGroup(name="2019", show=False).add_to(m)
jaar_2020 = folium.FeatureGroup(name="2020", show=False).add_to(m)
jaar_2021 = folium.FeatureGroup(name="2021", show=False).add_to(m)
jaar_2022 = folium.FeatureGroup(name="2022", show=False).add_to(m)





#for index, row in races2009.iterrows():
  #  jaar_2009.add_child(folium.CircleMarker(location=[row['lat'], row['lng']],
                                   # fill=True, popup=row['name_x']).add_to(m))

#for index, row in races2010.iterrows():
    #jaar_2010.add_child(folium.CircleMarker(location=[row['lat'], row['lng']],#fill=True, popup=row['name_x']).add_to(m))

    
colormap = cm.LinearColormap(colors=['darkblue', 'blue', 'cyan', 'yellow', 'orange', 'red'],
                             index=[0, 20, 40, 60, 80 , 100], vmin=0, vmax=100,
                             caption='Totaal aantal pitstops per GP')





for index, row in races2011.iterrows():
    color = colormap(row['total pitstops'])
    jaar_2011.add_child(folium.CircleMarker(location=[row['lat'], row['lng']],
                                     fill=True, popup=row['name_x'], color=color).add_to(m))
    m.add_child(colormap)
for index, row in races2012.iterrows():
    color = colormap(row['total pitstops'])
    jaar_2012.add_child(folium.CircleMarker(location=[row['lat'], row['lng']],
                                    fill=True, popup=row['name_x'], color=color).add_to(m))
    m.add_child(colormap)
for index, row in races2013.iterrows():
    color = colormap(row['total pitstops'])
    jaar_2013.add_child(folium.CircleMarker(location=[row['lat'], row['lng']],
                                    fill=True, popup=row['name_x'], color=color).add_to(m))
    m.add_child(colormap)
for index, row in races2014.iterrows():
    color = colormap(row['total pitstops'])
    jaar_2014.add_child(folium.CircleMarker(location=[row['lat'], row['lng']],
                                    fill=True, popup=row['name_x'], color=color).add_to(m))
    m.add_child(colormap)
for index, row in races2015.iterrows():
    color = colormap(row['total pitstops'])
    jaar_2015.add_child(folium.CircleMarker(location=[row['lat'], row['lng']],
                                    fill=True, popup=row['name_x'], color=color).add_to(m))
    m.add_child(colormap)
for index, row in races2016.iterrows():
    color = colormap(row['total pitstops'])
    jaar_2016.add_child(folium.CircleMarker(location=[row['lat'], row['lng']],
                                    fill=True, popup=row['name_x'], color=color).add_to(m))
    m.add_child(colormap)
for index, row in races2017.iterrows():
    color = colormap(row['total pitstops'])
    jaar_2017.add_child(folium.CircleMarker(location=[row['lat'], row['lng']],
                                    fill=True, popup=row['name_x'], color=color).add_to(m))
    m.add_child(colormap)
for index, row in races2018.iterrows():
    color = colormap(row['total pitstops'])
    jaar_2018.add_child(folium.CircleMarker(location=[row['lat'], row['lng']],
                                    fill=True, popup=row['name_x'], color=color).add_to(m))
    m.add_child(colormap)
for index, row in races2019.iterrows():
    color = colormap(row['total pitstops'])
    jaar_2019.add_child(folium.CircleMarker(location=[row['lat'], row['lng']],
                                    fill=True, popup=row['name_x'], color=color).add_to(m))
    m.add_child(colormap)
for index, row in races2020.iterrows():
    color = colormap(row['total pitstops'])
    jaar_2020.add_child(folium.CircleMarker(location=[row['lat'], row['lng']],
                                    fill=True, popup=row['name_x'], color=color).add_to(m))
    m.add_child(colormap)
for index, row in races2021.iterrows():
    color = colormap(row['total pitstops'])
    jaar_2021.add_child(folium.CircleMarker(location=[row['lat'], row['lng']],
                                    fill=True, popup=row['name_x'], color=color).add_to(m))
    m.add_child(colormap)
for index, row in races2022.iterrows():
    color = colormap(row['total pitstops'])
    jaar_2022.add_child(folium.CircleMarker(location=[row['lat'], row['lng']],
                                    fill=True, popup=row['name_x'], color=color).add_to(m))
    m.add_child(colormap)

                                            

folium.LayerControl(position='bottomleft', collapsed=False).add_to(m)



# In[7]: #DASHBOARD
pages = st.sidebar.radio('Menu', options=['Home','Pitstops', 'Circuits', 'Races'])

if pages == "Home":
    image = Image.open('F1.jpg')
    st.title("Eindpresentatie VA")
    st.header("Formule 1 races en circuits")
    st.subheader("Sil Buyck en Thomas Lammers")
    st.image(image)

elif pages == 'Pitstops':
    st.sidebar.header('Selecteer assen voor scatterplot pitstops')
    x_selectbox = st.sidebar.selectbox('Selecteer X-as', options = pitstop.columns)
    y_selectbox = st.sidebar.selectbox('Selecteer Y-as', options = pitstop.columns)
    
    
    st.title("Pitstops Formule 1")
        
    c1, c2 = st.columns((7,3))
    with c1:
        st.plotly_chart(fig2)

    with c2: 
        fig = px.scatter(pitstop, x=x_selectbox, y=y_selectbox, color='stop',trendline='ols', trendline_color_override='red',
        title='Duurpitstop per ronde')
        fig.update_xaxes(title='Ronde')
        fig.update_yaxes(title='Duur pitstop (s)')
        st.plotly_chart(fig)
 
    c1, c2 = st.columns((7,3))
    with c1:
        st.plotly_chart(fig3)

    with c2: 
        st.plotly_chart(fig4)
    
 
    
elif pages == 'Circuits':
    st.title('Overzicht circuits in de formule 1')
    st.markdown('**Circuit statistieken**')
    col1, col2, col3 = st.columns(3)
    col1.metric("Aantal circuits 2022", "22")
    col2.metric("Continent met meeste races", "Europa")
    col3.metric("Aantal circuits waarop gereden", "39")
    st.plotly_chart(fig5, use_container_width=True)
    st.subheader('Kaart circuits per jaar')
    folium_static(m)
    
elif pages == 'Races':
    st.title('Overzicht races in de formule 1')
    st.plotly_chart(figaantal, use_container_width=True)
    st.title('Voorspelling aantal races in de toekomst')
    st.markdown('**Samenvatting model**')
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Correlatie", "0.935")
    col2.metric("R^2", "0.875")
    col3.metric("Intercept", "-323.138")
    col4.metric("Delta", "0.170")
    st.plotly_chart(fig_voorspelling, use_container_width=True)
    
    

    
    
        
        
        
        










