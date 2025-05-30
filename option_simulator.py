import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.title("옵션 수익 시뮬레이터")

# 입력
option_type = st.selectbox("옵션 종류를 선택하세요", ["Call", "Put"])
is_covered = st.checkbox("주식을 보유하고 있나요? (Covered 전략)")
num_stocks_owned = st.number_input("보유한 주식 수 (Covered일 경우)", min_value=0, value=1) if is_covered else 0
strike_price = st.number_input("행사가 (₩)", min_value=0, value=50000)
option_premium = st.number_input("옵션 프리미엄 (₩)", min_value=0, value=5000)
num_options = st.number_input("옵션 계약 수 (1계약 = 1주 기준)", min_value=1, value=1)

# 그래프 표시 체크박스
st.markdown("### 표시할 그래프 선택")
show_option = st.checkbox("옵션 수익 그래프 보기", value=True)
show_stock = st.checkbox("주식 수익 그래프 보기", value=True) if is_covered else False
show_total = st.checkbox("총 수익 그래프 보기", value=True)

# 주가 범위
stock_prices = np.linspace(strike_price - 20000, strike_price + 20000, 500)

# 옵션 수익 계산
if option_type == "Call":
    option_profit = np.where(
        stock_prices <= strike_price,
        option_premium * num_options,
        option_premium * num_options - (stock_prices - strike_price) * num_options
    )
else:
    option_profit = np.where(
        stock_prices >= strike_price,
        option_premium * num_options,
        option_premium * num_options - (strike_price - stock_prices) * num_options
    )

# 주식 수익 계산
stock_profit = (stock_prices - strike_price) * num_stocks_owned if is_covered else np.zeros_like(stock_prices)

# 총 수익 계산
total_profit = option_profit + stock_profit

# 그래프
fig, ax = plt.subplots(figsize=(10, 6))
if show_option:
    ax.plot(stock_prices, option_profit, label="Option Profit", color='blue')
if is_covered and show_stock:
    ax.plot(stock_prices, stock_profit, label="Stock Profit", color='green')
if show_total:
    ax.plot(stock_prices, total_profit, label="Total Profit", color='purple', linewidth=2)

# 기준선
ax.axhline(0, color='gray', linestyle='--')
ax.axvline(strike_price, color='red', linestyle='--', label=f'Strike Price (₩{strike_price:,})')

# ✅ y축 범위는 항상 전체 수익 항목 기준 (숨겨진 항목 포함)
all_y_values = np.concatenate([option_profit, stock_profit, total_profit])
y_min = int(all_y_values.min()) - 10000
y_max = int(all_y_values.max()) + 10000
yticks_range = np.arange(y_min, y_max + 1, 10000)
ax.set_ylim(y_min, y_max)
ax.set_yticks(yticks_range)
ax.set_yticklabels([f"{int(y):,}" for y in yticks_range])

# x축 설정
ax.set_title("Profit vs. Stock Price")
ax.set_xlabel("Stock Price (₩)")
ax.set_ylabel("Profit (₩)")
ax.grid(True)
ax.legend()
ax.set_xticks(np.linspace(stock_prices.min(), stock_prices.max(), 9))
ax.set_xticklabels([f"{int(x):,}" for x in np.linspace(stock_prices.min(), stock_prices.max(), 9)])

# 출력
st.pyplot(fig)
