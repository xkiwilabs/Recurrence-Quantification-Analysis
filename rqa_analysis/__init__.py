# Import key functions from auto_rqa, cross_rqa, and multivariate_rqa
from .autoRQA import autoRQA
from .crossRQA import crossRQA
from .multivariateRQA import multivariateRQA, multivariateXRQA

# Optionally import utilities for advanced users
from .utils.norm_utils import normalize_data
from .utils.plot_utils import plot_rqa_results
from .utils.output_io_utils import write_rqa_stats

# Define what the package exports
__all__ = [
    "autoRQA",
    "crossRQA",
    "multivariateRQA",
    "multivariateXRQA",
    "normalize_data",
    "plot_rqa_results",
    "write_rqa_stats"
]