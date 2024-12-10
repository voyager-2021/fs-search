from setuptools import setup
from Cython.Build import cythonize


if __name__ == '__main__':
    setup(
        ext_modules=cythonize("fs_search/*.py", compiler_directives={'language_level': "3"}),
    )