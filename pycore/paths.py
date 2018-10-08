"""
"""

import os

from . import utils


# @utils.Singleton
# class Paths:
class Paths(utils.Singleton):

    # MODULE = PATH_MODULE

    def __init__(self, **kwargs):
        self._node_name = os.uname().nodename

        '''
        # Construct input path
        # ---------------------------
        if 'harvard' in self._node_name:
            self._INPUT_BASE = astrom_gw.PATH_INPUT_BASE_ODYSSEY
        else:
            self._INPUT_BASE = astrom_gw.PATH_INPUT_BASE

        if not os.path.isdir(self._INPUT_BASE):
            raise RuntimeError("input base path '{}' does not exist!".format(self._INPUT_BASE))

        # Construct output path
        # --------------------------
        path = os.path.join(self.MODULE, DNAME_OUTPUT, '')
        path_static = os.path.join(self.MODULE, DNAME_OUTPUT, '')
        if OUTPUT_TO_GIT_HASH:
            git_hash = utils.git_hash()
            path = os.path.join(path, git_hash, '')
        # Modify path if already exists
        if os.path.isdir(path) and astrom_gw.UNIQUE_OUTPUT_DIRS:
            path = zio.modify_exists(path)
        # Create path if needed
        zio.check_path(path)
        zio.check_path(path_static)
        self.__OUTPUT_PATH = path
        self.__OUTPUT_PATH_STATIC = path_static
        '''

        # Construct a list of required files
        req_files = []
        # req_files.append(self.MERGED_GAIA_FNAME)

        self._req_files = req_files
        # Make sure required files exist
        self._check_files()
        return

    def _check_files(self):
        """
        """
        for ff in self._req_files:
            if not os.path.exists(ff):
                raise RuntimeError("Required file '{}' does not exist!".format(ff))

    @staticmethod
    def check_path(tpath, create=True):
        """Create the given filepath if it doesn't already exist.

        Arguments
        ---------
        tpath : str
            Path to check.
        create : bool
            Create the path if it doesnt already exist.
            If `False`, and the path does *not* exist, `None` is returned

        Returns
        -------
        path : str or `None`
            If the path exists, or is created, this is the name of the directory portion of the path.
            If the path does not exist, `None` is returned

        """
        path, name = os.path.split(tpath)
        if len(path) > 0:
            if not os.path.isdir(path):
                if create:
                    try:
                        os.makedirs(path)
                    except FileExistsError:
                        if not os.path.isdir(path):
                            raise
                else:
                    return None

        return path

    '''
    @property
    def OUTPUT(self):
        path = self.__OUTPUT_PATH
        return path

    @property
    def OUTPUT_PLOTS(self):
        path = os.path.join(self.OUTPUT, DNAME_OUTPUT_PLOTS, '')
        zio.check_path(path)
        return path
    '''


def modify_filename(fname, prepend='', append=''):
    """Modify the given filename.

    Arguments
    ---------
    fname : str
        Filename to modify.
    prepend : str
        String to prepend to beginning of filename.
        Added after the terminal slash, otherwise at the beginning.
    append : str
        String to appended to end of filename.
        Added before the terminal '.' if it exists, otherwise at the end.

    Returns
    -------
    new_name : str
        New filename, with modifications.

    """
    is_dir = fname.endswith('/')
    if is_dir:
        o_path, o_name = _path_fname_split(fname)
    else:
        o_path, o_name = os.path.split(fname)

    new_name = prepend + o_name
    if len(append) > 0:
        o_split = new_name.split('.')
        if (len(o_split) >= 2) and (1 < len(o_split[-1]) < 5):
            o_split[-2] += append
        else:
            o_split[-1] += append
        new_name = '.'.join(o_split)

    new_name = os.path.join(o_path, new_name)
    if is_dir:
        new_name = os.path.join(new_name, '')
    return new_name


