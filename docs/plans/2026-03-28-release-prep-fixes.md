# Release Preparation — All Fixes Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix all bugs, modernize packaging, add docs and tests so the package can be published to PyPI as a proper `pip install rqa-analysis` release.

**Architecture:** Fix broken `__init__.py` filenames, clean up imports/exports, extract duplicated code, modernize to `pyproject.toml`-only build, add MANIFEST.in, add novice-friendly docs, add smoke tests, add GitHub Actions CI with cibuildwheel.

**Tech Stack:** Python 3.9+, pybind11/C++14, pytest, GitHub Actions, cibuildwheel

---

### Task 1: Rename `__int__.py` → `__init__.py` (both locations)

**Files:**
- Rename: `__int__.py` → `__init__.py`
- Rename: `utils/__int__.py` → `utils/__init__.py`

**Step 1: Rename files via git mv**

```bash
cd /home/mrichardson/Projects/Recurrence-Quantification-Analysis
git mv __int__.py __init__.py
git mv utils/__int__.py utils/__init__.py
```

**Step 2: Verify**

```bash
ls __init__.py utils/__init__.py
```
Expected: both files listed.

---

### Task 2: Fix root `__init__.py` — bad import + missing exports

**Files:**
- Modify: `__init__.py` (after rename)

**Changes:**
- Line 4: `multivariateXRQA` → `multivariateCrossRQA`
- Line 16: same fix in `__all__`
- Add imports for `DRP`, `crossDRP`, `diagonalRP`
- Add `filter_utils` imports (after Task 4 fixes it)

---

### Task 3: Fix `utils/__init__.py` — stale exports

**Files:**
- Modify: `utils/__init__.py` (after rename)

**Changes:**
- Remove `xRQA_dist` and `xRQA_stats` from `__all__` (they don't exist)
- Add exports for `write_drp_profile`, `plot_drp_results`

---

### Task 4: Fix `utils/filter_utils.py` — add missing imports

**Files:**
- Modify: `utils/filter_utils.py`

**Changes:**
- Add `from scipy.signal import butter, filtfilt`
- Add `import pandas as pd` (for type hints in docstrings)

---

### Task 5: Extract duplicated metrics printing

**Files:**
- Create: `utils/metrics_utils.py`
- Modify: `autoRQA.py`
- Modify: `crossRQA.py`
- Modify: `multivariateRQA.py`

**Changes:**
- Create `print_rqa_metrics(rs, extra_info=None)` function
- Replace 5-line print blocks in all three files with single call

---

### Task 6: Fix `crossRQA.py` plot mode check

**Files:**
- Modify: `crossRQA.py:39`

**Change:** `if 'rp' in params['plotMode']` → `if params.get('plotMode', 'rp') in ('rp', 'rp-timeseries')`

---

### Task 7: Modernize `pyproject.toml` + remove `setup.py`

**Files:**
- Rewrite: `pyproject.toml` (full PEP 621 metadata)
- Delete: `setup.py`

**Changes:**
- Move all metadata from setup.py into pyproject.toml
- Add classifiers, python_requires, project URLs
- Use setuptools + pybind11 build backend
- Keep C++ extension config

---

### Task 8: Add `MANIFEST.in`

**Files:**
- Create: `MANIFEST.in`

**Content:** Include `utils/*.cpp`, `exampleData/`, `LICENSE`, `README.md`, etc.

---

### Task 9: Add `INSTALL.md` (novice-friendly)

**Files:**
- Create: `INSTALL.md`

**Content:** OS-by-OS prerequisites (Python, C++ compiler), pip install, building from source, common errors.

---

### Task 10: Add `CONTRIBUTING.md`

**Files:**
- Create: `CONTRIBUTING.md`

**Content:** Dev setup, running tests, code style, PR process.

---

### Task 11: Add `CHANGELOG.md`

**Files:**
- Create: `CHANGELOG.md`

**Content:** Initial 1.0.0 release notes.

---

### Task 12: Add basic pytest smoke tests

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/test_auto_rqa.py`
- Create: `tests/test_cross_rqa.py`
- Create: `tests/test_multivariate_rqa.py`
- Create: `tests/test_drp.py`
- Create: `tests/test_norm_utils.py`

**Content:** Smoke tests using example data, known-answer tests for white noise vs chaotic data.

---

### Task 13: Add GitHub Actions CI

**Files:**
- Create: `.github/workflows/tests.yml`
- Create: `.github/workflows/build-wheels.yml`

**Content:** Run tests on push, build wheels with cibuildwheel on release tags.

---

### Task 14: Update `README.md`

**Changes:**
- Update install instructions for PyPI (`pip install rqa-analysis`)
- Fix import examples to use package name
- Add badges (CI, PyPI version)
- Link to INSTALL.md for troubleshooting

---

### Task 15: Update `.gitignore`

**Changes:**
- Clean up duplicates
- Add `dist/`, `*.egg-info/`, `.pytest_cache/`, standard Python ignores

---
