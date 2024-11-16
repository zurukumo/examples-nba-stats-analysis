import json

import pandas as pd
from scipy.stats import binom

with open('this.json') as f:
    data = json.load(f)

    headers = data['resultSets'][0]['headers']
    rows = data['resultSets'][0]['rowSet']

    this_df = pd.DataFrame(rows, columns=headers)
    this_df = this_df[["PLAYER_ID", "PLAYER_NAME", "FG3A", "FG3M", "FG3_PCT"]]
    this_df = this_df.rename(columns={"FG3A": "THIS_FG3A", "FG3M": "THIS_FG3M", "FG3_PCT": "THIS_FG3_PCT"})

with open('last.json') as f:
    data = json.load(f)

    headers = data['resultSets'][0]['headers']
    rows = data['resultSets'][0]['rowSet']

    last_df = pd.DataFrame(rows, columns=headers)
    last_df = last_df[["PLAYER_ID", "FG3A", "FG3M", "FG3_PCT"]]
    last_df = last_df.rename(columns={"FG3A": "LAST_FG3A", "FG3M": "LAST_FG3M", "FG3_PCT": "LAST_FG3_PCT"})

merged_df = pd.merge(this_df, last_df, on="PLAYER_ID")

# 昨シーズンより3PT%が5%以上向上した選手を抽出
merged_df['FG3_PCT_DIFF'] = merged_df['THIS_FG3_PCT'] - merged_df['LAST_FG3_PCT']
merged_df = merged_df[merged_df['FG3_PCT_DIFF'] > 0.05]

# 昨シーズン3PTAが200本以上の選手を抽出
merged_df = merged_df[merged_df['LAST_FG3A'] >= 200]

# 今シーズン3PTAが20本以上の選手を抽出
merged_df = merged_df[merged_df['THIS_FG3A'] >= 20]

merged_df = merged_df[['PLAYER_NAME', 'THIS_FG3A', 'THIS_FG3M', 'THIS_FG3_PCT', 'LAST_FG3A', 'LAST_FG3M', 'LAST_FG3_PCT']]

merged_df["LIKELIHOOD"] = 1 - binom.cdf(merged_df['THIS_FG3M'] - 1, merged_df['THIS_FG3A'], merged_df['LAST_FG3_PCT'])

merged_df = merged_df.sort_values('LIKELIHOOD', ascending=False)

print(merged_df)
