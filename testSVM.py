import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import StratifiedKFold
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV

#Load the data
data = np.load('X_workersupply.npy')
targets = np.load('Y_workersupply.npy')
X_train, X_test, Y_train, Y_test = train_test_split(data, targets,
                                                    test_size=0.2,
                                                    random_state=0)
                                                    
#Scale the data
scl = StandardScaler() 
X_train = scl.fit_transform(X_train)
X_test = scl.transform(X_test)

#Cross-validation 
cv = StratifiedKFold(Y_train, n_folds=4)

#Fit hyper-parameters
gamma_range = 10.0**np.arange(-3,3)
C_range = 10.0**np.arange(-3,3)
parameters = {"gamma" : gamma_range, "C": C_range}
grid = GridSearchCV(SVC(), param_grid = parameters, cv=cv, verbose = True)

#Fit to the training data
grid.fit(X_train, Y_train)

#Evaluate 
print "SVM classifier with RBF Kernel"
print "Best hyper-parameters:", grid.best_params_
print "Accuracy on training set:", grid.score(X_train, Y_train)
print "Accuracy on test set:", grid.score(X_test, Y_test)