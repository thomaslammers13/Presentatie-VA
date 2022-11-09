#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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
from geopy.geocoders import Nominatim
import numpy as np
import os
from streamlit_folium import st_folium
from streamlit_folium import folium_static
import folium
import plotly.graph_objects as go



# In[6]: #KAART WFO
#fig3 = go.Figure()
#fig3.add_trace(
  #go.Bar(x=dates['datum'], y=dates['zonnepanelen'], name='Aantal Zonnepanelen'))
#fig3.add_trace(
 # go.Scatter(x=dates['datum'], y=dates['dagopbrengst_kwh'], name='Dagopwekking kWh'))

# In[7]: #DASHBOARD
pages = st.sidebar.radio('Menu', options=['Home','Verbruik Bestelwagens', 'Verbruik Vrachtwagens', 'Energieverbruik', "Voorspelling elektrische auto's", "Kaart WFO", "Kaart Schiphol Trade Centre"])


# #!/usr/bin/env python
# # coding: utf-8
# 
# # In[1]:
# #importeren packages
# import pandas as pd
# import streamlit as st
# import plotly.express as px
# import plotly as plt
# from PIL import Image
# import geopandas as gpd
# from geopy.geocoders import Nominatim
# import numpy as np
# import os
# from streamlit_folium import st_folium
# from streamlit_folium import folium_static
# import folium
# import plotly.graph_objects as go
# 
# # In[2]: #INLADEN DATA
# dfmerge = pd.read_csv("dfmerge.csv")
# dfmerge = dfmerge.drop(["Unnamed: 0"], axis=1)
# dates = pd.read_csv('dates.csv')
# dates2 = pd.read_csv('dates2.csv')
# 
# # In[4]: #ENERGIEGEBRUIK
# fig = px.line(dfmerge, x="uur", y=dfmerge.columns, title='Energieverbruik per uur voor eerste dag van de maand')
# 
# fig.update_xaxes(title_text='Uur van de dag',
#     dtick="M1",
#     tickformat="%b\n%Y")
# 
# fig.update_yaxes(title_text='Energieverbruik')
# 
# fig.update_layout(legend_title='Maanden')
# 
# # In[5]: #KAART STP
# fig2 = go.Figure()
# fig2.add_trace(
#   go.Bar(x=dates2['datum'], y=dates2['zonnepanelen'], name='Aantal Zonnepanelen'))
# fig2.add_trace(
#   go.Scatter(x=dates2['datum'], y=dates2['dagopbrengst_kwh'], name='Dagopwekking kWh'))
# 
# # In[6]: #KAART WFO
# #fig3 = go.Figure()
# #fig3.add_trace(
#   #go.Bar(x=dates['datum'], y=dates['zonnepanelen'], name='Aantal Zonnepanelen'))
# #fig3.add_trace(
#  # go.Scatter(x=dates['datum'], y=dates['dagopbrengst_kwh'], name='Dagopwekking kWh'))
# 
# # In[7]: #DASHBOARD
# pages = st.sidebar.radio('Menu', options=['Home','Verbruik Bestelwagens', 'Verbruik Vrachtwagens', 'Energieverbruik', "Voorspelling elektrische auto's", "Kaart WFO", "Kaart Schiphol Trade Centre"])
# 
# if pages == "Home":
#     image = Image.open('Vrachtwagen.jpg')
#     st.title("Hackathon 2022")
#     st.header("Elektrische vrachtwagens en laadpalen")
#     st.subheader("Groep 17, 23 en 25")
#     st.image(image)
# elif pages == 'Verbruik Bestelwagens':
#     st.title("Verbruik Bestelwagens")
#     option = st.selectbox("Selecteer vermogen of locatie", ("22KW", "150KW", "Alleen Depot", "Klant en Depot"))
#     if option == "22KW":
#         image2 = Image.open('Verbruik BEstelwagens 22 Kw alleen op depot laden.jpeg')
#         st.image(image2)
#         image3 = Image.open('Bestelwagen 22kw klant en depot laden.jpeg')
#         st.image(image3)
#     elif option == "150KW":
#         image4 = Image.open('Verbruik Bestelwagens 150kw alleen op depot laden.jpeg')
#         st.image(image4)
#         image5 = Image.open('Bestelwagen 150kw bij klant en depot laden.jpeg')
#         st.image(image5)
#     elif option == "Alleen Depot":
#         image2 = Image.open('Verbruik BEstelwagens 22 Kw alleen op depot laden.jpeg')
#         st.image(image2)
#         image4 = Image.open('Verbruik Bestelwagens 150kw alleen op depot laden.jpeg')
#         st.image(image4)
#     elif option == "Klant en Depot":
#         image3 = Image.open('Bestelwagen 22kw klant en depot laden.jpeg')
#         st.image(image3)
#         image5 = Image.open('Bestelwagen 150kw bij klant en depot laden.jpeg')
#         st.image(image5)
# elif pages == 'Verbruik Vrachtwagens':
#     st.title("Verbruik Vrachtwagens")
#     option2 = st.selectbox("Selecteer vermogen of locatie", ("43KW", "150KW","Waterstof", "Alleen Depot", "Klant en Depot"))
#     if option2 == "43KW":
#         image6 = Image.open('Vrachtwagen 43 kw alleen op depot laden.jpeg')
#         st.image(image6)
#         image7 = Image.open('Vrachtwagen 43kw bij klant en depot laden.jpeg')
#         st.image(image7)
#     elif option2 == "150KW":
#         image8 = Image.open('Verbruik Vrachtwagen 150kw alleen op depot laden.jpeg')
#         st.image(image8)
#         image9 = Image.open('Vrachtwagen 150kw bij klant en depot laden.jpeg')
#         st.image(image9)
#     elif option2 == "Waterstof":
#         image15 = Image.open('Vrachtwagen waterstof op depot .jpeg')
#         st.image(image15)
#         image16 = Image.open('Vrachtwagen waterstof tanken bij klant en depot.jpeg')
#         st.image(image16)
#     elif option2 == "Alleen Depot":
#         image6 = Image.open('Vrachtwagen 43 kw alleen op depot laden.jpeg')
#         st.image(image6)
#         image8 = Image.open('Verbruik Vrachtwagen 150kw alleen op depot laden.jpeg')
#         st.image(image8)
#         image15 = Image.open('Vrachtwagen waterstof op depot .jpeg')
#         st.image(image15)
#     elif option2 == "Klant en Depot":
#         image7 = Image.open('Vrachtwagen 43kw bij klant en depot laden.jpeg')
#         st.image(image7)
#         image9 = Image.open('Vrachtwagen 150kw bij klant en depot laden.jpeg')
#         st.image(image9)
#         image16 = Image.open('Vrachtwagen waterstof tanken bij klant en depot.jpeg')
#         st.image(image16)       
# elif pages == 'Energieverbruik':
#     st.title("Energieverbruik")
#     st.markdown("*KPI's*")
#     col1, col2, col3 = st.columns(3)
#     col1.metric("Max verbruik (maand)", "Januari")
#     col2.metric("Meest voorkomend profiel", "9")
#     col3.metric("Max energieverbruik", "0,0056%")
#     st.plotly_chart(fig)
# elif pages == "Voorspelling elektrische auto's":
#     st.title("Voorspelling elektrische auto's")
#     image10 = Image.open('Elektrische voertuigen door de jaren heen.jpeg')
#     st.image(image10)
#     image11 = Image.open('Prognose E-trucks en bestelwagens.jpeg')
#     st.image(image11)
#     image12 = Image.open('Toekomstvoorspelling elektrische voertuigen.jpeg')
#     st.image(image12)
# elif pages == "Kaart WFO":
#     st.title('Kaart WFO')
#     image13 = Image.open('Oppervlakte WFO.jpeg')
#     st.image(image13)
#     st.plotly_chart(fig3)
# elif pages == "Kaart Schiphol Trade Centre":
#     st.title('Kaart Schiphol Trade Centre')
#     image14 = Image.open('Schiphol Trade Centre.jpeg')
#     st.image(image14)
#     st.plotly_chart(fig2)

# In[ ]:




