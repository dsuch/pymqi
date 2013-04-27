Mingw32
=================================

How To Build Python Extensions Without a Microsoft Compiler
-----------------------------------------------------------


These note were written by Jaco Smuts. If you have any questions about them, please e-mail Jaco `directly <jaco.smuts@clover.co.za>`_.

Notes on how to compile Python extensions on windows without the Microsoft compiler. I assume some basic skills in Windows. Most of this is simply copied from http://sebsauvage.net/python/mingw.html.

Steps:

   #. Get and install MinGW gcc
   #. Create libpython2?.a
   #. Tweak distutils
   #. Compile/install the extension with distutils.

Get and install MinGW gcc
~~~~~~~~~~~~~~~~~~~~~~~~~

Get MinGW gcc from http://mingw.org (Minimalist GNU For Windows). I've only
downloaded MinGW-3.1.0-1.exe (14.8 Mb). This will install the compiler,
libraries and support utilities in your chosen directory. I can't remember
if I had to do this manually, make sure your {install dir}\\bin is added to
your path environment variable. To test it type gcc -- version in at the
command prompt to test your installation.

Create libpython2?.a
~~~~~~~~~~~~~~~~~~~~
To create Python extensions, you need to link against the Python library.
Unfortunately, most Python distributions are provided with Python2?.lib,
a library in Microsoft Visual C++ format. GCC expects a .a file (libpython2?.a
to be precise.). Here's how to convert python2?.lib to libpython2?.a:

   1. Download pexports from http://starship.python.net/crew/kernr/mingw32/.
   2. Extract files and make sure the bin directory is in your path.
   3. Locate Python2?.dll (Found mine under C:\\WINNT\\system32).
   4. Run::

          pexports python2?.dll > python2?.def 

      This will extract all symbols from python2?.dll and write them into python2?.def.
   5. Run::
           
          dlltool --dllname python2?.dll --def python2?.def --output-lib libpython2?.a

      This will create libpython2?.a (dlltool is part of MinGW utilities).
   6. Copy libpython2?.a to {your install}\\python2?\\libs\\ (in the same directory
      as python22.lib). This trick should work for all Python versions,
      including future releases of Python. You can also use this trick to
      convert other libraries. (Will see about that soon) 

Tweak Distutils
~~~~~~~~~~~~~~~
From memory, this was not required for my python 2.3 version, I include this
for the sake of completeness.

You can compile and link your Python extensions yourself, but distutil is
the preffered way (it will make all the necessary calls to the different
compilers, call SWIG if necessary and your extensions will be easier to
distribute). Locate build_ext.py in your Python directory (should be somewhere
around C:\\Python22\\Lib\\distutils\\command\\). Change the 2 following lines::

     
    #new_sources.append(base + target_ext) # old
    new_sources.append(base + '_wrap' + target_ext) # new
    
    #swig_cmd = [swig, "-python", "-dnone", "-ISWIG"] # old
    swig_cmd = [swig, "-python"] # new

Compile/install the extension with distutils
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This is how I compiled the pymqi extension..

There seems to be a problem doing the install with the build in one go,
so I first build then I install without building In the setup.py file I
changed the include_dirs to::
     
    C:/Program Files/IBM/WebSphere MQ/Tools/c/include

Library_dirs to::

    C:/Program Files/IBM/WebSphere MQ/Tools/Lib

(note the forward slashes) Then I run::

    setup.py build -cmingw32 client

or::

    setup.py build -cmingw32 server

next the install::

    setup.py install --skip-build

(note I'm doing the install and the build separately) 
