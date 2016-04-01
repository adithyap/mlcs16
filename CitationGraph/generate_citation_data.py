import os
import re
import time
import numpy as np
from bs4 import BeautifulSoup


def process_dir(data_dir):
    """
    Processes a directory containing a set of case documents and generates the citation data.
    The citatation data thus generated shall be stored in {data_dir}.txt.
    """

    case_files = get_files(data_dir)
    ops = parse_files(case_files)

    # Write to file
    np.savetxt(data_dir + '.txt', np.array(ops), fmt='%s')


def get_files(dir):
    """
    Returns the files in a directory
    """

    if os.path.exists(dir):
        return [os.path.join(dir, f) for f in os.listdir(dir) if is_valid_file(dir, f)]

    return None

def is_valid_file(dir, path):
    """
    Checks if a given path points to a valid file
    """
    if not_ds_store(path):
        if os.path.isfile(os.path.join(dir, path)):
            return True

    return False

def not_ds_store(f):
    """
    Mac specific - checks if the file is system file (.DS_Store) or not
    """
    return f != '.DS_Store'


def parse_files(files):
    """
    Parses all the case files provided as input and generates the citation data
    :param files: List of paths of files who contain the case data
    :return: A list of tuples containing (Case ID, Cite ID, [Citations])
    """

    ops = []

    for i in range(len(files)):

        ops.append(parse_single_file(files[i]))

    return ops


def parse_single_file(cfile):
    """
    Parses a single case file and extracts its Cite ID and the list of citations from it
    """

    filename = (os.path.splitext(cfile)[0]).split('/')[1]

    soup = BeautifulSoup(read_file_to_string(cfile), "lxml")

    # Identify its name
    name = None
    for h2tag in soup.find_all('h2', {'class': 'organization'}):

        temp = h2tag.contents[2].split(',')[-1]
        name = clean_cite_id(str(temp.split('(')[0].strip()))
        break

    # Identify backwards citations
    b_citations = []
    for atag in soup.find_all('a'):

        if (atag is None) or (not atag.has_attr('href')):
            continue

        href = atag.get('href')

        if '#jcite' in href:
            try:
                citation = clean_cite_id( (''.join([str(x) for x in atag.contents])) )
                b_citations.append(str(citation).encode('ascii', 'ignore'))
            except:
                # Non ascii string can cause an exception
                pass

    return filename, name, b_citations



def clean_cite_id(text):
    """
    Cleans the provided HTML string to adhere to the standardized format of a Cite ID
    """

    return strip_tags(text.translate(None, ' []\'.,')).lower()


def strip_tags(text):
    """
    Removes all tags from the provided text
    """

    text = re.sub('<[^<]+?>', '', text)
    return text


def read_file_to_string(cfile):
    """
    Reads the content of a file into a string
    """

    with open(cfile, 'r') as myfile:
        data = myfile.read()
        return data


def main():

    start = time.time()

    data_dir = '1880_complete'
    process_dir(data_dir)

    print('*** Completed processing in ', time.time() - start, '(s)')

if __name__ == '__main__':
    main()
