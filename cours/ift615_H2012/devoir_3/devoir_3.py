# -*- coding: utf-8 -*-

from numpy import *
from pylab import *
import cPickle,sys

def save(p, filename):
    """
    Pickles object ``p`` and saves it to file ``filename``.
    """
    f=file(filename,'wb')
    cPickle.dump(p,f,cPickle.HIGHEST_PROTOCOL) 
    f.close()

def load(filename): 
    """
    Loads pickled object in file ``filename``.
    """
    f=file(filename,'rb')
    y=cPickle.load(f)
    f.close()
    return y

def show_ocr_letter(x,with_grid=True):
    imshow(x.reshape(16,8),cmap = cm.Greys, interpolation='nearest')
    if with_grid:
        xlim(-0.5,7.5)
        ylim(15.5,-0.5)
        grid(True)
        xticks(arange(0.5,8.5,1))
        yticks(arange(0.5,16.5,1))
    else:
        xticks([])
        yticks([])


##############################
# Execution en tant que script
##############################

def main():
    usage = """Usage: python devoir_3.py"""
    if len(sys.argv) > 1:
        print usage
        return

    import solution


    X,Y = load('train.pkl')
    X_test, Y_test = load('test.pkl')

    N = 5
    alpha = 0.1
    
    perceptron = solution.Perceptron(alpha,N)
    perceptron.initialisation(zeros((128,)),1)
    perceptron.entrainement(X,Y)
    
    # Calculer les erreurs de classification
    erreur_train = mean([ y != perceptron.prediction(x) for x,y in zip(X,Y)])
    print 'Erreur de classification sur ensemble d\'entraînement:',str(erreur_train*100)+'%'
    
    erreur_test = mean([ y != perceptron.prediction(x) for x,y in zip(X_test,Y_test)])
    print 'Erreur de classification sur ensemble de test:',str(erreur_test*100)+'%'

    wb = perceptron.parametres()
    w,b = wb
    w_attendu,b_attendu = load('parametres_attendus.pkl')

    print 'Différence entre le w trouvé et celui attendu:',((w_attendu-w)**2).sum()
    print 'Différence entre le b trouvé et celui attendu:',((b_attendu-b)**2)

    # Visualisation des prédictions sur l'ensemble de test
    n_test = len(X_test)
    grid_size = (4,5)
    i = 0
    for x,y in zip(X_test,Y_test):
        y_pred = perceptron.prediction(x)
        subplot(grid_size[0],grid_size[1],i+1)
        subplots_adjust(hspace=0.5)
        show_ocr_letter(x,False)
        title('y='+str(y)+u', h(x)='+str(y_pred))
        i+=1
    show()

if __name__ == "__main__":
    main()
