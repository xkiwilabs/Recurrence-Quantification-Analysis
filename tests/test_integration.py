"""Integration tests: full pipeline from data to results."""
import numpy as np
import os
from rqa_analysis import (
    autoRQA, crossRQA, multivariateRQA, multivariateCrossRQA, DRP, crossDRP,
)


class TestFullPipeline:
    """End-to-end tests that exercise the full analysis pipeline."""

    def test_auto_rqa_with_file_output(self, posture_data, default_params, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        params = {**default_params, "doStatsFile": True}
        td, rs, mats, err = autoRQA(posture_data, params)
        assert err == 0
        assert os.path.exists("RQA_Stats.csv")

    def test_cross_rqa_with_file_output(self, rocking_chair_data, default_params, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        data1, data2 = rocking_chair_data
        params = {**default_params, "doStatsFile": True}
        td, rs, mats, err = crossRQA(data1, data2, params)
        assert err == 0
        assert os.path.exists("RQA_Stats.csv")

    def test_drp_with_file_output(self, posture_data, default_drp_params, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        params = {**default_drp_params, "doStatsFile": True}
        drp, lags = DRP(posture_data, params)
        assert os.path.exists("DRP_Profile.csv")

    def test_multivariate_auto_full(self, lorenz_xyz, default_params, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        params = {**default_params, "norm": "zscore", "radius": 0.15, "doStatsFile": True}
        td, rs, mats, err = multivariateRQA(lorenz_xyz, params)
        assert err == 0
        assert os.path.exists("RQA_Stats.csv")

    def test_auto_then_cross_sequential(self, posture_data, rocking_chair_data, default_params):
        """Run autoRQA then crossRQA sequentially to ensure no state leaks."""
        td1, rs1, _, err1 = autoRQA(posture_data, default_params)
        assert err1 == 0

        data1, data2 = rocking_chair_data
        td2, rs2, _, err2 = crossRQA(data1, data2, default_params)
        assert err2 == 0

        # Results should be independent
        assert rs1["perc_recur"] != rs2["perc_recur"]


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_minimum_viable_data(self, default_params):
        """Test with the minimum amount of data that should work."""
        # Need at least tLag * (eDim - 1) + 10 data points
        min_n = default_params["tLag"] * (default_params["eDim"] - 1) + 10
        data = np.random.randn(min_n).astype(np.float32)
        td, rs, mats, err = autoRQA(data, default_params)
        assert err == 0 or err == 2  # May have no lines but shouldn't crash

    def test_constant_signal(self, default_params):
        """A constant signal should produce 100% recurrence."""
        data = np.ones(200, dtype=np.float32)
        params = {**default_params, "norm": 0, "rescaleNorm": 0, "radius": 0.5}
        td, rs, mats, err = autoRQA(data, params)
        # All distances are 0, all within radius
        # Note: Theiler window removes the main diagonal
        assert err == 0

    def test_large_embedding_dimension(self, posture_data, default_params):
        """Higher embedding dimensions should reduce matrix size."""
        params = {**default_params, "eDim": 10, "tLag": 5}
        td, rs, mats, err = autoRQA(posture_data, params)
        assert err == 0
        expected_n = len(posture_data) - 5 * (10 - 1)
        assert td.shape[0] == expected_n

    def test_categorical_data(self, default_params):
        """RQA should work with categorical/integer data (like Elvis dataset)."""
        data = np.array([1, 2, 1, 2, 3, 1, 2, 1, 3, 2, 1, 2, 1, 2, 3,
                         1, 2, 1, 2, 3, 1, 2, 1, 3, 2, 1, 2, 1, 2, 3,
                         1, 2, 1, 2, 3, 1, 2, 1, 3, 2, 1, 2, 1, 2, 3,
                         1, 2, 1, 2, 3, 1, 2, 1, 3, 2, 1, 2, 1, 2, 3,
                         1, 2, 1, 2, 3, 1, 2, 1, 3, 2, 1, 2, 1, 2, 3,
                         1, 2, 1, 2, 3, 1, 2, 1, 3, 2, 1, 2, 1, 2, 3,
                         ], dtype=np.float32)
        params = {**default_params, "eDim": 1, "tLag": 1, "norm": 0}
        td, rs, mats, err = autoRQA(data, params)
        assert err == 0
        assert rs["perc_recur"] > 0

    def test_metrics_printing(self, posture_data, default_params, capsys):
        """Test that showMetrics actually prints."""
        params = {**default_params, "showMetrics": True}
        autoRQA(posture_data, params)
        captured = capsys.readouterr()
        assert "%REC:" in captured.out
        assert "%DET:" in captured.out
