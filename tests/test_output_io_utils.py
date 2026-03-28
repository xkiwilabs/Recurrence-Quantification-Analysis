"""Tests for output I/O utilities."""
import os
import numpy as np
import pytest
from rqa_analysis.utils.output_io_utils import write_rqa_stats, write_drp_profile


class TestWriteRqaStats:
    """Tests for write_rqa_stats CSV output."""

    def test_creates_csv_file(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        params = {"eDim": 3, "tLag": 15, "rescaleNorm": 1, "radius": 0.1}
        rs = {
            "perc_recur": 5.0, "perc_determ": 80.0, "maxl_found": 100.0,
            "mean_line_length": 4.0, "std_line_length": 2.0, "count_line": 50,
            "entropy": 2.0, "laminarity": 0.7, "trapping_time": 3.0,
            "vmax": 20.0, "divergence": 0.01,
            "trend_lower_diag": -0.1, "trend_upper_diag": 0.2,
        }
        write_rqa_stats("test_data", params, rs, err_code=0)
        assert os.path.exists("RQA_Stats.csv")

    def test_csv_has_header(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        params = {"eDim": 3, "tLag": 15, "rescaleNorm": 1, "radius": 0.1}
        rs = {
            "perc_recur": 5.0, "perc_determ": 80.0, "maxl_found": 100.0,
            "mean_line_length": 4.0, "std_line_length": 2.0, "count_line": 50,
            "entropy": 2.0, "laminarity": 0.7, "trapping_time": 3.0,
            "vmax": 20.0, "divergence": 0.01,
            "trend_lower_diag": -0.1, "trend_upper_diag": 0.2,
        }
        write_rqa_stats("test_data", params, rs, err_code=0)
        with open("RQA_Stats.csv") as f:
            header = f.readline()
        assert "filename" in header
        assert "perc_recur" in header

    def test_appends_multiple_entries(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        params = {"eDim": 3, "tLag": 15, "rescaleNorm": 1, "radius": 0.1}
        rs = {
            "perc_recur": 5.0, "perc_determ": 80.0, "maxl_found": 100.0,
            "mean_line_length": 4.0, "std_line_length": 2.0, "count_line": 50,
            "entropy": 2.0, "laminarity": 0.7, "trapping_time": 3.0,
            "vmax": 20.0, "divergence": 0.01,
            "trend_lower_diag": -0.1, "trend_upper_diag": 0.2,
        }
        write_rqa_stats("run1", params, rs, err_code=0)
        write_rqa_stats("run2", params, rs, err_code=0)
        with open("RQA_Stats.csv") as f:
            lines = f.readlines()
        assert len(lines) == 3  # header + 2 data rows

    def test_error_code_writes_zeros(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        params = {"eDim": 3, "tLag": 15, "rescaleNorm": 1, "radius": 0.1}
        write_rqa_stats("error_run", params, {}, err_code=1)
        with open("RQA_Stats.csv") as f:
            lines = f.readlines()
        assert "0.0" in lines[1]


class TestWriteDrpProfile:
    """Tests for write_drp_profile CSV output."""

    def test_creates_csv_file(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        params = {"eDim": 3, "tLag": 15, "rescaleNorm": 1, "radius": 0.1}
        lags = np.array([-2, -1, 0, 1, 2])
        drp = np.array([0.1, 0.2, 0.5, 0.2, 0.1])
        write_drp_profile("test_drp", params, lags, drp)
        assert os.path.exists("DRP_Profile.csv")

    def test_writes_one_row_per_lag(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        params = {"eDim": 3, "tLag": 15, "rescaleNorm": 1, "radius": 0.1}
        lags = np.array([-2, -1, 0, 1, 2])
        drp = np.array([0.1, 0.2, 0.5, 0.2, 0.1])
        write_drp_profile("test_drp", params, lags, drp)
        with open("DRP_Profile.csv") as f:
            lines = f.readlines()
        assert len(lines) == 6  # header + 5 lag rows
