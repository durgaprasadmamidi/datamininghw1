
import streamlit as st
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from google.cloud.exceptions import NotFound
from google.oauth2 import id_token
from google.auth.transport import requests
import altair as alt
import os
# Authenticate with Google Cloud and create a BigQuery client
# Replace 'your-project-id' with your actual Google Cloud project ID

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"])

client = bigquery.Client(credentials=credentials)



# client = bigquery.Client(project='data-mining-415919')
# client = documentai.DocumentProcessorServiceClient(credentials=credentials)


# Write your BigQuery SQL query to fetch the COVID-19 data
query = """
SELECT 
    month,
    total_cases_positive_increase,
    total_tests_total,
    total_deaths
FROM 
    `data-mining-415919.covid.summary`
    
"""

# Execute the query and fetch the results into a Pandas DataFrame
df = client.query(query).to_dataframe()

# Create a Streamlit app
st.title('COVID-19 Data Visualization')

# Bar graph: Total positive cases by month
st.subheader('Bar Graph: Total Positive Cases by Month')
st.bar_chart(df.set_index('month')['total_cases_positive_increase'])

# Line graph: Total tests conducted over time
st.subheader('Line Graph: Total Tests Conducted Over Time')
st.line_chart(df.set_index('month')['total_tests_total'])

# Statistical graph: Box plot for Total Deaths using Altair
st.subheader('Box Plot: Total Deaths')
chart = alt.Chart(df).mark_boxplot().encode(
    x='month',
    y='total_deaths'
)
st.altair_chart(chart)
