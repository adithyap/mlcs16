
# coding: utf-8
import random
import pandas as pd
import numpy as np
import multiprocessing
from joblib import Parallel, delayed
import time
import gc

def get_file_obj(filename):
	return open(filename, 'r')

def get_year_map(filename):
	f = get_file_obj(filename)
	year_map = {}
	for line in f:
		year, from_case, to_case = line[:-1].split(',')
	
		if from_case not in year:
			year_map[from_case] = int(year)
	f.close()

	return year_map

def get_graph(filename, b_enforce_random = False):
    
    if b_enforce_random:
        random_start = 0
        random_end = 5000
        random_target = random_start + (random_end - random_start) / 2
    
    year_map = get_year_map(filename)

    #Begin building citation graph
    f = get_file_obj(data_file)
    g = nx.DiGraph()
    
    for line in f:
        year, from_case, to_case = line[:-1].split(',')
     
        # Citing a future case is invalid
        if (to_case in year_map) and (from_case in year_map) and (year_map[from_case] < year_map[to_case]):
            continue

        # If the cite each other, it is most likely that both are a wrong edge
        if (to_case in g) and (from_case in g[to_case]):
            del g[to_case][from_case]
            continue
 	
   	 #add edges 
        if (b_enforce_random == False) or (random_target == random.randrange(random_start, random_end)):
            g.add_edge(from_case, to_case)
            g.node[from_case]['year']=int(year)
            g.node[from_case]['ifCounted']=False
            #g.node[from_case]['traversed']=False
            g.node[from_case]['isMemer']=False
            g.node[from_case]['citesMemer']=False
            g.node[to_case]['ifCounted']=False
            #g.node[to_case]['traversed']=False
            g.node[to_case]['isMemer']=False
            g.node[to_case]['citesMemer']=False
            
    f.close()
    
    return eliminate_cycles(g)




def display_graph(graph):
    
    print graph.nodes()


def topological_sort(graph):
    """
    Sorts graph by year.
    Argument: graph
    Returns: a list of nodes of the graph sorted by dependencies
    """
    
    return nx.topological_sort(graph)


# In[366]:

data_file = '../../raw/graph_stripped.csv'

g = get_graph(data_file, True)

#print 'Graph node order:'
#display_graph(g)


# In[367]:

print 'Graph node order:'
display_graph(g)


# In[368]:

sorted_list = topological_sort(g)

print 'Graph node order AFTER sorting:'
print sorted_list


# In[369]:

'XDOJINQNB5G0' in sorted_list


# In[370]:

nx.edges(g,'X4995T')


# In[371]:

# Accessing children of nodes in sorted list

for node in sorted_list:
    
    print nx.edges(g, node)


# In[372]:

data_dir='/scratch/sv1239/projects/mlcs/mlcs16/n_grams/'


# In[373]:

import os
#for filename in os.listdir(data_dir):
test=pd.read_csv(data_dir +'XFJD1I.txt', sep=",",header=None)
test.columns = ['text','count']


# In[374]:

test.head()


# In[375]:

'not intended' in test['text'].tolist()


# In[24]:

gram_graph=nx.DiGraph()
f = open(data_dir +'XFJD1I.txt', 'r')


# In[29]:

'XFKLAA.txt'[:-4]


# In[48]:

gram_dict={}


# In[33]:

gram_dict={'a':{'ab':1,'aab':2},'b':{'bc':3}}


# In[49]:

gram_dict2={'a':['ab','aab'],'b':['bc']}


# In[57]:

gram_dict2


# In[56]:

gram_dict2['a'].append('aacd')


# In[42]:

gram_dict['c']={}


# In[47]:

gram_dict


# In[46]:

gram_dict['c']['cb']=2


# In[40]:

gram_dict.has_key('bc')


# In[377]:

import os
gram_dict={}
test=['XFKEIQ.txt','XFKK8M.txt','XFLD3P.txt']
for filename in os.listdir(data_dir):
    f = open(data_dir+filename, 'r')
    name = filename[:-4]
    gram_dict[name]={}
    for line in f:
        #print line
        #print line
        text, count = line.rsplit(',',1)
        count=int(count[:-2])
        if count>1:
            gram_dict[name][text]=count
    f.close()


# In[378]:

gram_dict.keys()


# In[379]:

haskeys=[]


# In[380]:

for nd in gram_dict.keys():
    if nd in g.nodes():
        print nd


# In[381]:

for nd in g.nodes():
    if gram_dict.has_key(nd):
        print nd
        haskeys.append(nd)


