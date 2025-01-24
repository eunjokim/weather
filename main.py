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
    st.title("By Month")

    # Load data
    data = load_data()

    # Month names in English
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }

    # Filter by month and show daily rainfall as boxplot
    st.subheader("By Month")
    month = st.selectbox("Select a month", [month_names[m] for m in sorted(data['월'].unique())])
    selected_month = list(month_names.keys())[list(month_names.values()).index(month)]
    monthly_data = data[data['월'] == selected_month]

    if monthly_data.empty:
        st.warning(f"No data available for {month}.")
    else:
        fig, ax = plt.subplots()
        ax.boxplot(
            [monthly_data[monthly_data['일'] == day]['강수량'].dropna() for day in monthly_data['일'].unique()],
            labels=monthly_data['일'].unique(),
            patch_artist=True,
            boxprops=dict(facecolor='lightblue', color='black'),
            medianprops=dict(color='red')
        )
        ax.set_xlabel('Day of Month')
        ax.set_ylabel('Rainfall (mm)')
        st.pyplot(fig)

if __name__ == "__main__":
    main()


