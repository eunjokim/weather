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
    # Format the date column
    data['date'] = pd.to_datetime(data['date'], errors='coerce')
    data.dropna(subset=['date'], inplace=True)
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
data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]

# Extract month-day for analysis
data['month_day'] = data['date'].dt.strftime('%m-%d')

# Group by month-day to calculate probabilities
probability_data = data.groupby('month_day').apply(
    lambda x: {
        'rain_probability': (x['rainfall'] > 0).mean() * 100,
        'average_rainfall': x.loc[x['rainfall'] > 0, 'rainfall'].mean()
    }
).apply(pd.Series).reset_index()

# Main app
st.title("Rainfall Probability Predictor")
st.write("### Based on records from 1973-12-01 to 2025-01-21")

# User input
input_date = st.text_input("Enter a date (MM-DD):", value="02-20")

if input_date:
    # Find the probability and average rainfall for the input date
    result = probability_data[probability_data['month_day'] == input_date]

    if result.empty:
        st.warning(f"No data available for the date {input_date}.")
    else:
        rain_probability = result['rain_probability'].values[0]
        average_rainfall = result['average_rainfall'].values[0]

        st.subheader(f"Rainfall Analysis for {input_date}")
        st.write(f"**Probability of Rain:** {rain_probability:.2f}%")
        st.write(f"**Average Rainfall:** {average_rainfall:.2f} mm")

