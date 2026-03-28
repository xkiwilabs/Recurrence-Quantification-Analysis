"""Tests for the C++ extension module directly."""
import numpy as np
import pytest
from rqa_analysis.utils import rqa_utils_cpp


class TestRqaDist:
    """Tests for rqa_dist (distance matrix computation)."""

    def test_returns_dict_with_expected_keys(self):
        a = np.random.randn(100).astype(np.float32)
        ds = rqa_utils_cpp.rqa_dist(a, a, dim=1, lag=1)
        assert "d" in ds
        assert "dim" in ds
        assert "lag" in ds

    def test_distance_matrix_is_square(self):
        a = np.random.randn(100).astype(np.float32)
        ds = rqa_utils_cpp.rqa_dist(a, a, dim=2, lag=5)
        d = ds["d"]
        assert d.shape[0] == d.shape[1]

    def test_self_distance_diagonal_is_zero(self):
        a = np.arange(50, dtype=np.float32)
        ds = rqa_utils_cpp.rqa_dist(a, a, dim=1, lag=1)
        d = ds["d"]
        np.testing.assert_allclose(np.diag(d), 0.0, atol=1e-6)

    def test_distance_is_nonnegative(self):
        a = np.random.randn(100).astype(np.float32)
        b = np.random.randn(100).astype(np.float32)
        ds = rqa_utils_cpp.rqa_dist(a, b, dim=2, lag=5)
        assert np.all(ds["d"] >= 0)

    def test_distance_is_symmetric_for_self(self):
        a = np.random.randn(100).astype(np.float32)
        ds = rqa_utils_cpp.rqa_dist(a, a, dim=3, lag=5)
        d = ds["d"]
        np.testing.assert_allclose(d, d.T, atol=1e-6)

    def test_output_size_matches_embedding(self):
        n = 100
        dim = 3
        lag = 5
        a = np.random.randn(n).astype(np.float32)
        ds = rqa_utils_cpp.rqa_dist(a, a, dim=dim, lag=lag)
        expected_n = n - lag * (dim - 1)
        assert ds["d"].shape == (expected_n, expected_n)

    def test_short_series_raises(self):
        a = np.array([1.0, 2.0, 3.0], dtype=np.float32)
        with pytest.raises(RuntimeError):
            rqa_utils_cpp.rqa_dist(a, a, dim=3, lag=5)


class TestRqaRadius:
    """Tests for rqa_radius (thresholding)."""

    def test_returns_binary_matrix(self):
        d = np.random.rand(50, 50).astype(np.float32)
        td = rqa_utils_cpp.rqa_radius(d, rescale=1, rad=0.5, diag_ignore=0)
        unique = set(np.unique(td))
        assert unique <= {0, 1}

    def test_larger_radius_more_recurrence(self):
        d = np.random.rand(50, 50).astype(np.float32)
        td_small = rqa_utils_cpp.rqa_radius(d, rescale=1, rad=0.1, diag_ignore=0)
        td_large = rqa_utils_cpp.rqa_radius(d, rescale=1, rad=0.5, diag_ignore=0)
        assert np.sum(td_large) >= np.sum(td_small)

    def test_diag_ignore_zeros_diagonals(self):
        d = np.zeros((20, 20), dtype=np.float32)  # All distances = 0
        td = rqa_utils_cpp.rqa_radius(d, rescale=0, rad=1.0, diag_ignore=2)
        # Main diagonal and one off-diagonal should be zeroed
        assert td[0, 0] == 0
        assert td[0, 1] == 0
        assert td[1, 0] == 0

    def test_negative_radius_raises(self):
        d = np.random.rand(20, 20).astype(np.float32)
        with pytest.raises(RuntimeError):
            rqa_utils_cpp.rqa_radius(d, rescale=0, rad=-0.1, diag_ignore=0)


