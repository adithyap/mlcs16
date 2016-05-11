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

#############################################
# PANDAS HELPERS
#############################################


def remove_column_from_data_frame(col_to_remove, data_frame):

    if col_to_remove in list(data_frame.columns):
        data_frame.drop(col_to_remove, axis=1, inplace=True)

        
def remove_columns_from_data_frame(cols_to_remove, data_frame):

    column_dict = {x: None for x in list(data_frame.columns)}

    cols_to_remove = [x for x in cols_to_remove if x in column_dict]

    data_frame.drop(labels=cols_to_remove, axis=1, inplace=True)
    

def remove_columns_like(column_pattern, data_frame):
    
    to_remove = [x for x in list(data_frame.columns) if column_pattern in x]

    return remove_columns_from_data_frame(to_remove, data_frame)


def fill_nas(value, data_frame):
    
    data_frame.fillna(0, inplace=True)



#############################################
# DATA RETRIEVAL HELPERS
#############################################

def get_data(n_rows=None):
    
    if n_rows is not None:
        # df = pd.read_csv('final_feats_without_dummies_3.csv', low_memory=False, nrows=n_rows)
        df = pd.read_csv('final_feats_4.csv', low_memory=False, nrows=n_rows)
        df_y = pd.read_csv('final_outs_3.csv', low_memory=False, nrows=n_rows)
    else:
        # df = pd.read_csv('final_feats_without_dummies_3.csv', low_memory=False)
        df = pd.read_csv('final_feats_4.csv', low_memory=False)
        df_y = pd.read_csv('final_outs_3.csv', low_memory=False)
    
    
    # Drop labels and a redundant column
    # remove_columns_from_data_frame(['Unnamed: 0', 'Unnamed: 0.1' 'dissent', 'dissentdummy'], df)
    # df,df_y=remove_bad_rows(df,df_y)
    # df=drop_unneeded_cols(df)
    # df=drop_dissent(df)
    # df=dummify(df)
    
    # Extras -- for analysis
    # CASE 1: REMOVE TOP 2
    # CASE 2: REMOVE ALL 'DISS'

    remove_columns_like('Unnamed', df)
    
#     remove_columns_from_data_frame(['type', 'turnonthresh'], df)
#     remove_columns_from_data_frame(['type1', 'last3'], df)
#     remove_columns_like('diss', df)
    if ('Unnamed: 0' or 'Unnamed: 0.1') in df_y.columns:
        df_y.drop(labels=['Unnamed: 0','Unnamed: 0.1'],axis=1,inplace=True)
    
    return df, df_y


def get_x_y(n_rows=None):
    
    df, df_y = get_data(n_rows)

    #fill_nas(0, df)
    for y in df_y.columns:
        if len(pd.unique(df_y.ix[:,y]))==2:
            y=df_y.ix[:,y].values
            break
    return df.values, y


def get_columns():
    
    df, df_y = get_data(1000) 
    return list(df.columns)


def print_report(y, y_pred):

    print classification_report(y, y_pred)
    

#############################################
# MODEL HELPERS
#############################################

def grid_search(X, y, clf, param_grid, n_jobs=1):
    
#     param_dict={'average': 'weighted'}
    scorer = make_scorer(average_precision_score)


    gridclf = GridSearchCV(estimator=clf, param_grid=param_grid, scoring=scorer, cv=3, verbose=1, n_jobs=n_jobs)

    gridclf.fit(X, y)
   
    return gridclf


def get_top_n_feats(n, feat_arr, cols):
    args=np.argsort(feat_arr)
    assert len(feat_arr)==len(cols)
    col_scores=col_scores=np.array(zip(cols,feat_arr))
    return col_scores[args[-n:]].tolist()[::-1]


# def get_top_n(n, arr, col_names, prev_list=[]):
    
#     if n <= 0:
#         return []
    
#     most_imp = -1
#     most_imp_index = -1

#     for i in range(len(arr)):

#         if i in prev_list:
#             continue

#         if arr[i] > most_imp:
#             most_imp = arr[i]
#             most_imp_index = i

#     prev_list.append(most_imp_index)

#     return [ (col_names[most_imp_index], most_imp) ] + get_top_n(n - 1, arr, col_names, prev_list)


# In[3]:

