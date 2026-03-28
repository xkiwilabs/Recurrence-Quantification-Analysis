"""Tests for Auto Recurrence Quantification Analysis."""
import numpy as np
from rqa_analysis import autoRQA


class TestAutoRQA:
    """Smoke tests for autoRQA."""

    def test_runs_on_posture_data(self, posture_data, default_params):
        td, rs, mats, err_code = autoRQA(posture_data, default_params)
        assert err_code == 0
        assert td is not None
        assert rs["perc_recur"] > 0

    def test_returns_expected_keys(self, posture_data, default_params):
        td, rs, mats, err_code = autoRQA(posture_data, default_params)
        expected_keys = [
            "perc_recur", "perc_determ", "maxl_found",
            "mean_line_length", "std_line_length", "count_line",
            "entropy", "laminarity", "trapping_time",
            "vmax", "divergence", "trend_lower_diag", "trend_upper_diag",
        ]
        for key in expected_keys:
            assert key in rs, f"Missing key: {key}"

    def test_white_noise_low_determinism(self, white_noise_data, default_params):
        """White noise should have very low %DET compared to structured data."""
        td, rs, mats, err_code = autoRQA(white_noise_data, default_params)
        assert err_code == 0
        assert rs["perc_determ"] < 50, "White noise should not be highly deterministic"

    def test_thresholded_matrix_is_binary(self, posture_data, default_params):
        td, rs, mats, err_code = autoRQA(posture_data, default_params)
        unique_vals = set(np.unique(td))
        assert unique_vals <= {0, 1}, f"Expected binary matrix, got values: {unique_vals}"

    def test_thresholded_matrix_shape(self, posture_data, default_params):
        td, rs, mats, err_code = autoRQA(posture_data, default_params)
        assert td.shape[0] == td.shape[1], "Thresholded matrix should be square"
        n = len(posture_data) - default_params["tLag"] * (default_params["eDim"] - 1)
        assert td.shape[0] == n

    def test_different_norm_methods(self, posture_data, default_params):
        """All normalization methods should produce valid results."""
        for norm in [0, 1, 2, 3]:
            params = {**default_params, "norm": norm}
            td, rs, mats, err_code = autoRQA(posture_data, params)
            assert err_code == 0, f"Failed with norm={norm}"

    def test_different_embedding_dims(self, posture_data, default_params):
        for dim in [1, 2, 5]:
            params = {**default_params, "eDim": dim}
            td, rs, mats, err_code = autoRQA(posture_data, params)
            assert err_code == 0, f"Failed with eDim={dim}"

    def test_metrics_are_nonnegative(self, posture_data, default_params):
        td, rs, mats, err_code = autoRQA(posture_data, default_params)
        assert rs["perc_recur"] >= 0
        assert rs["perc_determ"] >= 0
        assert rs["entropy"] >= 0
        assert rs["laminarity"] >= 0
        assert rs["trapping_time"] >= 0

    def test_recurrence_bounded(self, posture_data, default_params):
        td, rs, mats, err_code = autoRQA(posture_data, default_params)
        assert 0 <= rs["perc_recur"] <= 100
        assert 0 <= rs["perc_determ"] <= 100

    def test_sinusoid_high_determinism(self, default_params):
        """A pure sine wave should be highly deterministic."""
        t = np.linspace(0, 10 * np.pi, 1000)
        data = np.sin(t).astype(np.float32)
        params = {**default_params, "radius": 0.15}
        td, rs, mats, err_code = autoRQA(data, params)
        assert err_code == 0
        assert rs["perc_determ"] > 80, "Sine wave should be highly deterministic"
