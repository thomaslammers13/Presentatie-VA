#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import numpy as np
import plotly as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import datetime
import time
import plost
from shapely.geometry import Point
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib.pyplot as plt
from scipy import stats

pages = st.sidebar.radio('Menu', options=['Home','Verbruik Bestelwagens', 'Verbruik Vrachtwagens', 'Energieverbruik', "Voorspelling elektrische auto's", "Kaart WFO", "Kaart Schiphol Trade Centre"])





# In[2]:


st.set_page_config(layout='wide', initial_sidebar_state = 'expanded')


# # Elektrische auto's 
# 

# In[3]:


r = requests.get('https://opendata.rdw.nl/resource/w4rt-e856.json?$limit=2000000')
x = r.json()
df = pd.DataFrame.from_dict(x)


# In[4]:


st.title("Dashboard elektrische auto's")
st.markdown("**Hieronder ziet u het dashboard voor de dataset over alle elektrische auto's van 1970 tot en met oktober 2022**")

    


# ROW A
st.markdown('**Metrics**')
col1, col2, col3 = st.columns(3)
col1.metric("Gem prijs", "$53,541")
col2.metric("Populairste merk", "Tesla", "1450%")
col3.metric("Gem gewicht", "1,749kg")


df.dropna(subset = ['datum_tenaamstelling'])
df.drop(57052, inplace = True)
df['datum_tenaamstelling']= df['datum_tenaamstelling'].astype(int)
df['datum_tenaamstelling']= df['datum_tenaamstelling'].astype(str)
df['datum_tenaamstelling'] = pd.to_datetime(df['datum_tenaamstelling'])
df.drop(df[df['vervaldatum_apk'] <= df['datum_tenaamstelling']].index, inplace = True)
df.dropna(subset = ['catalogusprijs'], inplace = True)
df['catalogusprijs']= df['catalogusprijs'].astype(int)
df = df[df['catalogusprijs'] <= 500000]

dftest = df.groupby('merk')['kenteken'].count()
df101 = pd.DataFrame(data=dftest).reset_index()
df101.sort_values(by=['kenteken'], ascending = False, inplace=True)
dffinal =df101[0:6]

c1, c2 = st.columns((7,3))
with c1:
    st.markdown('**Scatterplot**')
    figcatalogus = px.scatter(df, x='catalogusprijs', y='datum_tenaamstelling', color = 'merk')

    figcatalogus.update_layout(title_text="Catalogusprijs per auto per jaar")
    figcatalogus.update_yaxes(title_text="Jaar")
    figcatalogus.update_xaxes(title_text="Catalogusprijs")

    st.plotly_chart(figcatalogus)

with c2: 
    st.markdown('**Donut chart top merken**')
    figdonut = px.pie(dffinal, names='merk',values='kenteken', title='Donut chart top merken')
    st.plotly_chart(figdonut)
    

st.markdown("**Aanschaf elektrische auto's per maand**")


df['jaar'] = df['datum_tenaamstelling'].dt.year
df['maand'] = df['datum_tenaamstelling'].dt.month
dff = df.groupby(['jaar', 'maand'])['datum_tenaamstelling'].count()
df10 = pd.DataFrame(data=dff).reset_index()
df10 = df10[df10['jaar']>=2017]



figauto = px.line(df10, x="maand", y = "datum_tenaamstelling",
                 animation_frame="jaar", width=900, height=500)

figauto["layout"].pop("updatemenus")
figauto.update_layout(title_text="Aangeschafte auto's per maand per jaar", yaxis_range=[0,20000])
figauto.update_yaxes(title_text="Aantal auto's aangeschaft")
figauto.update_xaxes(title_text="Maand")

figauto.show()
st.plotly_chart(figauto)


x=df['jaar']
y=df['catalogusprijs']


slope, intercept, r, p, std_err = stats.linregress(x, y)

def myfunc(x):
      return slope * x + intercept

mymodel = list(map(myfunc, x))


plt.scatter(x, y)
plt.plot(x, mymodel)
plt.xlabel('Jaar')
plt.ylabel('Catalogusprijs (€)')
plt.title('Catalogusprijs verdeling per jaar')
px = plt
st.pyplot(px)


    


st.sidebar.header('Slider for year selection')
x = st.sidebar.slider(
    'Select a year', 2000, 2050, (2000))

def myfunc(x):
  return slope * x + intercept
year=myfunc(x)
st.write('De catalogusprijs van de auto in jaar', x, 'is', year, 'euro.')


# # Laadpaaldata

# In[5]:


laadpaal = pd.read_csv('laadpaaldata.csv')


# In[6]:


laadpaal.drop(laadpaal[laadpaal['ChargeTime'] < 0].index, inplace = True)
laadpaal.drop(laadpaal[laadpaal['ConnectedTime'] < 0].index, inplace = True)

