import pysolr
import pandas as pd
import tqdm
import numpy as np

users_to_docs = {}
docs_to_users = {}

NUM_DOCS = 50000
docs = []


def build_databases(solr_docs, solr_clicks):
    doc_ids = solr_docs.search("*:*", rows=50000, fl='ID')

    # Get the document IDs in the collection
    for doc_id_json in tqdm.tqdm(doc_ids):
        doc_id = doc_id_json['ID']

        # For every doc, find the users that clicked on the document
        users_clicked = solr_clicks.search("DocumentID:{0}".format(doc_id), fl='UserID')
        if len(users_clicked) > 0:
            # Create the set of users (without duplicates)
            user_ids = list(set([user_clicked_json['UserID'] for user_clicked_json in users_clicked if 'UserID' in user_clicked_json]))

            # Add the users that clicked on this document to the docs_to_users dict
            docs_to_users[doc_id] = user_ids
            docs.append(doc_id)

            for user_id in user_ids:
                # If the user id is in the users_to_docs, but the doc is not in that user entry, add it
                if user_id in users_to_docs:
                    if doc_id not in users_to_docs[user_id]:
                        users_to_docs[user_id].append(doc_id)
                else:
                    users_to_docs[user_id] = [doc_id]

def main():
    solr_docs = pysolr.Solr('http://localhost:8983/solr/Legal_Data')
    solr_clicks = pysolr.Solr('http://localhost:8983/solr/LILog')

    build_databases(solr_docs, solr_clicks)

    clicks = []

    for i, doc_a in tqdm.tqdm(enumerate(docs)):
        for j, doc_b in enumerate(docs[i+1:]):
            assert doc_a != doc_b
            users_clicked_a = set(docs_to_users[doc_a])
            users_clicked_b = set(docs_to_users[doc_b])
            users_clicked_both = users_clicked_a.intersection(users_clicked_b)
            if len(users_clicked_both) > 0:
                clicks.append([doc_a,doc_b,len(users_clicked_both)])

    clicks_pd = pd.DataFrame(data=clicks, columns=['ID', 'OtherID', 'Count'])
    clicks_pd.to_csv('click_data.csv', index=False)


if __name__ == '__main__':
    main()
