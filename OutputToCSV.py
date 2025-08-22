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
    all_scripts = soup.find_all("script")

    # すべての <script> タグの中身を表示（デバッグ用）
    st.subheader("取得した <script> タグ一覧（先頭1000文字）")
    for i, script in enumerate(all_scripts):
        script_content = script.string or ''.join(script.contents)
        if script_content:
            st.text(f"--- script[{i}] ---")
            st.code(script_content[:1000])  # 長すぎる場合は先頭1000文字だけ表示

        # chartOptionsData を含むスクリプトを探す
        if "chartOptionsData" in script_content and not target_script:
            target_script = script_content

    if target_script:
        # 柔軟な正規表現で chartOptionsData を含む JSON を抽出
        match = re.search(r'1,000株あたりのビットコイン\', target_script, re.S)
        if not match:
            match = re.search(r'1,000株あたりのビットコイン', target_script, re.S)

        if match:
            raw_json = match.group(1)

            # エスケープ文字の処理
            fixed_json_str = raw_json.encode("utf-8").decode("unicode_escape")

            try:
                data_obj = json.loads(fixed_json_str)
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
                st.code(fixed_json_str[:500])
        else:
            st.error("chartOptionsData を含む JSON 部分が見つかりませんでした")
            st.subheader("対象スクリプトの内容（先頭1000文字）")
            st.code(target_script[:1000])
    else:
        st.error("対象の <script> が見つかりませんでした")