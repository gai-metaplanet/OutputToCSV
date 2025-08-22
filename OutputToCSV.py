import re
import requests
import streamlit as st
from bs4 import BeautifulSoup

st.title("Metaplanet Analytics chartOptionsData 抽出（文字列モード）")

url = "https://metaplanet.jp/jp/analytics"

if st.button("データ取得"):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    all_scripts = soup.find_all("script")
    found = False

    for i, script in enumerate(all_scripts):
        script_content = script.string or ''.join(script.contents)
        if not script_content or "self.__next_f.push" not in script_content:
            continue

        matches = re.findall(r'self\.__next_f\.push\(\[\d+,"(.*?)"\]\);', script_content, re.S)
        for j, escaped_str in enumerate(matches):
            decoded_str = bytes(escaped_str, "utf-8").decode("unicode_escape")

            # chartOptionsData を含む部分を文字列として抽出
            chart_match = re.search(r'("chartOptionsData"\s*:\s*\[.*?\])', decoded_str, re.S)
            if chart_match:
                chart_text = chart_match.group(1)
                found = True

                st.subheader(f"[{i}-{j}] chartOptionsData 抽出結果（文字列）")
                st.code(chart_text[:3000])  # 長すぎる場合は先頭だけ表示

                st.download_button(
                    label="chartOptionsData_raw.txt をダウンロード",
                    data=chart_text,
                    file_name="chartOptionsData_raw.txt",
                    mime="text/plain"
                )

    if not found:
        st.warning("chartOptionsData を含む self.__next_f.push(...) が見つかりませんでした")