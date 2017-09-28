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
        pattern = '(artikel ?[1-9]{{0,3}})(.([1-9]{{1,3}}([a-z])?))?(, )?(.{{0,10}}lid)?((, )(aanhef en )?onder ([a-z])?)?(,? van de {})'.format(wetboek)
        match = re.search(pattern, input_sentence)
        return match.groups()
    return info