def drop_unneeded_cols(df):
    del_cols = ['fileid','cite','vol','beginpg','endopin','endpage','docnum','priorpub','_merge','year',
            'circuit','pseatno','decision_date','aatty_first_name','aatty_last_name','afirm_name',
            'ratty_first_name','ratty_last_name','rname_of_first_listed_amicus_gro','rfirm_namew','decisiondatenew2',
           'j1name','j2name','j3name','quartertoelect','pname','seatno','success','lsuc','ls1','ls2','ls3','lp',
            'lp2','lp3','sseatno','congress','congreso','afirst_listed_amicus_group','yearquarter','name','Name','State','j',
            'codej4','j4vote1','j4vote2','j4maj1','j4maj2','codej5','j5vote1','j5vote2','j5maj1','j5maj2',
            'codej6','j6vote1','j6vote2','j6maj1','j6maj2','codej7','j7vote1','j7vote2','j7maj1','j7maj2',
            'codej8','j8vote1','j8vote2','j8maj1','j8maj2','codej9','j9vote1','j9vote2','j9maj1','j9maj2',
            'codej10','j10vote1','j10vote2','j10maj1','j10maj2','codej11','j11vote1','j11vote2','j11maj1','j11maj2',
            'codej12','j12vote1','j12vote2','j12maj1','j12maj2','codej13','j13vote1','j13vote2','j13maj1','j13maj2',
            'codej14','j14vote1','j14vote2','j14maj1','j14maj2','codej15','j15vote1','j15vote2','j15maj1','j15maj2','j16maj1','j16vote1']
    df.drop(labels=del_cols,axis=1,inplace=True)
    
    moredropcolumns=df.columns.tolist() # .tolist?
    for i in moredropcolumns:
        if len(pd.unique(df[i]))==1:
            df.drop(labels=i,axis=1,inplace=True)

    df.drop(labels=['casenum','j2vote1','j2vote2','j2maj1','direct1',
                          'j2maj2','j3vote1','j3vote2','j3maj1','j3maj2','majvotes','ids'],axis=1,inplace=True)
    return df
    
def dummify(df):
    new_cols=df.columns
    new_cols=new_cols.tolist()
#     keep_cols=['j1score','j2score','j3score','popularpct','electoralpct','closerd','fartherd','dAds3','dF2Ads3',
#            'dF1Ads3','dL1Ads3','dL2Ads3','dL3Ads3','dL4Ads3','dL5Ads3','logAds3','logL1Ads3','logL2Ads3','logF1Ads3',
#           'logF2Ads3','decade2','propneg','likely_elev2','score','d12','d13','d23','sat_together_count']

    float_cols=['j1score','j2score','j3score','popularpct','electoralpct','closerd','fartherd','dAds3','dF2Ads3',
           'dF1Ads3','dL1Ads3','dL2Ads3','dL3Ads3','dL4Ads3','dL5Ads3','logAds3','logL1Ads3','logL2Ads3','logF1Ads3',
          'logF2Ads3','decade2','propneg','likely_elev2','score','d12','d13','d23',
           'judgecitations','experience','experiencetrun','age2trun','agego','assets','ba','liable',
            'networth','totalcities','sat_together_count','keytotal','lengthopin','Wopinionlenght','Wtotalcites','age']

    remove_for_now=['Ads3','F1Ads3','F2Ads3','L1Ads3','L2Ads3','L3Ads3','L4Ads3','L5Ads3','Unnamed: 0.1','appel1','appel2',
               'citevol','codej3','id','usc2sect','usc1sect','age2','distjudg','respond1','respond2','yearb','pred','csb']

#    df.drop(labels=remove_for_now,inplace=True,axis=1)
 
    for x in remove_for_now:
        if x in df.columns:
            print "dropped: ",x
            df.drop(labels=[x],inplace=True,axis=1)
    
    sum1=0
    
    dummy_cols=[]
    for col in df.columns:
        if col not in float_cols:
            if len(pd.unique(df.ix[:,col]))>100 or (df.ix[:,col].dtype!='float64' and df.ix[:,col].dtype!='int64'): 
                sum1+= len(pd.unique(df.ix[:,col]))
                dummy_cols.append(col)
    print "# of dummy columns: ",sum1
    print df.shape
    print dummy_cols
    df2=pd.get_dummies(df,columns=dummy_cols,dummy_na=True,sparse=True)
    print df2.shape
    df2.fillna(value=0,inplace=True)

    return df2


def remove_bad_rows(df_x,df_y):
    
    #remove rows where codej1==codej2
#     df[df.codej1==df.codej2].index
    same_cols = df_x[df_x.codej1==df_x.codej2].index
    df_x=df_x.drop(same_cols).reset_index(drop=True)
    df_y=df_y.drop(same_cols).reset_index(drop=True)
    #remove rows where >3 judges occur
#     pp = pd.read_csv('../raw/Votelevel_stuffjan2013.csv')
#     qq=pp.groupby(by=['casenum']).count()
#     pd.unique(qq.month)
#     rr=qq[qq.month==6].reset_index()
#     rr.shape
    
    #remove rows where codej2==null
    #df[map(lambda x: not(x),pd.notnull(df.ix[:]["codej2"]).tolist())]
    nan_cols=df_x[map(lambda x: not(x),pd.notnull(df_x.ix[:]["codej2"]).tolist())].index
    nan_cols.append(df_x[map(lambda x: not(x),pd.notnull(df_x.ix[:]["codej1"]).tolist())].index)
    df_x=df_x.drop(nan_cols).reset_index(drop=True)
    df_y=df_y.drop(nan_cols).reset_index(drop=True)
    
    return df_x,df_y

def drop_dissent(df,drop=['diss','concur','unan']):
    
    def func(a, b):
        return not set(a).isdisjoint(set(b))
    
    diss_list=[]
    for col in df.columns:
        for x in drop:
            if x in col:
                diss_list.append(col)
    diss_list=list(set(diss_list))
    df.drop(labels=diss_list,axis=1,inplace=True)
    return df
