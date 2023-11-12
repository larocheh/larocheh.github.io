# -*- coding: utf-8 -*-

import copy, sys
import numpy as np
from string import Template

def joueur_humain(etat,transitions,but,joueur):
    
    actions_str = '; '.join([ a.__str__() for a in transitions(etat).keys()])
    action = raw_input('Entrer un choix d\'action puis appuyer sur Enter.\nChoisir parmi: {'+actions_str+'}\n')
    while True:
        try:
            exec 'action_ret = ' + action
            transitions(etat)[action_ret]
            break
        except:
            action = raw_input('L\'action n\'est pas valide. Réessayer à nouveau, puis appuyer sur Enter\n')
    return action_ret

def joueur_aleatoire(etat,transitions,but,joueur):
    actions = transitions(etat).keys()
    return actions[np.random.randint(len(actions))]


class Jeu:
    """
    Classe de jeu.
    
    Initialize à partir de la fonction but,
    fonction transitions et l'état inital du jeu.
    
    La méthode "jouer_partie" simule une partie 
    où un joueur Max (les 'X') et un joueur Min (les 'O')
    s'affrontent.
    """
    def __init__(self,but,transitions,etat_initial):
        self.but = but
        self.transitions = transitions
        self.etat_initial = etat_initial

    def print_message(self,resultat):
        if resultat > 0:
            print 'Joueur X a gagné'
        elif resultat == 0:
            print 'Partie nulle'
        else:
            print 'Joueur O a gagné'

    def jouer_partie(self,joueur_max, joueur_min):
        etat = copy.deepcopy(self.etat_initial)
        print etat
        while True:
            action = joueur_max(copy.deepcopy(etat),self.transitions,self.but,'X')
            etat = self.transitions(etat)[action]
            print etat
            resultat = self.but(etat)
            if resultat is not None:
                self.print_message(resultat)
                break
            action = joueur_min(copy.deepcopy(etat),self.transitions,self.but,'O')
            etat = self.transitions(etat)[action]
            print etat
            resultat = self.but(etat)
            if resultat is not None:
                self.print_message(resultat)
                break

##############################################
# Etat, transitions et but pour le tic-tac-toe
##############################################

class TicTacToeEtat:

    def __init__(self):
        self.tableau = np.array([ [' ',' ',' '],
                                  [' ',' ',' '],
                                  [' ',' ',' '] ])

    def __str__(self):
        t = Template("""
   0   1   2
     |   |   
0  $a | $b | $c
     |   |   
  ---+---+---
     |   |   
1  $d | $e | $f
     |   |
  ---+---+---
     |   |   
2  $g | $h | $i
     |   |
""")
        return t.substitute(a=self.tableau[0,0],b=self.tableau[0,1],c=self.tableau[0,2],
                            d=self.tableau[1,0],e=self.tableau[1,1],f=self.tableau[1,2],
                            g=self.tableau[2,0],h=self.tableau[2,1],i=self.tableau[2,2])

def tic_tac_toe_transitions(etat):
    # Determiner c'est le tour à qui
    if np.sum(etat.tableau == 'X') > np.sum(etat.tableau == 'O'):
        # Tour de O
        symbol = 'O'
    else:
        # Tour de X
        symbol = 'X'
    positions_vides = np.nonzero(etat.tableau == ' ')
    actions = {}
    for i,j in zip(positions_vides[0],positions_vides[1]):
        nouvel_etat = copy.deepcopy(etat)
        nouvel_etat.tableau[i,j] = symbol
        actions[(i,j)] = nouvel_etat
    return actions

def tic_tac_toe_but(etat):
    # Vérifie si X a gagné
    X_gagne = False
    X_gagne |= etat.tableau[0,0] == 'X' and etat.tableau[0,1] == 'X' and etat.tableau[0,2] == 'X' 
    X_gagne |= etat.tableau[1,0] == 'X' and etat.tableau[1,1] == 'X' and etat.tableau[1,2] == 'X' 
    X_gagne |= etat.tableau[2,0] == 'X' and etat.tableau[2,1] == 'X' and etat.tableau[2,2] == 'X' 
    X_gagne |= etat.tableau[0,0] == 'X' and etat.tableau[1,0] == 'X' and etat.tableau[2,0] == 'X' 
    X_gagne |= etat.tableau[0,1] == 'X' and etat.tableau[1,1] == 'X' and etat.tableau[2,1] == 'X' 
    X_gagne |= etat.tableau[0,2] == 'X' and etat.tableau[1,2] == 'X' and etat.tableau[2,2] == 'X' 
    X_gagne |= etat.tableau[0,0] == 'X' and etat.tableau[1,1] == 'X' and etat.tableau[2,2] == 'X' 
    X_gagne |= etat.tableau[0,2] == 'X' and etat.tableau[1,1] == 'X' and etat.tableau[2,0] == 'X' 
    if X_gagne:
        return 100000+np.sum(etat.tableau == ' ')

    # Vérifie si O a gagné
    O_gagne = False
    O_gagne |= etat.tableau[0,0] == 'O' and etat.tableau[0,1] == 'O' and etat.tableau[0,2] == 'O' 
    O_gagne |= etat.tableau[1,0] == 'O' and etat.tableau[1,1] == 'O' and etat.tableau[1,2] == 'O' 
    O_gagne |= etat.tableau[2,0] == 'O' and etat.tableau[2,1] == 'O' and etat.tableau[2,2] == 'O' 
    O_gagne |= etat.tableau[0,0] == 'O' and etat.tableau[1,0] == 'O' and etat.tableau[2,0] == 'O' 
    O_gagne |= etat.tableau[0,1] == 'O' and etat.tableau[1,1] == 'O' and etat.tableau[2,1] == 'O' 
    O_gagne |= etat.tableau[0,2] == 'O' and etat.tableau[1,2] == 'O' and etat.tableau[2,2] == 'O' 
    O_gagne |= etat.tableau[0,0] == 'O' and etat.tableau[1,1] == 'O' and etat.tableau[2,2] == 'O' 
    O_gagne |= etat.tableau[0,2] == 'O' and etat.tableau[1,1] == 'O' and etat.tableau[2,0] == 'O' 
    if O_gagne:
        return -100000-np.sum(etat.tableau == ' ')

    # Vérifie si c'est une partie nulle
    if np.sum(etat.tableau != ' ') == 9:
        return 0
    return None