class TestRqaStats:
    """Tests for rqa_stats (full analysis)."""

    def test_returns_four_elements(self):
        a = np.random.randn(200).astype(np.float32)
        ds = rqa_utils_cpp.rqa_dist(a, a, dim=3, lag=5)
        result = rqa_utils_cpp.rqa_stats(ds["d"], rescale=1, rad=0.1, diag_ignore=2, minl=2)
        assert len(result) == 4  # td, rs, mats, err_code

    def test_auto_mode_ignores_diagonals(self):
        a = np.random.randn(200).astype(np.float32)
        ds = rqa_utils_cpp.rqa_dist(a, a, dim=3, lag=5)
        td, rs, mats, err = rqa_utils_cpp.rqa_stats(
            ds["d"], rescale=1, rad=0.1, diag_ignore=2, minl=2, rqa_mode="auto"
        )
        assert rs["diag_ignore"] == 2

    def test_cross_mode_no_diag_ignore(self):
        a = np.random.randn(200).astype(np.float32)
        b = np.random.randn(200).astype(np.float32)
        ds = rqa_utils_cpp.rqa_dist(a, b, dim=3, lag=5)
        td, rs, mats, err = rqa_utils_cpp.rqa_stats(
            ds["d"], rescale=1, rad=0.1, diag_ignore=5, minl=2, rqa_mode="cross"
        )
        # Cross mode should override diag_ignore to 0
        assert rs["diag_ignore"] == 0


class TestRqaDistMultivariate:
    """Tests for rqa_dist_multivariate."""

    def test_returns_dict(self):
        data = np.random.randn(100, 3).astype(np.float32)
        ds = rqa_utils_cpp.rqa_dist_multivariate(data, data)
        assert "d" in ds
        assert ds["multivariate"] == True
        assert ds["lag"] == 0

    def test_distance_matrix_shape(self):
        n = 100
        data = np.random.randn(n, 3).astype(np.float32)
        ds = rqa_utils_cpp.rqa_dist_multivariate(data, data)
        assert ds["d"].shape == (n, n)

    def test_self_distance_diagonal_zero(self):
        data = np.random.randn(50, 2).astype(np.float32)
        ds = rqa_utils_cpp.rqa_dist_multivariate(data, data)
        np.testing.assert_allclose(np.diag(ds["d"]), 0.0, atol=1e-5)

    def test_dimension_mismatch_raises(self):
        a = np.random.randn(50, 2).astype(np.float32)
        b = np.random.randn(50, 3).astype(np.float32)
        with pytest.raises(RuntimeError, match="same number of dimensions"):
            rqa_utils_cpp.rqa_dist_multivariate(a, b)

    def test_short_series_raises(self):
        data = np.random.randn(5, 2).astype(np.float32)
        with pytest.raises(RuntimeError, match="too short"):
            rqa_utils_cpp.rqa_dist_multivariate(data, data)


class TestRqaDrp:
    """Tests for rqa_drp (diagonal recurrence profile)."""

    def test_output_length(self):
        n = 30
        td = np.random.randint(0, 2, (n, n)).astype(np.int8)
        drp = rqa_utils_cpp.rqa_drp(td)
        assert len(drp) == 2 * n - 1

    def test_all_ones_matrix(self):
        n = 20
        td = np.ones((n, n), dtype=np.int8)
        drp = rqa_utils_cpp.rqa_drp(td)
        # All diagonals should be 100% recurrence
        np.testing.assert_allclose(drp, 100.0, atol=1e-10)

    def test_all_zeros_matrix(self):
        n = 20
        td = np.zeros((n, n), dtype=np.int8)
        drp = rqa_utils_cpp.rqa_drp(td)
        np.testing.assert_allclose(drp, 0.0, atol=1e-10)

    def test_values_bounded(self):
        td = np.random.randint(0, 2, (50, 50)).astype(np.int8)
        drp = rqa_utils_cpp.rqa_drp(td)
        assert np.all(drp >= 0)
        assert np.all(drp <= 100)
