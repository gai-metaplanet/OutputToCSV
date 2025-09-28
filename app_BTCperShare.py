import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.title("Bitcoin（JPY）と 3350.T 株価の比較グラフ")

# --- 期間選択 ---
period = st.selectbox("期間を選択してください", ["1mo", "3mo", "6mo", "1y", "2y"], index=0)

# --- データ取得方法選択 ---
data_source = st.radio("データの取得方法を選択", ["yfinanceから取得", "CSVをアップロード"])

plot_df = None  # 後で代入する用

# --- yfinanceから取得 ---
if data_source == "yfinanceから取得":
    if st.button("データ取得（yfinance）"):
        btc_data = yf.download("BTC-JPY", period=period)
        stock_data = yf.download("3350.T", period=period)

        if btc_data.empty:
            st.error("BTC-JPY のデータが取得できませんでした。ティッカー名や期間を確認してください。")
        elif stock_data.empty:
            st.error("3350.T のデータが取得できませんでした。ティッカー名や期間を確認してください。")
        else:
            btc_close = btc_data[['Close']].copy()
            btc_close.columns = ['BTC_JPY']

            stock_close = stock_data[['Close']].copy()
            stock_close.columns = ['3350.T']

            plot_df = pd.concat([btc_close, stock_close], axis=1)
            plot_df.dropna(inplace=True)

            plot_df['BTC purchasable per shares'] = plot_df['3350.T'] / plot_df['BTC_JPY'] * 1000 / 1.25
            plot_df['BTC holdings per shares'] = 0

# --- CSVアップロード ---
elif data_source == "CSVをアップロード":
    uploaded_file = st.file_uploader("CSVファイルを選択してください", type=["csv"])
    if uploaded_file is not None:
        plot_df = pd.read_csv(uploaded_file, index_col=0, parse_dates=True)

# --- データがある場合のみ以下を表示 ---
if plot_df is not None:
    st.write("取得したデータ列名:", plot_df.columns.tolist())
    st.dataframe(plot_df.head())

    # CSVダウンロードボタン
    csv = plot_df.to_csv(index=True)
    st.download_button(
        label="グラフデータをCSVでダウンロード",
        data=csv,
        file_name='graph_data.csv',
        mime='text/csv'
    )

    # --- グラフ描画 ---
    st.subheader("価格推移グラフ")
    fig, ax1 = plt.subplots(figsize=(10, 5))

    fig.patch.set_facecolor('black')
    ax1.set_facecolor('black')

    ax1.plot(plot_df.index, plot_df['BTC purchasable per shares'],
             label="Bitcoin purchasable per 1,000 shares", color='orange')
    ax1.plot(plot_df.index, plot_df['BTC holdings per shares'],
             label="Bitcoin holdings per 1,000 shares", color='lime')

    ax1.set_ylabel("Bitcoin purchasable", color='white')
    ax1.tick_params(axis='y', labelcolor='white')
    ax1.tick_params(axis='x', colors='white')
    ax1.spines['bottom'].set_color('white')
    ax1.spines['left'].set_color('white')

    # 2軸目（株価）
    ax2 = ax1.twinx()
    ax2.set_facecolor('black')
    ax2.plot(plot_df.index, plot_df['3350.T'], label="3350.T", color='cyan')
    ax2.set_ylabel("3350.T (JPY)", color='cyan')
    ax2.tick_params(axis='y', labelcolor='cyan')
    ax2.spines['right'].set_color('cyan')

    plt.title("Bitcoin (JPY) vs 3350.T", color='white')

    fig.tight_layout()
    st.pyplot(fig)
else:
    st.info("データを取得するかCSVをアップロードしてください。")
