import pandas as pd
from wetscraper import wetten
import numpy as np


def fix_csv():
    df = pd.read_csv('../data/law_references.csv', encoding='latin1', dtype=str)
    df = df.replace(np.nan, '', regex=True)
    df["wetboek"] = df["wetboek"] + ' ' + df["bwnummer"]
    df["wetboeklink"] = df["wetboek"].str.lower()
    df["wetboeklink"] = df["wetboeklink"].str.strip()
    keys = list(wetten.keys())
    lowerkeys = [k.lower() for k in keys]
    df = df.loc[df["wetboeklink"].isin(lowerkeys)]
    df["wetboeklink"] = df["wetboeklink"].apply(lambda x: wetten[keys[lowerkeys.index(x)]])
    df["wetboeklink"] = '/' + df["wetboeklink"] + '/artikel' + df['artikel']
    df["wetboeklink"].loc[df["lid"] != ''] = df["wetboeklink"].loc[df["lid"] != ''] + '/lid' + df["lid"].loc[df["lid"] != '']
    df2 = df.groupby(['ID', 'wetboek', 'artikel', 'lid', 'wetboeklink']).size()
    df2 = df2.reset_index()
    df2.columns.values[5] = 'count'
    df2.to_csv('../data/law_references2.csv', index=False)

fix_csv()