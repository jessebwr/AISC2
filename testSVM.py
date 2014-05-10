import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import StratifiedKFold
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV

#Load the data
data = np.load('X_wl_ws_mm5-32.npy')
targets = np.load('Y_wl_ws_mm5-32.npy')

def toBoolean(race):
    """
    Changes a race represented by an integer (0, 1, or 2) to a vector of 
    booleans ((1,0,0), (0,1,0), or (0,0,1)). It makes more sense to change the
    representation of race from one dimensions to three dimensions (it makes
    no sense to think of the distance between two races on the same dimension).
    """
    if race == 0:
        return (1,0,0)
    elif race == 1:
        return (0,1,0)
    else:
        return (0,0,1)
newdata = []
for d in data:
    events_ws = d[:600]
    events_mm = d[600:1200]
    races = d[1200:]
    player1race, player2race = toBoolean(races[0]), toBoolean(races[1])
    newdata.append(np.concatenate((player1race, player2race, events_ws)))
data = np.array(newdata)

X_train, X_test, Y_train, Y_test = train_test_split(data, targets,
                                                    test_size=0.2,
                                                    random_state=42)
                                                    
#Scale the data
scl = StandardScaler() 
X_train = scl.fit_transform(X_train)
X_test = scl.transform(X_test)

#Cross-validation 
cv = StratifiedKFold(Y_train, n_folds=3)

#Fit hyper-parameters
gamma_range = 2.0**np.arange(-20,20)
C_range = 2.0**np.arange(-20,20)
parameters = {"gamma" : gamma_range, "C": C_range}
grid = GridSearchCV(SVC(), param_grid = parameters, cv=cv, verbose = True)

#Fit to the training data
grid.fit(X_train, Y_train)

#Evaluate 
print "SVM classifier with RBF Kernel"
print "Best hyper-parameters:", grid.best_params_
print "Accuracy on training set:", grid.score(X_train, Y_train)
print "Accuracy on test set:", grid.score(X_test, Y_test)

#Plot learning curve of the model
