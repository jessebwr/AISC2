#testkNN.py
#Author: Henry Tay and Jesse Watts-Russell

#Overview: Testing the performance of a k-Nearest-Neighbors classification 
#model to the APM data

import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.grid_search import GridSearchCV

#Load the data
data = np.load('X_apm.npy')
targets = np.load('Y_apm.npy')
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
k_range = [2 + i for i in range(10)]
parameters = {"n_neighbors" : k_range}
knn_uniform = KNeighborsClassifier(weights='uniform')
knn_distance = KNeighborsClassifier(weights='distance')
grid_uniform = GridSearchCV(knn_uniform, parameters, verbose=True, cv=cv)
grid_distance = GridSearchCV(knn_distance, parameters, verbose=True, cv=cv)

#Fit to the training data
grid_uniform.fit(X_train, Y_train)
grid_distance.fit(X_train, Y_train)

#Evaluate 
print "k-Nearest-Neighbors with uniform weight"
print "Best hyper-parameters:", grid_uniform.best_params_
print "Accuracy on training set:", grid_uniform.score(X_train, Y_train)
print "Accuracy on test set:", grid_uniform.score(X_test, Y_test)
print "k-Nearest-Neighbors with distance weight"
print "Best hyper-parameters:", grid_distance.best_params_
print "Accuracy on training set:", grid_distance.score(X_train, Y_train)
print "Accuracy on test set:", grid_distance.score(X_test, Y_test)
