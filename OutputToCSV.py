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

    target_script = None
    for script in soup.find_all("script"):
        if script.string and "chartOptionsData" in script.string:
            target_script = script.string
            break

    if target_script:
        # self.__next_f.push([...]) 内の "..." を抜き出す
        match = re.search(r'self\.__next_f\.push\(\[.*?"(.*chartOptionsData.*)".*\]\)', target_script, re.S)
        if match:
            raw_str = match.group(1)

            try:
                # 1回目の json.loads でエスケープ解除
                unescaped = json.loads(f'"{raw_str}"')
                # 2回目で dict 化
                data_obj = json.loads(unescaped)

                chart_data_list = data_obj["chartOptionsData"]

                for chart in chart_data_list:
                    df = pd.DataFrame(chart["chartData"])
                    df["label"] = chart["label"]
                    df["ticker"] = chart["ticker"]

                    st.subheader(chart["label"])
                    st.write(df.head())

                    csv = df.to_csv(index=False)
                    st.download_button(
                        label=f"{chart['ticker']}.csv をダウンロード",
                        data=csv,
                        file_name=f"{chart['ticker']}.csv",
                        mime="text/csv"
                    )

            except Exception as e:
                st.error(f"JSONパース失敗: {e}")
                st.text(raw_str[:500])
        else:
            st.error("chartOptionsData を含む文字列が見つかりませんでした")
    else:
        st.error("対象の <script> が見つかりませんでした")
