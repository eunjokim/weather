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
            months = {i: calendar.month_name[i] for i in range(1, 13)}
            month_name = st.selectbox("월을 선택하세요:", list(months.values()))
            
            # 선택한 월 데이터 필터링
            month_num = [k for k, v in months.items() if v == month_name][0]
            filtered_data = data[data['월'] == month_num]
            
            if not filtered_data.empty:
                st.write(f"선택한 월: {month_name}")
                
                # 박스플롯 생성
                fig, ax = plt.subplots()
                filtered_data.boxplot(column='강수량', by='일', ax=ax)
                ax.set_title(f"{month_name}의 날짜별 강수량 분포")
                ax.set_xlabel("날짜")
                ax.set_ylabel("강수량")
                plt.suptitle("")  # Remove default subplot title
                st.pyplot(fig)
            else:
                st.warning("선택한 월에 데이터가 없습니다.")
        else:
            st.error("데이터에 '날짜' 또는 '강수량' 열이 없습니다.")
    except Exception as e:
        st.error(f"데이터를 불러오는 데 문제가 발생했습니다: {e}")

if __name__ == "__main__":
    main()
