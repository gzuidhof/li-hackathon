import pysolr
import numpy as np
import re
import pandas as pd
import datetime
import tqdm

import extract_article

import dateutil.parser

LEN_LD = 32303       #411724
LEN_RVDR = 99453     #419864

NUM_LD = 30000     # How many docs from Legal_Data ?
NUM_RVDR = 90000   # How many docs from RvdR ?

ROWS_PER_QUERY = 1000

selected_keys = ['ID', 'PublicationNumber', 'ProcedureType', 'TopLevelNavigation', 'Authors', 'Classifications', 'LawArea', 'Sources', 'Topic', 'Summary_Text', 'Title_Text', 'timestamp', 'SearchNumber']
law_keys = ['wetboek','bwnummer','artikel','lid']

wetboek_conversion = {}

with open('wetten.txt', 'r') as f:
    laws = f.read()
    short_names_all = []
    full_names_all = []
    for line in laws.split('\n'):
        split = line.split(';')
        full_name = split[0]
        full_names_all.append(full_name)
        short_names = split[1:]
        for short_name in short_names:
            short_names_all.append(short_name)
            if not short_name.lower() in  wetboek_conversion:
                wetboek_conversion[short_name.lower()] = full_name
    laws_short = "|".join(short_names_all)
    laws_full = "|".join(full_names_all)

print(wetboek_conversion)

ljn_re = "(LJN)[ :]*([A-Z]{2}) *([0-9]{4})"
ecli_re = "ECLI:[A-Z]*:[A-Z]*:[0-9]*:[0-9]+"

def extract_references(doc, ecli):
    # Search for ECLI numbers
    result = re.findall(ecli_re, doc)
    # Search for LJN numbers
    result.extend(re.findall(ljn_re, doc))

    if result and len(result) > 0:
        result = ["".join(r) for r in result]

        if ecli:
            result = [r for r in result if r != ecli]
        un, c = np.unique(np.asarray(result), return_counts=True)
        return list(un), list(c)
    return None, None

def extract_fields(result):
    values = []

    for key in selected_keys:
        value = result[key] if key in result else None

        if key == 'timestamp':
            time = dateutil.parser.parse(value)
            time = time.replace(tzinfo=None)
            value = int((time - datetime.datetime(1970, 1, 1)).total_seconds())

        values.append(value)
    return values


def extract_laws(doc, id):
    law_references = []
    for m in re.finditer(laws_full, doc, re.IGNORECASE):
        law_name = m.group(0)
        context = doc[m.start(0)-80:m.end(0)+80]
        info = extract_article.get_article(context,law_name)
        if info is None:
            continue
        if info['wetboek'].lower() in wetboek_conversion:
            info['wetboek'] = wetboek_conversion[info['wetboek'].lower()]
        lr = [id]
        lr.extend([info[key] if key in info else None for key in law_keys])
        law_references.append(lr)

    for m in re.finditer(laws_short, doc):
        law_name = m.group(0)
        context = doc[m.start(0)-80:m.end(0)+80]

        info = extract_article.get_article(context,law_name)
        if info is None:
            continue
        if info['wetboek'].lower() in wetboek_conversion:
            info['wetboek'] = wetboek_conversion[info['wetboek'].lower()]
        lr = [id]
        lr.extend([info[key] if key in info else None for key in law_keys])
        law_references.append(lr)

    return law_references

def results_to_csvs(results, collection=True, ECLI=True, law_references=True):
    references_db = []
    law_references_db = []
    documents_db = []

    for r in results:
        # Get document fields
        if collection:
            documents_db.append(extract_fields(r))

        # Get ECLI & LJN references
        if ECLI:
            ecli = r['SearchNumber'] if 'SearchNumber' in r else None
            references, counts = extract_references(r['Text_Text_1'], ecli)

            if references is not None and len(references) > 0:
                for ref, c in zip(references, counts):
                    references_db.append([r['ID'], ecli, ref, c])

        # Get Law References
        if 'ID' in r and law_references:
            laws = extract_laws(r['Text_Text_1'], r['ID'])
            if len(laws) > 0:
                law_references_db.extend(laws)

    references_pd = None
    lr_pd = None
    documents_pd = None

    if ECLI:
        references_pd = pd.DataFrame(data=references_db, columns=['ID', 'SearchNumber', 'References', 'Counts'])
        #references_pd.to_csv('references.csv')

    if law_references:
        lr_pd = pd.DataFrame(data=law_references_db, columns=['ID', 'wetboek', 'bwnummer', 'artikel', 'lid'])
        #lr_pd.to_csv("law_references.csv", index=None)

    if collection:
        documents_pd = pd.DataFrame(data=documents_db, columns=selected_keys)

    return references_pd, lr_pd, documents_pd

def main():
    solr_ld = pysolr.Solr('http://localhost:8983/solr/Legal_Data')
    solr_rvdr =  pysolr.Solr('http://localhost:8983/solr/RvdR_Data')
    return
    references_pd = pd.DataFrame(columns=['ID','SearchNumber','References','Counts'])
    references_pd.to_csv('references.csv',index=False)

    lr_pd = pd.DataFrame(columns=['ID','wetboek','bwnummer','artikel','lid'])
    lr_pd.to_csv('law_references.csv', index=False)

    documents_pd = pd.DataFrame(columns=selected_keys)
    documents_pd.to_csv('documents.csv', index=False)

    with open('documents.csv', 'a', encoding='UTF-8') as docs, open('law_references.csv', 'a', encoding='UTF-8') as law_refs, open('references.csv', 'a', encoding='UTF-8') as refs:
        print("Querying Legal_Data\n")
        for i in tqdm.tqdm(range(int(NUM_LD / ROWS_PER_QUERY))):
            results = solr_ld.search("LawArea:\"Burgerlijk recht\" AND NOT Source:Rechtspraak.nl", start=i * ROWS_PER_QUERY, rows=ROWS_PER_QUERY)
            references_pd, lr_pd, documents_pd = results_to_csvs(results)
            references_pd.to_csv(refs, index=False, header=False)
            lr_pd.to_csv(law_refs, index=False, header=False)
            documents_pd.to_csv(docs, index=False, header=False)
        print("Querying RvdR_Data\n")
        for i in tqdm.tqdm(range(int(NUM_RVDR / ROWS_PER_QUERY))):
            results = solr_rvdr.search("LawArea:\"Burgerlijk recht\"", start=i * ROWS_PER_QUERY, rows=ROWS_PER_QUERY)
            references_pd, lr_pd, documents_pd = results_to_csvs(results)
            references_pd.to_csv(refs, index=False, header=False)
            lr_pd.to_csv(law_refs, index=False, header=False)
            documents_pd.to_csv(docs, index=False, header=False)
    #results = solr.search("*:*", rows=50000)
    #results_to_csvs(results,collection=False,ECLI=False)


def countfunctie():
    solr = pysolr.Solr('http://localhost:8983/solr/Legal_Data')
    field = "Sources"
    results = solr.search("*:*", rows=50000)
    content = np.asarray([r[field] for r in results if field in r])
    un,c = np.unique(content, return_counts=True)
    sort = np.argsort(-c)
    for type, count in zip(un[sort], c[sort]):
        print("{0}: {1}".format(type, count))

if __name__ == '__main__':
    main()