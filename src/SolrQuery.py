import pysolr
import numpy as np
import re
import pandas as pd
import datetime
import tqdm

import dateutil.parser

selected_keys = ['ID', 'ProcedureType', 'TopLevelNavigation', 'Authors', 'Classifications', 'LawArea', 'Sources', 'Topic', 'Summary_Text', 'Title_Text', 'timestamp', 'SearchNumber']

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
    result.extend(re.findall(ljn_re, doc))
    # result = re.findall(".{40}Wet[ b].{40}",doc,re.IGNORECASE)
    # result = re.findall(".{40}LJN.{40}", doc, re.IGNORECASE)
    # result = re.findall(laws_re, doc, re.IGNORECASE)
    if result and len(result) > 0:
        result = ["".join(r) for r in result]

        if ecli:
            result = [r for r in result if r != ecli]
        print(result)
        un, c = np.unique(np.asarray(result), return_counts=True)
        # result_c = []
        # for unique, count in zip(un, c):
        #    result_c.append((unique, count))
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


def extract_laws(doc):
    # Search for ECLI numbers
    re_full = re.compile(laws_full, re.IGNORECASE)
    re_short = re.compile(laws_short)
    #re_full = "\n.*({0}).*\n".format(laws_full)
    #print(re_full)
    #re_short = "\n.*({0}).*\n".format(laws_short)
    #print(re_short)
    #result = re.findall(re_full, doc, re.IGNORECASE)
    #result.extend(re.findall(re_short, doc))


    for m in re.finditer(laws_full, doc):
        law_name = m.group(0)
        context = doc[m.start(0)-80:m.end(0)+80]

    return None

    if result and len(result) > 0:
        #result_c = []
        #for unique, count in zip(un, c):
        #    result_c.append((unique, count))
        return result
    return None


def results_to_csv(results, fname):
    selected_fields = []
    for r in results:
        selected_fields.append(extract_fields(r))

    df = pd.DataFrame(data=np.asarray(selected_fields), columns=selected_keys)
    df.to_csv(fname, index=False)


def main():
    solr = pysolr.Solr('http://localhost:8983/solr/Legal_Data')
    # field = "SearchNumber"
    results = solr.search("*:*", rows=50000)
    # results_to_csv(results, "documents.csv")
    """
    law_references = []

    for r in tqdm.tqdm(results):
        results_laws = extract_laws(r['Text_Text_1'])
        if results_laws is not None:
            law_references.extend(results_laws)
            print(results_laws)

    #un, counts = np.unique(np.asarray(law_references), return_counts=True)
    #sort = np.argsort(-counts)
    #for u, c in zip(un[sort], counts[sort]):
    #    print("{0}: {1}".format(u, c))

    """

    references_db = []
    
    for r in tqdm.tqdm(results):
        ecli = r['SearchNumber'] if 'SearchNumber' in r else None
        references, counts = extract_references(r['Text_Text_1'], ecli)
        if references is not None and len(references) > 0:
            for ref, c in  zip(references, counts):
                references_db.append([r['ID'], ecli, ref, c])
    
    #df = pd.DataFrame(data=references_db, columns=['ID','SearchNumber','References','Counts'])
    #df.to_csv("references.csv", index=False)

    # content = np.asarray([r[field] for r in results if field in r])
    # un,c = np.unique(content, return_counts=True)
    # sort = np.argsort(-c)
    # for type, count in zip(un[sort], c[sort]):
    #    print("{0}: {1}".format(type, count))


def get_article(input_sentence, wetboek):
    info = {}
    info['wetboek'] = wetboek
    wetboek = wetboek.lower()
    match = None
    if wetboek == 'bw' or wetboek == 'burgelijk wetboek':
        pattern = '([0-9]{1,2}a?A?):([0-9]{1,5}) (BW ?)?(Burgerlijk Wetboek ?)?(.{0,10}lid [0-9]{1,2})?'
        match = re.search(pattern, input_sentence)
        bwnummer, artikel, _, __, lid = match.groups()
        info['bwnummer'] = bwnummer
        info['artikel'] = artikel
        info['lid'] = lid
    elif wetboek == 'awb' or wetboek == 'algemene wet bestuursrecht':
        pattern = 'artikel ?([0-9]{1,3}:[0-9]{1,3})(, )?(.{1,15}lid)?(.{1,20})?(Awb|Algemene wet bestuursrecht)'
        match = re.search(pattern, input_sentence)
        artikel, _, lid, __, wb = match.groups()
        info['wetboek'] = wb
        info['artikel'] = artikel
        info['lid'] = lid
        info['bwnummer'] = None
    return info

if __name__ == '__main__':
    main()
