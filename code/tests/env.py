# test environment settings

import sys
import os


def add_syspath(p):
    """Add path p to sys.path without defeating PYTHONPATH.

    Appends to sys.path if PYTHONPATH is set, otherwise put p at sys.path index
    1.
    """
    if p not in sys.path:
        if "PYTHONPATH" in os.environ:
            sys.path.append(p)
        else:
            sys.path.insert(1, p)


# Add pymqi code directory to sys.path for import from checkout
# (needs in-place build of pymqe.so)
add_syspath(os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))

