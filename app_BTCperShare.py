import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.ticker import ScalarFormatter
from datetime import datetime, timedelta

st.title("MetaPlanet BTC per 1,000 Shares")

# ▼ CSV読み込み
uploaded_file = st.file_uploader("CSVファイルをアップロード", type="csv")
if uploaded_file is None:
    st.stop()
clean_meta = pd.read_csv(uploaded_file)

x = np.arange(len(clean_meta['DateLabel']))
forecast_days = 20

# 実データ
x_actual = np.arange(len(clean_meta['DateLabel']))
y_actual = clean_meta['希薄化率'].values
y2_actual = clean_meta['BTC購入量'].values

# フィッティング関数
def exp_func(x, a, b):
    return a * np.exp(b * x)

params, _ = curve_fit(exp_func, x_actual, y_actual, p0=(1, 0.01))
a_fit, b_fit = params
x_extended = np.arange(len(x_actual) + forecast_days)
y_fit_extended = exp_func(x_extended, a_fit, b_fit)
y_fit = exp_func(x_actual, a_fit, b_fit)

# 描画
fig, ax1 = plt.subplots(figsize=(14, 6), facecolor='black')
fig.subplots_adjust(hspace=0.4)
ax1.set_facecolor('black')

ax1.scatter(clean_meta['DateLabel'], y_actual, color='orange', alpha=1, s=10,
            label='BTC purchasable per 1,000 shares')
ax1.plot(clean_meta['DateLabel'], clean_meta['BTC/株'],
         label='BTC holdings per 1,000 shares',
         color='red', linewidth=3)

ax3 = ax1.twinx()
ax3.bar(clean_meta['DateLabel'], y2_actual, label='BTC Purchase Volume', color='cyan', alpha=0.8, width=1)
ax3.set_ylabel('BTC Purchase Volume', color='cyan')
ax3.tick_params(axis='y', colors='cyan')

ax1.set_ylim(0, 0.14)
ax3.set_ylim(0, 3500)

ax1.set_xlabel('Elapsed Days', color='white')
ax1.set_ylabel('BTC Per 1,000 Shares', color='orange')
ax1.tick_params(axis='x', colors='white')
ax1.tick_params(axis='y', colors='orange')
ax1.grid(True, color='white', alpha=0.2)
ax1.set_title('MetaPlanet BTC per 1000 shares', color='white')

# x軸ラベル
ax1.set_xticks(clean_meta['DateLabel'][::20])
ax1.set_xticklabels(clean_meta['DateLabel'][::20], rotation=45, fontsize=12)

# 縦軸の指数表記をオフ
ax1.yaxis.set_major_formatter(ScalarFormatter())
ax1.ticklabel_format(style='plain', axis='y')

legend1 = ax1.legend(loc='upper left', fontsize=12)
legend1.get_frame().set_facecolor('black')
for text in legend1.get_texts():
    text.set_color('white')

plt.tight_layout()
st.pyplot(fig)
