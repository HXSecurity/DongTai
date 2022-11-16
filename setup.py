from distutils.core import setup
from Cython.Build import cythonize
import glob

dir_set = set(glob.glob('**/*.py', recursive=True))

dir_set.remove('manage.py')
dir_set.remove('setup.py')


setup(ext_modules=cythonize(
    dir_set,
    compiler_directives={'language_level': 3},
    exclude_failures=True,
))
