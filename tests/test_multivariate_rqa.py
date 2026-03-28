"""Tests for Multivariate Recurrence Quantification Analysis."""
import numpy as np
import pytest
from rqa_analysis import multivariateRQA, multivariateCrossRQA


class TestMultivariateRQA:
    """Tests for multivariate auto-RQA."""

    def test_runs_on_lorenz_data(self, lorenz_xyz, default_params):
        params = {**default_params, "norm": "zscore", "radius": 0.15}
        td, rs, mats, err_code = multivariateRQA(lorenz_xyz, params)
        assert err_code == 0
        assert rs["perc_recur"] > 0

    def test_accepts_list_of_arrays(self, lorenz_xyz, default_params):
        """Should accept list of 1D arrays as input."""
        arrays = [lorenz_xyz[:, i] for i in range(lorenz_xyz.shape[1])]
        params = {**default_params, "norm": "zscore", "radius": 0.15}
        td, rs, mats, err_code = multivariateRQA(arrays, params)
        assert err_code == 0

    def test_rejects_1d_input(self, posture_data, default_params):
        with pytest.raises(ValueError, match="2D"):
            multivariateRQA(posture_data, default_params)

    def test_rejects_single_dimension(self, default_params):
        data = np.random.randn(100, 1)
        with pytest.raises(ValueError, match="at least 2"):
            multivariateRQA(data, default_params)

    def test_lorenz_is_deterministic(self, lorenz_xyz, default_params):
        """Lorenz attractor should show high determinism."""
        params = {**default_params, "norm": "zscore", "radius": 0.15}
        td, rs, mats, err_code = multivariateRQA(lorenz_xyz, params)
        assert rs["perc_determ"] > 50, "Lorenz should be deterministic"

    def test_metrics_bounded(self, lorenz_xyz, default_params):
        params = {**default_params, "norm": "zscore", "radius": 0.15}
        td, rs, mats, err_code = multivariateRQA(lorenz_xyz, params)
        assert 0 <= rs["perc_recur"] <= 100
        assert 0 <= rs["perc_determ"] <= 100
        assert rs["laminarity"] >= 0


class TestMultivariateCrossRQA:
    """Tests for multivariate cross-RQA."""

    def test_runs_on_lorenz_pair(self, lorenz_xyz, lorenz_xyz_2, default_params):
        params = {**default_params, "norm": "zscore", "radius": 0.15}
        td, rs, mats, err_code = multivariateCrossRQA(lorenz_xyz, lorenz_xyz_2, params)
        assert err_code == 0
        assert rs["perc_recur"] > 0

    def test_self_cross_high_recurrence(self, lorenz_xyz, default_params):
        """Cross-RQA of multivariate data with itself should show high recurrence."""
        params = {**default_params, "norm": "zscore", "radius": 0.15}
        td, rs, mats, err_code = multivariateCrossRQA(lorenz_xyz, lorenz_xyz, params)
        assert err_code == 0
        assert rs["perc_recur"] > 1
