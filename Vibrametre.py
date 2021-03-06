# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 14:40:01 2017

@author: Christophe
"""

from oscillo import *
from curseurs import *

class ShowVibra(Frame):
    """Démonstration de mouvements vibratoires harmoniques"""
    def __init__(self, boss =None):
        Frame.__init__(self)        # constructeur de la classe parente
        self.couleur = ['dark green', 'red', 'purple']
        self.trace = [0]*3          # liste des tracés (courbes à dessiner)
        self.controle = [0]*3       # liste des panneaux de contrôle

        # Instanciation du canevas avec axes X et Y : 
        self.gra = OscilloGraphe(self, larg =400, haut=200)
        self.gra.configure(bg ='white', bd=2, relief=SOLID)
        self.gra.pack(side =TOP, pady=5)

        # Instanciation de 3 panneaux de contrôle (curseurs) : 
        for i in range(3):
            self.controle[i] = ChoixVibra(self, self.couleur[i])
            self.controle[i].pack()

        # Désignation de l'événement qui déclenche l'affichage des tracés :    
        self.master.bind('<Control-Z>', self.montreCourbes)
        self.master.title('Mouvements vibratoires harmoniques')
        self.pack()
        
    def montreCourbes(self, event):
        """(Ré)Affichage des trois graphiques élongation/temps"""   
        for i in range(3):

            # D'abord, effacer le tracé précédent (éventuel) :
            self.gra.delete(self.trace[i])

            # Ensuite, dessiner le nouveau tracé :  
            if self.controle[i].chk.get():
                self.trace[i] = self.gra.traceCourbe(
                                    coul = self.couleur[i],
                                    freq = self.controle[i].freq,
                                    phase = self.controle[i].phase,
                                    ampl = self.controle[i].ampl)                    
            
#### Code pour tester la classe : ###
        
if __name__ == '__main__':    
    ShowVibra().mainloop()