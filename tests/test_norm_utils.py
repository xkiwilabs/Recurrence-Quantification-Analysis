"""Tests for normalization utilities."""
import numpy as np
import pytest
from rqa_analysis.utils.norm_utils import normalize_data


class TestNormalizeData:
    """Tests for normalize_data function."""

    def test_minmax_1d(self):
        data = np.array([1.0, 5.0, 3.0, 9.0, 2.0])
        result = normalize_data(data, "minmax")
        assert np.isclose(result.min(), 0.0)
        assert np.isclose(result.max(), 1.0)

    def test_minmax_by_int(self):
        data = np.array([1.0, 5.0, 3.0, 9.0])
        result = normalize_data(data, 1)
        assert np.isclose(result.min(), 0.0)
        assert np.isclose(result.max(), 1.0)

    def test_zscore_1d(self):
        data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        result = normalize_data(data, "zscore")
        assert np.isclose(np.mean(result), 0.0, atol=1e-10)
        assert np.isclose(np.std(result), 1.0, atol=1e-10)

    def test_zscore_by_int(self):
        data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        result = normalize_data(data, 2)
        assert np.isclose(np.mean(result), 0.0, atol=1e-10)

    def test_center_1d(self):
        data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        result = normalize_data(data, "center")
        assert np.isclose(np.mean(result), 0.0, atol=1e-10)

    def test_center_by_int(self):
        data = np.array([10.0, 20.0, 30.0])
        result = normalize_data(data, 3)
        assert np.isclose(np.mean(result), 0.0, atol=1e-10)

    def test_none_passthrough(self):
        data = np.array([1.0, 2.0, 3.0])
        result = normalize_data(data, "none")
        np.testing.assert_array_equal(result, data)

    def test_none_by_int_zero(self):
        data = np.array([1.0, 2.0, 3.0])
        result = normalize_data(data, 0)
        np.testing.assert_array_equal(result, data)

    def test_invalid_norm_raises(self):
        data = np.array([1.0, 2.0])
        with pytest.raises(ValueError, match="Invalid norm"):
            normalize_data(data, "bogus")

    def test_minmax_2d(self):
        data = np.array([[1.0, 10.0], [2.0, 20.0], [3.0, 30.0]])
        result = normalize_data(data, "minmax")
        assert result.shape == data.shape
        assert np.isclose(result[:, 0].min(), 0.0)
        assert np.isclose(result[:, 0].max(), 1.0)

    def test_zscore_2d(self):
        data = np.array([[1.0, 10.0], [2.0, 20.0], [3.0, 30.0]])
        result = normalize_data(data, "zscore")
        for col in range(result.shape[1]):
            assert np.isclose(np.mean(result[:, col]), 0.0, atol=1e-10)

    def test_preserves_shape(self):
        data = np.random.randn(100)
        for norm in ["minmax", "zscore", "center", "none"]:
            result = normalize_data(data, norm)
            assert result.shape == data.shape, f"Shape changed with norm={norm}"
