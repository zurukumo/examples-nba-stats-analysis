import json

import pandas as pd

# 1.json ~ 4.jsonまで読み込み
with open('1.json', 'r') as f:
    data = json.load(f)

    headers = data['resultSets'][0]['headers']
    rows = data['resultSets'][0]['rowSet']

    df1 = pd.DataFrame(rows, columns=headers)
    df1 = df1[["PLAYER_ID", "PLAYER_NAME", "FG3A"]]
    df1 = df1.rename(columns={"FG3A": "FG3A_VERY_TIGHT"})

with open('2.json', 'r') as f:
    data = json.load(f)

    headers = data['resultSets'][0]['headers']
    rows = data['resultSets'][0]['rowSet']

    df2 = pd.DataFrame(rows, columns=headers)
    df2 = df2[["PLAYER_ID", "FG3A"]]
    df2 = df2.rename(columns={"FG3A": "FG3A_TIGHT"})

with open('3.json', 'r') as f:
    data = json.load(f)

    headers = data['resultSets'][0]['headers']
    rows = data['resultSets'][0]['rowSet']

    df3 = pd.DataFrame(rows, columns=headers)
    df3 = df3[["PLAYER_ID", "FG3A"]]
    df3 = df3.rename(columns={"FG3A": "FG3A_OPEN"})

with open('4.json', 'r') as f:
    data = json.load(f)

    headers = data['resultSets'][0]['headers']
    rows = data['resultSets'][0]['rowSet']

    df4 = pd.DataFrame(rows, columns=headers)
    df4 = df4[["PLAYER_ID", "FG3A"]]
    df4 = df4.rename(columns={"FG3A": "FG3A_WIDE_OPEN"})

# 1.json ~ 4.jsonを結合
merged_df = pd.merge(df1, df2, on='PLAYER_ID')
merged_df = pd.merge(merged_df, df3, on='PLAYER_ID')
merged_df = pd.merge(merged_df, df4, on='PLAYER_ID')

merged_df["FG3A"] = merged_df["FG3A_VERY_TIGHT"] + merged_df["FG3A_TIGHT"] + \
    merged_df["FG3A_OPEN"] + merged_df["FG3A_WIDE_OPEN"]

# FG3Aが100本以上の選手だけ抽出
merged_df = merged_df[merged_df["FG3A"] >= 100]

merged_df["VERY_TIGHT_RATIO"] = merged_df["FG3A_VERY_TIGHT"] / merged_df["FG3A"]
merged_df["TIGHT_RATIO"] = merged_df["FG3A_TIGHT"] / merged_df["FG3A"]
merged_df["OPEN_RATIO"] = merged_df["FG3A_OPEN"] / merged_df["FG3A"]
merged_df["WIDE_OPEN_RATIO"] = merged_df["FG3A_WIDE_OPEN"] / merged_df["FG3A"]

merged_df = merged_df[["PLAYER_ID", "PLAYER_NAME",
                       "VERY_TIGHT_RATIO", "TIGHT_RATIO", "OPEN_RATIO", "WIDE_OPEN_RATIO"]]


merged_df = merged_df.sort_values("WIDE_OPEN_RATIO", ascending=False)

pd.set_option('display.max_rows', 500)

print(merged_df)
