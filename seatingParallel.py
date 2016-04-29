
import pandas as pd
import numpy as np
from copy import deepcopy
import time
from joblib import Parallel, delayed
import multiprocessing
import gc


pd.set_option('max_rows',2000)
pd.set_option('max_columns',2000)
np.set_printoptions()


df = pd.read_stata('Votelevel_stuffjan2013.dta')


new_cols=df.columns
new_cols=new_cols.tolist()

keep_cols=['casenum','j2vote1','j2maj1','direct1','j3vote1','j3maj1','majvotes','ids','year','codej1','codej2','codej3']


for col in keep_cols:
        new_cols.remove(col)

df.drop(labels=new_cols,axis=1,inplace=True)

print df.shape


caseList=pd.unique((df.casenum).dropna())
print len(caseList)

caseList=caseList[:20
]
num_cores = multiprocessing.cpu_count()

start=time.time()
## on my computer, about 0.5 second per case
## there will be 6 rows for each case. codej1 correspond to primary judge 

def for_seating(case):
    newframe=pd.DataFrame()                ##  the rearrange of the original data
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
    return newframe


print "parallel jobs started"
jobs=Parallel(n_jobs=num_cores)(delayed(for_seating)(case) for case in caseList)

bignew=pd.DataFrame()
print "parallel jobs done"
print "concatenating df's and out's"
    
for x in jobs:
    if bignew.empty:
        bignew=x
    else:
        bignew=pd.concat([bignew,x],ignore_index=True)
    gc.collect()            
#newframe=newframe.reset_index()              ## need to reset the index, otherwise will all be 0
#newframe=newframe.drop('index',1)  


print time.time()-start


finalframe=bignew.loc[:,['casenum','year','codej2','codej3','j2vote1','j3vote1','j2maj1','j3maj1','direct1','majvotes']]

finalframe.to_csv('seating.csv')




