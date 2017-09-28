import re

wetboek_conversion = {
    'awbz': 'Algemene Wet Bijzondere Ziektekosten',
    'arbowet': 'Arbeidsomstandighedenwet',
    'bopz': 'Bijzonder Opnemingen Psychiatrische Ziekenhuis',
    'bw': 'Burgerlijk Wetboek',
    'ww': 'Werkeloosheidswet',
    'wabo': 'Wet algemene bepalingen omgevingsrecht',
    'waz': 'Wet ambulancezorg',
    'ib 2001': 'Wet inkomstenbelasting 2001',
    'wet mot': 'Wet melding ongebruikelijke transacties',
    'wat': 'Wet op de architectentitel',
    'wgbo': 'Wet op de Geneeskundige Behandelingsovereenkomst',
    'wiv': 'Wet op de inlichtingen- en veiligheidsdiensten',
    'wor': 'Wet op de ondernemingsraden',
    'wao': 'Wet op de arbeidsongeschiktheidsverzekering',
    'vpb 1969':'Wet op de vennootschapsbelasting 1969',
    'whw':'Wet op het hoger onderwijs en wetenschappelijk onderzoek',
    'wft':'Wet op het financieel toezicht',
    'wob': 'Wet openbaarheid van bestuur',
    'wp2000': 'Wet personenvervoer 2000',
    'wia': 'Wet werk en inkomen naar arbeidsvermogen'
}

lid_conversion = {
    'lid een' : 1,
    'lid twee' : 2,
    'lid drie' : 3,
    'lid vier' : 4,
    'lid vijf' : 5,
    'eerste lid' : 1,
    'tweede lid' : 2,
    'derde lid' : 3,
    'vierde lid' : 4,
    'vijfde lid' : 5,
    'zesde lid' : 6,
    'zevende lid' : 7,
    'achtste lid' : 8,
    'negende lid' : 9,
    'tiende lid' : 10,
    'elfde lid' : 11,
    'twaalfde lid' : 12,
    'dertiende lid' : 13,
    'veertiende lid' : 14,
    'vijftiende lid' : 15,
    'zestiende lid' : 16,
    'zeventiende lid' : 17,
    'achttiende lid' : 18,
    'negentiende lid' : 19,
    'twintigste lid' : 20,
    None : None
}

def get_article(input_sentence, wetboek):
    info = {}
    info['wetboek'] = wetboek
    match = None
    if wetboek.lower() == 'bw' or wetboek.lower() == 'burgelijk wetboek':
        pattern = '([0-9]{1,2}a?A?):([0-9]{1,5}) (BW ?)?(Burgerlijk Wetboek ?)?(.{0,10}lid [0-9]{1,2})?'
        match = re.search(pattern, input_sentence)
        if match is None:
            return None
        bwnummer, artikel, _, __, lid = match.groups()
        if artikel is None or len(artikel) == 0:
            return None
        info['bwnummer'] = bwnummer
        info['artikel'] = artikel
        info['lid'] = lid
    elif wetboek.lower() == 'awb' or wetboek.lower() == 'algemene wet bestuursrecht':
        pattern = 'artikel ?([0-9]{1,3}:[0-9]{1,3})(, )?(.{1,15}lid)?(.{1,20})?(Awb|Algemene wet bestuursrecht)'
        match = re.search(pattern, input_sentence)
        if match is None:
            return None
        artikel, _, lid, __, wb = match.groups()
        if artikel is None or len(artikel) == 0:
            return None
        info['wetboek'] = wb
        info['artikel'] = artikel
        info['lid'] = lid
        info['bwnummer'] = None
    else:
        pattern = '(artikel ?(([1-9]{{0,3}})(.([1-9]{{1,3}}([a-z])?))))?(, )?(.{{0,10}}lid)?((, )(aanhef en )?onder ([a-z])?)?(,? van de ({}))'.format(wetboek)
        match = re.search(pattern, input_sentence)
        if match is None:
            return None
        groups = match.groups()
        if groups[1] is None or len(groups[1]) == 0:
            return None
        info['wetboek'] = wetboek
        info['artikel'] = groups[1]
        info['lid'] = groups[7]
        info['bwnummber'] = None

    if info['lid'] in lid_conversion:
        info['lid'] = lid_conversion[info['lid']]

    if info['wetboek'].lower() in wetboek_conversion:
        info['wetboek'] = wetboek_conversion[info['wetboek'].lower()]
    return info
