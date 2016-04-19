import numpy as np
import networkx as nnx
import sys

def parseText():
	
	return

def gramScorer(gram):
   """
   Calculates meme score for each ngram.
   """
    graph_size = size(sorted) #number of nodes
    dm2m=0
    d2m=0
    dm2n=0
    d2n=0
    memers=0
    for node in sorted:
        #every node stores 3 vars - isMemer, citesMemer, ifCounted (in sum)
        if !node.ifCounted: #if not counted in sum
            if node.next!=null: #has children (citers)
                if len(node.next)==1: #just one child (citer)
                    child=node.next
                    node.citesMemer=child.isMemer
                else:
                    for i in node.next:
                        if i.isMemer==True:
                            node.citesMemer=True
                            break
            if !node.traversed: #not been traversed
                node.traversed=True
                if gram in node: #if gram present
                    memers+=1 #has meme
                    node.isMemer=True
            if node.isMemer==True and node.citesMemer==True:
                dm2m+=1 #memer cites memer 
                d2m+=1 #cites memer
                node.ifCounted=1
            elif node.isMemer==True and node.citesMemer==False:
                dm2n+=1 #memer cites non-memers
                d2n+=1 #cites non-memers
                node.ifCounted=1
            elif isMemer==False and node.citesMemer==True:
                d2m+=1 #cites memers
            elif isMemer==False and node.citesMemer==False:
                d2n+=1 #cites non-memers

    
    prop_score = (dm2m/d2m)/(dm2n/d2n)
    freq = memers/graph_size
    meme_score = prop_score*freq
    return meme_score

def timeSort(graph):
   """
   Sorts graph by year.
   Argument: graph
   Returns: graph sorted by year
   """
	return sorted_graph


def saveScoreDict(dicti):
   """
   Saves score dictionary.
   """
	return 

def main():
	graph_dir='../raw/'
	gram_dir=''
	sys.path.append(graph_dir)
	sys.path.append(gram_dir)
	graph = #read graph here
	gram_dict = parseText() #read dict of ngrams here
	score_dict = #duplicate gramdict here
	sorted = timeSort(graph) #sort by year/topological
	#save sorted graph for future ref.
	for i in sorted:
		assert i.year <= sorted.next.year #check that time-sorted
		for gram in gram_dict[i]:
			gramScore = gramScorer(gram)
			score_dict[i][gram] = gramScore
	saveScoreDict(score_dict) #save score dict.

if __name__ == '__main__':
    main()