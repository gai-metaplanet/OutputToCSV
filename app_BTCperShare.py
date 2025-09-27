import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.title("Bitcoin（JPY）と 3350.T 株価の比較グラフ")

period = st.selectbox("期間を選択してください", ["1mo", "3mo", "6mo", "1y", "5y"], index=0)

# データ取得
btc_data = yf.download("BTC-JPY", period=period)
stock_data = yf.download("3350.T", period=period)

# 空データチェック
if btc_data.empty:
    st.error("BTC-JPY のデータが取得できませんでした。ティッカー名や期間を確認してください。")
elif stock_data.empty:
    st.error("3350.T のデータが取得できませんでした。ティッカー名や期間を確認してください。")
else:
    # Close列を抽出して明示的に名前を付ける
    btc_close = btc_data[['Close']].copy()
    btc_close.columns = ['BTC_JPY']

    stock_close = stock_data[['Close']].copy()
    stock_close.columns = ['3350.T']

    # index を揃えて結合
    plot_df = pd.concat([btc_close, stock_close], axis=1)
    plot_df.dropna(inplace=True)

    # BTC ÷ 3350.T の列を追加
    plot_df['BTC purchasable per shares'] = plot_df['3350.T'] / plot_df['BTC_JPY'] / 1000
    plot_df['BTC holdings per shares'] = 0

    st.write("取得したデータ列名:", plot_df.columns.tolist())
    st.dataframe(plot_df.head())

# グラフ描画
st.subheader("価格推移グラフ")

fig, ax1 = plt.subplots(figsize=(10, 5))

# 図全体の背景を黒に
fig.patch.set_facecolor('black')
# ax1の背景も黒に
ax1.set_facecolor('black')

# 1軸目（Bitcoin）
ax1.plot(plot_df.index, plot_df['BTC purchasable per shares'], label="Bitcoin purchasable per 1,000 shares", color='orange')
# ★ここで追加線を描画★
ax1.plot(plot_df.index, plot_df['BTC holdings per shares'], label="Bitcoin holdings per 1,000 shares", color='lime')

ax1.set_ylabel("Bitcoin purchasable", color='orange')
ax1.tick_params(axis='y', labelcolor='orange')
ax1.tick_params(axis='x', colors='white')  # x軸ラベルも白に
ax1.spines['bottom'].set_color('white')
ax1.spines['left'].set_color('orange')

# 2軸目（株価）
ax2 = ax1.twinx()
ax2.set_facecolor('black')  # twinx側も黒に
ax2.plot(plot_df.index, plot_df['3350.T'], label="3350.T", color='cyan')
ax2.set_ylabel("3350.T (JPY)", color='blue')
ax2.tick_params(axis='y', labelcolor='blue')
ax2.spines['right'].set_color('blue')

# タイトルを白に
plt.title("Bitcoin (JPY) vs 3350.T", color='white')

fig.tight_layout()
st.pyplot(fig)

