import pandas as pd
import numpy as np
from copy import deepcopy
import time
from joblib import Parallel, delayed
import multiprocessing
import gc

df=pd.read_csv('BloombergVOTELEVEL_Touse.csv',nrows=42000)         




print df.shape

                       
colum=df.columns.tolist()                                 # drop columns that only have one value
droplist=[]
for case in colum:
    if len(pd.unique(df[case]))==1:
        droplist.append(case)

if ('Dissenting1' in droplist):
        droplist.remove('Dissenting1')


df.drop(labels=droplist,axis=1,inplace=True)






droplistAgain=['docketnumber','citation','JudgeCONCURRING','JudgeDissentingTouse','songername','jOrigname','dissentdate',
         'JudgesListTouse','Judgeconcurring','dateamended','month','day','AmendedDate','distanceAM','quartertoelectAM'
         ,'JudgeDISSENTING1','JudgeDISSENTING2','Author','AppointmentDate1','TerminationDate1','RecessAppointDate1',
         'AppointmentDate2','TerminationDate2','RecessAppointDate2','AppointmentDate3','TerminationDate3','AppointmentDate',
         'TerminationDate','SenateConfirmationdate','RecessAppointDate','birthday','birthyear','birthmonth','deathmonth',
         'deathday','deathyear','judgelastname','judgefirstname','judgemiddlename','retirementfromactiveservice','degreeyear1',
         'degreeyear2','degreeyear3','degreeyear4','vicelastnamepredecessor','vicefirstnamepredecessor','hearings',
         'placeofdeathcity','deathdate','dateoftermination']
              
weird=['MajOpinionWordCount','MajSelfCertainWords','minOpinionWordCount1','MinSelfCertainWords1',
       'ConcurenceWordCount1','ConcurSelfCertainWords1','minOpinionWordCount2','MinSelfCertainWords2','ConcurenceWordCount2',
      'ConcurSelfCertainWords2','senatevoteayesnays']
weird2=['dissentOrconcurCaseid','yearq','Circuitjudge1','Circuitjudge2','id','nominationdatesenateexecutivej','recessappointmentdate',
       'committeeactiondate','senatevotedateconfirmationdate','commissiondate','startdate','BecameSenior']



droplist3=['RecessAppointDate4','AppointmentDate5','TerminationDate5','RecessAppointDate5','AppointmentDate6',
          'TerminationDate6','RecessAppointDate6','RecessAppointDate3']


#   these are columns that can be droped

droplistAgain=droplistAgain+weird+weird2+droplist3

colum=df.columns.tolist()

droplist2=[]
for case in droplistAgain:
     if (case in colum):
        droplist2.append(case)

df.drop(labels=droplist2,axis=1,inplace=True)



print df.shape


df.Dissenting1=df.Dissenting1.fillna(value=0)   ## this value tells which judge (1,2 or 3) disagree the other

nterm=df.columns.tolist().index('Term')         ## prepare to copy the features after and including 'Term' 
copylist=df.columns.tolist()[nterm:]            ## because thoes are features of judge's biography
copylist.append('judgeidentificationnumber')

caseList=pd.unique(df['caseid'])
caseList=caseList[pd.notnull(caseList)].tolist()

Length=len(caseList)

def for_voting(caseLIST,st,end):
    if end>Length:
         end=Length
    print st,end
    newframe=pd.DataFrame()
    output=[]
    for case in caseList:
        temper=np.where(df.caseid==case)
        temper=(temper[0]).tolist()
        for i in range(len(temper)):
            for j in [1,2]:            
                for term in copylist:
                    name='%sANO'%(term)
                    df.loc[temper[i],name]=df.ix[temper[i-j],term]
                newframe=newframe.append(df.ix[temper[i]])
        if df.loc[temper[0],'Dissenting1']==0:      ## if dissenting is 0, no one disagree
           output=output+[0,0,0,0,0,0]
        else :
           a=df.loc[temper[0],'Dissenting1']        ## otherwise, find the one with 'j' value equal to Dissent1
           for i in range(len(temper)):             ##  'j' value correspond to the judge in that row, 
               if a==df.loc[temper[i],'j']:         ## take values 1,2,3
                   output=output+[1,1]
               elif a==df.loc[temper[i-1],'j']:
                   output=output+[1,0]
               elif a==df.loc[temper[i-2],'j']:
                   output=output+[0,1]
    
    
    assert newframe.shape[0]==len(output)   
    filename="tryvoting%i.csv"%(st)
    filename2="tryvoteoutput%i.csv"%(st)
    newframe.to_csv(filename)
    (pd.DataFrame(output)).to_csv(filename2)
    return output



num_cores = multiprocessing.cpu_count()


print "parallel jobs started"




numarray=[]
i=0
while i<Length:
    numarray.append(i)
    i=i+1000
print numarray


jobs=Parallel(n_jobs=num_cores)(delayed(for_voting)(caseList,a,a+1000) for a in numarray)





















