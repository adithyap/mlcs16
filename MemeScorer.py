import networkx as nx
import random
import pandas as pd
import numpy as np
import multiprocessing
from joblib import Parallel, delayed
import copy, os, csv, time
import fnmatch
import random


g_filename = None
g_case_list = None
g_year_map = None

def ensure_dir(directory):
    """
    Ensures that the specified directory exists, creates if it doesn't exist
    """

    if not os.path.exists(directory):
        os.makedirs(directory)
    

def save_list_to_file(target_path, list_to_save):
    """
    Saves the provided list into the specified path
    """

    np.savetxt(target_path, list_to_save, fmt='%s')


def get_file_obj(filename):
    return open(filename, 'r')


def get_year_map(filename):
    
    global g_filename
    global g_case_list
    global g_year_map
    
    if (g_filename is not None) and (g_filename == filename):
        if (g_case_list is not None) and (g_year_map is not None):
            return g_year_map, g_case_list
        
    
    f = get_file_obj(filename)
    
    year_map = {}
    case_list = []
    
    for line in f:
        year, from_case, to_case = line[:-1].split(',')
        
        if from_case not in year:
            year_map[from_case] = int(year)
            case_list.append(from_case)
        
    f.close()
    
    g_filename = filename
    g_year_map = year_map
    g_case_list = case_list
    
    return year_map, case_list


def get_graph(filename, b_enforce_random = False):
    
    if b_enforce_random:
        random_start = 0
        random_end = 5000
        random_target = random_start + (random_end - random_start) / 2
    
    year_map, case_list = get_year_map(filename)
    
    # Begin building citation graph
    f = get_file_obj(filename)    
    g = nx.DiGraph()
    
    for line in f:
    
        year, from_case, to_case = line[:-1].split(',')

        # Citing a future case is invalid
        if (to_case in year_map) and (from_case in year_map) and (year_map[from_case] < year_map[to_case]):
            continue
            
        # If they cite each other, it is most likely that both are a wrong edge
        if (to_case in g) and (from_case in g[to_case]):
            del g[to_case][from_case]
            continue
        
        # Add edges
        if (b_enforce_random == False) or (random_target == random.randrange(random_start, random_end)):
            g.add_edge(from_case, to_case)
#             g.node[from_case]['year']=int(year)
            g.node[from_case]['ifCounted']=False
            g.node[from_case]['isMemer']=False
            g.node[from_case]['citesMemer']=False
            g.node[to_case]['ifCounted']=False
            g.node[to_case]['isMemer']=False
            g.node[to_case]['citesMemer']=False
                
    f.close()
    
    return g


def display_graph(graph):
    
    print graph.nodes()


def topological_sort(graph):
    """
    Sorts graph by year.
    Argument: graph
    Returns: a list of nodes of the graph sorted by dependencies
    """
    
    global g_filename
    
    if g_filename is None:
        return graph.nodes()
    
    year_map, case_list = get_year_map(g_filename)
    
    return case_list

def freshen_graph(g):
    for node in g.nodes():
        g.node[node]['ifCounted']=False
        g.node[node]['isMemer']=False
        g.node[node]['citesMemer']=False
    return g


