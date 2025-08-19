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
        # chartOptionsData の JSON 部分を抜き出し
        match = re.search(r'"chartOptionsData":(\[.*?\])', target_script, re.S)
        if match:
            raw_json = match.group(1)

            # JSON内のエスケープを直す（\" → " など）
            fixed_json = raw_json.encode("utf-8").decode("unicode_escape")

            try:
                chart_data_list = json.loads(fixed_json)
            except Exception as e:
                st.error(f"JSONパース失敗: {e}")
                st.text(fixed_json[:500])  # デバッグ表示
                chart_data_list = []

            for chart in chart_data_list:
                df = pd.DataFrame(chart["chartData"])
                df["label"] = chart["label"]
                df["ticker"] = chart["ticker"]

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
            st.error("chartOptionsData を抽出できませんでした（正規表現マッチなし）")
    else:
        st.error("対象の <script> が見つかりませんでした")
