import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
def load_data():
    file_path = '강수량.csv'
    data = pd.read_csv(file_path, encoding='euc-kr')
    data['날짜'] = pd.to_datetime(data['날짜'])  # Convert date column to datetime
    data['월'] = data['날짜'].dt.month  # Extract month from date
    data['일'] = data['날짜'].dt.day  # Extract day from date
    return data

# Streamlit app
def main():
    st.title("Daily Rainfall Analysis")

    # Load data
    data = load_data()

    # Filter by month and show daily rainfall as pie chart
    st.subheader("Monthly Rainfall Distribution")
    month = st.selectbox("Select a month", sorted(data['월'].unique()))
    monthly_data = data[data['월'] == month]

    if monthly_data.empty:
        st.warning(f"No data available for month {month}.")
    else:
        daily_rainfall = monthly_data.groupby('일')['강수량'].sum()
        fig, ax = plt.subplots()
        ax.pie(daily_rainfall, labels=daily_rainfall.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.tab20.colors)
        ax.set_title(f'Daily Rainfall Distribution for Month {month}')
        st.pyplot(fig)

if __name__ == "__main__":
    main()

