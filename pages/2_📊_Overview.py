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

st.title(":bar_chart: Overview Of Data")

st.markdown('<style>div.block-container{padding-top:1rem;}</style>',
            unsafe_allow_html=True)

df = pd.read_csv(r"C:\Users\sawsa_v1iymt5\OneDrive\Documents\data_science\kiva_loan_project\Kiva_Cleaned_Data.csv")
df1 = pd.read_csv(r'C:\Users\sawsa_v1iymt5\OneDrive\Documents\data_science\kiva_loan_project\Kiva_Loan.csv')
df2 = pd.read_csv(r'C:\Users\sawsa_v1iymt5\OneDrive\Documents\data_science\kiva_loan_project\Cleaned.csv')

# row a
a1, a2, a3, a4 = st.columns(4)
total_loans = len(df2)
# Create a DataFrame with the counts of each gender
gender_counts = df2[['Female', 'Male', 'Not specified']].sum()
# Calculate the percentage count for the 'Female' category
percentage_count_female = ((gender_counts['Female'] / gender_counts.sum()) * 100).round(2)
# Format the total 
formatted_percentage_supported_by_women = f"{percentage_count_female:.1f}%"

# Calculate the total loan funded amount
total_funded_amount = df2['funded_amount'].sum()
# Format the total loan funded amount using humanize
formatted_total_funded_amount = f"{total_funded_amount / 1e6:.1f} M"

# Calculate the total number of borrowers received loans
total_borrowers_received_loans = df2[['Female', 'Male', 'Not specified']].sum().sum()
formatted_total_borrowers = f"{total_borrowers_received_loans  / 1e6:.2f} M"
# Calculate the total number of lenders
total_lenders = df2['lender_count'].sum()
# formatted_total_lenders = f"{total_lenders / 1e6:.1f} M"
formatted_total_lenders = f"{total_lenders  / 1e6:.2f} M"


# Display the formatted total loan funded amount
a1.metric("Total Loan Amount", formatted_total_funded_amount)
a2.metric("Loans by Women", formatted_percentage_supported_by_women)
a3.metric("T. Borrowers Received Loans", formatted_total_borrowers)
a4.metric("Total Lenders", formatted_total_lenders)


# Sidebar for additional information
st.sidebar.title('Kiva Dashboard')
image = Image.open(r"C:\Users\sawsa_v1iymt5\Downloads\My-Github\Kiva_Loan_Dashboard\kuva.png")
st.sidebar.image(image)
st.sidebar.write("This dashboard is using Kiva dataset from Kaggle for Python Data Analysis Diploma.")
st.sidebar.write("")

# Filter options
st.sidebar.header("Choose your filter: ")
# Create for Countery
country = st.sidebar.multiselect("Pick Country", df["country"].unique())
if not country:
    df2 = df.copy()
else:
    df2 = df[df["country"].isin(country)]

# Create for Sector
sector = st.sidebar.multiselect("Pick the Sector", df2["sector"].unique())
if not sector:
    df3 = df2.copy()
else:
    df3 = df2[df2["sector"].isin(sector)]

# Create for Activity
activity = st.sidebar.multiselect("Pick the Activity",df3["activity"].unique())

# Filter the data based on Country, Sector and Activity

if not country and not sector and not activity:
    filtered_df = df
elif not sector and not activity:
    filtered_df = df[df["country"].isin(country)]
elif not country and not activity:
    filtered_df = df[df["sector"].isin(sector)]
elif sector and activity:
    filtered_df = df3[df["sector"].isin(sector) & df3["activity"].isin(activity)]
elif country and sector:
    filtered_df = df3[df["country"].isin(country) & df3["sector"].isin(sector)]
elif country and activity:
    filtered_df = df3[df["country"].isin(country) & df3["activity"].isin(activity)]
elif sector:
    filtered_df = df3[df3["sector"].isin(sector)]
else:
    filtered_df = df3[df3["country"].isin(country) & df3["sector"].isin(sector) & df3["activity"].isin(activity)]

col1, col2 = st.columns((2))
with col1:
    sector_loan = (filtered_df.groupby(by = ['sector'], as_index= False)['funded_amount'].sum()).round(2)

# Create a bar plot using Plotly Express
    fig = px.bar(sector_loan, x='sector', y='funded_amount',
             title='Sectors in Terms of Funded Loan Amount',
             labels={'sector': 'Loan Sector', 'funded_amount': 'Total Funded Loan Amount'},
             text=['${:,.2f}'.format(x) for x in sector_loan['funded_amount']],
             template="seaborn",color='sector' )
    st.plotly_chart( fig, use_container_width=True,height=600)


with col2:
    st.subheader("Country vs. Funded Amount")
    category_counts = filtered_df['country'].value_counts()
    fig = px.pie(category_counts,
                  names=category_counts.index, 
                  values=category_counts.values)
    fig.update_traces(textinfo='percent+label', pull=[0.1, 0.1, 0.1])
    st.plotly_chart(fig, use_container_width=True,)



# Define a function for data view and download
def view_and_download_data(data, download_filename, download_label):
    st.write(data.style.background_gradient(cmap="Blues"))
    csv = data.to_csv(index=False).encode('utf-8')
    st.download_button(download_label, 
                       data=csv, 
                       file_name=download_filename, 
                       mime="text/csv", 
                       help=f'Click here to download the {download_label} as a CSV file')

