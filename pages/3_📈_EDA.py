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


st.markdown('<style>div.block-container{padding-top:1rem;}</style>',
            unsafe_allow_html=True)

st.title(":chart_with_upwards_trend: Exploratory Data Analysis")

df = pd.read_csv(r"C:\Users\sawsa_v1iymt5\OneDrive\Documents\data_science\kiva_loan_project\Kiva_Cleaned_Data.csv")
df1 = pd.read_csv(r'C:\Users\sawsa_v1iymt5\OneDrive\Documents\data_science\kiva_loan_project\Kiva_Loan.csv')
df2 = pd.read_csv(r'C:\Users\sawsa_v1iymt5\OneDrive\Documents\data_science\kiva_loan_project\Cleaned.csv')

# Sidebar for additional information
st.sidebar.title('Kiva Dashboard')
image = "kuva.png"
st.sidebar.image(image, caption='Image', use_column_width=True)
st.sidebar.write("This dashboard is using Kiva dataset from Kaggle for Python Data Analysis Diploma.")
st.sidebar.write("")


# Set page title and description
st.subheader("Funded Amount vs. Sector")
st.write("Explore the relationship between Numerical and Categorical Data by selecting from the sidebar")

# Sidebar with filters
st.sidebar.header("Sector Filters:")
num_filter= st.sidebar.selectbox("Select a Numerical Column",[None,'funded_amount', 'loan_amount', 'term_in_months', 'lender_count'])
cat_filter = st.sidebar.selectbox("Select a Categorical Column",[None,'activity', 'sector', 'country', 'currency', 'repayment_interval'])

if num_filter is not None:
    fig = px.scatter(df1, 
                     x="funded_amount", 
                     y='lender_count',
                     color=cat_filter,
                     size=num_filter)

    st.plotly_chart(fig, use_container_width=True)



with st.expander("View Data"):
    st.write(df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))

# Download orginal DataSet
    csv = df.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', 
                   data = csv, 
                   file_name = "Data.csv",
                   mime = "text/csv")


@st.cache_data

def load_data():
    df = pd.read_csv(r"C:\Users\sawsa_v1iymt5\OneDrive\Documents\data_science\test_project\kiva_cleaned_data.csv")

    return df

# Define the main function
def main():
    df = load_data()

    # Create a sidebar for page navigation
    page = st.sidebar.selectbox('Select a Page', ['Sector Analysis', 'Activity Analysis'])

    if page == 'Sector Analysis':
        st.subheader('Popular Loan Sectors in Terms of Funded Amount')
        plot_sector_analysis(df)

    elif page == 'Activity Analysis':
        st.subheader('Popular Loan Activities in Terms of Funded Amount')
        plot_activity_analysis(df)

# Create a function to plot sector analysis
def plot_sector_analysis(df):
    plot_df_sector_popular_loan = (df.groupby(['sector'])['funded_amount'].mean()).round(2).reset_index()
    fig = px.bar(
        plot_df_sector_popular_loan,
        x='sector',
        y='funded_amount',
        title='Average Funded Amount by Sector',
        labels={'sector': 'Loan Sector', 'funded_amount': 'Average Funded Amount'},
        text='funded_amount',
        height=600,
        color='sector'
    )
    fig.update_xaxes(tickangle=45, tickfont=dict(size=14))
    fig.update_yaxes(title_text='Average Funded Amount in Dollar', title_font=dict(size=16))
    fig.update_layout(title_font=dict(size=24))
    st.plotly_chart(fig, use_container_width=True)

# Create a function to plot activity analysis
def plot_activity_analysis(df):
    plot_df_activity_popular_loan = (df.groupby(['activity'])['funded_amount'].mean()).round(2).sort_values(ascending=False)[:20].reset_index()
    fig = px.bar(
        plot_df_activity_popular_loan,
        x='activity',
        y='funded_amount',
        title='Average Funded Amount by Activity',
        labels={'activity': 'Funded Activity', 'funded_amount': 'Average Funded Amount'},
        text='funded_amount',
        height=600,
        color='activity'
    )
    fig.update_xaxes(tickangle=45, tickfont=dict(size=14))
    fig.update_yaxes(title_text='Average Funded Amount in Dollar', title_font=dict(size=16))
    fig.update_layout(title_font=dict(size=24))
    st.plotly_chart(fig, use_container_width=True)

if __name__ == '__main__':
    main()


# Create functions to display box plots
def loan_amount_by_country(df):
    fig = px.box(df, x='funded_amount', y='country',
                 title='Distribution by Country',
                 category_orders={"country": df.groupby("country")["funded_amount"].sum().sort_values(ascending=False).index},
                 width=1000, height=1500, color='country')
    st.plotly_chart(fig)

def loan_amount_by_sector(df):
    fig = px.box(df, x='funded_amount', y='sector',
                 title='Distribution by Sector',
                 width=800, height=800, color='sector')
    st.plotly_chart(fig)


# Sidebar selector for user to choose a plot
plot_choice = st.sidebar.selectbox("Select a Plot", ["Loan Amount by Country", "Loan Amount by Sector"])

# Instructions
st.sidebar.markdown("Explore the distribution of Funded loan amounts by selecting a plot.")

# Display the selected plot and title
if plot_choice == "Loan Amount by Country":
    st.subheader("Funded Loan Amount Distribution by Country")
    loan_amount_by_country(df)
else:
    st.subheader("Funded Loan Amount Distribution by Sector")
    loan_amount_by_sector(df)


# Signature
st.sidebar.write("")
st.sidebar.markdown("Made with :green_heart: by Eng. [Sawsan Abdulbari](https://www.linkedin.com/in/sawsan-abdulbari-5a4533104)")
