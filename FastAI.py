import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
import matplotlib.ticker as ticker

import fastbook

from google.colab import files

import keras
from keras.models import Sequential
from keras.layers import Activation, Dense

from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import classification_report

from fastai.basics import *
from fastai.tabular.all import *
from fastai.vision.all import *
from fastai.metrics import *
from fast_tabnet.core import *

#Test data ROC
lr_i = 0.05
filenames = ["FILENAME"]
for f in filenames:
  roc_value_fpr = []
  roc_value_tpr = []
  AUC_list = []
  print("Beginning of dataset: " + f)
  dataset = pd.read_csv(f + ".csv", sep=",")
  
  #Make test dataset of the size of 10%.
  dataset = dataset.drop(['s_code', 'id'], axis=1)
  y = dataset['I63_CASE']
  X = dataset.drop(['I63_CASE', 'Unnamed: 0'], axis = 1)
  X_train_valid, X_test, y_train_valid, y_test = train_test_split(
    X, y, test_size=0.1, random_state=54)

  data_training = pd.concat([X_train_valid, y_train_valid], axis=1)
  data_testing = pd.concat([X_test, y_test], axis =1)


  dataset_TabNet = data_training.fillna(0)

  y = dataset_TabNet['I63_CASE']
  X = dataset_TabNet.drop(['I63_CASE'], axis = 1)
  X = X.drop(['days_before'], axis = 1)
  X


  cont_names = dataset_TabNet.columns.values.tolist()
  cont_names.remove('I63_CASE')
  cont_names.remove('days_before')
  cont_names.remove('sex')
  cont_names.remove('ICD10')
  cont_names.remove('time')
  cat_names = ['sex', 'ICD10'] #FillMissing
  procs = [Categorify, Normalize]
  #####################

  fprs, tprs, scores = [], [], []
  
  dls = TabularDataLoaders.from_df(dataset_TabNet, y_names="I63_CASE",
    y_block = CategoryBlock,
    cat_names = cat_names,
    cont_names = cont_names,
    procs = procs, 
    bs = 2048)
  roc_auc = RocAucBinary()

  learn = tabular_learner(dls, layers=[500 , 1000], metrics=roc_auc, opt_func=Adam)
  learn.lr_find()
  learn.fit_one_cycle(45, lr_i, cbs=[ShowGraphCallback()]) #45
  

  tab_test = data_testing.fillna(0)
  dl = learn.dls.test_dl(tab_test)
  probs, preds = learn.get_preds(dl=dl)
  pickle.dump(probs, open("FastAI_LOCF_Probs_TEST", 'wb'))
  pickle.dump(preds, open("FastAI_LOCF_Preds_TEST", 'wb'))


  fpr, tpr, thresholds = roc_curve(y_test, probs[:,1], pos_label=1)
  AUC_list.append(auc(fpr, tpr))

  roc_value_fpr.append(fpr)
  roc_value_tpr.append(tpr)
  fig, ax = plt.subplots()
  plt.plot(roc_value_fpr[0], roc_value_tpr[0],alpha=0.7,color='b', label=str("AUC: " + str(round(AUC_list[0], 3)))) 

  ax.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
        label='Chance', alpha=.8)
  ax.set(xlim=[-0.05, 1.05], ylim=[-0.05, 1.05],
       title="Receiver operating characteristic")
  ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
  plt.ylabel("True Positive Rate")
  plt.xlabel("False Positive Rate")
  plt.savefig("FastAI_LOCF_TEST_"+ str(f)+".png", bbox_inches='tight')
  plt.show()
  learn.save("FastAI_LOCF_TEST")
