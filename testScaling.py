#testScaling.py
#Author: Henry Tay and Jesse Watts-Russell

#Overview: Control with no fit scaling to see how much scaling improves the
#performance of an SVM classifier 

import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import StratifiedKFold
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV


#Load the data
data = np.load('X_apm.npy')
targets = np.load('Y_apm.npy')
data = (data - np.min(data, 0)) / (np.max(data, 0) + 0.0001)  # 0-1 scaling
X_train, X_test, Y_train, Y_test = train_test_split(data, targets,
                                                    test_size=0.2,
                                                    random_state=0)
                                                    
#Models we will use
svc = SVC()

#Set values of hyper-parameters
C_range = 10.0 ** np.arange(-2, 2)
gamma_range = 10.0 ** np.arange(-2, 2)
parameters = {'C':C_range, 
              'gamma':gamma_range}
              
#Cross validation
cv = StratifiedKFold(Y_train, n_folds=3)

grid = GridSearchCV(svc, parameters, verbose=True, cv=cv)

#Train the the RBM-SVC Pipeline
grid.fit(X_train,Y_train)
