"""
"""

import traceback
import warnings
import sys

import cosmopy

from . import utils, paths, logger, settings


def warn_with_traceback(message, category, filename, lineno, file=None, line=None):
    log = file if hasattr(file, 'write') else sys.stderr
    traceback.print_stack(file=log)
    log.write(warnings.formatwarning(message, category, filename, lineno, line))
    return


class Core(utils.Singleton):

    _CLASS_SETTINGS = settings.Settings
    _CLASS_PATHS = paths.Paths

    def __init__(self, sets={}, paths={}, log={}):

        if not isinstance(sets, self._CLASS_SETTINGS):
            sets = self._CLASS_SETTINGS(**sets)

        self.sets = sets

        # `self.sets` must be set before initializing paths
        if not isinstance(paths, self._CLASS_PATHS):
            paths = self._CLASS_PATHS(self)

        self.paths = paths

        self.log = logger.get_logger(self.sets)

        self.log.debug("Core initializing... loaded: `sets`, `paths`, `log`")
        self.cosmo = cosmopy.get_cosmology()
        self.log.debug("Loaded `cosmo`")

        '''
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
        self.log.debug("Adding traceback to warnings")
        warnings.showwarning = warn_with_traceback

        '''
        try:
            comm = MPI.COMM_WORLD
            rank = comm.rank
        except:
            rank = 0

        self.__root = (rank == 0)
        '''

        import sys

        def _excepthook(exctype, exc, tb):
            self.log.exception("An unhandled exception occurred.", exc_info=(exctype, exc, tb))

        sys.excepthook = _excepthook
                                                                                                    
        return

    '''
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

    '''
    @property
    def root(self):
        return self.__root
    '''
