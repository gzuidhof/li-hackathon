import pandas as pd

df1 = pd.read_csv('~/neo4j-community-3.2.5/import/documents.csv.bak', error_bad_lines=False)
print(len(df1))
import ipdb
ipdb.set_trace()
df2 = pd.read_csv('pagerank.csv')

df1 = df1.set_index('ID')
df2 = df2.set_index('id')
df1['pagerank'] = df2.pagerank

df1.to_csv('merged.csv')
