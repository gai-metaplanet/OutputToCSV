import re
import json
import requests
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup

st.title("Metaplanet Analytics グラフデータ収集")

url = "https://metaplanet.jp/jp/analytics"

if st.button("データ取得"):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    all_scripts = soup.find_all("script")
    found = False

    st.subheader("取得した <script> タグの中から self.__next_f.push(...) を探索")

    for i, script in enumerate(all_scripts):
        script_content = script.string or ''.join(script.contents)
        if not script_content or "self.__next_f.push" not in script_content:
            continue

        # push(...) の中の JSON風文字列をすべて抽出
        matches = re.findall(r'self\.__next_f\.push\(\[\d+,"(.*?)"\]\);', script_content, re.S)
        for j, escaped_str in enumerate(matches):
            try:
                decoded_str = bytes(escaped_str, "utf-8").decode("unicode_escape")
                json_match = re.search(r'({\s*"chartOptionsData"\s*:\s*\[.*?\]})', decoded_str, re.S)
                if json_match:
                    json_str = json_match.group(1)
                    data_obj = json.loads(json_str)
                    chart_data_list = data_obj["chartOptionsData"]

                    for chart in chart_data_list:
                        df = pd.DataFrame(chart["chartData"])
                        df["label"] = chart.get("label", "")
                        df["ticker"] = chart.get("ticker", "")

                        st.subheader(chart.get("label", ""))
                        st.write(df.head())

                        csv = df.to_csv(index=False)
                        st.download_button(
                            label=f"{chart.get('ticker', 'chart')}.csv をダウンロード",
                            data=csv,
                            file_name=f"{chart.get('ticker', 'chart')}.csv",
                            mime="text/csv"
                        )
                    found = True
            except Exception as e:
                st.error(f"[{i}-{j}] JSONパース失敗: {e}")
                st.code(decoded_str[:1000])

    if not found:
        st.warning("chartOptionsData を含む self.__next_f.push(...) が見つかりませんでした")