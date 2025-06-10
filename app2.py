import streamlit as st
import pandas as pd

def calculate_investment(monthly_investment, initial_capital, investment_years, annual_return_rate):
    """
    투자 시뮬레이션을 수행하고 연도별 누적 자산을 계산합니다.
    """
    # 월별 수익률 및 분기별 수익률 계산
    # 연간 수익률이 주어진 경우, 분기별 수익률로 변환
    # (1 + 연간 수익률) = (1 + 분기별 수익률)^4 가정
    quarterly_return_rate = (1 + annual_return_rate)**(1/4) - 1

    total_months = investment_years * 12
    current_balance = initial_capital
    monthly_balances = [0] * (total_months + 1) # 월별 잔액 기록 (인덱스 0은 초기값, 1부터 시작)
    
    # 초기 자본 설정
    monthly_balances[0] = initial_capital

    yearly_cumulative_assets = {}

    for month in range(1, total_months + 1):
        # 매월 1일 매월 투자금 입금
        current_balance += monthly_investment
        
        # 분기월(3, 6, 9, 12월) 말일 수익금 발생
        if month % 3 == 0:
            # 해당 분기의 시작 잔액부터 수익률 적용 (해당 분기 입금된 금액 포함)
            # 여기서는 현재 잔액에 수익률을 적용하는 방식으로 진행
            # 발생된 수익금
            quarterly_profit = current_balance * quarterly_return_rate
            current_balance += quarterly_profit # 수익금 즉시 재투자
            
        monthly_balances[month] = current_balance

        # 연도 말 누적 자산 기록
        if month % 12 == 0:
            year = month // 12
            yearly_cumulative_assets[f"Year {year}"] = current_balance
            
    return yearly_cumulative_assets, monthly_balances

# Streamlit 앱 시작
st.set_page_config(layout="wide") # 페이지 레이아웃을 넓게 설정

st.title("💰 투자 시뮬레이터")

st.markdown("""
    이 앱은 초기 자본, 매월 투자금, 투자 기간, 그리고 예상 수익률을 기반으로 
    연도별 누적 자산을 시뮬레이션하여 보여줍니다.
    수익금은 분기별로 발생하며, 발생 즉시 다음 달 전액 재투자됩니다.
""")

st.header("입력 값")

col1, col2 = st.columns(2)

with col1:
    monthly_investment = st.number_input("매월 투자금 (원)", min_value=0, value=1000000, step=100000, key="monthly_inv")
    st.markdown(f"현재 입력된 값: **{monthly_investment:,}** 원") # 쉼표 추가

    initial_capital = st.number_input("초기 자본 (원)", min_value=0, value=10000000, step=1000000, key="initial_cap")
    st.markdown(f"현재 입력된 값: **{initial_capital:,}** 원") # 쉼표 추가


with col2:
    investment_years = st.number_input("총 투자 기간 (년)", min_value=1, value=10, step=1, key="years")
    annual_return_rate = st.slider("연간 투자율 (수익률, %)", min_value=0.0, max_value=30.0, value=8.0, step=0.1) / 100

if st.button("시뮬레이션 실행"):
    if monthly_investment < 0 or initial_capital < 0 or investment_years <= 0 or annual_return_rate < 0:
        st.error("모든 입력 값은 0보다 크거나 같아야 하며, 투자 기간은 1년 이상이어야 합니다.")
    else:
        st.subheader("📊 시뮬레이션 결과")
        yearly_results, monthly_balances = calculate_investment(monthly_investment, initial_capital, investment_years, annual_return_rate)

        st.write("---")
        st.subheader("연도별 누적 자산")
        
        st.dataframe(
            pd.DataFrame([
                {"연도": year, "누적 자산 (원)": f"{int(asset):,}"} 
                for year, asset in yearly_results.items()
            ]),
            column_config={
                "연도": st.column_config.TextColumn("연도"),
                "누적 자산 (원)": st.column_config.TextColumn("누적 자산 (원)"),
            },
            hide_index=True,
        )
        
        # 월별 잔액 변화 섹션과 그래프를 제거합니다.
        # st.write("---")
        # st.subheader("월별 잔액 변화 (초기 몇 개월 및 마지막 몇 개월)")

        # balance_df = pd.DataFrame({
        #     '월': range(len(monthly_balances)),
        #     '잔액': monthly_balances
        # })
        
        # balance_df['월'] = balance_df['월'].apply(lambda x: f"{x}개월" if x > 0 else "초기")
        
        # st.line_chart(balance_df.set_index('월'))

        # 가장 마지막 월의 총 자산 표시
        st.success(f"**총 {investment_years}년 후 예상 누적 자산:** **{int(yearly_results[f'Year {investment_years}']):,}** 원")