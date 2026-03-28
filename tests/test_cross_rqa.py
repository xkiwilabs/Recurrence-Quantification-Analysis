"""Tests for Cross Recurrence Quantification Analysis."""
import numpy as np
from rqa_analysis import crossRQA


class TestCrossRQA:
    """Smoke tests for crossRQA."""

    def test_runs_on_rocking_chair_data(self, rocking_chair_data, default_params):
        data1, data2 = rocking_chair_data
        td, rs, mats, err_code = crossRQA(data1, data2, default_params)
        assert err_code == 0
        assert rs["perc_recur"] > 0

    def test_returns_expected_keys(self, rocking_chair_data, default_params):
        data1, data2 = rocking_chair_data
        td, rs, mats, err_code = crossRQA(data1, data2, default_params)
        expected_keys = [
            "perc_recur", "perc_determ", "maxl_found",
            "mean_line_length", "entropy", "laminarity",
        ]
        for key in expected_keys:
            assert key in rs, f"Missing key: {key}"

    def test_identical_series_high_recurrence(self, posture_data, default_params):
        """Cross-RQA of a signal with itself should show high recurrence."""
        td, rs, mats, err_code = crossRQA(posture_data, posture_data, default_params)
        assert err_code == 0
        assert rs["perc_recur"] > 0, "Self cross-RQA should show some recurrence"

    def test_uncorrelated_signals_low_recurrence(self, default_params):
        """Two independent random signals should have low cross-recurrence."""
        np.random.seed(42)
        data1 = np.random.randn(500).astype(np.float32)
        data2 = np.random.randn(500).astype(np.float32)
        td, rs, mats, err_code = crossRQA(data1, data2, default_params)
        assert err_code == 0
        assert rs["perc_determ"] < 50

    def test_thresholded_matrix_is_binary(self, rocking_chair_data, default_params):
        data1, data2 = rocking_chair_data
        td, rs, mats, err_code = crossRQA(data1, data2, default_params)
        unique_vals = set(np.unique(td))
        assert unique_vals <= {0, 1}

    def test_cross_rqa_no_theiler_window(self, rocking_chair_data, default_params):
        """Cross-RQA should not ignore any diagonals (diag_ignore=0)."""
        data1, data2 = rocking_chair_data
        td, rs, mats, err_code = crossRQA(data1, data2, default_params)
        assert rs["diag_ignore"] == 0
