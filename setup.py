# Setup script usable for distutils.
#
# Original Author: Maas-Maarten Zeeman
#
# Linux build is re-entrant/multithreaded.

# stdlib
import os
import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from distutils.core import Extension
from distutils import spawn
from struct import calcsize

version = '1.12.11'

# Build either in bindings or client mode.
bindings_mode = 0
if sys.argv[-1] in ('bindings', 'server'):
    bindings_mode = 1
    sys.argv = sys.argv[:-1]
if sys.argv[-1] == 'client':
    bindings_mode = 0
    sys.argv = sys.argv[:-1]

# Are we running 64bits?
if calcsize('P') == 8:
    bits = 64
else:
    bits = 32

def get_windows_settings():
    """ Windows settings.
    """
    if bits == 64:
        library_dirs = [r'{}\tools\Lib64'.format(os.environ.get('MQ_FILE_PATH', '.')),
                        r'c:\Program Files (x86)\IBM\WebSphere MQ\tools\Lib64']
        include_dirs = [r'{}\tools\c\include'.format(os.environ.get('MQ_FILE_PATH', '.')),
                        r'c:\Program Files (x86)\IBM\WebSphere MQ\tools\c\include']
    else:
        library_dirs = [r'{}\tools\Lib'.format(os.environ.get('MQ_FILE_PATH', '.')),
                        r'c:\Program Files\IBM\WebSphere MQ\Tools\Lib']
        include_dirs = [r'{}\tools\c\include'.format(os.environ.get('MQ_FILE_PATH', '.')),
                        r'c:\Program Files\IBM\WebSphere MQ\tools\c\include']

    if bindings_mode:
        libraries = ['mqm']
    else:
        if bits == 64:
            libraries = ['mqic']
        else:
            libraries = ['mqic32']

    return library_dirs, include_dirs, libraries

def get_sunos_zlinux_settings():
    """ SunOS and z/Linux settings.
    """
    if bits == 64:
        library_dirs = ['{}/lib64'.format(os.environ.get('MQ_FILE_PATH', '.')),
                        '/opt/mqm/lib64']
    else:
        library_dirs = ['{}/lib'.format(os.environ.get('MQ_FILE_PATH', '.')),
                        '/opt/mqm/lib']

    include_dirs = ['{}/inc'.format(os.environ.get('MQ_FILE_PATH', '.')),
                    '/opt/mqm/inc']

    if bindings_mode:
        libraries = ['mqm', 'mqmcs', 'mqmzse']
    else:
        libraries = ['mqic']

    return library_dirs, include_dirs, libraries

def get_aix_settings():
    """ AIX settings.
    """
    if bits == 64:
        library_dirs = ['{}/lib64'.format(os.environ.get('MQ_FILE_PATH', '.')),
                        '/usr/mqm/lib64']
    else:
        library_dirs = ['{}/lib'.format(os.environ.get('MQ_FILE_PATH', '.')),
                        '/usr/mqm/lib']

    include_dirs = ['{}/inc'.format(os.environ.get('MQ_FILE_PATH', '.')),
                    '/usr/mqm/inc']

    if bindings_mode:
        libraries = ['mqm_r']
    else:
        libraries = ['mqic_r']

    return library_dirs, include_dirs, libraries

def get_generic_unix_settings():
    """ Generic UNIX, including Linux, settings.
    """
    if bits == 64:
        library_dirs = ['{}/lib64'.format(os.environ.get('MQ_FILE_PATH', '.')),
                        '/opt/mqm/lib64']
    else:
        library_dirs = ['{}/lib'.format(os.environ.get('MQ_FILE_PATH', '.')),
                        '/opt/mqm/lib']

    include_dirs = ['{}/inc'.format(os.environ.get('MQ_FILE_PATH', '.')),
                    '/opt/mqm/inc']

    if bindings_mode:
        libraries = ['mqm_r']
    else:
        libraries = ['mqic_r']

    return library_dirs, include_dirs, libraries

def get_locations_by_command_path(command_path):
    """ Extracts directory locations by the path to one of MQ commands, such as dspmqver.
    """
    command_dir = os.path.dirname(command_path)
    mq_installation_path = os.path.abspath(os.path.join(command_dir, '..'))

    if bits == 64:
        library_dirs = ['{}/lib64'.format(mq_installation_path)]
    else:
        library_dirs = ['{}/lib'.format(mq_installation_path)]

    include_dirs = ['{}/inc'.format(mq_installation_path)]

    if bindings_mode:
        libraries = ['mqm_r']
    else:
        libraries = ['mqic_r']

    return library_dirs, include_dirs, libraries

