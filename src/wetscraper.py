from lxml import html
import requests
import re
import pandas as pd

wetten = {'Arbeidsomstandighedenwet': 'arbeidsomstandighedenwet',
          'Algemene wet bestuursrecht': 'algemene-wet-bestuursrecht',
          'Boswet': 'boswet',
          'Burgerlijk wetboek 1': 'burgerlijk-wetboek-boek-1',
          'Burgerlijk wetboek 2': 'burgerlijk-wetboek-boek-2',
          'Burgerlijk wetboek 3': 'burgerlijk-wetboek-boek-3',
          'Burgerlijk wetboek 4': 'burgerlijk-wetboek-boek-4',
          'Burgerlijk wetboek 5': 'burgerlijk-wetboek-boek-5',
          'Burgerlijk wetboek 6': 'burgerlijk-wetboek-boek-6',
          'Burgerlijk wetboek 7': 'burgerlijk-wetboek-boek-7',
          'Burgerlijk wetboek 7a': 'burgerlijk-wetboek-boek-7a',
          'Burgerlijk wetboek 8': 'burgerlijk-wetboek-boek-8',
          'Burgerlijk wetboek 10': 'burgerlijk-wetboek-boek-10',
          'Grondwet': 'grondwet',
          'Opiumwet': 'opiumwet',
          'Leerplichtwet 1969': 'leerplichtwet-1969',
          'Participatiewet': 'participatiewet',
          'Warenwet': 'warenwet',
          'Wegenverkeerswet 1994': 'wegenverkeerswet-1994',
          'Werkloosheidswet': 'werkloosheidswet',
          'Wet algemene bepalingen omgevingsrecht': 'wet-algemene-bepalingen-omgevingsrecht',
          'Wet arbeidsongeschiktheidsverzekering zelfstandigen': 'wet-arbeidsongeschiktheidsverzekering-zelfstandigen',
          'Wet bescherming persoonsgegevens': 'wet-bescherming-persoonsgegevens',
          'Wetboek van Strafrecht': 'wetboek-van-strafrecht',
          'Wet bijzondere opnemingen in psychiatrische ziekenhuizen': 'wet-bijzondere-opnemingen-in-psychiatrische-ziekenhuizen',
          'Wet geluidhinder': 'wet-geluidhinder',
          'Wet inkomstenbelasting 2001': 'grondwet',
          'Wet op de arbeidsongeschiktheidsverzekering': 'wet-op-de-arbeidsongeschiktheidsverzekering',
          'Wet op de beroepen in de individuele gezondheidszorg': 'wet-op-de-beroepen-in-de-individuele-gezondheidszorg',
          'Wet op de inlichtingen- en veiligheidsdiensten 2002': 'wet-op-de-inlichtingen--en-veiligheidsdiensten-2002',
          'Wet op de lijkbezorging': 'wet-op-de-lijkbezorging',
          'Wet op de ondernemingsraden': 'Wet op de ondernemingsraden',
          'Wet op de vennootschapsbelasting 1969': 'wet-op-de-vennootschapsbelasting-1969',
          'Wet openbaarheid van bestuur': 'wet-openbaarheid-van-bestuur',
          'Wet op het financieel toezicht': 'wet-op-het-financieel-toezicht',
          'Wet wapens en munitie': 'wet-wapens-en-munitie',
          'Wet werk en inkomen naar arbeidsvermogen': 'wet-werk-en-inkomen-naar-arbeidsvermogen',
          'Winkeltijdenwet': 'winkeltijdenwet',
          'Zondagswet': 'zondagswet',}


def main():
    data = []
    for wet in wetten.keys():
        page = requests.get('http://maxius.nl/{wet}'.format(wet=wetten[wet]))
        tree = html.fromstring(page.content)
        artikelen = tree.xpath("//div[@class='artikel'] | //div[@class='lid'] | //div[@class='onderdeel'] | //div[@class='sub']")
        for artikel in artikelen:
            text = artikel.xpath('text()')
            text = ''.join(text)
            text = re.sub('  +', '', text)
            text = re.sub('\n', '', text)
            link = artikel.xpath('a[@href]/@href')
            link = link[0]
            if text != '':
                data.append((wet, link, text))
    df = pd.DataFrame(data, columns=['wet', 'link', 'text'])
    df.to_csv('../data/wetboekenteksten.csv', sep=',', index=False)

if __name__ == '__main__':
    main()