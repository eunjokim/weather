import pandas as pd
import streamlit as st

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

# Ensure the date column exists and is properly formatted
if 'date' in data.columns:
    # Split the 'date' column into year, month, and day assuming the format is YYYY-MM-DD
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

# Create a 'month-day' column for easier filtering
data['month_day'] = data['date'].dt.strftime('%m-%d')

# Main page for date selection
st.title("Rainfall Analysis by Specific Date")
input_date = st.text_input("Enter a date (MM-DD):", value="02-20")

if input_date:
    # Filter data for the specified date
    filtered_data = data[data['month_day'] == input_date]

    if filtered_data.empty:
        st.warning(f"No data available for the date {input_date}.")
    else:
        # Calculate probability of rainfall and average rainfall
        rain_days = filtered_data[filtered_data['rainfall'] > 0]
        total_days = len(filtered_data)
        probability = len(rain_days) / total_days * 100
        average_rainfall = rain_days['rainfall'].mean()

        # Display results
        st.subheader(f"Rainfall Analysis for {input_date}")
        st.write(f"**Probability of Rain:** {probability:.2f}%")
        st.write(f"**Average Rainfall:** {average_rainfall:.2f} mm")
