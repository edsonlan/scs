
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import randint



import pandas as pd
import sys
import numpy as np

def main():
    file_path= sys.argv[1]
    
    dataframe = pd.read_csv(file_path,sep=";",low_memory=False)
    
    
    dataframe['classe_solos_nivel_1']= dataframe["classe_solos_nivel_1"].astype("category")
    
    X = dataframe.drop('classe_solos_nivel_1',axis=1)
    y = dataframe["classe_solos_nivel_1"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
    rf = RandomForestClassifier()
          
    param_dist = {'n_estimators': randint(50,500),
              'max_depth': randint(1,20)}

    rf = RandomForestClassifier()

    rand_search = RandomizedSearchCV(rf, 
                                     param_distributions = param_dist, 
                                     n_iter=5, 
                                     cv=2)

    rand_search.fit(X_train, y_train)
    
    y_pred = rand_search.fit(X_test)
        
    print(pd.Series(rand_search.best_estimator_.feature_importances_,index=X_train.columns))
    
    print('Best hyperparameters:',  rand_search.best_params_)
    accuracy = accuracy_score(y_test, y_pred)
    
    print("Accuracy:", accuracy)
    

if __name__ == "__main__":
    main()