# In[382]:

haskeys


# In[383]:

for node in g.nodes():
    if len(g.successors(node))>1:
        print node
        print g.successors(node)


# In[438]:

def gramScorer(gram,sorted_list,graph,gram_dict):
    """
    Calculates meme score for each ngram.
    Arguments:
    gram: an n-gram or phrase for which meme score to be calculated
    sorted_list: a sorted list of all nodes in graph
    graph: a NetworkX DAG of nodes/cases with edges
    gram_dict: dict storing n-grams
    Returns:
    meme_score: final meme_score of the n-gram
"""
    graph_size = len(sorted_list) #number of nodes
    dm2m=0
    d2m=0
    dm2n=0
    d2n=0
    memers=0
    for node in sorted_list: #list of nodes sorted topologically
        #every node stores 3 vars - isMemer, citesMemer, ifCounted (in sum)
        if not graph.node[node]['ifCounted']: #if not counted in sum
            if node in gram_dict.keys():
                if gram_dict[node].has_key(gram): #if gram present
                    memers+=1 #has meme
                    graph.node[node]['isMemer']=True
            graph.node[node]['ifCounted']=True
            if len(graph.successors(node))>0: #has children (citers)
#                 if len(graph.successors(node))==1: #just one child (citer)
#                     child=graph.successors(node)[0]
#                     graph.node[node]['citesMemer']=graph.node[child]['isMemer']
#                 else:
                for child in graph.successors_iter(node):
                    if graph.node[child]['isMemer']==True:
                        graph.node[node]['citesMemer']=True
                        break
#             if not graph.node['node']['traversed']: #not been traversed
#                 graph.node['node']['traversed']=True
#                 if gram_dict[node].has_key(gram): #if gram present
#                     memers+=1 #has meme
#                     graph.node['node']['isMemer']=True
            if graph.node[node]['isMemer']==True and graph.node[node]['citesMemer']==True:
                dm2m+=1 #memer cites memer
                d2m+=1 #cites memer
                graph.node[node]['ifCounted']=True
            elif graph.node[node]['isMemer']==True and graph.node[node]['citesMemer']==False:
                dm2n+=1 #memer cites non-memers
                d2n+=1 #cites non-memers
                graph.node[node]['ifCounted']=True
            elif graph.node[node]['isMemer']==False and graph.node[node]['citesMemer']==True:
                d2m+=1 #cites memers
            elif graph.node[node]['isMemer']==False and graph.node[node]['citesMemer']==False:
                d2n+=1 #cites non-memers
    print dm2m
    print d2m
    print dm2n
    print d2n
    
    prop_score = ((dm2m)/(d2m+3.))/((dm2n+3.)/(d2n+3.))
    freq = memers/graph_size
    meme_score = prop_score*freq
    print prop_score
    print freq
    print meme_score
    return meme_score


# In[385]:

for node in sorted_list:
    if gram_dict.has_key(node):
        print node
print "there's nothing"


# In[386]:

for i in ['XDOJINQNB5G0']:
    #assert i.year <= sorted.next.year #check that time-sorted
    for gram in gram_dict[i]:
        gramScore = gramScorer(gram,sorted_list,g)
        score_dict[i][gram] = gramScore


# ### Since we don't have n-grams for nodes in graph_stripped, we'll use dummy data.

# In[421]:

dummy_dict={}


# In[422]:

len(gram_dict.keys())


# In[439]:

for i in range(len(gram_dict.keys())):
    state=random.randrange(0,len(sorted_list))
    while sorted_list[state] in dummy_dict.keys():
        state=random.randrange(0,len(sorted_list))
    dummy_dict[sorted_list[state]]=gram_dict.values()[i]


# In[440]:

len(dummy_dict)


# In[441]:

cnt=0
for go in dummy_dict.keys():
    if go in sorted_list:
        cnt=cnt+1
print cnt


# In[442]:

print dummy_dict.has_key('X3U1T6')
print 'X3U1T6' in sorted_list
print 'X3U1T6' in g.nodes()


# In[443]:

dummy_dict.keys()[0]


# In[444]:

testset=[dummy_dict.keys()[0]]
score_dict={}
for i in testset:
    score_dict[i] = {}
    for gram in dummy_dict[i]:
        gramScore = gramScorer(gram,sorted_list,g,dummy_dict)
        score_dict[i][gram] = gramScore
        print gram,gramScore


# In[446]:

score_dict


# In[ ]:



