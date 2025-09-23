import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from scipy.optimize import curve_fit
from matplotlib.ticker import ScalarFormatter
from datetime import datetime, timedelta

# clean_metaは事前に読み込んでおく
# 例: clean_meta = pd.read_csv('your_data.csv')

st.title("MetaPlanet BTC per 1,000 Shares")

# 日本語フォント（Windows用）
jp_font = fm.FontProperties(fname='C:\\Windows\\Fonts\\meiryo.ttc')
plt.rcParams['font.family'] = jp_font.get_name()

x = np.arange(len(clean_meta['DateLabel']))  # X軸の位置
forecast_days = 20

# 実データ
x_actual = np.arange(len(clean_meta['DateLabel']))
y_actual = clean_meta['希薄化率'].values
y2_actual = clean_meta['BTC購入量'].values

# フィッティング関数
def exp_func(x, a, b):
    return a * np.exp(b * x)

# 曲線フィッティング
params, _ = curve_fit(exp_func, x_actual, y_actual, p0=(1, 0.01))
a_fit, b_fit = params

# 拡張X軸
x_extended = np.arange(len(x_actual) + forecast_days)
y_fit_extended = exp_func(x_extended, a_fit, b_fit)
y_fit = exp_func(x_actual, a_fit, b_fit)

# 描画
fig, ax1 = plt.subplots(figsize=(14, 6), facecolor='black')
fig.subplots_adjust(hspace=0.4)
ax1.set_facecolor('black')

# 散布図・棒グラフ
ax1.scatter(clean_meta['DateLabel'], y_actual, color='orange', alpha=1, s=10,
            label='1000株あたりの購入可能BTC - BTC purchasable per 1,000 shares')
ax1.plot(clean_meta['DateLabel'], clean_meta['BTC/株'],
         label='1000株あたりのBTC保有量 - BTC holdings per 1,000 shares',
         color='red', linewidth=3)

ax3 = ax1.twinx()
ax3.bar(clean_meta['DateLabel'], y2_actual, label='BTC購入量', color='cyan', alpha=0.8, width=1)
ax3.set_ylabel('BTC購入量 BTC Purchase Volume', color='cyan')
ax3.tick_params(axis='y', colors='cyan')

ax1.set_ylim(0, 0.14)
ax3.set_ylim(0, 3500)

# 軸ラベル・タイトル
ax1.set_xlabel('経過日数 Elapsed Days', color='white', fontproperties=jp_font)
ax1.set_ylabel('BTC/1000株 BTC Per 1,000 Shares', color='orange', fontproperties=jp_font)
ax1.tick_params(axis='x', colors='white')
ax1.tick_params(axis='y', colors='orange')
ax1.grid(True, color='white', alpha=0.2)

ax1.set_title('MetaPlanet BTC per 1000 shares', color='white', fontproperties=jp_font)

# x軸ラベル
ax1.set_xticks(clean_meta['DateLabel'][::20])
ax1.set_xticklabels(clean_meta['DateLabel'][::20], rotation=45,
                    fontsize=12, fontproperties=jp_font)

# 縦軸の指数表記をオフ
ax1.yaxis.set_major_formatter(ScalarFormatter())
ax1.ticklabel_format(style='plain', axis='y')

# 凡例
legend1 = ax1.legend(loc='upper left', fontsize=12)
legend1.get_frame().set_facecolor('black')
for text in legend1.get_texts():
    text.set_color('white')

plt.tight_layout()

# Streamlitで表示
st.pyplot(fig)
