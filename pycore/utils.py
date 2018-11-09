"""
"""


class Singleton(object):
    """Singleton implementation from the official python docs.

    Allows for subclassing.

    See: https://www.python.org/download/releases/2.2/descrintro/#__new__
    """

    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it

    def init(self, *args, **kwds):
        pass


def python_environment():
    """Tries to determine the current python environment, one of: 'jupyter', 'ipython', 'terminal'.
    """
    try:
        # NOTE: `get_ipython` should not be explicitly imported from anything
        ipy_str = str(type(get_ipython())).lower()  # noqa
        # print("ipy_str = '{}'".format(ipy_str))
        if 'zmqshell' in ipy_str:
            # return 'jupyter'
            return 'notebook'
        if 'terminal' in ipy_str:
            return 'ipython'
    except:
        return 'script'
