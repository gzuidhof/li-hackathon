import re
import datetime
from dateutil import parser as dateparser
from enum import IntEnum
import pprint


class IssuingInstanceType(IntEnum):
    Unknown = 0
    Gerechtshof = 1
    HogeRaad = 2

    @staticmethod
    def issuing_institution_to_type(issuing_institution):
        # TODO: remnants of hackathon code, may need to check
        if "hoge raad" in issuing_institution.lower():
            return IssuingInstanceType.HogeRaad
        elif "gerechtshof" in issuing_institution.lower():
            return IssuingInstanceType.Gerechtshof
        else:
            return IssuingInstanceType.Unknown



class SolrParser(object):
    selected_keys = ['ID', 'PublicationNumber', 'ProcedureType', 'TopLevelNavigation', 'Authors', 'Classifications',
                     'LawArea', 'Sources', 'Topic', 'Summary_Text', 'Title_Text', 'timestamp', 'SearchNumber']

    def __init__(self):
        pass

    def parse_solr_response(self, response, forward_references=True, include_bwb=True):
        # TODO: Check if this solr response is actually a response from term vector response handler (trvh)

        term_vectors = response['termVectors']
        solr_documents = response['response']['docs']

        """{'Authors': ['Onbekend'],
             'Classifications': ['Civiel recht'],
             'InstanceType': '2',
             'LawArea': ['Burgerlijk recht'],
             'PublicationNumber': 'ECLI:NL:PHR:2016:987',
             'SearchNumber': 'ECLI:NL:PHR:2016:987',
             'Sources': ['Rechtspraak.nl'],
             'Summary': 'CAO-recht. CAO Taxivervoer. Uitleg ‘pauzeregeling’. '
                        'Vaststellingsovereenkomst en dwingend recht (art. 7:902 BW). '
                        'Betekenis vaststellingsovereenkomst tussen werkgever en '
                        'oud-werknemers voor vordering van cao-partners tot naleving van '
                        'cao en betaling van boete (art. 15 Wet cao, art. 3 lid 4 Wet '
                        'AVV).',
             'Timestamp': 1496426613,
             'Title': 'CAO-recht. CAO Taxivervoer. Uitleg ‘pauzeregeling’. '
                      'Vaststellingsovereenkomst en dwingend recht (art. 7:902 BW). '
                      'Betekenis vaststellingsovereenkomst tussen werkgever en '
                      'oud-werknemers voor vordering van cao-partners tot naleving van cao '
                      'en betaling van boete (art. 15 Wet cao, art. 3 lid 4 Wet AVV).',
             'TopLevelNavigation': ['Nederland|Rechtspraak'],
             'Topic': ['Civiel recht'],
             'Verdict': 'False',
             'id': 22129570}
            """

        docs = []
        references = []
        for solr_doc in solr_documents:
            instance_type = IssuingInstanceType.issuing_institution_to_type(
                solr_doc['IssuingInstitution']) if 'IssuingInstitution' in solr_doc else IssuingInstanceType.Unknown

            verdict, verdict_text = SolrParser.get_verdict(instance_type, solr_doc['Text_Text_1'])
            pprint.pprint(sorted(list(solr_doc.keys())))
            doc = {
                'id': solr_doc['ID'],
                'InstanceType': instance_type,
                'Timestamp': solr_doc['PublicationDate'],
                'IssuingInstitution_Group': solr_doc['IssuingInstitution_Group']
            }

            if 'SearchNumber' in solr_doc and len(solr_doc['SearchNumber']) > 0:
                doc['SearchNumber'] = solr_doc['SearchNumber']
            elif 'PublicationNumber' in solr_doc:
                doc['SearchNumber'] = solr_doc['PublicationNumber']

            if 'Title_Text' in solr_doc:
                doc['Title'] = solr_doc['Title_Text']

            if 'Summary_Text' in solr_doc:
                doc['Summary'] = solr_doc['Summary_Text']

            for key in ['Authors', 'Classifications', 'LawArea', 'PublicationNumber', 'Sources', 'Topic',
                        'TopLevelNavigation']:
                if key in solr_doc:
                    doc[key] = solr_doc[key]

            if verdict is not None:
                doc['Verdict'] = verdict
            if verdict_text is not None:
                doc['VerdictText'] = verdict_text

            for id, term_vector in zip(term_vectors[::2], term_vectors[1::2]):
                if id == solr_doc['ID']:
                    r = self.parse_term_vectors(term_vector, include_bwb=include_bwb)
                    break

            doc['TermVector'] = r
            docs.append(doc)

            if forward_references:
                references.append(r)
        return docs, references

    @staticmethod
    def timestring_to_timestamp(timestring):
        time = dateparser.parse(timestring)
        time = time.replace(tzinfo=None)
        return int((time - datetime.datetime(1970, 1, 1)).total_seconds())

    @staticmethod
    def get_verdict(instance_type: IssuingInstanceType, text_body):
        """
        Get the verdict from a given text body using regex search.
        :param instance_type: IssuingInstanceType corresponding to this document
        :param text_body: str, Text containing the verdict at some location. Usually 'Text_Text_1'
        :return: Optional[bool], True if the instance agreed with the defendant, False if the instance agreed with the
                                 previous decision. None if the IssuingInstanceType is Unknown.
                 Optional[str], Verdict text, only returned when the IssuingInstanceType is Unknown.
        """
        # TODO: remnants of hackathon code, check validity

        if instance_type == IssuingInstanceType.HogeRaad or instance_type == IssuingInstanceType.Gerechtshof:
            regex = "(beslissing|conclusie).*(verwerp|verworp|verniet|bekrach).*(.)"
            match = re.search(regex, text_body, re.IGNORECASE)
            if match is not None:
                groups = match.groups()
                verdict = groups[1]
                if verdict.lower() == 'verniet':
                    # Het vonnis van de rechtbank is vernietigd (oftewel, hoger beroep was een succes)
                    return True, None
                elif verdict.lower() in {'verwerp', 'verworp', 'bekrach'}:
                    # Het vonnis van de rechtbank is bekrachtigd,
                    # of anders gezegd: het hoger beroep verworpen.
                    return False, None
            else:
                # No matches
                return None, None
        else:
            regex = "( beslissing:? )(?!.*beslissing:? de.*)(de.*)"
            match = re.search(regex, text_body, re.IGNORECASE)
            if match is not None:
                groups = match.groups()
                verdict = groups[1]
                # We don't know if the verdict was positive or negative, so just return the verdict text.
                return None, verdict
            else:
                return None, None

    def parse_term_vectors(self, term_vector, include_bwb=False):
        print("====== TERM VECTORS ======")
        for fieldname, terms in zip(term_vector[::2], term_vector[1::2]):
            if fieldname == 'Text_Text_2':
                # Remove [] items
                terms = list(filter(lambda x: isinstance(x, str), terms))
                eclis = set(filter(lambda x: x.lower().startswith('ecli:'), terms))
                if include_bwb:
                    bwbs = set(filter(lambda x: x.startswith('BWB'), terms))
                    relevant_terms = list(map(lambda x: x.upper(), eclis.union(bwbs)))
                else:
                    relevant_terms = list(map(lambda x: x.upper(), eclis))
                print(relevant_terms)
                return relevant_terms
        return []
