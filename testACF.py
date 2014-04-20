#testACF.py
#Author: Henry Tay and Jesse Watts-Russell

#Overview: This is a test to see if using an autocorrelation function as a
#feature vector improves the performance of an SVM classifier on the APM data.

import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import StratifiedKFold
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV

def acf(x,maxLag):
    """
    Returns the autocorrelation function of the time series x.
    """
    return [1]+[np.corrcoef(x[:-i], x[i:])[0,1] for i in range(1, maxLag)]
        
#Load the data
data = np.load('X_apm.npy')
targets = np.load('Y_apm.npy')

#Compute the acf of the data
X = [(acf(x, 50), targets[i]) for i, x in enumerate(data) \
                            if not np.isnan(sum(acf(x,50)))]
                            
targets = np.array([x[1] for x in X])
X_train, X_test, Y_train, Y_test = train_test_split(data, targets,
                                                    test_size=0.2,
                                                    random_state=43)
                                                    
                                                
#Use cross-validation to fit the hyper-parameters
C_range = 10.0 ** np.arange(-2, 2)
gamma_range = 10.0 ** np.arange(-2, 2)
cv = StratifiedKFold(y=Y_train, n_folds=3)
parameters = dict(gamma=gamma_range, C=C_range)                                    
grid = GridSearchCV(SVC(), parameters, cv=cv, verbose=True)
   
#Training the classifier              
grid.fit(X_train, Y_train)

#Evaluate the classifier on the test data
grid.score(X_test, Y_test)