'''
def modify_exists(fname, max=1000):
    """If the given filename already exists, return a modified version.

    Returns a filename, modified by appending a 0-padded integer to the input `fname`.
    For example, if the input is 'some_dir/some_filename.txt' (assuming it already exists),
    the modified filename would be 'some_dir/some_filename_01.txt', or if that already exists,
    then 'some_dir/some_filename_02.txt' (or higher if needed, up to ``max-1``).
    Suffix numbers with the incorrect number of digits (e.g. 'some_dir/some_filename_002.txt) will
    be ignored.

    Arguments
    ---------
    fname : str
        Filename to be checked and modified.
    max : int or `None`
        Maximum number of modified filenames to try.  `None` means no limit.

    Returns
    -------
    new_name : {str, `None`}
        The input filename `fname` if it does not exist, or an appropriately modified version
        otherwise.  If the number for the new file exceeds the maximum `max`, then a warning is
        raise and `None` is returned.


    Errors
    ------
    RuntimeError is raised if:
    -   Unable to parse existing files with modified names.
    -   The new, modified filename already exists.

    Warnings
    --------
    -   The next modified filename exceeds the allowed maximum `max` number.
        In this case, `None` is returned.

    """
    # If file doesnt already exist, do nothing - return filename
    if not os.path.exists(fname):
        return fname

    is_dir = os.path.isdir(fname)

    # Determine number of digits for modified filenames to allow up to `max` files
    prec = np.int(np.ceil(np.log10(max)))

    # Look for existing, modified filenames
    # -------------------------------------
    num = 0
    # if is_dir:
    #     path, filename = _path_fname_split(fname)
    # else:
    path, filename = os.path.split(fname)
    if len(path) == 0:
        path += './'

    # construct regex for modified files
    #     look specifically for `prec`-digit numbers at the end of the filename
    # regex = modify_filename(re.escape(filename), append='_([0-9]){{{:d}}}'.format(prec))
    if is_dir:
        filename = os.path.join(filename, '')
    regex = modify_filename(re.escape(filename), append='_([0-9]){{{:d}}}'.format(prec))
    regex = regex.replace('./', '')
    if regex.endswith('/'):
        regex = regex[:-1]
    matches = sorted([ff for ff in os.listdir(path) if re.search(regex, ff)])
    # If there are matches, find the highest file-number in the matches
    if len(matches):
        mat = matches[-1]
        mat = mat.split("_")[-1]
        mat = mat.split(".")[0]
        # Try to convert to integer, raise error on failure
        try:
            num = np.int(mat)+1
        except:
            errStr = "Could not match integer from last match = '{}', mat = '{}'.".format(
                matches[-1], mat)
            raise RuntimeError(errStr)

    # If the new filename number is larger than allowed `max`, return `None`
    if num >= max:
        warnings.warn("Next number ({}) exceeds maximum ({})".format(num, max))
        return None

    # Construct new filename
    # ----------------------
    if is_dir:
        filename = os.path.join(filename, '')
    new_name = modify_filename(fname, append='_{0:0{1:d}d}'.format(num, prec))

    # New filename shouldnt exist; if it does, raise warning
    if os.path.exists(new_name):
        # raise RuntimeError("New filename '{}' already exists.".format(new_name))
        warnings.warn("New filename '{}' already exists.".format(new_name))
        return modify_exists(new_name)

    return new_name
'''


def _path_fname_split(fname):
    """
    """
    path, filename = os.path.split(fname)
    # Make sure `filename` stores directory names if needed
    #    If a `fname` looks like "./dname/", then split yields ('./dname', '')
    #    convert this to ('', './dname')
    # print("\t", path, filename)
    if len(filename) == 0 and len(path) > 0:
        filename = path
        path = ''
    # convert ('', './dname') --> ('./', 'dname')
    if filename.startswith('./'):
        path = filename[:2]
        filename = filename[2:]

    # Either path should have a path stored, or it should be the local directory
    if len(path) == 0:
        path = './'
    # print("\t", path, filename)
    return path, filename
