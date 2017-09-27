import pysolr
import numpy as np

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

if __name__ == '__main__':
    main()