# Define the layout of columns
cl1, cl2 = st.columns(2)

# Sector Data
with cl1:
    with st.expander("Sector_ViewData"):
        sector_data = sector_loan
        view_and_download_data(sector_data, "Sector.csv", "Download Sector Data")

# Country Data
with cl2:
    with st.expander("Country_ViewData"):
        country = filtered_df.groupby(by = "country", as_index = False)["funded_amount"].sum().round(2)

        country_data = country
        view_and_download_data(country_data, "Country.csv", "Download Country Data")




# Sidebar layout
st.sidebar.header("Date Range Filters:")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime('2013-01-01'))
end_date = st.sidebar.date_input("End Date", pd.to_datetime('2017-12-31'))

# Date range validation
start_date = pd.to_datetime(start_date)  # Convert start_date to datetime
end_date = pd.to_datetime(end_date)  # Convert end_date to datetime
if start_date > end_date:
    st.error("Start date should be before the end date.")
else:
    # Data preprocessing
    df['date'] = pd.to_datetime(df['date'])
    filtered_data = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    # Time series data aggregation
    time_series_data = filtered_data.groupby(filtered_data['date'].dt.strftime("%Y-%b"))['funded_amount'].sum().reset_index()

    # Create time series chart
    st.subheader("Time Series Analysis of Funded Amount")
    st.markdown("This dashboard allows you to analyze loan data over a specified date range.")
    fig2 = px.line(time_series_data, x='date', y="funded_amount", markers=True, labels={"funded_amount": "Amount"})
    fig2.update_xaxes(type='category')  # To ensure proper sorting on the x-axis
    fig2.update_layout(height=500, width=1000, template="plotly_white")

    # Add a trendline
    trendline = go.Scatter(x=time_series_data['date'], y=time_series_data['funded_amount'],
                           mode='lines', line=dict(color='red'), name='Trendline')
    fig2.add_trace(trendline)

    # Add an annotation
    fig2.add_annotation(x="2017-Jul", y=30000, 
                        text="Significant Decrease", 
                        showarrow=True, arrowhead=1,
                        arrowsize=1.5, arrowwidth=2)

    st.plotly_chart(fig2, use_container_width=True)



chart1, chart2 = st.columns((2))
with chart1:

    # Create a Pie Chart for Repayment Intervals
    st.subheader('Repayment vs. Funded Amount')
    fig1 = px.pie(filtered_df, 
                  values='funded_amount', 
                  names='repayment_interval')
    st.plotly_chart(fig1, use_container_width=True)
    

with chart2:
# Data Preprocessing for Gender Distribution
    gender_list = df1['borrower_genders'].str.split(', ').explode()
    gender_counts = gender_list.value_counts()



# Create a Pie Chart for Borrower Gender Distribution
    st.subheader('Gender Distribution')
    fig2 = px.pie(names=gender_counts.index, 
                  values=(gender_counts / gender_counts.sum()) * 100)
    st.plotly_chart(fig2, use_container_width=True)


# Signature
st.sidebar.write("")
st.sidebar.markdown("Made with :green_heart: by Eng. [Sawsan Abdulbari](https://www.linkedin.com/in/sawsan-abdulbari-5a4533104)")


with st.expander("View Data"):
    st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))

# Download orginal DataSet
    csv = df.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', 
                   data = csv, 
                   file_name = "Data.csv",
                   mime = "text/csv")


st.subheader("Hierarchical view of Loan")

# Filter out rows with zero funded_amount
filtered_df = df[df['funded_amount'] > 0]

# Create the treemap figure
fig3 = px.treemap(filtered_df, 
                  path=["country", "sector", "activity"],
                  values="funded_amount",
                  hover_data=["funded_amount"],
                  color="funded_amount",  # Adjust the color based on funded_amount
                  color_continuous_scale='Viridis',  # Choose a color scale
                  )

# Customize the layout
fig3.update_layout(
    width=800,
    height=650,
    margin=dict(l=0, r=0, b=0, t=30),  # Adjust margin to make space for subheader
)

# Add more interactivity
fig3.update_traces(
    hoverinfo="label+value+percent parent",
    textinfo="label+value",
)

# Set the title and axis labels
fig3.update_layout(
    title="Loan Funding by Country, Sector, and Activity",
    xaxis_title="Funded Amount",
    yaxis_title="Category",
)

st.plotly_chart(fig3, use_container_width=True)


# Convert the "date" column to datetime data type
df["date"] = pd.to_datetime(df["date"])

# Now you can use the .dt accessor to extract the month name
df["month_name"] = df["date"].dt.month_name()
import plotly.figure_factory as ff
st.subheader(":point_right: Monthly Activity Loan Summary")
with st.expander("Summary_Table"):
    df_sample = df[0:5][["country","sector","activity","funded_amount","currency","repayment_interval"]]
    fig = ff.create_table(df_sample, colorscale = "Cividis")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("Month wise Activity Table")
    # filtered_df["date"] = filtered_df["date"].dt.month_name()
    sub_category_Year = pd.pivot_table(data =df, 
                                       values = "funded_amount", 
                                       index = ["activity"],
                                       columns = "date")
    st.write(sub_category_Year.style.background_gradient(cmap="Blues"))
