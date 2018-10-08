"""
"""
import os
import logging
import traceback
import warnings
import sys
# import shutil

import numpy as np

from zcode.tools.singleton import Singleton
from zcode import inout as zio
import zcode.inout.log  # noqa

# from . import utils
# import astrom_gw
# from . import (PATH_MODULE, OUTPUT_TO_GIT_HASH, DNAME_OUTPUT, DNAME_OUTPUT_PLOTS, ERROR_WARNINGS,
#                DNAME_INPUT, DNAME_INPUT_GAIA, FNAME_GAIA_MERGED, DNAME_OUTPUT_NOTEBOOK,
#                DNAME_OUTPUT_DATA, DNAME_OUTPUT_DATA_SENS, DNAME_SENS, FNAME_SENS, LOG_MEMORY,
#                FNAME_SENS_MERGED)
#
# from . import VERBOSE, DEBUG


def warn_with_traceback(message, category, filename, lineno, file=None, line=None):
    log = file if hasattr(file, 'write') else sys.stderr
    traceback.print_stack(file=log)
    log.write(warnings.formatwarning(message, category, filename, lineno, line))
    return


@Singleton
class Core:

    def __init__(self):
        self.paths = Paths.Instance()
        self.log = load_logger()
        self.log.debug("Core.__init__()")
        self.log.warning("Initializing Core instance")

        if ERROR_WARNINGS:
            self.log.warning("Turning all warnings into errors!  [ERROR_WARNINGS = {}]".format(
                ERROR_WARNINGS))
            warnings.simplefilter("error")
            warnings.filterwarnings("ignore", message="numpy.dtype size changed")
            warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
        else:
            self.log.info("Adding traceback to warnings")
            warnings.showwarning = warn_with_traceback

        '''
        try:
            comm = MPI.COMM_WORLD
            rank = comm.rank
        except:
            rank = 0

        self.__root = (rank == 0)
        '''
        return

    def save_fig(self, fig, fname, modify_exists=True, save_kwargs={},
                 close=None, show=None, subdir=None, append=None, prepend=None, recent_copy=True):
        self.log.info("Core.save_fig()")
        import matplotlib.pyplot as plt

        if show is None:
            show = False
        if close is None:
            close = (not show)

        fname = self.paths.plot_fname(fname, modify_exists=modify_exists, subdir=subdir)
        if (append is not None) or (prepend is not None):
            fname = zio.modify_filename(fname, append=append, prepend=prepend)
        fig.savefig(fname, **save_kwargs)
        self.log.info("Saved figure to '{}'".format(fname))
        if close:
            plt.close(fig)
        if show:
            plt.show(block=False)
        return fname

    '''
    @property
    def root(self):
        return self.__root
    '''


@Singleton
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


def load_logger(log={}, paths=None, info_file=True):
    """
    """
    if isinstance(log, logging.Logger):
        return log

    # Load/set-default parameters
    kwargs = dict(log)
    name = kwargs.pop('name', "astrom_gw")
    debug = kwargs.pop('debug', DEBUG)
    verbose = kwargs.pop('verbose', VERBOSE)

    log_lvl = None
    rank = None
    # Change filenames based on MPI rank
    try:
        comm = MPI.COMM_WORLD
        rank = comm.rank
        if rank > 0:
            name += "_rank{:03d}".format(rank)
            log_lvl = logging.ERROR
    except Exception as err:
        print("Error loading MPI rank: '{}'".format(err))

    # Determine logging level
    if log_lvl is None:
        if debug:
            log_lvl = logging.DEBUG
        elif verbose:
            log_lvl = logging.INFO
        else:
            log_lvl = logging.WARNING

    # Establish paths
    if paths is None:
        paths = Paths.Instance()
    fname = os.path.join(paths.OUTPUT, name + '.log')
    zio.check_path(fname)
    fname = zio.modify_exists(fname)

    # Set parameters and initialize
    kwargs.setdefault('tofile', fname)
    kwargs.setdefault('level_stream', log_lvl)
    if (rank is None) or (rank < 2):
        print("logging to '{}'".format(fname))
    log = zio.log.get_logger(name, info_file=info_file, **kwargs)
    return log


def log_raise_error(err):
    log = load_logger()
    if isinstance(err, str):
        err = RuntimeError(err)
    log.raise_error(str(err), err.__class__)
