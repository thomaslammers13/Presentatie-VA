#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import numpy as np
#import plotly as plt
#import plotly.express as px
#import plotly.graph_objects as go
#from plotly.subplots import make_subplots
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







