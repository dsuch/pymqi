# Setup script usable for distutils.
#
# Original Author: Maas-Maarten Zeeman
#
# Linux build is re-entrant/multithreaded.

import sys, os
from struct import calcsize

from setuptools import setup, find_packages
from distutils.core import Extension

version = "1.5"

# Munge the args if a server or client build was asked for.
build_server = 0
if sys.argv[-1] == 'server':
    build_server = 1
    sys.argv = sys.argv[:-1]
if sys.argv[-1] == 'client':
    build_server = 0
    sys.argv = sys.argv[:-1]

# Are we running 64bits?
if calcsize("P") == 8:
    bits = 64
else:
    bits = 32

def get_windows_settings():
    """ Windows settings.
    """
    if bits == 64:
        library_dirs = [r"c:\Program Files (x86)\IBM\WebSphere MQ\tools\Lib64"]
        include_dirs = [r"c:\Program Files (x86)\IBM\WebSphere MQ\tools\c\include"]
    else:
        library_dirs = [r"c:\Program Files\IBM\WebSphere MQ\Tools\Lib"]
        include_dirs = [r"c:\Program Files\IBM\WebSphere MQ\tools\c\include"]

    if build_server:
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
        library_dirs = ['/opt/mqm/lib64']
    else:
        library_dirs = ['/opt/mqm/lib']

    include_dirs = ['/opt/mqm/inc']

    if build_server:
        libraries = ['mqm','mqmcs','mqmzse']
    else:
        libraries = ['mqic']

    return library_dirs, include_dirs, libraries

def get_aix_settings():
    """ AIX settings.
    """
    if bits == 64:
        library_dirs = ['/usr/mqm/lib64']
    else:
        library_dirs = ['/usr/mqm/lib']

    include_dirs = ['/usr/mqm/inc']

    if build_server:
        libraries = ['mqm_r']
    else:
        libraries = ['mqic_r']

    return library_dirs, include_dirs, libraries

def get_generic_unix_settings():
    """ Generic UNIX, including Linux, settings.
    """
    if bits == 64:
        library_dirs = ['/opt/mqm/lib64']
    else:
        library_dirs = ['/opt/mqm/lib']

    include_dirs = ['/opt/mqm/inc']

    if build_server:
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

# Try generic UNIX for any other platform, including Linux
else:
    library_dirs, include_dirs, libraries = get_generic_unix_settings()


if build_server:
    print "Building PyMQI server %sbits" % bits
else:
    print "Building PyMQI client %sbits" % bits


setup(name = 'pymqi',
    version = version,
    description = 'Python IBM MQI Extension for WebSphere MQ (formerly known as MQSeries).',
    long_description= 'PyMQI is a Python library for working with WebSphere MQ (formerly known as MQSeries) implementing MQI and PCF protocols.',
    author='Dariusz Suchojad',
    author_email='dsuch at zato.io',
    url='https://pythonhosted.org/pymqi/',
    download_url='https://pypi.python.org/pypi/pymqi',
    platforms='OS Independent',
    packages = find_packages('pymqi'),
    license='Python Software Foundation License',
    keywords=('pymqi WebSphere MQ WMQ MQSeries IBM middleware messaging queueing asynchronous SOA EAI ESB integration'),
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
    ext_modules = [Extension('pymqi.pymqe',['pymqi/pymqe.c'],
            define_macros=[('PYQMI_SERVERBUILD', build_server)],
        library_dirs = library_dirs,
        include_dirs = include_dirs,
        libraries = libraries)])
