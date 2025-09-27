import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.title("Bitcoin（JPY）と 3350.T 株価の比較グラフ")

period = st.selectbox("期間を選択してください", ["1mo", "3mo", "6mo", "1y", "5y"], index=1)

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

    st.write("取得したデータ列名:", plot_df.columns.tolist())
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
