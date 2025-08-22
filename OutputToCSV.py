        match = re.search(r'self\.__next_f\.push\(\[\d+,"(.*?)"\]\);', target_script, re.S)
        if match:
            escaped_str = match.group(1)
            decoded_str = bytes(escaped_str, "utf-8").decode("unicode_escape")
        
            json_match = re.search(r'({\s*"chartOptionsData"\s*:\s*\[.*?\]})', decoded_str, re.S)
            if json_match:
                json_str = json_match.group(1)
                try:
                    data_obj = json.loads(json_str)
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
                    st.code(json_str[:500])
            else:
                st.error("chartOptionsData を含む JSON 部分が見つかりませんでした")
                st.code(decoded_str[:1000])
        else:
            st.error("self.__next_f.push(...) の構造が見つかりませんでした")