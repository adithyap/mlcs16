import helper
import nltk.data
from nltk.util import ngrams
import time


def process_dir(data_dir, MIN_N_GRAM, MAX_N_GRAM):
    """
    Processes a directory containing a set of case documents and generates n-grams.
    The n-grams thus generated shall be stored in {data_dir}/n-grams/
    """

    case_files = helper.get_files(data_dir)

    case_files = case_files[:10]

    for case_file in case_files:

        case_data = helper.read_file_to_string(case_file)

        # sentences = get_sentences(case_data)

        n_grams = []

        for sentence in get_sentences(case_data):
            for n in range(MIN_N_GRAM, MAX_N_GRAM):

                n_grams.extend([str(x) for x in ngrams(sentence.split(), n)])
                

def get_sentences(case_data):

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    return tokenizer.tokenize(case_data)


def main():

    start = time.time()

    MIN_N_GRAM = 3
    MAX_N_GRAM = 7

    data_dir = '1881_complete/txt'
    process_dir(data_dir, MIN_N_GRAM, MAX_N_GRAM)

    print('*** Completed processing in ', time.time() - start, '(s)')

if __name__ == '__main__':
    main()