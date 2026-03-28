# Contributing

Thanks for your interest in contributing to the RQA Analysis package!

## Development Setup

1. Clone the repository:

```bash
git clone https://github.com/xkiwilabs/Recurrence-Quantification-Analysis.git
cd Recurrence-Quantification-Analysis
```

2. Create a virtual environment and install in development mode:

```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows

pip install -e ".[dev]"
```

This installs the package in editable mode with test dependencies.

## Running Tests

```bash
pytest
```

To run a specific test file:

```bash
pytest tests/test_auto_rqa.py -v
```

## Project Structure

```
.
├── autoRQA.py           # Auto Recurrence Quantification Analysis
├── crossRQA.py          # Cross Recurrence Quantification Analysis
├── multivariateRQA.py   # Multivariate RQA (no embedding needed)
├── diagonalRP.py        # Diagonal Recurrence Profiles
├── __init__.py          # Package exports
├── utils/
│   ├── rqa_utils.cpp    # C++ core (pybind11)
│   ├── norm_utils.py    # Data normalization
│   ├── plot_utils.py    # Visualization
│   ├── output_io_utils.py  # CSV output
│   ├── metrics_utils.py # Console metrics display
│   └── filter_utils.py  # Signal filtering
├── tests/               # pytest test suite
├── exampleData/         # Example datasets
└── analysisExamples.ipynb  # Jupyter notebook examples
```

## Making Changes

1. Create a branch for your work:

```bash
git checkout -b my-feature
```

2. Make your changes and add tests if applicable.

3. Run the test suite to make sure everything passes:

```bash
pytest
```

4. Commit and push:

```bash
git add <files>
git commit -m "Brief description of change"
git push origin my-feature
```

5. Open a Pull Request on GitHub.

## C++ Extension

The core RQA algorithms live in `utils/rqa_utils.cpp` and are compiled via pybind11. After modifying the C++ code, rebuild:

```bash
pip install -e .
```

## Code Style

- Python: Follow existing conventions in the codebase
- C++: C++14 standard, consistent with existing style in `rqa_utils.cpp`
- Keep functions focused and well-documented

## Reporting Issues

Please open an issue on GitHub with:
- What you expected to happen
- What actually happened
- Your OS, Python version, and how you installed the package
- A minimal code example that reproduces the problem
