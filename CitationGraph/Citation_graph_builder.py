
# coding: utf-8

# In[7]:

get_ipython().magic(u'matplotlib inline')

import networkx as nx
import matplotlib.pyplot as plt
import random

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
    
    # Begin building citation graph
    f = get_file_obj(filename)    
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
        
        # Add edges
        if (b_enforce_random == False) or (random_target == random.randrange(random_start, random_end)):
            g.add_edge(from_case, to_case)
        
    f.close()
    
    return eliminate_cycles(g)


def eliminate_cycles(g):

    # Get the MST
    mst = nx.algorithms.minimum_spanning_tree(g.to_undirected())
    
    tree_edges = set(mst.edges())
    
    valid_edges = [e for e in g.edges() if e in tree_edges or reversed(e) in tree_edges]
    
    # Rebuild graph
    g = nx.DiGraph()
    
    g.add_edges_from(valid_edges)
    
    return g
    

def display_graph(graph):
    
    print graph.nodes()


def topological_sort(graph):
    """
    Sorts graph by year.
    Argument: graph
    Returns: a list of nodes of the graph sorted by dependencies
    """
    
    return nx.topological_sort(graph)


# In[12]:

get_ipython().run_cell_magic(u'time', u'', u"\ndata_file = 'Data/graph_mini.csv'\n\ng = get_graph(data_file)")


# In[13]:

get_ipython().run_cell_magic(u'time', u'', u'\nsorted_list = topological_sort(g)')


# In[34]:

# Accessing children of nodes in sorted list

for node in sorted_list:
    
    print nx.edges(g, node)

