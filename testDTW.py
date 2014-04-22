#testDTW.py
#Author: Henry Tay and Jesse Watts-Russell
#Dynamic time warping code adapted from StackOverFlow : Stefan Novak

#Overview: Using K-Nearest-Neighbors with a dynamic time warping similarity
#measure. 

#For dynamic time warping
import numpy as np
import rpy2.robjects.numpy2ri
from rpy2.robjects.packages import importr

#For learning
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import StratifiedKFold
from sklearn.grid_search import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier

# Set up R namespaces
R = rpy2.robjects.r
DTW = importr('dtw')

# Generate the data
idx = np.linspace(0, 2*np.pi, 100)
template = np.cos(idx)
query = np.sin(idx) + np.array(R.runif(100))/10

# Calculate the alignment vector and corresponding distance
alignment = R.dtw(query, template, keep=True)
dist = alignment.rx('distance')[0][0]

print(dist)