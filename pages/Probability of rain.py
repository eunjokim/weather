import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load data
file_path = '강수량.csv'
@st.cache_data
def load_data(path):
    try:
        return pd.read_csv(path, encoding='utf-8')
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding='euc-kr')

data = load_data(file_path)

# Rename columns for consistency
if '날짜' in data.columns:
    data.rename(columns={'날짜': 'date'}, inplace=True)
if '강수량' in data.columns:
    data.rename(columns={'강수량': 'rainfall'}, inplace=True)

# Ensure the date column exists and is properly formatted
if 'date' in data.columns:
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

# Feature engineering
data['month'] = data['date'].dt.month
data['day'] = data['date'].dt.day
data['rain'] = (data['rainfall'] > 0).astype(int)  # Create target variable

# Train-test split for rain prediction
X_rain = data[['month', 'day']]
y_rain = data['rain']
X_train_rain, X_test_rain, y_train_rain, y_test_rain = train_test_split(X_rain, y_rain, test_size=0.2, random_state=42)

# Train a Random Forest Classifier for rain prediction
rain_model = RandomForestClassifier(random_state=42)
rain_model.fit(X_train_rain, y_train_rain)

# Train-test split for rainfall amount prediction
X_rainfall = data[data['rainfall'] > 0][['month', 'day']]
y_rainfall = data[data['rainfall'] > 0]['rainfall']
X_train_rainfall, X_test_rainfall, y_train_rainfall, y_test_rainfall = train_test_split(X_rainfall, y_rainfall, test_size=0.2, random_state=42)

# Train a Random Forest Regressor for rainfall amount
from sklearn.ensemble import RandomForestRegressor
rainfall_model = RandomForestRegressor(random_state=42)
rainfall_model.fit(X_train_rainfall, y_train_rainfall)

# Main app
st.title("Rainfall Prediction using Machine Learning")

# User input
month = st.number_input("Enter month (1-12):", min_value=1, max_value=12, value=2)
day = st.number_input("Enter day (1-31):", min_value=1, max_value=31, value=20)

if st.button("Predict"):
    # Predict rainfall probability
    rain_prediction = rain_model.predict([[month, day]])
    rain_probability = rain_model.predict_proba([[month, day]])[0][1] * 100

    # Predict rainfall amount
    predicted_rainfall = rainfall_model.predict([[month, day]])[0]

    # Display results in tabs
    tab1, tab2 = st.tabs(["Rain Probability", "Rainfall Amount"])

    with tab1:
        if rain_prediction[0] == 1:
            st.write(f"### It is likely to rain on {month:02d}-{day:02d}.")
            st.write(f"**Predicted Probability of Rain:** {rain_probability:.2f}%")
        else:
            st.write(f"### It is unlikely to rain on {month:02d}-{day:02d}.")
            st.write(f"**Predicted Probability of Rain:** {rain_probability:.2f}%")

    with tab2:
        if rain_prediction[0] == 1:
            st.write(f"### Predicted Rainfall Amount on {month:02d}-{day:02d}: {predicted_rainfall:.2f} mm")
        else:
            st.write(f"### No rainfall predicted for {month:02d}-{day:02d}.")
