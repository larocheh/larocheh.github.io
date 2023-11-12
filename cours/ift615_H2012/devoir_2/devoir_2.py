# -*- coding: utf-8 -*-

import copy, sys
import numpy as np
import random

class Noeud:
    
    def __init__(self, variable, domaine, parents,
                 p_variable_etant_donnes_parents):
        self.variable = variable
        self.domaine = domaine
        self.parents = parents
        self.p_variable_etant_donnes_parents = p_variable_etant_donnes_parents

    def sample(self, valeur_parents, rng):
        p = np.array([ 
                self.p_variable_etant_donnes_parents[(i,) + valeur_parents] 
                for i in self.domaine ])
        return rng.multinomial(1,p).argmax()

##############################
# Execution en tant que script
##############################

def main():
    usage = """Usage: python devoir_2.py"""
    if len(sys.argv) > 1:
        print usage
        return

    import solution

    ###################################################
    # Example du cours avec Cambriolage, Alarme, etc. #
    ###################################################
    C = Noeud('C',range(2),[],np.array([0.999,0.001]))
    S = Noeud('S',range(2),[],np.array([0.998,0.002]))
    A = Noeud('A',range(2),['S','C'],np.array([ [[0.999,0.001],
                                                 [0.71,0.29]],
                                                [[0.06,0.94],
                                                 [0.05,0.95]]]).T)
    J = Noeud('J',range(2),['A'],np.array([[0.95,0.05],
                                           [0.1,0.9]]).T)
    M = Noeud('M',range(2),['A'],np.array([[0.99,0.01],
                                           [0.3,0.7]]).T)

    rng = np.random.mtrand.RandomState(1234)
    noeuds = [C,S,A,J,M]
    random.shuffle(noeuds)

    RB = solution.ReseauBayesien(noeuds)
    p_enum = RB.p_exacte('C',{'J':1,'M':1})
    p_echan = RB.p_echantillonnage_direct('C',{'J':1,'M':1},10000,rng)

    print "Example du cours avec Cambriolage, Alarme, etc."
    print 'P(C=true|J=true,M=true) = ' + str(p_enum[1]) + ' (exacte), ',
    print str(p_echan[1]) + ' (échantillonnage)    [réponse=0.284171835364]'

    print 'P(C=false|J=true,M=true) = ' + str(p_enum[0]) + ' (exacte), ',
    print str(p_echan[0]) + ' (échantillonnage)   [réponse=0.715828164636]'

    ####################################
    # Example du cours avec F,M,H,O,T. #
    ####################################
    F = Noeud('F',range(2),[],np.array([0.8,0.2]))
    M = Noeud('M',range(2),[],np.array([0.5,0.5]))
    H = Noeud('H',range(2),['M','F'],np.array([ [[0.5,0.5],
                                                 [0.,1.]],
                                                [[0.99,0.01],
                                                 [0.98,0.02]]]).T)
    O = Noeud('O',range(2),[],np.array([0.4,0.6]))
    T = Noeud('T',range(2),['O','H'],np.array([ [[0.9,0.1],
                                                 [0.5,0.5]],
                                                [[0.5,0.5],
                                                 [0.,1.]]]).T)

    rng = np.random.mtrand.RandomState(1234)
    noeuds = [F,M,H,O,T]
    random.shuffle(noeuds)
    RB = solution.ReseauBayesien(noeuds)

    print ''
    print "Example du cours avec F,M,H,O,T"
    print 'P(T=true|F=false,M=true) = ' + str(RB.p_exacte('T',{'F':0,'M':1})[1]) + ' (exacte)' ,
    print str(RB.p_echantillonnage_direct('T',{'F':0,'M':1},1000,rng)[1]) + ' (échantillonnage)    [réponse=0.8]'
    print 'P(T=true|M=true) = ' + str(RB.p_exacte('T',{'M':1})[1])  + ' (exacte)' ,
    print str(RB.p_echantillonnage_direct('T',{'M':1},1000,rng)[1]) + ' (échantillonnage)        [réponse=0.70984]' 


if __name__ == "__main__":
    main()
