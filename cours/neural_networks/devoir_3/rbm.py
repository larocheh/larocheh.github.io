import numpy as np
import mlpython.learners.generic as mlgen 
import mlpython.learners.classification as mlclass
import mlpython.mlproblems.generic as mlpb 
import mlpython.mlproblems.classification as mlpbclass

class RBM(mlgen.Learner):
    """
    Restricted Boltzmann Machine trained with unsupervised learning.

    Option ``lr`` is the learning rate.

    Option ``hidden_size`` is the size of the hidden layer.

    Option ``CDk`` is the number of Gibbs sampling steps used
    by contrastive divergence.

    Option ``seed`` is the seed of the random number generator.
    
    Option ``n_epochs`` number of training epochs.
    """

    def __init__(self, 
                 lr,             # learning rate
                 hidden_size,    # hidden layer size
                 CDk=1,          # nb. of Gibbs sampling steps
                 seed=1234,      # seed for random number generator
                 n_epochs=10     # nb. of training iterations
                 ):
        self.n_epochs = n_epochs
        self.hidden_size = hidden_size
        self.lr = lr
        self.CDk = CDk
        self.seed = seed
        self.rng = np.random.mtrand.RandomState(self.seed)   # create random number generator

    def train(self,trainset):
        """
        Train RBM for ``self.n_epochs`` iterations.
        """
        # Initialize parameters
        input_size = trainset.metadata['input_size']

        # Parameter initialization
        self.W = (self.rng.rand(input_size,self.hidden_size)-0.5)/(max(input_size,self.hidden_size))
        self.b = np.zeros((self.hidden_size,))
        self.c = np.zeros((input_size,))
        
        for it in range(self.n_epochs):
            for input in trainset:
                # Perform CD-k
                # - you must use the matrix self.W and the bias vectors self.b and self.c

                "PUT CODE HERE"

                
    def show_filters(self):
        from matplotlib.pylab import show, draw, ion
        import mlpython.misc.visualize as mlvis
        mlvis.show_filters(0.5*self.W.T,
                           200,
                           16,
                           8,
                           10,20,2)
        show()
