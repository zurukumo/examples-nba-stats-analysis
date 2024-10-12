import json

import pandas as pd

# cs読み込み
with open('cs.json', 'r') as f:
    data = json.load(f)

    headers = data['resultSets'][0]['headers']
    rows = data['resultSets'][0]['rowSet']

    cs_df = pd.DataFrame(rows, columns=headers)
    cs_df = cs_df[["PLAYER_ID", "PLAYER_NAME", "FG3A"]]
    cs_df = cs_df.rename(columns={"FG3A": "FG3A_CS"})

# pu読み込み
with open('pu.json', 'r') as f:
    data = json.load(f)

    headers = data['resultSets'][0]['headers']
    rows = data['resultSets'][0]['rowSet']

    pu_df = pd.DataFrame(rows, columns=headers)
    pu_df = pu_df[["PLAYER_ID", "FG3A"]]
    pu_df = pu_df.rename(columns={"FG3A": "FG3A_PU"})

# cs_dfとpu_dfをPLAYER_IDをキーにして結合
merged_df = cs_df.merge(pu_df, on='PLAYER_ID')

merged_df["FG3A"] = merged_df["FG3A_PU"] + merged_df["FG3A_CS"]

# FG3Aが200本以上の選手だけ抽出
merged_df = merged_df[merged_df["FG3A"] >= 200]

merged_df["CS_RATIO"] = merged_df["FG3A_CS"] / merged_df["FG3A"]
merged_df["PU_RATIO"] = merged_df["FG3A_PU"] / merged_df["FG3A"]

merged_df = merged_df.sort_values("PU_RATIO", ascending=False)


pd.set_option('display.max_rows', 500)

print(merged_df)
