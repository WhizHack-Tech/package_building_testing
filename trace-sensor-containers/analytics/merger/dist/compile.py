from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
ext_modules = [
    Extension("controller",  ["controller.py"]),
    Extension("merger",  ["merger.py"]),
    ]
setup(
    name = 'ZH Merger',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)
