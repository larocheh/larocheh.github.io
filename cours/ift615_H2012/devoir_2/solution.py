# -*- coding: utf-8 -*-

import numpy as np
import copy

class ReseauBayesien:
    
    def __init__(self, noeuds):
        self.noeuds = noeuds
        
        # Ordonner les noeuds
        domaines_des_noeuds = {}
        ordre_noeuds = []
        while len(self.noeuds) > 0:
            no = self.noeuds[0]
            self.noeuds = self.noeuds[1:]
            domaines_des_noeuds[no.variable] = no.domaine
            dans_ordre_noeuds = False
            if len(no.p_variable_etant_donnes_parents.shape) == 1:
                # Noeud n'a pas de parent
                ordre_noeuds = [no] + ordre_noeuds
                dans_ordre_noeuds = True
            else:
                parents = copy.copy(no.parents)
                for i in range(len(ordre_noeuds)):
                    autre_no = ordre_noeuds[i]
                    if autre_no.variable in parents:
                        parents.remove(autre_no.variable)
                    if len(parents) == 0:
                        # Peut insérer ce noeud
                        ordre_noeuds.append(no)
                        dans_ordre_noeuds = True
                        break

            if not dans_ordre_noeuds:
                self.noeuds.append(no)
                

        # Les noeuds sont dans le bon ordre
        self.noeuds = ordre_noeuds
        self.domaines_des_noeuds = domaines_des_noeuds

    def prob_conjointe(self,observations):
        ret = 1.0
        for n in self.noeuds:
            e = (observations[n.variable],) + tuple( [observations[ei] for ei in n.parents] )
            ret *= n.p_variable_etant_donnes_parents[e]
        return ret

    def p_exacte(self, variable_requete, observations):
        domaine_variable_requete = self.domaines_des_noeuds[variable_requete]
        p = np.zeros((len(domaine_variable_requete)))

        for i in xrange(len(domaine_variable_requete)):
            val_requete = domaine_variable_requete[i]
            observations[variable_requete] = val_requete
            p[i] = self.p_exacte_recursive(copy.copy(self.noeuds),observations)
            del observations[variable_requete]
        return p/p.sum()

    def p_exacte_recursive(self, noeuds, observations):
        if len(noeuds) == 0:
            return 1.
        no = noeuds[0]
        noeuds = noeuds[1:]
        if no.variable in observations:
            e = (observations[no.variable],) + tuple( [observations[ei] for ei in no.parents] )
            return no.p_variable_etant_donnes_parents[e] * self.p_exacte_recursive(noeuds, observations)
        else:
            somme = 0
            for v in no.domaine:
                observations[no.variable] = v
                e = (observations[no.variable],) + tuple( [observations[ei] for ei in no.parents] )
                somme += no.p_variable_etant_donnes_parents[e] * self.p_exacte_recursive(noeuds, observations)
                del observations[no.variable]
            return somme

    def p_echantillonnage_direct(self, variable_requete,observations, 
                                 n_echantillons, rng):
        domaine_variable_requete = self.domaines_des_noeuds[variable_requete]
        p = np.zeros((len(domaine_variable_requete)))
        for i in xrange(n_echantillons):
            echantillon = self.echantillon(rng)
            for k,v in observations.items():
                if echantillon[k] != v:
                    break
            else:
                p[echantillon[variable_requete]] += 1
        return p/p.sum()
        

    def echantillon(self, rng):
        sample = {}
        for no in self.noeuds:
            parents = tuple( [sample[ei] for ei in no.parents] )
            sample[no.variable] = no.sample(parents,rng)

        return sample
