
# coding: utf-8

import pandas as pd
import numpy as np
from datetime import datetime


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
    
    for column in list(data_frame.columns):
        if column_pattern in column:
            data_frame.drop(column, axis=1, inplace=True)


def fill_nas(value, data_frame):
    
    data_frame.fillna(0, inplace=True)


# In[74]:

#############################################
# DATA RETRIEVAL HELPERS
#############################################

def get_data(n_rows=None):

    if n_rows is not None:
        df = pd.read_csv('final_feats_without_dummies_2.csv', low_memory=False, nrows=n_rows)
        df_y = pd.read_csv('final_outs_2.csv', low_memory=False, nrows=n_rows)
    else:
        df = pd.read_csv('final_feats_without_dummies_2.csv', low_memory=False)
        df_y = pd.read_csv('final_outs_2.csv', low_memory=False)
    
    
    # Drop labels and a redundant column
    remove_columns_from_data_frame(['Unnamed: 0', 'Unnamed: 0.1' 'dissent', 'dissentdummy'], df)
    
    
    return df, df_y


def get_x_y(n_rows=None):
    
    df, df_y = get_data(n_rows)

    #fill_nas(0, df)
    
    return df.values, df_y.ix[:,1].values


def get_columns(df):
    
    #df = pd.read_csv('final_feats_without_dummies_2.csv', low_memory=False, nrows=2)
    return list(df.columns)


def print_report(y, y_pred):

    print classification_report(y, y_pred)
    


# In[5]:

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
    keep_cols=['j1score','j2score','j3score','popularpct','electoralpct','closerd','fartherd','dAds3','dF2Ads3',
           'dF1Ads3','dL1Ads3','dL2Ads3','dL3Ads3','dL4Ads3','dL5Ads3','logAds3','logL1Ads3','logL2Ads3','logF1Ads3',
          'logF2Ads3','decade2','propneg','likely_elev2','score','d12','d13','d23']
    for col in keep_cols:
        if col in new_cols:
            new_cols.remove(col)
    df2=pd.get_dummies(df,columns=new_cols,dummy_na=True,sparse=False)
    df2=df2.fillna(value=0)
    return df2

def remove_bad_rows(df):
    
    #remove rows where codej1==codej2
#     df[df.codej1==df.codej2].index
    same_cols = df[df.codej1==df.codej2].index
    df=df.drop(same_cols).reset_index(drop=True)
    
    #remove rows where >3 judges occur
#     pp = pd.read_csv('../raw/Votelevel_stuffjan2013.csv')
#     qq=pp.groupby(by=['casenum']).count()
#     pd.unique(qq.month)
#     rr=qq[qq.month==6].reset_index()
#     rr.shape
    
    #remove rows where codej2==null
    #df[map(lambda x: not(x),pd.notnull(df.ix[:]["codej2"]).tolist())]
    nan_cols=df[map(lambda x: not(x),pd.notnull(df.ix[:]["codej2"]).tolist())].index
    nan_cols.append(df[map(lambda x: not(x),pd.notnull(df.ix[:]["codej1"]).tolist())].index)
    df=df.drop(nan_cols).reset_index(drop=True)
    
    return df


# ### Feat 1: If sat together previously

# In[75]:

df_x, df_y = get_data()



def ret_datetime(yr,month,date):
    from datetime import datetime
    return datetime(int(yr),int(month),int(date))

def return_sat_together_count(df):
    """
    Arguments:
    df: dataframe of judge frames
    Returns: None.
    Appends column with sat_together_count feature.
    """
    ###assumes df.time, df.month, df.day present
    df['datetime'] = df.apply(lambda row: ret_datetime(row['year'], row['month'], row['day']), axis=1)
    df['sat_together_count']=0
    #df['judge_pairs']=df.apply(lambda row: tuple([row['codej1'],row['codej2']]),axis=1)
    df['judge_pairs']=pd.Series(zip(df.codej1.values,df.codej2.values))
    for ind,pair in enumerate(df.judge_pairs):
        templist=[]
        for ind2,pair2 in enumerate(df.judge_pairs):
            if set(pair)==set(pair2):
                if df.ix[ind2,'datetime']<df.ix[ind,'datetime']:
                    templist.append(df.ix[ind2,'datetime'])
        df.ix[ind,'sat_together_count']=len(set(templist)) #df.ix[ind,'sat_together_count']+1
    df.drop(labels=['judge_pairs','datetime'],axis=1,inplace=True)
    return df
    
    


print df_x.shape

print "removing bad rows ..."

df_x=remove_bad_rows(df_x)

print df_x.shape

df2=df_x.select(lambda x: x=='year' or x=='day' or x=='month' or x=='codej1' or x=='codej2' or x=='casenum',axis=1)


# In[78]:

print df2.shape

    

df2=return_sat_together_count(df2)


df_x['sat_together_count']=df2['sat_together_count']

print df_x.shape


print "converting to csv..."
df_x.to_csv('final_feats_without_dummies_3.csv')

print "converted to csv!"



