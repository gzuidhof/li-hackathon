import re

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
        bwnummer, artikel, _, __, lid = match.groups()
        info['bwnummer'] = bwnummer
        info['artikel'] = artikel
        info['lid'] = lid
    elif wetboek.lower() == 'awb' or wetboek.lower() == 'algemene wet bestuursrecht':
        pattern = 'artikel ?([0-9]{1,3}:[0-9]{1,3})(, )?(.{1,15}lid)?(.{1,20})?(Awb|Algemene wet bestuursrecht)'
        match = re.search(pattern, input_sentence)
        artikel, _, lid, __, wb = match.groups()
        info['wetboek'] = wb
        info['artikel'] = artikel
        info['lid'] = lid
        info['bwnummer'] = None
    else:
        pattern = '(artikel ?(([1-9]{{0,3}})(.([1-9]{{1,3}}([a-z])?))))?(, )?(.{{0,10}}lid)?((, )(aanhef en )?onder ([a-z])?)?(,? van de ({}))'.format(wetboek)
        match = re.search(pattern, input_sentence)
        groups = match.groups()
        info['wetboek'] = wetboek
        info['artikel'] = groups[1]
        info['lid'] = groups[7]
        info['bwnummber'] = None

    info['lid'] = lid_conversion[info['lid']]
    return info
