# Test helpers and utilities

import sys
import os
import inspect
import functools # >= Python 2.5


def with_env_complement(env_var_name, envvar_value):
    """Decorate test with environment additions.

    Use for tests with mandatory environment variable requirements. If env
    variable env_var_name is not set before test invocation, add it to the
    environment with a value of envvar_value, run the test and remove
    env_var_name again.
    Runs the test without environment changes if env_var_name is set.
    """
    # The actual decorator that will accept the test function argument and wrap
    # it with the optional env additions
    def decorate(test_func):
        @functools.wraps(test_func)
        def _env_complemented(*args, **kwargs):
            if not env_var_name in os.environ.keys():
                # enhance environment if env variable is not set
                os.environ[env_var_name] = envvar_value
                try:
                    return test_func(*args, **kwargs)
                finally:
                    del os.environ[env_var_name]
            else:
                # run test as is, without changes to the environment
                return test_func(*args, **kwargs)
        return _env_complemented
    return decorate


# a helper to access the config class attributes
def _visit(cls, prefix=()):
    """Recursively traverse non-special cls attributes and yield
    (qualified-name, value)-tuples. Generator function.

    A "qualified" name is a (prefix, outer-cls, [inner-cls,] attr-name)-tuple.
    Args:
        cls: The (config) class to traverse for attribute lookup.
        prefix: Optional prefix tuple.
    """
    for attr_name, attr_val in cls.__dict__.items():
        if not attr_name.startswith('__'):
            # ignore names that appear "special"
            if inspect.isclass(attr_val):
                # recursively
                for visited in _visit(
                        attr_val, prefix=prefix + (cls.__name__,)):
                    yield visited
            else:
                yield (prefix + (cls.__name__, attr_name), attr_val)


def print_config(*cfg_classes):
    """Print configuration set in configuration classes cfg_classes.
    """
    print
    print("Active configuration:")
    for cls in cfg_classes:
        for q_attr_name, attr_val in sorted(_visit(cls, prefix=('config',))):
            print(("  %s: %s" % ('.'.join(q_attr_name), attr_val)).encode(
                sys.stdout.encoding, 'replace'))