###########################################
# Etat, transitions et but pour le Connect4
###########################################

class Connect4Etat:

    def __init__(self):
        self.n_colonnes = 8
        self.n_rangees = 6
        self.tableau = np.array([[' ']*self.n_colonnes]*self.n_rangees)

    def __str__(self):
        ret = ''
        for i,r in enumerate(self.tableau):
            ret += '|'+'|'.join(r)+'|\n'
        ret += '-'*(2*self.n_colonnes+1)+'\n'
        ret += ' '+' '.join([str(i) for i in range(self.n_colonnes)])+'\n'
        return ret

def connect4_transitions(etat):
    # Determiner c'est le tour à qui
    if np.sum(etat.tableau == 'X') > np.sum(etat.tableau == 'O'):
        # Tour de O
        symbol = 'O'
    else:
        # Tour de X
        symbol = 'X'

    actions = {}
    for i in range(etat.n_colonnes):
        try:
            rangee_pour_i = np.nonzero(etat.tableau.T[i] == ' ')[0].max()
            nouvel_etat = copy.deepcopy(etat)
            nouvel_etat.tableau[rangee_pour_i,i] = symbol
            actions[i] = nouvel_etat
        except:
            pass
    return actions

def connect4_but(etat):
    def symbol_gagne(symbol):
        gagne = False
        #for i in range(etat.n_rangees):
        #    for j in range(etat.n_colonnes):
        if np.sum(etat.tableau==symbol) == 0:
            return False
        x,y = np.nonzero(etat.tableau==symbol)
        for i,j in zip(x,y):
                # Vérifie 4 pareil sur une rangée...
                gagne |= np.sum(etat.tableau[i,j:j+4] == symbol) == 4
                # ... sur une colonne
                gagne |= np.sum(etat.tableau[i:i+4,j] == symbol) == 4
                # ... sur une diagonale gauche-droite
                gagne |= np.sum(np.diag(etat.tableau[i:i+4,j:j+4]) == symbol) == 4
                # ... sur une diagonale droite-gauche
                gagne |= np.sum(np.diag(etat.tableau[i-4+1:i+1,j:j+4][::-1]) == symbol) == 4
                if gagne:
                    return gagne
        return gagne

    # Vérifie si X a gagné
    X_gagne = symbol_gagne('X')
    if X_gagne:
        return 100000+np.sum(etat.tableau == ' ')

    # Vérifie si O a gagné
    O_gagne = symbol_gagne('O')    
    if O_gagne:
        return -100000-np.sum(etat.tableau == ' ')

    # Vérifie si c'est une partie nulle
    if np.sum(etat.tableau != ' ') == etat.n_colonnes*etat.n_rangees:
        return 0
    return None

##############################
# Execution en tant que script
##############################

def main():
    usage = """Usage: python devoir_1.py jeu adversaire

où "jeu" est "tic-tac-toe" ou "connect4"
et "adversaire" est "humain", "soi-meme" ou "aleatoire"."""

    if len(sys.argv) != 3:
        print usage
        return None
    else:
        jeu = sys.argv[1]
        adversaire = sys.argv[2]
        
    if adversaire not in ['aleatoire','humain','soi-meme']:
        print usage
        return None

    if jeu == 'tic-tac-toe':
        # Jouer une partie de tic-tac-toe
        tic_tac_toe = Jeu(tic_tac_toe_but,
                          tic_tac_toe_transitions,
                          TicTacToeEtat())
        
        import solution
        
        if adversaire == 'aleatoire':
            # Pour jouer contre un joueur aleatoire
            tic_tac_toe.jouer_partie(solution.joueur_alpha_beta_tic_tac_toe,joueur_aleatoire)
        
        if adversaire == 'humain':
            # Pour jouer contre un joueur humain
            tic_tac_toe.jouer_partie(solution.joueur_alpha_beta_tic_tac_toe,joueur_humain)
        
        if adversaire == 'soi-meme':
            # Pour joueur contre sa propre solution
            tic_tac_toe.jouer_partie(solution.joueur_alpha_beta_tic_tac_toe,solution.joueur_alpha_beta_tic_tac_toe)

    elif jeu == 'connect4':
        # Jouer une partie de tic-tac-toe
        connect4 = Jeu(connect4_but,
                       connect4_transitions,
                       Connect4Etat())
                                     
        import solution
        
        temps_maximal = 10
        def joueur_alpha_beta(etat,transitions,but,joueur):
            return solution.joueur_alpha_beta_connect4(etat,transitions,but,joueur,temps_maximal)

        if adversaire == 'aleatoire':
            # Pour jouer contre un joueur aleatoire
            connect4.jouer_partie(joueur_alpha_beta,joueur_aleatoire)
        
        if adversaire == 'humain':
            # Pour jouer contre un joueur humain
            connect4.jouer_partie(joueur_alpha_beta,joueur_humain)
        
        if adversaire == 'soi-meme':
            # Pour joueur contre sa propre solution
            connect4.jouer_partie(joueur_alpha_beta,joueur_alpha_beta)
        
    else:
        print 'Jeu',jeu,'n\'est pas reconnu'

if __name__ == "__main__":
    main()
