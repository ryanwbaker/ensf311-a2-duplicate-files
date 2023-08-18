import sys
import hash_functions as hfcs
import dir_functions as dfcs
import argparse

def get_hash(filename, hash='hashmd5'):
    """Hashes a file using MD5 algorithm. See the hashmd5() function in hash_functions.py for more information.

    filename (string): The file to be hashed.
    hash (string): the hash function to be called in hash_functions.py.

    returns: returns: (str) hash as hex formatted string.
    """
    fin = open(filename, 'rb')
    message = fin.read()
    fin.close()
    return eval('hfcs.'+hash+'({})'.format(message))


def get_all_hashes(dirname, hash):
    """Creates a dictionary of all hashes for a given directory.

    dirname (string): The directory to search.
    hash (string): the hash function to be called in hash_functions.py.

    returns: (dict) Dictionary of hashes. key (str): hash, value (list): filename(s).
    """
    file_names = dfcs.walk(dirname)
    
    d = {}

    for name in file_names:

        h = get_hash(name, hash)

        if h in d:
            d[h].append(name)
        else:
            d[h] = [name]
    return d

def print_duplicates(hash_dict, print_val):
    """Prints directories and files that have the same hash.

    hash_dict (dict): Dictionary of hashes. key (str): hash, value (list): filename(s).
    print_val (bool): TRUE == print the actual hash. FALSE == do not print the hash.

    returns: None.
    """
    for hash, names in hash_dict.items():
        # len > 1 if two files have the same hash for a given directory
        if len(names)>1:
            print("These files have the same hash{}:".format(f' ({hash})' if print_val else ''))
            for name in sorted(names):
                print(f"\t{name}")

def cli(args=None):
    """Allows command line interface functionality, and prints names of duplicate files. Type duplicates_cli.py -h for argument information.

    parser (argparse.ArgumentParser): an argparse.ArgumentParser object.
    args (list): List of parsed arguments from parser.ArgumentParser().

    returns: None.
    """
    # This is needed to allow for testing command line interface with pytest
    if not args:
        args = sys.argv[1:]

    #TODO: Add ArgumentParser() here.
    parser = argparse.ArgumentParser(description='Finds duplicate files in a directory.')
    parser.add_argument('dirname', help='The relative directory path to search.')
    parser.add_argument('-e','--extension', help='Only find duplicates of a certain file extension. Eg: duplicates_cli files -e txt would search for .txt files.')
    parser.add_argument('-hf','--hash', default='hashmd5', help='Specified hash. Choices are: string_hash, hash8, hash64, hashfnv32a, or hashmd5. Eg: duplicates_cli files -h hashfnv32a would use hashfnv32a hashing from hash_functions.py.')
    parser.add_argument('-p', '--print_hash', action='store_true', help='Print the calculated hash for duplicates. Eg: duplicates_cli files -p will print the MD5 hash for any found duplicates.')
    args = parser.parse_args(args)
    dirname = args.dirname

    file_hashes = get_all_hashes(dirname, args.hash)

    if args.extension:
        file_hashes = {key:val for (key,val) in file_hashes.items() if val[0].endswith(args.extension)}

    print_duplicates(file_hashes, args.print_hash) 


if __name__ == '__main__':
    cli()
