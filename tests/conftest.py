"""Shared fixtures for RQA tests."""
import os
import numpy as np
import pandas as pd
import pytest

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "exampleData")


@pytest.fixture
def posture_data():
    """Load PostureData (single time series)."""
    return pd.read_csv(os.path.join(DATA_DIR, "PostureData.csv"), header=None).iloc[:, 0].values


@pytest.fixture
def rocking_chair_data():
    """Load RockingChairData (two time series for cross-RQA)."""
    df = pd.read_csv(os.path.join(DATA_DIR, "RockingChairData.csv"), header=None)
    return df.iloc[:, 0].values, df.iloc[:, 1].values


@pytest.fixture
def white_noise_data():
    """Load WhiteNoiseData (random baseline)."""
    return pd.read_csv(os.path.join(DATA_DIR, "WhiteNoiseData.csv"), header=None).iloc[:, 0].values


@pytest.fixture
def lorenz_xyz():
    """Load 3D Lorenz chaotic data for multivariate RQA."""
    df = pd.read_csv(os.path.join(DATA_DIR, "lorenz_chaotic_xyz.csv"))
    return df[["x", "y", "z"]].values


@pytest.fixture
def lorenz_xyz_2():
    """Load second 3D Lorenz trajectory for cross multivariate RQA."""
    df = pd.read_csv(os.path.join(DATA_DIR, "lorenz_chaotic_xyz_2.csv"))
    return df[["x", "y", "z"]].values


@pytest.fixture
def default_params():
    """Standard RQA parameter set."""
    return {
        "norm": 1,
        "eDim": 3,
        "tLag": 15,
        "rescaleNorm": 1,
        "radius": 0.1,
        "tw": 2,
        "minl": 2,
        "plotMode": "none",
        "pointSize": 2,
        "saveFig": False,
        "showMetrics": False,
        "doStatsFile": False,
    }


@pytest.fixture
def default_drp_params():
    """Standard DRP parameter set."""
    return {
        "norm": 1,
        "eDim": 3,
        "tLag": 15,
        "rescaleNorm": 1,
        "radius": 0.1,
        "tw": 1,
        "maxLag": 100,
        "plotMode": "none",
        "pointSize": 2,
        "saveFig": False,
        "showMetrics": False,
        "doStatsFile": False,
    }
