"""Parameter and Argument handling.
"""

import argparse
from datetime import datetime

import numpy as np

from . import utils


class Settings(utils.Singleton):

    NAME = ""
    VERBOSITY = 20     # 30: warning, 20: info, 10:debug
    LOG_FILENAME = None        # To log to file, provide filename

    def __init__(self, parse_cl=None, **kwargs):
        """
        """
        time_beg = datetime.now()

        name_max_len = 40
        for name, value in kwargs.items():
            old = None
            if hasattr(self, name):
                old = getattr(self, name)
            setattr(self, name, value)
            print("{name:{size:}s} : '{old:}' ==> '{new:}'".format(
                size=name_max_len, name=name, old=old, new=value))

        # Find the stored arguments which are variables for modication
        # ----------------------------------------------------------------------
        var_names = self._get_internal_var_names()

        var_types = []
        name_max_len = 0

        parser = argparse.ArgumentParser()
        for ii, name in enumerate(var_names):
            kw = {}
            value = getattr(self, name)
            vtype = None if value is None else type(value)
            if vtype == list:
                kw.setdefault("nargs", "+")
                vtype = type(value[0])
                var_types.append([vtype])
            else:
                var_types.append(vtype)

            vtype = str2bool if vtype == bool else vtype
            parser.add_argument("--" + name, type=vtype, dest=name, default=value, **kw)

            name_max_len = len(name) if len(name) > name_max_len else name_max_len

        self.add_arguments(parser)

        self._parser = parser
        self._var_names = var_names
        self._var_types = var_types
        self._name_max_len = name_max_len
        self.time_beg = time_beg

        # Determine runtime environment
        # -------------------------------------
        self._pyenv = utils.python_environment().lower().strip()
        _is_script = self._pyenv.startswith('script')

        # Parse Command-Line Arugments
        # ---------------------------------------
        if parse_cl is None:
            parse_cl = _is_script

        if parse_cl:
            self.parse_args()

        return

    def add_arguments(self, parser):
        pass

    def _get_internal_var_names(self):
        """Find internal variable names which can be set/modified.
        """

        def test(vname):
            if not vname.isupper():
                return False

            if vname.startswith('_'):
                return False

            if callable(getattr(self, vname)):
                return False

            return True

        var_names = [nn for nn in dir(self) if test(nn)]

        return var_names

    def __str__(self):
        rv = self._str_all()
        rv = "\n".join(rv)
        return rv

    def _str_all(self):
        mlen = self._name_max_len
        rv = []
        for ii, name in enumerate(self._var_names):
            value = getattr(self, name)
            vtype = self._var_types[ii]
            _rv = "{name:{size:}s} : '{val:}' ({type:})".format(
                size=mlen, name=name, val=value, type=vtype)
            rv.append(_rv)

        return rv

    def parse_args(self):
        args = self._parser.parse_args()
        mlen = self._name_max_len

        for ii, name in enumerate(self._var_names):
            changed = False
            new_value = getattr(args, name)
            old_value = getattr(self, name)
            try:
                if new_value != old_value:
                    changed = True
            except ValueError as err:
                # print("name = '{}'".formart(name))
                # print("old = ", old_value)
                # print("new = ", new_value)
                # print(err)
                # print("\n")
                # raise
                if not np.all(new_value == old_value):
                    changed = True

            setattr(self, name, new_value)
            if changed:
                print("{name:{size:}s} : '{old:}' ==> '{new:}'".format(
                    size=mlen, name=name, old=old_value, new=new_value))

        return

    '''
    def _get_path_output(self, type):
        _valid_types = ['script', 'notebook']
        type = type.strip().lower()
        if type not in _valid_types:
            raise ValueError("`type` '{}' must be one of '{}'!".format(type, _valid_types))

        notebook_flag = (type == 'notebook')

        name_name = self.NAME
        now = self.time_beg
        dt_name = now.strftime("%Y-%m-%d_%H-%M-%S")
        if (name_name is not None) and (len(name_name) > 0):
            if notebook_flag:
                name = name_name
            else:
                name = dt_name + "_" + name_name
        else:
            if notebook_flag:
                name = ""
            else:
                name = dt_name

        base_path = PATH_OUTPUT_NOTEBOOK if notebook_flag else PATH_OUTPUT_SCRIPT

        path_output = os.path.join(base_path, name)
        if not notebook_flag:
            path_output = zio.modify_exists(path_output)
        path_output = os.path.join(path_output, "")
        zio.check_path(path_output)
        path_output_figs = os.path.join(path_output, FIGS_OUTPUT_FNAME, "")
        return path_output, path_output_figs
    '''

    def save_params(self, fname):
        # zio.check_path(fname)
        with open(fname, 'w') as out:
            rv = self._str_all()
            for line in rv:
                out.write(line + "\n")

        print("Parameters saved to '{}'".format(fname))
        return


@utils.Singleton
class Constants:

    MPC3_PER_AS2 = 1.1641   # Redshift z = 2.0

    def __init__(self):
        pass


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == "__main__":
    sets = Settings()
    print(sets)
