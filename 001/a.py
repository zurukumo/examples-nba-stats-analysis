import json

import pandas as pd

# traditionalデータの読み込み
with open('traditional.json', 'r') as f:
    data = json.load(f)

    headers = data['resultSets'][0]['headers']
    rows = data['resultSets'][0]['rowSet']

    traditional_df = pd.DataFrame(rows, columns=headers)

# advancedデータの読み込み
with open('advanced.json', 'r') as f:
    data = json.load(f)

    headers = data['resultSets'][0]['headers']
    rows = data['resultSets'][0]['rowSet']

    advanced_df = pd.DataFrame(rows, columns=headers)

# traditional_dfとadvanced_dfをPLAYER_IDをキーにして結合
merged_df = traditional_df.merge(advanced_df, on='PLAYER_ID')

# 必要な列だけ抽出
merged_df = merged_df[["PLAYER_NAME_x", "GP_x", "PTS", "TS_PCT"]]

# 列名を変更
merged_df = merged_df.rename(
    columns={"PLAYER_NAME_x": "PLAYER_NAME", "GP_x": "GP"})

# 得点を試合平均に換算
merged_df["PTS"] = merged_df["PTS"] / merged_df["GP"]

# 試合平均20点以上の選手だけ抽出
merged_df = merged_df[merged_df["PTS"] >= 20]

# TS_PCTで降順ソート
merged_df = merged_df.sort_values("TS_PCT", ascending=False)

print(merged_df)
