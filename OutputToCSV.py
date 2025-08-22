import re
import json
import requests
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup

st.title("Metaplanet Analytics グラフデータ収集")

url = "https://metaplanet.jp/en/analytics"

if st.button("データ取得"):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    target_script = None
    all_scripts = soup.find_all("script")

    st.subheader("取得した <script> タグ一覧（先頭1000文字）")
    for i, script in enumerate(all_scripts):
        script_content = script.string or ''.join(script.contents)
        if script_content:
            st.text(f"--- script[{i}] ---")
            st.code(script_content[:1000])

        # chartOptionsData を含むスクリプトを探す
        if "chartOptionsData" in script_content and not target_script:
            target_script = script_content

    if target_script:
        # Next.js の push(...) 内の JSON を抽出
        match = re.search(r'self\.__next_f\.push\(\[.*?({.*?"chartOptionsData".*?})\].*?\)', target_script, re.S)
        if match:
            raw_json = match.group(1)

            # JSON整形（必要に応じて修正）
            try:
                data_obj = json.loads(raw_json)
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
                st.subheader("抽出された JSON（先頭500文字）")
                st.code(raw_json[:500])
        else:
            st.error("chartOptionsData を含む JSON 部分が見つかりませんでした")
            st.subheader("対象スクリプトの内容（先頭1000文字）")
            st.code(target_script[:1000])
    else:
        st.error("対象の <script> が見つかりませんでした")