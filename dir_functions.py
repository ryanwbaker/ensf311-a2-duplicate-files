import os # needed for finding files and folders, creating paths

def walk(dirname):
    """Recursively finds files starting at dirname.

    Ignores .git folder and files contained

    dirname: (str) root of directory structure
    returns: (list) list of filenames starting from dirname
    """

    names = []

    # ignore .git folder and files within.
    if '.git' in dirname:
        return names

    # get all the files in current folder
    for name in os.listdir(dirname):
        path = os.path.join(dirname, name) # we want full path from initial root

        # Append files, recurse into sub-folders
        if os.path.isfile(path):
            names.append(path)
        else:
            names.extend(walk(path))
    return names


if __name__ == '__main__':

    """A test with sample file structure.

    Note that .DS_Store is not part of the sample file structure.
    Gets created on MacOSx.

    prints:
    files/.DS_Store
    files/fig/sines.pdf
    files/archive/.DS_Store
    files/archive/test_archive.txt
    files/archive/sines_archive.pdf
    files/txt/test2.txt
    files/txt/test_copy.txt
    files/txt/test.txt
    files/test2.txt
    files/test_copy.txt
    files/sines.pdf
    files/test.txt
    """
    file_names = walk('files/')
    for name in file_names:
        print(name)