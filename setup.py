"""Build configuration for the C++ extension module.

All package metadata is in pyproject.toml. This file exists only because
setuptools cannot declare C++ extensions in pyproject.toml yet.
"""
from setuptools import setup, Extension
import pybind11
import os
import sys

extra_compile_args = []
if sys.platform == "win32":
    extra_compile_args = ["/std:c++14"]
else:
    extra_compile_args = ["-std=c++14"]

ext_modules = [
    Extension(
        "rqa_analysis.utils.rqa_utils_cpp",
        [os.path.join("rqa_analysis", "utils", "rqa_utils.cpp")],
        include_dirs=[pybind11.get_include()],
        language="c++",
        extra_compile_args=extra_compile_args,
    )
]

setup(ext_modules=ext_modules)
