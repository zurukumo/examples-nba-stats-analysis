import json

import pandas as pd

# 1.json ~ 4.jsonまで読み込み
with open('1.json', 'r') as f:
    data = json.load(f)

    headers = data['resultSets'][0]['headers']
    rows = data['resultSets'][0]['rowSet']

    df1 = pd.DataFrame(rows, columns=headers)
    df1 = df1[["PLAYER_ID", "PLAYER_NAME", "PLAYER_LAST_TEAM_ABBREVIATION", "FG3A"]]
    df1 = df1.rename(columns={"PLAYER_LAST_TEAM_ABBREVIATION": "TEAM", "FG3A": "FG3A_VERY_TIGHT_RS"})

with open('2.json', 'r') as f:
    data = json.load(f)

    headers = data['resultSets'][0]['headers']
    rows = data['resultSets'][0]['rowSet']

    df2 = pd.DataFrame(rows, columns=headers)
    df2 = df2[["PLAYER_ID", "FG3A"]]
    df2 = df2.rename(columns={"FG3A": "FG3A_TIGHT_RS"})

with open('3.json', 'r') as f:
    data = json.load(f)

    headers = data['resultSets'][0]['headers']
    rows = data['resultSets'][0]['rowSet']

    df3 = pd.DataFrame(rows, columns=headers)
    df3 = df3[["PLAYER_ID", "FG3A"]]
    df3 = df3.rename(columns={"FG3A": "FG3A_OPEN_RS"})

with open('4.json', 'r') as f:
    data = json.load(f)

    headers = data['resultSets'][0]['headers']
    rows = data['resultSets'][0]['rowSet']

    df4 = pd.DataFrame(rows, columns=headers)
    df4 = df4[["PLAYER_ID", "FG3A"]]
    df4 = df4.rename(columns={"FG3A": "FG3A_WIDE_OPEN_RS"})

# 5.json ~ 8.jsonまで読み込み
with open('5.json', 'r') as f:
    data = json.load(f)

    headers = data['resultSets'][0]['headers']
    rows = data['resultSets'][0]['rowSet']

    df5 = pd.DataFrame(rows, columns=headers)
    df5 = df5[["PLAYER_ID", "FG3A"]]
    df5 = df5.rename(columns={"FG3A": "FG3A_VERY_TIGHT_PO"})

with open('6.json', 'r') as f:
    data = json.load(f)

    headers = data['resultSets'][0]['headers']
    rows = data['resultSets'][0]['rowSet']

    df6 = pd.DataFrame(rows, columns=headers)
    df6 = df6[["PLAYER_ID", "FG3A"]]
    df6 = df6.rename(columns={"FG3A": "FG3A_TIGHT_PO"})

with open('7.json', 'r') as f:
    data = json.load(f)

    headers = data['resultSets'][0]['headers']
    rows = data['resultSets'][0]['rowSet']

    df7 = pd.DataFrame(rows, columns=headers)
    df7 = df7[["PLAYER_ID", "FG3A"]]
    df7 = df7.rename(columns={"FG3A": "FG3A_OPEN_PO"})

with open('8.json', 'r') as f:
    data = json.load(f)

    headers = data['resultSets'][0]['headers']
    rows = data['resultSets'][0]['rowSet']

    df8 = pd.DataFrame(rows, columns=headers)
    df8 = df8[["PLAYER_ID", "FG3A"]]
    df8 = df8.rename(columns={"FG3A": "FG3A_WIDE_OPEN_PO"})


# 1.json ~ 8.jsonを結合
merged_df = pd.merge(df1, df2, on='PLAYER_ID')
merged_df = pd.merge(merged_df, df3, on='PLAYER_ID')
merged_df = pd.merge(merged_df, df4, on='PLAYER_ID')
merged_df = pd.merge(merged_df, df5, on='PLAYER_ID')
merged_df = pd.merge(merged_df, df6, on='PLAYER_ID')
merged_df = pd.merge(merged_df, df7, on='PLAYER_ID')
merged_df = pd.merge(merged_df, df8, on='PLAYER_ID')

merged_df["FG3A_RS"] = merged_df["FG3A_VERY_TIGHT_RS"] + merged_df["FG3A_TIGHT_RS"] + merged_df["FG3A_OPEN_RS"] + merged_df["FG3A_WIDE_OPEN_RS"]
merged_df["FG3A_PO"] = merged_df["FG3A_VERY_TIGHT_PO"] + merged_df["FG3A_TIGHT_PO"] + merged_df["FG3A_OPEN_PO"] + merged_df["FG3A_WIDE_OPEN_PO"]

# FG3AがRSで100本以上かつPOで20本以上の選手だけ抽出
merged_df = merged_df[(merged_df["FG3A_RS"] >= 100) & (merged_df["FG3A_PO"] >= 20)]

merged_df["WIDE_OPEN_RATIO_RS"] = merged_df["FG3A_WIDE_OPEN_RS"] / merged_df["FG3A_RS"]
merged_df["WIDE_OPEN_RATIO_PO"] = merged_df["FG3A_WIDE_OPEN_PO"] / merged_df["FG3A_PO"]
merged_df["WIDE_OPEN_RATIO_DIFF"] = merged_df["WIDE_OPEN_RATIO_PO"] - merged_df["WIDE_OPEN_RATIO_RS"]

merged_df = merged_df[
    ["PLAYER_NAME", "TEAM", "WIDE_OPEN_RATIO_RS", "WIDE_OPEN_RATIO_PO", "WIDE_OPEN_RATIO_DIFF"]
]


merged_df = merged_df.sort_values("WIDE_OPEN_RATIO_DIFF", ascending=False)

pd.set_option('display.max_rows', 500)

print(merged_df)
