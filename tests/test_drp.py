"""Tests for Diagonal Recurrence Profiles."""
import numpy as np
from rqa_analysis import DRP, crossDRP


class TestDRP:
    """Tests for auto DRP."""

    def test_runs_on_posture_data(self, posture_data, default_drp_params):
        drp, lags = DRP(posture_data, default_drp_params)
        assert len(drp) > 0
        assert len(drp) == len(lags)

    def test_lags_centered_at_zero(self, posture_data, default_drp_params):
        drp, lags = DRP(posture_data, default_drp_params)
        assert 0 in lags

    def test_drp_values_nonnegative(self, posture_data, default_drp_params):
        drp, lags = DRP(posture_data, default_drp_params)
        assert np.all(drp >= 0), "DRP values should be non-negative"

    def test_drp_values_bounded(self, posture_data, default_drp_params):
        drp, lags = DRP(posture_data, default_drp_params)
        assert np.all(drp <= 100), "DRP values should be <= 100 (percent)"

    def test_max_lag_truncation(self, posture_data, default_drp_params):
        max_lag = 50
        params = {**default_drp_params, "maxLag": max_lag}
        drp, lags = DRP(posture_data, params)
        assert np.all(np.abs(lags) <= max_lag)

    def test_symmetric_for_auto(self, posture_data, default_drp_params):
        """Auto DRP should be symmetric around lag=0."""
        drp, lags = DRP(posture_data, default_drp_params)
        center = np.where(lags == 0)[0][0]
        n = min(center, len(drp) - center - 1)
        left = drp[center - n:center]
        right = drp[center + 1:center + n + 1][::-1]
        np.testing.assert_allclose(left, right, atol=1e-10,
                                   err_msg="Auto DRP should be symmetric")

    def test_sinusoid_has_periodic_structure(self, default_drp_params):
        """DRP of a sine wave should show periodic recurrence structure."""
        t = np.arange(500, dtype=np.float32)
        data = np.sin(2 * np.pi * t / 50)
        params = {**default_drp_params, "eDim": 1, "tLag": 1, "maxLag": 200, "radius": 0.2}
        drp, lags = DRP(data, params)
        # Sine wave DRP should have recurrence above zero at multiple lags
        assert np.mean(drp) > 0, "Sine wave should show recurrence"
        # Should have variation (periodic peaks and valleys)
        assert np.std(drp) > 0, "DRP should show periodic variation"


class TestCrossDRP:
    """Tests for cross DRP."""

    def test_runs_on_rocking_chair_data(self, rocking_chair_data, default_drp_params):
        data1, data2 = rocking_chair_data
        drp, lags = crossDRP(data1, data2, default_drp_params)
        assert len(drp) > 0
        assert len(drp) == len(lags)

    def test_drp_values_bounded(self, rocking_chair_data, default_drp_params):
        data1, data2 = rocking_chair_data
        drp, lags = crossDRP(data1, data2, default_drp_params)
        assert np.all(drp >= 0)
        assert np.all(drp <= 100)
