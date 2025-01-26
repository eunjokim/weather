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

# Train-test split
X = data[['month', 'day']]
y = data['rain']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Classifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Main app
st.title("Rainfall Prediction using Machine Learning")
st.write(f"### Model Accuracy: {accuracy:.2f}")

# User input
month = st.number_input("Enter month (1-12):", min_value=1, max_value=12, value=2)
day = st.number_input("Enter day (1-31):", min_value=1, max_value=31, value=20)

if st.button("Predict Rainfall"):
    # Predict rainfall probability for the given month and day
    prediction = model.predict([[month, day]])
    probability = model.predict_proba([[month, day]])[0][1] * 100

    if prediction[0] == 1:
        st.write(f"### It is likely to rain on {month:02d}-{day:02d}.")
        st.write(f"**Predicted Probability of Rain:** {probability:.2f}%")
    else:
        st.write(f"### It is unlikely to rain on {month:02d}-{day:02d}.")
        st.write(f"**Predicted Probability of Rain:** {probability:.2f}%")
