"""
"""

import os

# import matplotlib.pyplot as plt

import zcode.inout as zio

from . import utils


# class Paths(utils.Singleton):
class Paths:

    # MODULE = PATH_MODULE
    # _DNAME_PLOTS = "figs"

    # Paths to create if they do not already exist
    _CHECK_PATHS = []
    _CWD = os.path.realpath(os.getcwd())

    def __init__(self, core, **kwargs):
        self._core = core
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

        # Make sure required directories exist
        for path in self._CHECK_PATHS:
            zio.check_path(path)

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

    def save_fig(self, fig, name, subdir=None, fignum=None, close=None, log_lvl=30):
        if (not name.endswith('.pdf')) and (not name.endswith('.png')):
            name += '.pdf'

        if close is None:
            if self._core._is_notebook:
                close = False
            elif self._core._is_ipython:
                close = True
            else:
                close = False

        modify_exists = False
        path = self.output_figs
        if subdir is not None:
            if subdir is True:
                subdir = name.split('.')[0]
            path = os.path.join(path, subdir)
            modify_exists = True

        fname = os.path.join(path, name)
        self.check_path(fname)
        if modify_exists:
            fname = zio.modify_exists(fname)

        fig.savefig(fname)
        self._core.log.log(log_lvl, "Saved to '{}'".format(fname))

        if fignum is not None:
            raise NotImplementedError("`fignum` support has not been implemented!")

            if isinstance(fignum, str):
                name = zio.modify_filename(name, prepend=fignum + "_")
            fname = os.path.join(self.path_output_figs, name)
            zio.check_path(fname)
            fig.savefig(fname)
            # if verbose:
            self._core.log.log(log_lvl, "Saved to '{}'".format(fname))

        if close:
            import matplotlib.pyplot as plt
            plt.close('all')

        return fname

    @property
    def output(self):
        path = self.check_path(self.OUTPUT)
        return path

    @property
    def output_figs(self):
        # path = os.path.join(self.output, self._DNAME_PLOTS, "")
        # path = self.check_path(path)
        # return path
        return self.output

    @property
    def output_logs(self):
        # return self.output
        return self._CWD


class Paths_Single(Paths, utils.Singleton):
    pass
