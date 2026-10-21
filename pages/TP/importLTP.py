import numpy as np
from lxml import etree

class ReadLTP():
    def __init__(self, nom, info=True):
        self.nom = nom

        # Ouverture du fichier
        with open( nom, encoding='utf16') as f:
            lignes = f.readlines()

        # Il faut ajouter des balises global, sinon Python ne le détecte pas comme un fichier XML lisible
        data = '<file>'+''.join(lignes)+'</file>'
        parser = etree.XMLParser(recover=True)
        tree = etree.fromstring(data, parser=parser)
    
        courbes = tree.find('BLOC-COURBES').find('LESCOURBES').find('C')
    
        self.courbes_data = []
        if info:
            print( 'Courbes disponibles :')
            print( f' num |   x   |   y' )
            print( '-'*26 )
        for i in range(len( courbes )):
            d = self.load_curve( courbes, i )
            xlabel = d['xlabel']
            ylabel = d['ylabel']
            if info:
                print( f'{i:4d} | {xlabel:5s} | {ylabel:10s}' )
            self.courbes_data.append( d )
            
    def courbe( self, i ):
        return self.courbes_data[i]

    def load_courbe_1D(self, curve):
        data_hex = curve.find('DONNEES').text
        label = curve.find('NOM').text
        data = np.frombuffer( bytes.fromhex(data_hex), dtype='>f8' )
        return data, label 
    
    def load_curve(self, courbes, i):
        C = courbes.getchildren()[i]
        x, xl = self.load_courbe_1D(C.find('DATAX').getchildren()[0])
        y, yl = self.load_courbe_1D(C.find('DATAY').getchildren()[0])
        return {'x':x, 'y':y, 'xlabel':xl, 'ylabel':yl}
