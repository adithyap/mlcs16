
# coding: utf-8

# In[40]:

import pandas as pd
import numpy as np
from copy import deepcopy
import time


# In[41]:

pd.set_option('max_rows',2000)
pd.set_option('max_columns',2000)
np.set_printoptions()


# In[71]:

#df = pd.read_stata('/scratch/sv1239/projects/mlcs/raw/Votelevel_stuffjan2013.dta')
df = pd.read_stata('Votelevel_stuffjan2013.dta')


# In[72]:

df.shape


# In[73]:

# columns to be removed, casenum or codej1... or j2vote... or j2maj... will be removed later
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
#
# to_dummies = ['month','day','method','state','district','origin','source','distjudg',
#               'applfrom','adminrev','opinstat','treat','classact','crossapp','counsel1','counsel2','sanction',
#               'initiate','numappel','appnatpr','appnatpr','appbus','appnonp','appfed','appsubst','appstate',
#               'appfiduc','ap_stid','genapel1','bank_ap1','genapel2','bank_ap2','appel1','appel2',]


# In[74]:

df.drop(labels=del_cols,axis=1,inplace=True)


# In[75]:

#df.shape


# In[76]:

moredropcolumns=df.columns.tolist() # .tolist?
for i in moredropcolumns:
    if len(pd.unique(df[i]))==1:
        df.drop(labels=i,axis=1,inplace=True)


# In[77]:

#df.shape


# In[52]:

## I use case id to find the record of each vote of the same case, caseList save each unique case id for one time. 
## There are 18000+ unique cases.

caseList=[]
for i in range(df.shape[0]):
    if pd.notnull(df.ix[i]["casenum"]) & (df.ix[i]["casenum"] not in caseList):
        caseList.append(df.ix[i]["casenum"])
# print len(caseList)


# In[53]:

## on my computer, about 0.5 second per case
## there will be 6 rows for each case. codej1 correspond to primary judge 
newframe=pd.DataFrame()                ##  the rearrange of the original data
output=[]                           ##   the corresponding alignment of judge 1 and judge 2, yes =1, no = -1
for case in caseList:    
    subtest=df[df.casenum==case].reset_index(drop=True)  ## 'subtest' only take the records that have a specific case id
    num=subtest.shape[0]                                 ## num will be 3, because usally there are 3 records for each case 
    for j in range(num):
        if pd.notnull(subtest.ix[j].codej1):
            j1=subtest.ix[j].codej1
        if pd.notnull(subtest.ix[j].codej2):
            j2=subtest.ix[j].codej2
        if pd.notnull(subtest.ix[j].codej3):
            j3=subtest.ix[j].codej3
    if subtest.ix[0].majvotes == 3:
        j1j2=1
        j1j3=1
        j2j3=1
    else:
        if subtest.ix[0].direct1==subtest.ix[0].j2vote1:
            j1j2=1
        else:
            j1j2=-1                
        if subtest.ix[0].direct1==subtest.ix[0].j3vote1:
            j1j3=1
        else:
            j1j3=-1
        if subtest.ix[0].j2vote1==subtest.ix[0].j3vote1:
            j2j3=1
        else:
            j2j3=-1
    for j in range(num):
        copytest=deepcopy(subtest.ix[j])
        if copytest.ids==j1:
            copytest.codej1=j1
            newframe=newframe.append(copytest)
            output.append(j1j2)
            copytest.codej2=j3
            copytest.codej3=j2
            newframe=newframe.append(copytest)
            output.append(j1j3)
        if copytest.ids==j2:
            copytest.codej1=j2
            copytest.codej2=j1
            newframe=newframe.append(copytest)
            output.append(j1j2)
            copytest.codej2=j3
            copytest.codej3=j1
            newframe=newframe.append(copytest)
            output.append(j2j3)
        if copytest.ids==j3:
            copytest.codej1=j3
            copytest.codej3=j1
            newframe=newframe.append(copytest)
            output.append(j2j3)
            copytest.codej2=j1
            copytest.codej3=j2
            newframe=newframe.append(copytest)
            output.append(j1j3)
            
newframe=newframe.reset_index()              ## need to reset the index, otherwise will all be 0
newframe=newframe.drop('index',1)  

assert newframe.shape[0]==len(output)
#print newframe.shape


# In[54]:

## remove the columns that we are done with
newframe.drop(labels=['casenum','j2vote1','j2vote2','j2maj1','direct1',
                      'j2maj2','j3vote1','j3vote2','j3maj1','j3maj2','majvotes','ids'],axis=1,inplace=True)


# In[55]:

new_cols=newframe.columns


# In[56]:

new_cols=new_cols.tolist()


# In[57]:

keep_cols=['j1score','j2score','j3score','popularpct','electoralpct','closerd','fartherd','dAds3','dF2Ads3',
           'dF1Ads3','dL1Ads3','dL2Ads3','dL3Ads3','dL4Ads3','dL5Ads3','logAds3','logL1Ads3','logL2Ads3','logF1Ads3',
          'logF2Ads3','decade2','propneg','likely_elev2','score','d12','d13','d23']

'''
This keep_cols are all float no categories. So null=0 will be fine.

for col in keep_cols:
    if len(pd.unique(newframe[col]))<4:
        print pd.unique(newframe[col]),col+"\n"
'''
#doubt that sth like dl4ads3 is also categories


# In[58]:

for col in keep_cols:
    if col in new_cols:
        new_cols.remove(col)


# In[59]:

#'dL1Ads3' in new_cols


# In[60]:

newframe=pd.get_dummies(newframe,columns=new_cols,dummy_na=True)


# In[61]:

newframe=newframe.fillna(value=0)         


# In[63]:

newframe.to_csv('out.csv')


# In[ ]:



