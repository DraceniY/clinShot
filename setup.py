from distutils.core import setup

from Cython.Build import cythonize

setup(ext_modules=cythonize("complementTools.pyx", nthreads=0, language_level="3"))
