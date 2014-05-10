The scripts that parse the replay files are labeled with the suffix Parser (except for eventParser). These scripts load the replay files using 
the sc2reader library and save the data into a numpy array file. 

Training, classification, and evaluation is done within the testSVM.py script. These scripts extensively use pre-built functions from the 
sci-kit learn library. SVM hyper-parameters are fit using grid-search and validation accuracy is evaluating using stratified k-fold cross validation.

gamelog is the class that performs vectorization. 

eventParser is a class that performs the mapping of actions to action classes during feature extraction. 