import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title='Kiva Loan Dashboard ', 
                   page_icon=":bar_chart:",
                   layout="wide")


st.title(" :bar_chart: :green[Kiva] Loan EDA Dashboard")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',
            unsafe_allow_html=True)

# Sidebar for additional information
st.sidebar.title('Kiva Dashboard')
<<<<<<< HEAD
image ="kuva.png"
st.sidebar.image(image, caption='Image', use_column_width=True)
=======
image = Image.open(r"C:\Users\sawsa_v1iymt5\Downloads\My-Github\Kiva_Loan_Dashboard\kuva.png")
st.sidebar.image(image)
>>>>>>> fb8056f97c026462ee014060033206eb0294e461
st.sidebar.write("This dashboard is using Kiva dataset from Kaggle for Python Data Analysis Diploma.")
st.sidebar.write("")
            

# Signature
st.sidebar.write("")
st.sidebar.markdown("Made with :green_heart: by Eng. [Sawsan Abdulbari](https://www.linkedin.com/in/sawsan-abdulbari-5a4533104)")


            
st.subheader("Exploration and Analysis")

st.markdown('''
**Welcome to the Kiva Loan Dashboard (2013-2017)**

*Your gateway to in-depth exploration and analysis of Kiva loans.*

**Overview:**

This interactive dashboard empowers you to delve into Kiva loan data from 2013 to 2017. Our goal is to display the data research and analysis by offering insightful information on the loans handled through Kiva.
            
**Features:**

1. **Insights:** Explore crucial statistics and metrics related to Kiva loans, including Funded loan amounts, Sector with Activity ,Time series  and Country ...etc.

2. **Navigation:** The left-hand sidebar menu makes it easy to navigate through various sections, including "Overview" and "Data Exploration & Analysis."

3. **Filtering:** The left-hand sidebar menu has a wide variety of data filtering options for desired specific insights.      

            
**Data Exporting:** 

The unfiltered and filtered data can be downloaded in .csv and .xls formats.

**Data Sources:**

We source data meticulously from Kiva dataset in Kaggle, ensuring data integrity and reliability.

**Conclusion and Summary:**
In this dashboard, we have presented key insights from the Kiva loan data analysis. We observed trends in loan posting, explored borrowed Loan amounts, and analyzed the distribution of loans by Country, sector and activity.


**Acknowledgment:**

A lot of gratitude to :green[Eng. Mostafa Othman] For guidance through out the project. 
We extend our gratitude to Kiva and the community for their valuable contributions, furthering the cause of poverty alleviation through microloans.
''', unsafe_allow_html=True)

# Increase font size for the entire introduction text
st.markdown('<div style="font-size: 24px;">---</div>', unsafe_allow_html=True)
