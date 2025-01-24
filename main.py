import streamlit as st

st.title('Weather')
st.write("Let's start")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
def load_data():
    file_path = '강수량.csv'
    data = pd.read_csv(file_path, encoding='euc-kr')
    data['날짜'] = pd.to_datetime(data['날짜'])  # Convert date column to datetime
    data['월'] = data['날짜'].dt.month  # Extract month from date
    return data

# Streamlit app
def main():
    st.title("Daily Rainfall Analysis")

    # Load data
    data = load_data()

    # Display raw data
    st.subheader("Raw Data")
    st.dataframe(data)

    # Basic statistics
    st.subheader("Basic Statistics")
    st.write(data.describe())

    # Line chart for rainfall over time
    st.subheader("Rainfall Over Time")
    fig, ax = plt.subplots()
    ax.plot(data['날짜'], data['강수량'], label='Daily Rainfall', color='blue')
    ax.set_xlabel('Date')
    ax.set_ylabel('Rainfall (mm)')
    ax.set_title('Daily Rainfall Trend')
    ax.legend()
    st.pyplot(fig)

    # Histogram for rainfall distribution
    st.subheader("Rainfall Distribution")
    fig, ax = plt.subplots()
    ax.hist(data['강수량'].dropna(), bins=20, color='skyblue', edgecolor='black')
    ax.set_xlabel('Rainfall (mm)')
    ax.set_ylabel('Frequency')
    ax.set_title('Rainfall Distribution')
    st.pyplot(fig)

    # Filter by month and show rainfall distribution
    st.subheader("Monthly Rainfall Distribution")
    month = st.selectbox("Select a month", sorted(data['월'].unique()))
    monthly_data = data[data['월'] == month]

    fig, ax = plt.subplots()
    ax.bar(monthly_data['날짜'].dt.day, monthly_data['강수량'], color='orange', edgecolor='black')
    ax.set_xlabel('Day of Month')
    ax.set_ylabel('Rainfall (mm)')
    ax.set_title(f'Rainfall Distribution for Month {month}')
    st.pyplot(fig)

if __name__ == "__main__":
    main()
