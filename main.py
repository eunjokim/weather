import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 데이터 로드 및 전처리
@st.cache
def load_data():
    # CSV 파일 불러오기
    data = pd.read_csv('강수량.csv')
    # 강수량 열의 빈칸을 0으로 채우기
    if '강수량' in data.columns:
        data['강수량'] = data['강수량'].fillna(0)
    return data

data = load_data()

# Streamlit 애플리케이션
st.title("월별 날짜별 강수량 분포")

# 월 선택 드롭다운 (영어 이름으로 표시)
months = {
    "January": 1, "February": 2, "March": 3, "April": 4, 
    "May": 5, "June": 6, "July": 7, "August": 8, 
    "September": 9, "October": 10, "November": 11, "December": 12
}
selected_month = st.selectbox("월을 선택하세요", list(months.keys()))
month_number = months[selected_month]

# 월 필터링
if '월' in data.columns and '일' in data.columns:
    filtered_data = data[data['월'] == month_number]

    # 박스플롯 그리기
    st.subheader(f"{selected_month} 날짜별 강수량 분포")
    if not filtered_data.empty:
        fig, ax = plt.subplots()
        # X축: 날짜, Y축: 강수량
        filtered_data.groupby('일')['강수량'].apply(list).plot.box(ax=ax)
        ax.set_title(f"{selected_month} 날짜별 강수량")
        ax.set_xlabel("날짜")
        ax.set_ylabel("강수량")
        st.pyplot(fig)
    else:
        st.write("선택한 월에 데이터가 없습니다.")
else:
    st.write("데이터에 '월' 또는 '일' 열이 없습니다.")
