import os
import time
from bs4 import BeautifulSoup


def process_dir(data_dir):
    """
    Processes a directory containing a set of case documents and generates the citation data.
    The citatation data thus generated shall be stored in {data_dir}.txt.
    """

    case_files = get_files(data_dir)

    # case_files = case_files[:20]

    ops = parse_files(case_files)

    write_files(ops, os.path.join(data_dir, 'txt'))


def get_files(data_dir):
    """
    Returns the files in a directory
    """

    if os.path.exists(data_dir):
        return [os.path.join(data_dir, f) for f in os.listdir(data_dir) if is_valid_file(data_dir, f)]

    return None

def is_valid_file(data_dir, path):
    """
    Checks if a given path points to a valid file
    """
    if not_ds_store(path):
        if os.path.isfile(os.path.join(data_dir, path)):
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
    :return: A list of tuples containing (Case ID, [Citations])
    """

    ops = []

    for i in range(len(files)):

        ops.append((get_case_data(files[i])))

    return ops

def get_case_data(cfile):

    soup = BeautifulSoup(read_file_to_string(cfile), "lxml")

    case_id = None
    case_data = None

    for metadata_tag in soup.find_all('div', {'class': 'docId'}):
        if metadata_tag is not None:
            case_id = str(metadata_tag.contents[0])
            break

    for content_tag in soup.find_all('div', {'id': 'contentMajOp'}):
        if content_tag is not None:
            case_data = content_tag.get_text()
            break

    # print('Completed', case_id)

    return case_id, case_data

def write_files(fdata, data_dir):
    """
    Expects a list of tuples, containing (case_id, case_data)
    Writes the {case_data} into {case_id}.txt
    All the files will be written into {data_dir} directory
    """

    ensure_dir(data_dir)

    for case_id, case_data in fdata:

        if (case_id is None) or (case_data is None):
            continue

        f = open(os.path.join(data_dir, case_id + '.txt'), 'w')
        f.write(case_data.encode('utf8'))
        f.close()

    pass


def read_file_to_string(cfile):
    """
    Reads the content of a file into a string
    """

    with open(cfile, 'r') as myfile:
        data = myfile.read()
        return data


def ensure_dir(directory):
    """
    Ensures that the specified directory exists, creates if it doesn't exist
    """

    if not os.path.exists(directory):
        os.makedirs(directory)


def main():

    start = time.time()

    data_dir = '1881_complete'
    process_dir(data_dir)

    print('*** Completed processing in ', time.time() - start, '(s)')

if __name__ == '__main__':
    main()
