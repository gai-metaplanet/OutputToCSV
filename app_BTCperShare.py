import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.title("Bitcoin（JPY）と 3350.T 株価の比較グラフ")

# 期間をユーザー指定できるように
period = st.selectbox("期間を選択してください", ["1mo", "3mo", "6mo", "1y", "5y"], index=1)

# Bitcoin JPY建てを直接取得
btc_data = yf.download("BTC-JPY", period=period)

# 3350.T (日本株)
stock_data = yf.download("3350.T", period=period)

# データ整理
plot_df = pd.DataFrame({
    'BTC_JPY': btc_data['Close'],
    '3350.T': stock_data['Close']
})

# 欠損を削除
plot_df.dropna(inplace=True)

st.write("取得したデータ（先頭）:")
st.dataframe(plot_df.head())

# グラフ描画
st.subheader("価格推移グラフ")

fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(plot_df.index, plot_df['BTC_JPY'], label="Bitcoin (JPY)", color='orange')
ax1.set_ylabel("Bitcoin (JPY)", color='orange')
ax1.tick_params(axis='y', labelcolor='orange')

ax2 = ax1.twinx()
ax2.plot(plot_df.index, plot_df['3350.T'], label="3350.T", color='blue')
ax2.set_ylabel("3350.T 株価 (JPY)", color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

plt.title("Bitcoin (JPY) vs 3350.T 株価")
fig.tight_layout()
st.pyplot(fig)
