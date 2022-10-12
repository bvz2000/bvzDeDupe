#! /usr/bin/env python3
"""
A series of functions to compare two files.
"""

import hashlib
import os.path


# ----------------------------------------------------------------------------------------------------------------------
def md5_partial_match(file_a_path,
                      file_b_path,
                      num_bytes=1024):
    """
    Takes two files and compares the hash of the first <num_bytes> of these files to see if they are the same. This is
    primarily used to do a quick compare of two files. If these bytes match, it still does not necessarily mean that the
    files are identical, just that they have a decent probability of being the same.

    :param file_a_path: The first file to compare
    :param file_b_path: The second file to compare
    :param num_bytes: The number of bytes to hash. Defaults to 1K (1024)

    :return: True if the first <num_bytes> bytes of the two files match (via a hash)
    """

    with open(file_a_path, 'rb') as f:
        chunk = f.read(num_bytes)
    md5 = hashlib.md5()
    md5.update(chunk)
    checksum_a = md5.hexdigest()

    with open(file_b_path, 'rb') as f:
        chunk = f.read(num_bytes)
    md5 = hashlib.md5()
    md5.update(chunk)
    checksum_b = md5.hexdigest()

    return checksum_a == checksum_b


# ----------------------------------------------------------------------------------------------------------------------
def md5_full_match(file_a_path,
                   file_b_path):
    """
    Performs a full md5 checksum compare between two files. If the files match, the md5 hash is returned. If they do not
    match, None is returned.

    :param file_a_path: The first file to compare
    :param file_b_path: The second file to compare

    :return: The checksum of the files if they match, None otherwise.
    """

    md5 = hashlib.md5()
    with open(file_a_path, 'rb') as f:
        for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
            md5.update(chunk)
    checksum_a = md5.hexdigest()

    md5 = hashlib.md5()
    with open(file_b_path, 'rb') as f:
        for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
            md5.update(chunk)
    checksum_b = md5.hexdigest()

    if checksum_a == checksum_b:
        return checksum_b
    else:
        return None


# ----------------------------------------------------------------------------------------------------------------------
def compare(file_a_path,
            file_b_path,
            single_pass=False):
    """
    Compares two files. Returns True if they are identical. False if not.

    :param file_a_path: The first file to be compared.
    :param file_b_path: The second file to be compared.
    :param single_pass: If True, then the two files will be compared using a full checksum of each file. If False, then
           only the first 1K bytes of each file will be checksummed. Only if these bytes match will a second, full
           checksum of both files be done.

    :return: True the files are identical, False otherwise.
    """

    assert os.path.exists(file_a_path)
    assert not os.path.isdir(file_a_path)
    assert not os.path.islink(file_a_path)
    assert os.path.exists(file_b_path)
    assert not os.path.isdir(file_b_path)
    assert not os.path.islink(file_b_path)

    if single_pass:
        return md5_full_match(file_a_path, file_b_path)
    else:
        if md5_partial_match(file_a_path, file_b_path):
            return md5_full_match(file_a_path, file_b_path)
        return False
