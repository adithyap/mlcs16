import os


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
