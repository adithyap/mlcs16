import pandas as pd
import numpy as np
from copy import deepcopy
import time
from joblib import Parallel, delayed
import multiprocessing
import gc


df=pd.read_csv('Sparse100.csv')
df['judge1dissent'] = pd.Series(np.zeros(df.shape[0]), index=df.index)


caseList=pd.unique(df['caseid'])
caseList=caseList[pd.notnull(caseList)].tolist()

Length=len(caseList)

print df.shape
print Length



def get_year(datetime):
        if pd.isnull(datetime):
            return datetime
        else:
            return datetime[-4:]




def for_seating(caseLIST,st,end):
    if end>Length:
         end=Length
    print st,end 
    newframe=pd.DataFrame()
    for case in caseLIST[st:end]:
         temper=np.where(df.caseid==case)
         temper=(temper[0]).tolist()
         for i in range(len(temper)):
               df.loc[temper[i],'judge2code']=df.ix[temper[i-1]]['judgeidentificationnumber']
               #df.loc[temper[i],'judge2dissent']=df.ix[temper[i-1]]['Dissenting1']
               #newframe=newframe.append(df.ix[temper[i]])        
         if df.ix[temper[0]]['Dissenting1']!=0:
               a=df.loc[temper[0],'Dissenting1']
               for i in range(len(temper)):
                     if a==df.loc[temper[i],'j']:
                        df.loc[temper[i],'judge1dissent']=1
                        df.loc[temper[i-2],'judge2dissent']=1
               
         
               
         for i in range(len(temper)):
               newframe=newframe.append(df.ix[temper[i]])
                 
    filename="seatingoutput/seating%i.csv"%(st)
    newframe.date=newframe.date.apply(get_year)
    newframe.to_csv(filename)
    return newframe


num_cores = multiprocessing.cpu_count()


print "parallel jobs started"

numarray=[]
i=0
while i<Length:
    numarray.append(i)
    i=i+1000
print numarray


jobs=Parallel(n_jobs=num_cores)(delayed(for_seating)(caseList,a,a+1000) for a in numarray)




