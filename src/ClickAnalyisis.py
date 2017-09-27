import pysolr
import pandas as pd
import tqdm
import numpy as np

click_db = {}
doc_db = {}

NUM_DOCS = 50000
docs = []

def build_databases(solr_docs, solr_clicks):
    ids = solr_docs.search("*:*", rows=50000, fl='ID')
    for id_ in tqdm.tqdm(ids):
        id = id_['ID']
        docs.append(id)
        users_clicked = solr_clicks.search("DocumentID:{0}".format(id), fl='UserID')
        ids_clicked = []
        for u in users_clicked:
            if 'UserID' in u:
                user_id = u['UserID']
                if users_clicked not in ids_clicked:
                    ids_clicked.append(user_id)
                    if user_id in click_db:
                        if id not in click_db[user_id]:
                            click_db[user_id].append(id)
                    else:
                        click_db[user_id] = [id]
        doc_db[id] = ids_clicked

def main():
    solr_docs = pysolr.Solr('http://localhost:8983/solr/Legal_Data')
    solr_clicks = pysolr.Solr('http://localhost:8983/solr/LILog')

    build_databases(solr_docs, solr_clicks)

    clicks = []

    for doc, users_clicked in tqdm.tqdm(doc_db.items()):
        relevant_docs = {}
        for user in users_clicked:
            for doc_clicked in click_db[user]:
                if doc_clicked is not doc:
                    if doc_clicked in relevant_docs:
                        relevant_docs[doc_clicked] += 1
                    else:
                        relevant_docs[doc_clicked] = 1
        for other_doc, count in  relevant_docs.items():
            clicks.append([doc, other_doc, count])

    clicks_pd = pd.DataFrame(data=clicks,columns=['ID','OtherID','Count'])
    clicks_pd.to_csv('click_data.csv',index=False)

if __name__=='__main__':
    main()