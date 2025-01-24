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

    fig, ax = plt.subplots()
    ax.bar(monthly_data['날짜'].dt.day, monthly_data['강수량'], color='orange', edgecolor='black')
    ax.set_xlabel('Day of Month')
    ax.set_ylabel('Rainfall (mm)')
    ax.set_title(f'Rainfall Distribution for Month {month}')
    st.pyplot(fig)

if __name__ == "__main__":
    main()
