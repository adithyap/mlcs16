import pandas as pd
from citation_translator import get_citation_from_citation, get_citation_from_priorpub

class CaseNode:
    
    def __init__(self, row_id, casenum, citation):
        self.row_id = 0
        self.casenum = 0
        self.citation = ''
        self.cited_by = []
        
    def add_citation(self, case_node):
        self.cited_by.append(case_node)


def main():

    # Create a dict to map to nodes
    citation_map = dict()
    index_map = dict()

    connections = 0
    DATA_FILE = '/scratch/sv1239/projects/mlcs/raw/merged_caselevel_data.csv'

    merged_caselevel = pd.read_csv(DATA_FILE, low_memory=False)

            
    # Phase 1: Build nodes
    for index, row in merged_caselevel.iterrows():
        
        # Convert the citation field into a presentable representation
        citation = get_citation_from_citation(row['citation'])
        
        # Create a node for the current row
        node = CaseNode(index, row['casenum'], citation)
        
        # Add it to citation_map and index_map
        citation_map[citation] = node
        index_map[index] = node


    # Phase 2: Build connections
    for index, row in merged_caselevel.iterrows():

        # Convert priorpub into citation for this row
        citation_priorpub = get_citation_from_priorpub(row['priorpub'])
        
        # Search for a matching case and link the two
        if citation_priorpub in citation_map:
            citation_map[citation_priorpub].add_citation(index_map[index])
            connections += 1
        
    print connections

if __name__ == '__main__':
    main()
