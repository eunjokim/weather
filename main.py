import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import calendar

# 데이터 파일 경로
file_path = '강수량.csv'

# Streamlit 앱
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
            month_names = list(calendar.month_name[1:])  # 1월부터 12월까지의 영문 이름 리스트
            selected_month = st.selectbox("월을 선택하세요:", month_names)
            
            # 선택한 월 데이터를 필터링
            month_num = month_names.index(selected_month) + 1  # 월 이름을 숫자로 변환
            filtered_data = data[data['월'] == month_num]
            
            if not filtered_data.empty:
                st.write(f"선택한 월: {selected_month}")
                
                # 박스플롯 생성
                fig, ax = plt.subplots(figsize=(10, 6))
                filtered_data.boxplot(column='강수량', by='일', ax=ax, vert=True)
                ax.set_title(f"{selected_month}의 날짜별 강수량 분포")
                ax.set_xlabel("날짜")
                ax.set_ylabel("강수량")
                plt.suptitle("")  # 기본 제목 제거
                st.pyplot(fig)
            else:
                st.warning("선택한 월에 데이터가 없습니다.")
        else:
            st.error("데이터에 '날짜' 또는 '강수량' 열이 없습니다.")
    except Exception as e:
        st.error(f"데이터를 불러오는 데 문제가 발생했습니다: {e}")

if __name__ == "__main__":
    main()
