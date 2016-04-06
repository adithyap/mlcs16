import os
import time
from bs4 import BeautifulSoup
import helper


def process_dir(data_dir):
    """
    Processes a directory containing a set of case documents and extracts the case data.
    The case data thus extracted shall be stored in {data_dir}/txt/.
    """

    case_files = helper.get_files(data_dir)

    ops = parse_files(case_files)

    write_files(ops, os.path.join(data_dir, 'txt'))


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

    soup = BeautifulSoup(helper.read_file_to_string(cfile), "lxml")

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

    helper.ensure_dir(data_dir)

    for case_id, case_data in fdata:

        if (case_id is None) or (case_data is None):
            continue

        f = open(os.path.join(data_dir, case_id + '.txt'), 'w')
        f.write(case_data.encode('utf8'))
        f.close()

    pass


def main():

    start = time.time()

    data_dir = '1881_complete'
    process_dir(data_dir)

    print('*** Completed processing in ', time.time() - start, '(s)')

if __name__ == '__main__':
    main()
