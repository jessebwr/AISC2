#testRBM.py
#Author: Henry Tay and Jesse Watts-Russell

#Overview: This is a script to test whether using  a restricted Boltzmann
#for feature transformation improves the performance of an SVM classifier on
#the APM data. 

import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import StratifiedKFold
from sklearn.svm import SVC
from sklearn.neural_network import BernoulliRBM
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV


#Load the data
data = np.load('X_apm.npy')
targets = np.load('Y_apm.npy')
data = (data - np.min(data, 0)) / (np.max(data, 0) + 0.0001)  # 0-1 scaling
X_train, X_test, Y_train, Y_test = train_test_split(data, targets,
                                                    test_size=0.2,
                                                    random_state=0)
                                                    
#Models we will use
scl = StandardScaler() 
svc = SVC()
rbm = BernoulliRBM(random_state=0, verbose=True)

clf = Pipeline(steps=[('scl', scl), ('rbm', rbm), ('svc', svc)])

#Set values of hyper-parameters
C_range = 10.0 ** np.arange(-2, 2)
gamma_range = 10.0 ** np.arange(-2, 2)
alpha_range = 2.0 ** np.arange(-5, -1) 
parameters = {'svc__C':C_range, 
              'svc__gamma':gamma_range, 
              'rbm__learning_rate':alpha_range}
grid = GridSearchCV(clf, parameters, verbose=True)

#Train the the RBM-SVC Pipeline
grid.fit(X_train,Y_train)