laadpaal.drop(laadpaal[laadpaal['ChargeTime'] > 8].index, inplace = True)
laadpaal.drop(laadpaal[laadpaal['ConnectedTime'] > 8].index, inplace = True)

mean = 'Gemiddelde = ' + str(laadpaal['ChargeTime'].mean().round(2))
median = 'Mediaan = ' + str(laadpaal['ChargeTime'].median().round(2))

x0 = laadpaal['ChargeTime']
x1 = laadpaal['ConnectedTime']

st.title('Dashboard laadpaaldata')

st.markdown('**Metrics laadpaaldata**')
col1, col2 = st.columns(2)
col1.metric("Gem laadtijd", "1u 53m")
col2.metric("Gem aansluittijd", "2u 46m")


c1, c2 = st.columns((5,5))
with c1:
    figlp = go.Figure()
    figlp.add_trace(go.Histogram(x=x0, name='Laadtijd', marker_color='orange'))
    figlp.add_trace(go.Histogram(x=x1, name='Aangesloten tijd', marker_color='limegreen'))   


    figlp.update_layout(title='Oplaadtijd vergeleken met aangesloten tijd', barmode='overlay', xaxis_title='Tijd in uur', 
    yaxis_title='Aantal waarnemingen')

    figlp.update_traces(opacity=0.75)

    figlp.add_annotation(text= mean, x=1, y=470, showarrow= False)
    figlp.add_annotation(text= median, x=1, y=430, showarrow= False)

    st.plotly_chart(figlp)

laadpaal.drop(laadpaal[laadpaal['TotalEnergy'] <= 100].index, inplace = True)
laadpaal.drop(laadpaal[laadpaal['MaxPower'] <= 100].index, inplace = True)

laadpaal.drop(laadpaal[laadpaal['TotalEnergy'] > 15000].index, inplace = True)
laadpaal.drop(laadpaal[laadpaal['MaxPower'] > 15000].index, inplace = True)

x2= laadpaal['TotalEnergy']
x3= laadpaal['MaxPower']

with c2: 

    figlp1 = go.Figure()
    figlp1.add_trace(go.Histogram(x=x2, name='Totale energie', marker_color='#EB89B5'))
    figlp1.add_trace(go.Histogram(x=x3, name='Maximaal vermogen', marker_color='#330C73'))


    figlp1.update_layout(title='Totale energie vergeleken met maximaal vermogen', barmode='overlay', xaxis_title='Energie', 
            yaxis_title='Aantal waarnemingen')

    figlp1.update_traces(opacity=0.75)

    st.plotly_chart(figlp1)

    



# # Kaart

# In[7]:


import numpy as pd
import pandas as pd
from shapely.geometry import Point
import folium
import requests
import json
import geopandas as gpd


# In[8]:


url = 'https://api.openchargemap.io/v3/poi/?key=160f4c55-057f-4bc3-9f15-e0f63c4e6a0f/'
url2 ='https://api.openchargemap.io/v3/poi/?key=160f4c55-057f-4bc3-9f15-e0f63c4e6a0f/output=json&countrycode=NL&maxresults=100&compact=true&verbose=false'


# In[9]:


params = {"countrycode": "NL", "output": "json", "compact": True, "verbose": False, "maxresults": 10000}

r = requests.get(url, params)
json_data = r.json()

#Uitpakken

normalize = pd.json_normalize(json_data)
    
df = pd.json_normalize(normalize.Connections)
df2 = pd.json_normalize(df[0])




Laadpalen = pd.concat([normalize, df2], axis=1)

Laadpalen = Laadpalen.rename(columns= {"AddressInfo.ID":"AddressID", 
                                           'AddressInfo.Title':'Title', 
                                           'AddressInfo.AddressLine1':'AddressLine1',
                                           'AddressInfo.Town':'Town',
                                           'AddressInfo.StateOrProvince':'StateOrProvince', 
                                           'AddressInfo.Postcode':'Postcode',
                                           'AddressInfo.CountryID':'CountryID', 
                                           'AddressInfo.Latitude':'Latitude',
                                           'AddressInfo.Longitude':'Longitude', 
                                           'AddressInfo.ContactTelephone1': 'ContactTelephone1',
                                           'AddressInfo.DistanceUnit':'DistanceUnit', 
                                           'AddressInfo.RelatedURL':'RelatedURL', 
                                           'AddressInfo.AccessComments':'AccessComments',
                                           'AddressInfo.ContactEmail':'ContactEmail', 
                                           'AddressInfo.ContactTelephone2':'ContactTelephone2',
                                           'AddressInfo.AddressLine2':'AddressLine2',
                                          })

