# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [1.0.1] - 2026-03-28

### Added
- First official release on PyPI
- Auto Recurrence Quantification Analysis (`autoRQA`)
- Cross Recurrence Quantification Analysis (`crossRQA`)
- Multivariate RQA (`multivariateRQA`, `multivariateCrossRQA`) for multi-dimensional data without time-delay embedding
- Diagonal Recurrence Profiles (`DRP`, `crossDRP`)
- High-performance C++ core via pybind11
- Full RQA metrics: %REC, %DET, MaxLine, MeanLine, Entropy, Laminarity, Trapping Time, Vmax, Divergence, Trend
- Data normalization utilities (min-max, z-score, centering)
- Recurrence plot visualization with optional time series overlay
- Signal filtering utilities (Butterworth lowpass, interpolation)
- CSV output for RQA statistics and DRP profiles
- 8 example datasets (physiological, chaotic, categorical, synthetic)
- Jupyter notebook with worked examples
- Comprehensive test suite
- GitHub Actions CI with automated wheel building
- Novice-friendly installation guide with OS-specific instructions

### Fixed
- Package `__init__.py` files were misnamed (`__int__.py`), breaking pip installs
- Incorrect import of `multivariateXRQA` (renamed to `multivariateCrossRQA`)
- Stale exports in `utils/__init__.py` referencing non-existent functions
- Missing imports in `filter_utils.py` (scipy, numpy)
- Inconsistent plot mode checking in `crossRQA`
- Duplicated metrics printing code extracted to shared utility
