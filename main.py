import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load data
file_path = '강수량.csv'
@st.cache_data
def load_data(path):
    try:
        # Attempt to read with utf-8 encoding
        return pd.read_csv(path, encoding='utf-8')
    except UnicodeDecodeError:
        # Fallback to euc-kr encoding
        return pd.read_csv(path, encoding='euc-kr')

data = load_data(file_path)

# Rename columns for consistency
if '날짜' in data.columns:
    data.rename(columns={'날짜': 'date'}, inplace=True)
if '강수량' in data.columns:
    data.rename(columns={'강수량': 'rainfall'}, inplace=True)

# Ensure the date column exists and is properly formatted if necessary
if 'date' in data.columns:
    # Split the 'date' column into year, month, and day assuming the format is YYYY-MM-DD or similar
    try:
        data['year'], data['month'], data['day'] = zip(*data['date'].str.split('-').apply(lambda x: (int(x[0]), int(x[1]), int(x[2]))))
    except Exception as e:
        st.error("Failed to process the 'date' column. Please ensure it follows the expected format (e.g., YYYY-MM-DD).")
        st.write(f"Error details: {e}")
        st.stop()
else:
    st.error("The dataset must have a 'date' column.")
    st.stop()

# Fill missing values in the rainfall column with 0
if 'rainfall' in data.columns:
    data['rainfall'] = data['rainfall'].fillna(0)
else:
    st.error("The dataset must have a 'rainfall' column.")
    st.stop()

# Filter data within the specified date range
start_date = '1973-12-01'
end_date = '2025-01-21'
data['date'] = pd.to_datetime(data['date'], errors='coerce')
data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]

# Main page for month selection
st.title("Monthly Rainfall Analysis")
month_selected = st.selectbox("Select a month:", range(1, 13), format_func=lambda x: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][x-1])

# Filter data for the selected month
filtered_data = data[data['month'] == month_selected]

if filtered_data.empty:
    st.warning(f"No data available for {['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][month_selected-1]}.")
else:
    # Create a boxplot for daily rainfall distribution
    fig, ax = plt.subplots(figsize=(12, 6), dpi=200)  # Increase the width of the plot and set dpi
    filtered_data.boxplot(column='rainfall', by='day', ax=ax, grid=False)

    ax.set_title(f"Rainfall Distribution in {['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][month_selected-1]}")
    ax.set_xlabel("Day of the Month")
    ax.set_ylabel("Rainfall (mm)")
    plt.suptitle("")  # Remove the default title from pandas boxplot

    st.pyplot(fig)
