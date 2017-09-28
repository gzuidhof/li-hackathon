import pysolr
import numpy as np
import re
import pandas as pd
import datetime
import tqdm

import extract_article

import dateutil.parser

selected_keys = ['ID', 'PublicationNumber', 'ProcedureType', 'TopLevelNavigation', 'Authors', 'Classifications', 'LawArea', 'Sources', 'Topic', 'Summary_Text', 'Title_Text', 'timestamp', 'SearchNumber']
law_keys = ['wetboek','bwnummer','artikel','lid']

with open('wetten.txt', 'r') as f:
    laws = f.read()
    laws_full = re.sub(';.+\n', "|", laws)
    laws_full = re.sub('\n', '|', laws_full)
    laws_short = re.findall(';.*\n', laws)
    laws_short = "|".join([re.sub("[;\n]", "", s) for s in laws_short])

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
        print(result)
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
    # Search for ECLI numbers
    #re_full = re.compile(laws_full, re.IGNORECASE)
    #re_short = re.compile(laws_short)
    #re_full = "\n.*({0}).*\n".format(laws_full)
    #print(re_full)
    #re_short = "\n.*({0}).*\n".format(laws_short)
    #print(re_short)
    #result = re.findall(re_full, doc, re.IGNORECASE)
    #result.extend(re.findall(re_short, doc))

    law_references = []
    for m in re.finditer(laws_full, doc, re.IGNORECASE):
        law_name = m.group(0)
        context = doc[m.start(0)-80:m.end(0)+80]
        info = extract_article.get_article(context,law_name)
        if info is None:
            continue
        lr = [id]
        lr.extend([info[key] if key in info else None for key in law_keys])
        law_references.append(lr)

    for m in re.finditer(laws_short, doc):
        law_name = m.group(0)
        context = doc[m.start(0)-80:m.end(0)+80]

        info = extract_article.get_article(context,law_name)
        if info is None:
            continue
        lr = [id]
        lr.extend([info[key] if key in info else None for key in law_keys])
        law_references.append(lr)

    return law_references

def results_to_csv(results, fname, more_results=None):
    selected_fields = []
    for r in tqdm.tqdm(results):
        selected_fields.append(extract_fields(r))

    if more_results:
        for r in tqdm.tqdm(more_results):
            selected_fields.append(extract_fields(r))

    df = pd.DataFrame(data=np.asarray(selected_fields), columns=selected_keys)
    df.to_csv(fname, index=False)

def results_to_csvs(results, more_results = None, collection=True, ECLI=True, law_references=True):
    print("Results to csv")
    if collection:
        results_to_csv(results, "documents.csv")

    references_db = []
    law_references_db = []

    for r in tqdm.tqdm(results):
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

    if more_results:
        for r in tqdm.tqdm(more_results):
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

    references_pd = pd.DataFrame(data=references_db, columns=['ID', 'SearchNumber', 'References', 'Counts'])
    references_pd.to_csv('references.csv')

    lr_pd = pd.DataFrame(data=law_references_db, columns=['ID', 'wetboek', 'bwnummer', 'artikel', 'lid'])
    lr_pd.to_csv("law_references.csv", index=None)

def main():
    solr = pysolr.Solr('http://localhost:8983/solr/Legal_Data')
    results = solr.search("*:*", rows=50000)


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