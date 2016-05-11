import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import accuracy_score,make_scorer,f1_score,classification_report,average_precision_score
from sklearn.preprocessing import Normalizer,MinMaxScaler,StandardScaler,normalize
from sklearn.cross_validation import train_test_split
import multiprocessing
import datetime
from time import gmtime, strftime
from grid_search_funs import *

def print_log(log_str):
    
    log_file_name = "jvap_log.txt"
    
    with open(log_file_name, "a") as f:
        
        entry = strftime("%Y-%m-%d %H:%M:%S") + '\t' + str(log_str) + '\n'

        f.write(entry)

        print(entry[:-1])


df_x,df_y = get_data(1000)

df_x,df_y=remove_bad_rows(df_x,df_y) #drops rows with codej1=codej2, codej2=nan
df_x=drop_unneeded_cols(df_x) #drops unneeded cols
df_x=drop_dissent(df_x) #drops dissent, concur columns

print_log((df_x.shape, df_y.shape))

df_x=dummify(df_x)

#GET X, Y AS NUMPY ARRAYS

X = df_x.values
y = df_y.ix[:,0].values

#MAKE SURE Y LOOKS LIKE [1 1 1 ... 1 1] (SOMETIMES IT CAN STORE INDICES)

print_log((X.shape, y.shape))

print_log(X[:10])
print_log(y[:10])

#############################################
# Split into training and test set
#############################################

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#look at size of df_x and X to make sure you have enough RAM

print_log(df_x.info())
print_log(("Size of X in GB: ", (X.nbytes * 1.0)/(1024 * 1024 *1024))) #size of X in GB

#check sizes match

print_log((X_train.shape, y_train.shape))
print_log((X_test.shape, y_test.shape))

#DONT DO FOR RANDOM FOREST

# #############################################
# # Standard scale
# #############################################

# scaler = StandardScaler()
# scaler.fit(X_train)

# X_test = scaler.transform(X_test)


#DONT DO FOR RANDOM FOREST

# #############################################
# # Min-Max scale
# #############################################

# scaler = MinMaxScaler()
# scaler.fit(X_train)

# X_test = scaler.transform(X_test)


#############################################
# [OPTIONAL]
# Random Forest Grid Search
#############################################

num_cores = multiprocessing.cpu_count()

print "numcores = ", num_cores

#modify/add params here you want to search over
param_grid = {'n_estimators': [10, 50, 100, 150, 200], 'max_depth': [1, 5, 10, 15, 20, 25]}


rf_clf = RandomForestClassifier(random_state=42)

gridclf = grid_search(X=X_train, y=y_train, clf=rf_clf, param_grid=param_grid, n_jobs=num_cores)

print_log(gridclf.best_params_)
print_log(gridclf.best_score_)


#############################################
# [OPTIONAL] Random Forest (RUN OVER BEST MODEL FROM GRID SEARCH)
#############################################

# Replace labels (in case SVM was run)
# y_train[y_train == 0.] = -1.
# y_test[y_test == 0.] = -1.


rf_clf = RandomForestClassifier(random_state=42, **gridclf.best_params_)
#                                 class_weight={1.0: 1, -1.0: 150})

rf_clf.fit(X_train, y_train)

y_pred = rf_clf.predict(X_test)

print_log(classification_report(y_test, y_pred))

#############################################
# [OPTIONAL]
# Feature importance analysis
#############################################

top_n = get_top_n_feats(25, rf_clf.feature_importances_, df_x.columns)

for t in top_n:
    print_log(t)