def gramScorer(gram,sorted_list,graph,gram_dict,verbose=0):
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

    if verbose>=1:
        print "graph_size is",graph_size
        
    dm2m=0
    d2m=0
    dm2n=0
    d2n=0
    memers=0
    nonmemers=0
    
    #every node stores 3 vars - isMemer, citesMemer, ifCounted (in sum)
    
    for node in sorted_list: #list of nodes sorted topologically
        
        if node not in graph:
            continue
        
        if not graph.node[node]['ifCounted']: #if not counted in sum
            
            if verbose >= 3:
                print node, graph.node[node]
                
            if node in gram_dict:

                if gram in gram_dict[node]: #if gram present
                    memers+=1 #has meme
                    graph.node[node]['isMemer']=True

                else:
                    nonmemers+=1

            graph.node[node]['ifCounted']=True


            if len(graph.successors(node)) > 0: #has children (citers)
                for child in graph.successors_iter(node):

                    if graph.node[child]['isMemer']==True: #soft-check if child has gram
                        graph.node[node]['citesMemer']=True
                    elif gram_dict.has_key(child) and gram_dict[child].has_key(gram): #hard-check using dictionary
                        graph.node[child]['isMemer']=True
                        graph.node[node]['citesMemer']=True
                        break

            if verbose>=3:
                print node,graph.node[node]
            
            if graph.node[node]['isMemer']==True and graph.node[node]['citesMemer']==True:
                dm2m+=1 #memer cites memer

            elif graph.node[node]['isMemer']==True and graph.node[node]['citesMemer']==False:
                if len(graph.successors(node))!=0: #make sure childless nodes not counted
                    dm2n+=1 #memer cites non-memers

            if graph.node[node]['citesMemer']==True:
                d2m+=1 #cites memers

            elif graph.node[node]['citesMemer']==False:
                if len(graph.successors(node))!=0: #make sure childless nodes not counted
                    d2n+=1 #cites non-memers

        elif verbose>=2:
            print str(node)+" is counted."
    
#     assert memers+nonmemers==graph_size #sanity check for memer size
    if verbose>=1:
        print "memers =",memers
        print "nonmemers =",nonmemers
        print "dm2m =",dm2m
        print "d2m =",d2m
        print "dm2n =",dm2n
        print "d2n =",d2n

    prop_score = (float(dm2m)/(d2m+3.))/((dm2n+3.)/(d2n+3.)) #ratio of sticking factor by sparking factor
    #we take a shifted prop. score to make sure score not infinite
    freq = float(memers)/(graph_size) #ratio of # of memers for that n-gram to size of graph
    meme_score = prop_score*freq #prop_score x meme frequency
    
    if verbose>=1:
        print "prop_score =",prop_score
        print "freq =",freq
        print "meme_score =",meme_score

    return meme_score


def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            
            if basename == '.DS_Store':
                continue
            
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename



data_file = 'data/graph_stripped.csv'
# data_file = 'data/graph_mini.csv'
data_dir = '../../data/'


g = get_graph(data_file)

print('Completed loading graph')

gram_dict={}

sorted_list = topological_sort(g)

#Generate dictionary of n-grams
for filename in find_files(data_dir, '*'):
    f = open(filename, 'r')
    name = os.path.basename(filename)
    gram_dict[name]={}
    
    for line in f:
        text, count = line.rsplit(',',1)
        count=int(count[:-2])
        
        if count>1:
            gram_dict[name][text]=count
            
    f.close()

print('Completed generating n-gram dictionary')

# testset=gram_dict.keys()
testset=gram_dict.keys()
random.shuffle(testset)
score_dict={}

target_dir = 'meme_scores'
ensure_dir(target_dir)

for i in testset[:10]: #testset of nodes
    
    non_zero_grams = []
    
    for gram in gram_dict[i]:
        
        if not score_dict.has_key(gram) and gram_dict[i][gram] >= 2: #not already scored, freq >= 2
            g = freshen_graph(g) # set all values to False
            gramScore = gramScorer(gram, sorted_list, g, gram_dict, 0)
            score_dict[gram] = (i,gramScore) # stores first node encountered and meme score

            # print i, gram, gramScore
            if int(gramScore) != 0: # only print those with non-zero scores
#                 print i, gram, gramScore
                non_zero_grams.append(str(gram) + ', ' + str(gramScore))
                
    if len(non_zero_grams) > 0:
        target_path = os.path.join(target_dir, i + '.csv')
        save_list_to_file(target_path, non_zero_grams)

    else:
        target_path = os.path.join(target_dir, i + '.csv')
        save_list_to_file(target_path, ['No non zero non_zero_grams'])
        
    print('Completed ', i, 'non_zero_grams=', len(non_zero_grams))
