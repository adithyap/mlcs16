import helper
import time

import nltk
import nltk.data
from nltk.util import ngrams
from nltk import CFG

import numpy as np
import os

import csv

grammar_string = """
  S -> TWO | THREE | FOUR

  TWO -> A N | N N | V N | V V | N V | V P
  THREE -> N N N | A A N | A N N | N A N | N P N | V A N | V N N | A V N | V V N | V P N | A N V | N V V | V D N | V V V | N N V | V V P | V A V | V V N | N C N | V C V | A C A | P A N
  FOUR -> N C V N | A N N N | N N N N | N P N N | A A N N | A N N N | A N P N | N N P N | N P A N | A C A N | N C N N | N N C N | A N C N | N C A N | P D A N | P N P N | V D N N | V D A N | V V D N

  A -> 'JJ' | 'JJR' | 'JJS'
  N -> 'NN' | 'NNS' | 'NNP' | 'NNPS' | 'PRP' | 'PRP$'
  V -> 'VB' | 'VBD' | 'VBG' | 'VBN' | 'VBP' | 'VBZ' | 'RB' | 'RBR' | 'RBS' | 'WRB'
  P -> 'IN'
  C -> 'CC' | 'CD'
  D -> 'DT' | 'PDT' | 'WDT'

  M -> '.' """

grammar = CFG.fromstring(grammar_string)

terminals = {'JJ': None, 'JJR': None, 'JJS': None, 'NN': None, 'NNS': None, 'NNP': None, 'NNPS': None, 'PRP': None,
             'PRP$': None, 'VB': None, 'VBD': None, 'VBG': None, 'VBN': None, 'VBP': None, 'VBZ': None, 'RB': None,
             'RBR': None, 'RBS': None, 'WRB': None, 'IN': None, 'CC': None, 'CD': None, 'DT': None, 'PDT': None,
             'WDT': None}


def process_dir(data_dir, MIN_N_GRAM, MAX_N_GRAM, b_verbose=False, b_size=None):
    """
    Processes a directory containing a set of case documents and generates n-grams.
    The n-grams thus generated shall be stored in {data_dir}/n-grams/
    """

    target_dir = os.path.join(data_dir, 'n_grams')

    # Make sure the target directory exists
    helper.ensure_dir(target_dir)

    # Get the case file list
    case_files = helper.get_files(data_dir)

    if b_size is not None:
        case_files = case_files[:b_size]

    total_count = len(case_files)
    progress = 0

    for case_file in case_files:

        # Compute the path to save the file
        target_file_name = os.path.basename(case_file)
        target_path = os.path.join(target_dir, target_file_name)

        # Read the case data from the string
        case_data = helper.read_file_to_string(case_file)

        valid_n_grams = {}

        # Go over every sentence in the document
        for sentence in get_sentences(case_data):

            pos_tuples = nltk.pos_tag(nltk.word_tokenize(sentence))

            # Update the grammar if required and get the POS tags
            pos_tags = get_pos_tags(pos_tuples)

            # Generate N-Grams of tags
            n_grams = []
            for n in range(MIN_N_GRAM, MAX_N_GRAM + 1):
                n_grams.extend([list(grams) for grams in ngrams(range(len(pos_tuples)), n)])

            # Get only the n-grams that match the defined grammar
            for i in range(len(n_grams)):

                # Generate n-gram list and check validity
                if parse([pos_tags[j] for j in n_grams[i]]):

                    # Append words to overall list
                    elements = ' '.join([pos_tuples[k][0] for k in n_grams[i]])

                    if elements in valid_n_grams:
                        valid_n_grams[elements] += 1
                    else:
                        valid_n_grams[elements] = 1

        # Save n-grams to file
        helper.save_dict_to_file(target_path, valid_n_grams)

        progress += 1

        if b_verbose:
            print(progress / (0.01 * total_count), ' % Complete')

    return target_dir


def get_pos_tags(pos_tuples):
    """
    Returns the POS tags from POS tuples of (word, tag)
    Updates the grammar for unknown tags
    """

    global grammar_string
    global grammar
    global terminals

    changed_grammar = False
    pos_tags = []

    for pos_tuple in pos_tuples:
        tag = pos_tuple[1]

        if tag not in terminals:

            if tag == '\'\'':
                tag = 'APOS'

            grammar_string += ' | \'' + tag + '\''

            terminals[tag] = None
            changed_grammar = True

        pos_tags.append(tag)

    if changed_grammar:
        grammar = CFG.fromstring(grammar_string)

    return pos_tags


def get_sentences(case_data):
    """
    Returns a list of sentences from a string of possibly many sentences
    """

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    return tokenizer.tokenize(case_data.decode('utf8'))


def parse(text):
    """
    Checks if the provided text has a valid parse
    """

    parser = nltk.ChartParser(grammar)
    tree = parser.parse(text)

    valid_parse = False

    for t in tree:
        valid_parse = True
        break

    return valid_parse


def main():

    start = time.time()

    MIN_N_GRAM = 2
    MAX_N_GRAM = 4

    data_dir = '1881_complete/txt'
    process_dir(data_dir, MIN_N_GRAM, MAX_N_GRAM)


    print('*** Completed processing in ', time.time() - start, '(s)')

if __name__ == '__main__':
    main()