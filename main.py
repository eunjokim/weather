import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load data
file_path = '강수량.csv'
@st.cache_data
def load_data(path):
    return pd.read_csv(path, encoding='euc-kr')

data = load_data(file_path)

# Ensure the date column exists and is properly formatted if necessary
if 'date' in data.columns:
    data['date'] = pd.to_datetime(data['date'], errors='coerce')
else:
    st.error("The dataset must have a 'date' column.")
    st.stop()

# Fill missing values in the rainfall column with 0
if 'rainfall' in data.columns:
    data['rainfall'] = data['rainfall'].fillna(0)
else:
    st.error("The dataset must have a 'rainfall' column.")
    st.stop()

# Extract month and day
data['month'] = data['date'].dt.month
data['day'] = data['date'].dt.day

# Sidebar for month selection
st.sidebar.title("Monthly Rainfall Analysis")
month_selected = st.sidebar.selectbox("Select a month:", range(1, 13), format_func=lambda x: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][x-1])

# Filter data for the selected month
filtered_data = data[data['month'] == month_selected]

if filtered_data.empty:
    st.warning(f"No data available for {['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][month_selected-1]}.")
else:
    # Create a boxplot for daily rainfall distribution
    st.title(f"Rainfall Distribution in {['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][month_selected-1]}")

    fig, ax = plt.subplots()
    filtered_data.boxplot(column='rainfall', by='day', ax=ax, grid=False)

    ax.set_title(f"Daily Rainfall Distribution in {['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][month_selected-1]}")
    ax.set_xlabel("Day of the Month")
    ax.set_ylabel("Rainfall (mm)")
    plt.suptitle("")  # Remove the default title from pandas boxplot

    st.pyplot(fig)
