import extract_article as ga
output1 = ga.get_article('Met de rechtbank moet worden geoordeeld dat in de brief van 16 januari 2015 uitsluitend de ontvangst van een bezwaar van appellant wordt bevestigd en dat deze brief niet is gericht op enig rechtsgevolg. Van een besluit als bedoeld in artikel 1:3, eerste lid, van de Awb is dus geen sprake. Dat het college in de ontvangstbevestiging van 16 december 2015 een verkeerde datum heeft vermeld, die overigens kort daarna is hersteld, leidt niet tot een ander oordeel.', 'Awb')
output2 = ga.get_article('kracht - op de in artikel 1:401 Burgerlijk Wetboek (BW) vermelde gronden; dat beide partijen bij een dergelijk geschil er daarom belang bij hebben dat de vaststelling berust op een juiste en volledige waardering van de van belang zijnde omstandigheden ten tijde van de uitspraak in hoogste ressort, en dat onverkort vasthouden aan de regel dat de rechter geen acht hoort te slaan op grieven die na een verzoekschrift respectievelijk het verweerschrift in hoger beroep worden aangevoerd, daaraan in de weg kan staan.' ,'bw')
output3 = ga.get_article('Ingevolge artikel 2.12, tweede lid, van de Wabo kan, in afwijking van het eerste lid, aanhef en onder a, onder 3°, de vergunning, voor zover zij betrekking heeft op een activiteit voor een bepaalde termijn, worden verleend, indien de activiteit niet in strijd is met een goede ruimtelijke ordening.', 'Wabo')

print(output1)
print(output2)
print(output3)
