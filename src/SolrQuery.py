import pysolr
import numpy as np
import re

def extract_fields(result):
    procedure = result['ProcedureType']                 # String
    toplevelnavigation = result['TopLevelNavigation']   #

def main():
    solr = pysolr.Solr('http://localhost:8983/solr/Legal_Data')
    field = "TopLevelNavigation"
    results = solr.search("*:*", rows=1, fl=field)
    #for r in results:
    #    extract_fields(r)
    
    content = np.asarray([r[field][0] for r in results if field in r])
    un,c = np.unique(content, return_counts=True)
    sort = np.argsort(-c)
    for type, count in zip(un[sort], c[sort]):
        print("{0}: {1}".format(type, count))

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
