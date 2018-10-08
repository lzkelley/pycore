"""
"""

from . import utils


@utils.Singleton
class Paths:

    MODULE = PATH_MODULE

    def __init__(self, **kwargs):
        self.nodename = os.uname().nodename

        # Construct input path
        # ---------------------------
        if 'harvard' in self.nodename:
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

        # Construct a list of required files
        req_files = []
        req_files.append(self.MERGED_GAIA_FNAME)

        self._req_files = req_files
        # Make sure required files exist
        self.check_files()
        return

    def check_files(self):
        """
        """
        for ff in self._req_files:
            if not os.path.exists(ff):
                raise RuntimeError("Required file '{}' does not exist!".format(ff))

    def plot_fname(self, fname, modify_exists=True, subdir=None):
        path = self.OUTPUT_PLOTS
        if subdir is not None:
            path = os.path.join(path, subdir, '')
        fname = os.path.join(path, fname)
        zio.check_path(fname)
        if modify_exists:
            fname = zio.modify_exists(fname)
        return fname

    @property
    def OUTPUT(self):
        path = self.__OUTPUT_PATH
        return path

    @property
    def OUTPUT_PLOTS(self):
        path = os.path.join(self.OUTPUT, DNAME_OUTPUT_PLOTS, '')
        zio.check_path(path)
        return path