Laadpalen['Geometry'] = Laadpalen.apply(lambda x: Point((x.Longitude, x.Latitude)),axis = 1)

municipal_boundaries = gpd.read_file('INDELING_STADSDEEL.csv') 
municipal_boundaries = municipal_boundaries.drop(columns = 'WKT_LNG_LAT', axis= 0 )

municipal_boundaries = municipal_boundaries[['Stadsdeel','WKT_LAT_LNG']]





# In[10]:


def color_producer(int):
    
        if int == 1.0 :
            color = 'gray'
        elif int == 2.0 :
            color = 'orangered'
        elif int == 3.0 :
            color = 'brown'
        elif int == 4.0 :
            color = 'darkorange'
        elif int == 5.0 :
            color = 'gold'
        elif int == 6.0 :
            color = 'green'
        elif int == 7.0 :
            color = 'aqua'
        elif int == 8.0 :
            color = 'darkslategray'
        elif int == 9.0 :
            color = 'indigo'
        elif int == 10.0 :
            color = 'darkviolet'
        elif int == 11.0 :
            color = 'darkkhaki'
        elif int == 12.0 :
            color = 'olive'
        elif int == 13.0 :
            color = 'olivedrab'
        elif int == 14.0 :
            color = 'lawngreen'
        elif int == 16.0 :
            color = 'palegreen'
        elif int == 18.0 :
            color = 'forestgreen'
        elif int == 20.0 :
            color = 'darkgreen'
        elif int == 24.0 :
            color = 'lime'
        elif int == 28.0 :
            color = 'aquamarine'
        else :
            color = 'darkviolet'
        return(color)


# In[11]:


municipal_boundaries = gpd.read_file('INDELING_STADSDEEL.csv') 
municipal_boundaries = municipal_boundaries.drop(columns = 'WKT_LNG_LAT', axis= 0 )

print(municipal_boundaries.crs)

municipal_boundaries.head(10)
municipal_boundaries = municipal_boundaries[['Stadsdeel','WKT_LAT_LNG']]


# In[12]:


def add_categorical_legend(folium_map, title, colors, labels):
    if len(colors) != len(labels):
        raise ValueError("colors and labels must have the same length.")

    color_by_label = dict(zip(labels, colors))
    
    legend_categories = ""     
    for label, color in color_by_label.items():
        legend_categories += f"<li><span style='background:{color}'></span>{label}</li>"
        
    legend_html = f"""
    <div id='maplegend' class='maplegend'>
      <div class='legend-title'>{title}</div>
      <div class='legend-scale'>
        <ul class='legend-labels'>
        {legend_categories}
        </ul>
      </div>
    </div>
    """
    script = f"""
        <script type="text/javascript">
        var oneTimeExecution = (function() {{
                    var executed = false;
                    return function() {{
                        if (!executed) {{
                             var checkExist = setInterval(function() {{
                                       if ((document.getElementsByClassName('leaflet-top leaflet-right').length) || (!executed)) {{
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.display = "flex"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.flexDirection = "column"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].innerHTML += `{legend_html}`;
                                          clearInterval(checkExist);
                                          executed = true;
                                       }}
                                    }}, 100);
                        }}
                    }};
                }})();
        oneTimeExecution()
        </script>
      """
   

    css = """

    <style type='text/css'>
      .maplegend {
        z-index:9999;
        float:right;
        background-color: rgba(255, 255, 255, 1);
        border-radius: 5px;
        border: 2px solid #bbb;
        padding: 10px;
        font-size:12px;
        positon: relative;
      }
      .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 0px solid #ccc;
        }
      .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend a {
        color: #777;
        }
    </style>
    """

    folium_map.get_root().header.add_child(folium.Element(script + css))

    return folium_map


# In[13]:


import streamlit_folium as st_folium
from streamlit_folium import folium_static


st.title('Kaart laadpunten')

#Kaart met provincie outline, wanneer je eroverheen hovert zie je het aantal laadpunten.

m = folium.Map(location=[52.3676, 4.9041],zoom_start=12,min_zoom=12,)

for index, row in Laadpalen.iterrows():    
    folium.CircleMarker(location = [row["Latitude"], row["Longitude"]],
                        fill_color = color_producer(row['NumberOfPoints']),
                        color = color_producer(row['NumberOfPoints']), 
                        fill_opacity=0.5,
                        line_opacity=0.1,
                        popup=row['NumberOfPoints'],
                        radius = 4
                       ).add_to(m)
    
#folium.GeoJson(data=municipal_boundaries).add_to(m)

m = add_categorical_legend(m, 'Number of Points',
                            colors = ['gray','orangered','brown','darkorange','gold','green','aqua','darkviolet'],
                            labels = ['1','2','3', '4', '5','6','7','>28'])



folium_static(m)




# In[ ]:





# In[ ]:




