import glob
import multiprocessing
import os
import sys
from distutils.core import setup
from tempfile import gettempdir

from Cython.Build import cythonize

CPU_COUNT = multiprocessing.cpu_count()

if "-j" not in sys.argv:
    sys.argv.append("-j")
    sys.argv.append(str(CPU_COUNT))

dir_set = set(glob.glob("**/*.py", recursive=True))

dir_set.remove("manage.py")
dir_set.remove("setup.py")

setup(
    ext_modules=cythonize(
        dir_set,
        compiler_directives={"language_level": 3, "annotation_typing": False},
        exclude_failures=True,
        cache=os.path.join(gettempdir(), "cythoncache"),
        nthreads=CPU_COUNT,
    )
)
