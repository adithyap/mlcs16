import time
import numpy as np
from bs4 import BeautifulSoup
import helper


def process_dir(data_dir):
    """
    Processes a directory containing a set of case documents and generates the citation data.
    The citation data thus generated shall be stored in {data_dir}.txt.
    """

    case_files = helper.get_files(data_dir)
    ops = parse_files(case_files)

    # Write to file
    np.savetxt(data_dir + '.txt', ops, fmt='%s')



def parse_files(files):
    """
    Parses all the case files provided as input and generates the citation data
    :param files: List of paths of files who contain the case data
    :return: A list of tuples containing (Case ID, [Citations])
    """

    ops = []

    for i in range(len(files)):

        ops.append(parse_single_file(files[i]))

    return ops


def parse_single_file(cfile):
    """
    Parses a single case file and extracts its Cite ID and the list of citations from it
    """

    case_id = None

    soup = BeautifulSoup(helper.read_file_to_string(cfile), "lxml")

    # Parse case ID
    for metadata_tag in soup.find_all('div', {'class': 'docId'}):

        if metadata_tag is not None:
            case_id = str(metadata_tag.contents[0])
            break

    # Identify backwards citations
    b_citations = []
    for a_tag in soup.find_all('a'):

        if (a_tag is None) or (not a_tag.has_attr('href')):
            continue

        href = a_tag.get('href')

        if '#jcite' in href:
            try:
                cited_doc_id = ((href.split('/'))[-1]).split('?')[0]
                b_citations.append(cited_doc_id)

            except:
                # Non ascii string can cause an exception
                # Handling them is not really required for this dataset
                pass

    return case_id, ','.join(b_citations)


def main():

    start = time.time()

    data_dir = '1881_complete'
    process_dir(data_dir)

    print('*** Completed processing in ', time.time() - start, '(s)')

if __name__ == '__main__':
    main()
