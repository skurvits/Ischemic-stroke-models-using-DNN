#Import required dependencies 

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

from google.colab import files
from google.colab import drive

from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.metrics import plot_roc_curve
from sklearn.metrics import classification_report

from sklearn.inspection import permutation_importance

import pickle

#Parameters of the Random Forest model 
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(
    n_estimators=1800, #1800
    criterion='gini',
    max_depth=60,
    min_samples_split=3,#9
    min_samples_leaf=5, #2
    min_weight_fraction_leaf=0.0,
    max_features='sqrt',
    max_leaf_nodes=None,
    min_impurity_decrease=0.0,
    min_impurity_split=None,
    bootstrap=True,
    oob_score=False,
    n_jobs=-1,
    random_state=0,
    verbose=0,
    warm_start=False,
    class_weight='balanced'
)

#Test data ROC

filenames = ["FILENAME_HERE"]
for f in filenames:
  dataset = pd.read_csv(f + ".csv", sep=",")
  
#One-hot encoding for ICD-10 scores
  helper = pd.get_dummies(dataset.ICD10, dummy_na=True)
  dataset = pd.concat([dataset, helper], axis=1)

#Make test dataset of the size of 10%.
  dataset = dataset.drop(['s_code', 'id', 'time', 'ICD10', 'days_before'], axis=1)
  dataset = dataset.fillna(0)
  y = dataset['I63_CASE']
  X = dataset.drop(['I63_CASE', 'Unnamed: 0'], axis = 1)
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=54)


  classifier.fit(X_train, y_train)
  # save the model to disk
  cls_f = 'RF_Final_LOCF_model.sav'
  pickle.dump(classifier, open(cls_f, 'wb'))
  fig, ax = plt.subplots()
  viz = plot_roc_curve(classifier, X_test, y_test,
                         name='AUC of Test dataset',
                         alpha=0.8, lw=2, color='b', ax=ax)
  ax.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
        label='Chance', alpha=.8)
  ax.set(xlim=[-0.05, 1.05], ylim=[-0.05, 1.05],
       title="Receiver operating characteristic")
  ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
  plt.savefig("RF_LOCF_TEST_ROC_"+ str(f)+".png")
  plt.show()
  
  
#Feature importance
  
perm_importance = permutation_importance(classifier, X_test, y_test)
  
sorted_idx = clf.feature_importances_.argsort()[-20:]
plt.barh(dataset_RF.columns[sorted_idx], clf.feature_importances_[sorted_idx])
plt.xlabel("Random Forest Feature Importance")
plt.savefig("RF_LOCF_TOP20_features_TEST.png")
  
