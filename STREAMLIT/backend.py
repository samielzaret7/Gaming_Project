import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

@st.cache
def load_data():
    url = 'https://raw.githubusercontent.com/data-bootcamp-v4/data/main/supermarket_sales.csv'
    data = pd.read_csv(url)
    data['Date'] = pd.to_datetime(data['Date'])
    return data

def get_summary(data):
    summary = pd.DataFrame({
        'Total Sales': [data['Total'].sum()],
        'Average Rating': [data['Rating'].mean()],
        'Total Transactions': [data['Invoice ID'].nunique()]
    })
    return summary

def plot_sales_over_time(data):
    data['Date'] = pd.to_datetime(data['Date'])
    sales_over_time = data.groupby(data['Date'].dt.date)['Total'].sum()
    plt.figure(figsize=(10, 5))
    plt.plot(sales_over_time.index, sales_over_time.values)
    plt.title('Sales Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Sales')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)