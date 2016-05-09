
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
from copy import deepcopy
import time


# In[2]:

pd.set_option('max_rows',2000)
pd.set_option('max_columns',2000)
np.set_printoptions()


# In[3]:

#df = pd.read_stata('/scratch/sv1239/projects/mlcs/raw/Votelevel_stuffjan2013.dta')
df = pd.read_stata('Votelevel_stuffjan2013.dta')


# In[4]:

new_cols=df.columns
new_cols=new_cols.tolist()


# In[5]:

keep_cols=['casenum','j2vote1','j2maj1','direct1','j3vote1','j3maj1','majvotes','ids','year','codej1','codej2','codej3']


# In[6]:

for col in keep_cols:
        new_cols.remove(col)


# In[7]:

df.drop(labels=new_cols,axis=1,inplace=True)


# In[8]:

df.shape


# In[9]:

caseList=pd.unique((df.casenum).dropna())
print len(caseList)


# In[11]:

start=time.time()
## on my computer, about 0.5 second per case
## there will be 6 rows for each case. codej1 correspond to primary judge 
newframe=pd.DataFrame()                ##  the rearrange of the original data
output=[]                           ##   the corresponding alignment of judge 1 and judge 2, yes =1, no = -1
for case in caseList:    
    subtest=df[df.casenum==case].reset_index(drop=True)  ## 'subtest' only take the records that have a specific case id
    num=subtest.shape[0]                                 ## num will be 3, because usally there are 3 records for each case 
    j1=(pd.unique((subtest.codej1).dropna()))[0]
    j2=(pd.unique((subtest.codej2).dropna()))[0]
    j3=(pd.unique((subtest.codej3).dropna()))[0]

    for j in range(num):
        copytest=deepcopy(subtest.ix[j])
        if copytest.ids==j1:

            newframe=newframe.append(copytest)

        if copytest.ids==j2:
            copytest.codej2=j1
            copytest.j2vote1=copytest.direct1
            copytest.j2maj1=1
            newframe=newframe.append(copytest)

        if copytest.ids==j3:
            copytest.codej3=j1
            copytest.j3vote1=copytest.direct1
            copytest.j3maj1=1
            newframe=newframe.append(copytest)           
            
newframe=newframe.reset_index()              ## need to reset the index, otherwise will all be 0
newframe=newframe.drop('index',1)  


print time.time()-start


# In[12]:

finalframe=newframe.loc[:,['casenum','year','codej2','codej3','j2vote1','j3vote1','j2maj1','j3maj1','direct1','majvotes']]


# In[15]:

finalframe.to_csv('seating.csv')


# In[ ]:



