#AISC2: Machine Learning over Starcraft II Files
================================================
### Authors: Henry Tay, Jesse Watts-Russell

Our AI final project that uses Support Vector Machines to learn over characteristics of Starcraft II (in replay files) to classify things such as player race and win/loss.

## Files to note:
1. The scripts that parse the replay files are labeled with the suffix Parser (except for eventParser). These scripts load the replay files using  the sc2reader library and save the data into a numpy array file. 
2. Training, classification, and evaluation is done within the testSVM.py script. These scripts extensively use pre-built functions from thesci-kit learn library. SVM hyper-parameters are fit using grid-search and validation accuracy is evaluating using stratified k-fold cross validation.
3. gamelog is the class that performs vectorization. 
4. eventParser is a class that performs the mapping of actions to action classes during feature extraction. 

