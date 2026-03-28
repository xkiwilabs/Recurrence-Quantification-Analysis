# Installation Guide

This package includes a C++ extension for performance. You need **Python** and a **C++ compiler** before installing.

---

## Prerequisites

### 1. Python (3.12 or newer)

Check your version:

```bash
python3 --version
```

If you don't have Python 3.12+, download it from [python.org](https://www.python.org/downloads/).

### 2. C++ Compiler

The package compiles C++ code during installation. You need a compiler that supports C++14.

#### macOS

Install the Xcode Command Line Tools:

```bash
xcode-select --install
```

A dialog will pop up asking you to confirm. Click **Install** and wait for it to finish.

#### Windows

Install **Visual Studio Build Tools**:

1. Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Run the installer
3. Select **"Desktop development with C++"**
4. Click **Install**

This is a large download (~2 GB). You only need the Build Tools, not the full Visual Studio IDE.

#### Linux (Ubuntu / Debian)

```bash
sudo apt update
sudo apt install build-essential python3-dev
```

#### Linux (Fedora / RHEL)

```bash
sudo dnf install gcc-c++ python3-devel
```

---

## Installation

### Option A: Install from PyPI (recommended)

```bash
pip install rqa-analysis
```

This is the simplest method. If pre-built wheels are available for your platform, no compiler is needed.

### Option B: Install from source (GitHub)

```bash
git clone https://github.com/xkiwilabs/Recurrence-Quantification-Analysis.git
cd Recurrence-Quantification-Analysis
pip install .
```

### Option C: Install in development mode

If you want to modify the code and have changes take effect immediately:

```bash
git clone https://github.com/xkiwilabs/Recurrence-Quantification-Analysis.git
cd Recurrence-Quantification-Analysis
pip install -e ".[dev]"
```

---

## Verify Installation

```python
python3 -c "from rqa_analysis import autoRQA; print('Installation successful!')"
```

---

## Virtual Environments (recommended)

It's best practice to install Python packages in a virtual environment:

```bash
# Create a virtual environment
python3 -m venv rqa_env

# Activate it
# macOS / Linux:
source rqa_env/bin/activate
# Windows:
rqa_env\Scripts\activate

# Install the package
pip install rqa-analysis

# When you're done working:
deactivate
```

---

## Troubleshooting

### "error: command 'gcc' failed" or "error: Microsoft Visual C++ 14.0 is required"

You're missing a C++ compiler. Follow the **Prerequisites** section above for your operating system.

### "ModuleNotFoundError: No module named 'pybind11'"

This should be installed automatically. If not:

```bash
pip install pybind11
pip install rqa-analysis
```

### "fatal error: Python.h: No such file or directory" (Linux)

Install the Python development headers:

```bash
# Ubuntu / Debian
sudo apt install python3-dev

# Fedora / RHEL
sudo dnf install python3-devel
```

### "error: invalid value 'c++14' in '-std=c++14'"

Your compiler is too old. You need GCC 5+ or Clang 3.4+. Update your compiler:

```bash
# Ubuntu / Debian
sudo apt install g++

# macOS (updates via Xcode tools)
xcode-select --install
```

### Import works but functions fail with "symbol not found"

The C++ extension was compiled for a different Python version. Rebuild:

```bash
pip install --force-reinstall --no-cache-dir rqa-analysis
```

### Permission errors

Use `--user` flag or a virtual environment:

```bash
pip install --user rqa-analysis
```

---

## Optional Dependencies

The core package needs only `numpy`, `matplotlib`, and `scipy`. For extra features:

```bash
# Signal filtering utilities (requires pandas)
pip install "rqa-analysis[filtering]"

# Development tools (pytest + pandas)
pip install "rqa-analysis[dev]"
```
