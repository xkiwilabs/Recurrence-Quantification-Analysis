"""Build configuration for the C++ extension module.

All package metadata is in pyproject.toml. This file exists only because
setuptools cannot declare C++ extensions in pyproject.toml yet.
"""
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup
import os

ext_modules = [
    Pybind11Extension(
        "rqa_analysis.utils.rqa_utils_cpp",
        [os.path.join("rqa_analysis", "utils", "rqa_utils.cpp")],
    )
]

setup(
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)
