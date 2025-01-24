import streamlit as st
import pandas as pd
import koreanize_matplotlib
import plotly.express as px

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 데이터 파일 경로
file_path = '강수량.csv'

# Month names in English
month_names = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'
}

def main():
    st.title("강수량 데이터 분석")

    # 데이터 불러오기
    try:
        data = pd.read_csv(file_path, encoding='euc-kr')

        # 날짜와 강수량 데이터 처리
        if '날짜' in data.columns and '강수량' in data.columns:
            data['날짜'] = pd.to_datetime(data['날짜'])
            data['월'] = data['날짜'].dt.month
            data['일'] = data['날짜'].dt.day

            # 월 선택
            st.subheader("월별 강수량 분포")
            selected_month_name = st.selectbox(
                "월을 선택하세요:",
                list(month_names.values())  # 월 이름 리스트
            )

            # 선택한 월 데이터를 필터링
            month_num = {v: k for k, v in month_names.items()}[selected_month_name]  # 영문 이름을 숫자로 변환
            filtered_data = data[data['월'] == month_num]

            if not filtered_data.empty:
                st.write(f"선택한 월: {selected_month_name}")

                # 박스플롯 생성
                fig, ax = plt.subplots(figsize=(12, 6))

                # 날짜별 강수량 데이터를 재구조화
                boxplot_data = [
                    filtered_data[filtered_data['일'] == day]['강수량'].values
                    for day in range(1, 32)  # 1일부터 31일까지
                ]
                # 박스플롯 그리기
                ax.boxplot(boxplot_data, positions=range(1, 32), widths=0.6)
                ax.set_title(f"{selected_month_name}의 날짜별 강수량 분포")
                ax.set_xlabel("날짜")
                ax.set_ylabel("강수량")
                ax.set_xticks(range(1, 32))  # 1부터 31까지 x축 설정
                ax.set_xticklabels(range(1, 32))  # x축 레이블 추가
                ax.tick_params(axis='x', rotation=45)  # x축 레이블 45도 회전
                
                st.pyplot(fig)
            else:
                st.warning("선택한 월에 데이터가 없습니다.")
        else:
            st.error("데이터에 '날짜' 또는 '강수량' 열이 없습니다.")
    except Exception as e:
        st.error(f"데이터를 불러오는 데 문제가 발생했습니다: {e}")

if __name__ == "__main__":
    main()