# Windows
if sys.platform == 'win32':
    library_dirs, include_dirs, libraries = get_windows_settings()

# SunOS and z/Linux
elif sys.platform == 'sunos5' or sys.platform == 'linux-s390':
    library_dirs, include_dirs, libraries = get_sunos_zlinux_settings()

# AIX
elif sys.platform.startswith('aix'):
    library_dirs, include_dirs, libraries = get_aix_settings()

# At this point, to preserve backward-compatibility we try out generic
# UNIX settings first, i.e. libraries and include files in well-known locations.
# Otherwise, to support Mac, we look up dspmqver in $PATH.
else:

    has_generic_lib = os.path.exists('/opt/mqm/lib64') if bits == 64 else os.path.exists('/opt/mqm/lib')
    has_mq_file_path = os.environ.get('MQ_FILE_PATH', False)

    if has_generic_lib or has_mq_file_path:
        library_dirs, include_dirs, libraries = get_generic_unix_settings()

    else:

        # On Mac, users can install MQ to any location so we look up
        # the path that dspmqver is installed to and find the rest
        # of the information needed in relation to that base directory.
        dspmqver_path = spawn.find_executable('dspmqver')

        # We have found the command so we will be able to extract the relevant directories now
        if dspmqver_path:
            library_dirs, include_dirs, libraries = get_locations_by_command_path(dspmqver_path)

        else:
            library_dirs, include_dirs, libraries = get_generic_unix_settings()

if bindings_mode:
    print('Building PyMQI bindings mode %sbits' % bits)
else:
    print('Building PyMQI client mode %sbits' % bits)

print('Using library_dirs:`%s`, include:`%s`, libraries:`%s`' % (library_dirs, include_dirs, libraries))

long_description = """
Python library for IBM MQ
-------------------------

PyMQI is a production-ready, open-source Python extension for IBM MQ (formerly known as WebSphere MQ and MQSeries).

For 20+ years, the library has been used by thousands of companies around the world with their queue managers running on
Linux, Windows, UNIX and z/OS.

Sample code
===========

To put a message on a queue:

.. code-block:: python

    import pymqi

    queue_manager = pymqi.connect('QM.1', 'SVRCONN.CHANNEL.1', '192.168.1.121(1434)')

    q = pymqi.Queue(queue_manager, 'TESTQ.1')
    q.put('Hello from Python!')

To read the message back from the queue:

.. code-block:: python

    import pymqi

    queue_manager = pymqi.connect('QM.1', 'SVRCONN.CHANNEL.1', '192.168.1.121(1434)')

    q = pymqi.Queue(queue_manager, 'TESTQ.1')
    msg = q.get()
    print('Here is the message:', msg)

The backbone of IBM MQ Python messaging
=======================================

PyMQI is a low-level library that requires one to know IBM MQ APIs well.

It serves, however, as the basis for
IBM MQ
support
in
`Zato <https://zato.io>`_,
which is an enterprise
API platform and backend application server in Python that lets one connect to many technologies
with little or no programming.

This includes IBM MQ queue managers as well as the ability to seamlessly integrate with Java JMS systems.

.. image:: https://zato.io/en/docs/3.2/gfx/api/screenshots/conn1.png

.. image:: https://zato.io/en/docs/3.2/gfx/api/screenshots/mq.png

Learn more
==========

Visit the `documentation <https://zato.io/en/docs/3.2/pymqi/index.html?gh>`_ for more information and usage examples.
"""

_ = setup(name = 'pymqi',
    version = version,
    description = 'Python IBM MQI Extension for IBM MQ (formerly WebSphere MQ and MQSeries).',
    long_description = long_description,
    author='Zato Source s.r.o.',
    author_email='pymqi@zato.io',
    url='https://zato.io/pymqi',
    download_url='https://zato.io/pymqi/install.html',
    platforms='OS Independent',
    package_dir = {'': 'code'},
    packages = ['pymqi'],
    license='Python Software Foundation License',
    keywords=('pymqi IBM MQ WebSphere WMQ MQSeries IBM middleware messaging queueing asynchronous SOA EAI ESB integration'),
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Python Software Foundation License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Object Brokering',
        ],
    py_modules = ['pymqi.CMQC', 'pymqi.CMQCFC', 'pymqi.CMQXC', 'pymqi.CMQZC'],
    ext_modules = [Extension('pymqi.pymqe',['code/pymqi/pymqe.c'], define_macros=[('PYQMI_BINDINGS_MODE_BUILD', bindings_mode)],
        library_dirs = library_dirs,
        include_dirs = include_dirs,
        libraries = libraries)])
