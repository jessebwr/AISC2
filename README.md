#AISC2: Machine Learning over Starcraft II Files
================================================
### Authors: Henry Tay, Jesse Watts-Russell

Our AI final project that uses Support Vector Machines to learn over characteristics of Starcraft II (in replay files) to classify things such as player race and win/loss.

## Files to note:
1. The scripts that parse the replay files are labeled with the suffix Parser (except for eventParser). These scripts load the replay files using  the sc2reader library and save the data into a numpy array file. 
2. Training, classification, and evaluation is done within the testSVM.py script. These scripts extensively use pre-built functions from thesci-kit learn library. SVM hyper-parameters are fit using grid-search and validation accuracy is evaluating using stratified k-fold cross validation.
3. gamelog is the class that performs vectorization. 
4. eventParser is a class that performs the mapping of actions to action classes during feature extraction. 

## Steps to use
The archive file comes with the datasets with different features already parsed into .npy files. Simply run the testSVM file to execute the script that trains and evaluates an SVM classifier on this data. In order to change the features used, change the file names in lines 9 and 10 of testSVM. The prefix X indicates the features and the prefix Y indicates the classes (targets). 

## Abbreviations
wl - win/loss
mm - micro/macro
ws - worker/supply 
5-32 - first five minutes of gameplay/32 frames per window

