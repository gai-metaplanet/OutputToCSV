import re
import json
import requests
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup

st.title("Metaplanet Analytics グラフデータ収集")

url = "https://metaplanet.jp/jp/analytics"

if st.button("データ取得"):
    # HTML取得
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    # <script>内から "chartOptionsData" を探す
    target_script = None
    for script in soup.find_all("script"):
        if script.string and "chartOptionsData" in script.string:
            target_script = script.string
            break

    if target_script:
        # chartOptionsData を抽出
        match = re.search(r'"chartOptionsData":(\[.*?\])', target_script, re.S)
        if match:
            chart_data_list = json.loads(match.group(1))

            for chart in chart_data_list:
                df = pd.DataFrame(chart["chartData"])
                df["label"] = chart["label"]     # グラフ名
                df["ticker"] = chart["ticker"]   # 識別子

                st.subheader(chart["label"])
                st.write(df.head())

                # CSV出力ボタン
                csv = df.to_csv(index=False)
                st.download_button(
                    label=f"{chart['ticker']}.csv をダウンロード",
                    data=csv,
                    file_name=f"{chart['ticker']}.csv",
                    mime="text/csv"
                )
        else:
            st.error("chartOptionsData を抽出できませんでした")
    else:
        st.error("対象の <script> が見つかりませんでした")
