import os
import zipfile
import shutil
import numpy as np
import csv


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

def get_name_without_extension(name):
    """
    Returns the filename without extension
    """

    return ''.join(os.path.basename(name).split('.')[:-1])


def unzip_file(zip_file, target_dir=None):
    """
    Unzips the 'zip_file' into the 'target_dir'
    If target is not specified, filename will be used
    Returns the name of the directory the contents are zipped into
    """

    if target_dir is None:
        target_dir = get_name_without_extension(zip_file)

    z = zipfile.ZipFile(zip_file)
    z.extractall(target_dir)
    z.close()

    return target_dir


def delete_dir(target_dir):
    """
    Deletes the specified directory recursively
    """

    shutil.rmtree(target_dir, ignore_errors=True)


def save_list_to_file(target_path, list_to_save):
    """
    Saves the provided list into the specified path
    """

    np.savetxt(target_path, list_to_save, fmt='%s')


def save_dict_to_file(target_path, dict_to_save):
    """
    Saves the provided dictionary into the specified path
    """

    writer = csv.writer(open(target_path, 'wb'))

    for key, value in dict_to_save.items():
        try:
            writer.writerow([key, value])
        except:
            pass


def move_dir(source, target):
    """
    Moves the source directory to the target directory
    """

    shutil.move(source, target)
