import pandas as pd

path = '/home/joris/neo4j-community-3.2.5/import/references.csv'

df = pd.read_csv(path)

new_df = pd.DataFrame(columns=['ID', 'SearchNumber', 'Reference', 'Count'])
for id, sn, refs, counts in df.itertuples(index=False):
    refs = eval(refs)
    counts = eval(counts)
    for r, c in zip(refs, counts):
        new_df = new_df.append({'ID': id, 'SearchNumber': sn, 'Reference': r, 'Count': c}, ignore_index=True)

new_df.to_csv(path + 'fixed.csv', index=False)