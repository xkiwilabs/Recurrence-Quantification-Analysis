"""Tests for signal filtering utilities."""
import numpy as np
from rqa_analysis.utils.filter_utils import butter_lowpass, apply_filter


class TestFilterUtils:
    """Tests for filtering functions."""

    def test_butter_lowpass_returns_coefficients(self):
        b, a = butter_lowpass(cutoff=10, fs=100, order=4)
        assert len(b) > 0
        assert len(a) > 0

    def test_apply_filter_preserves_length(self):
        data = np.random.randn(200)
        result = apply_filter(data, cutoff=10, fs=100, order=4)
        assert len(result) == len(data)

    def test_lowpass_removes_high_frequency(self):
        """A lowpass filter should attenuate high-frequency components."""
        fs = 100.0
        t = np.arange(0, 2, 1 / fs)
        # Low freq (5 Hz) + high freq (40 Hz)
        signal = np.sin(2 * np.pi * 5 * t) + np.sin(2 * np.pi * 40 * t)
        filtered = apply_filter(signal, cutoff=15, fs=fs, order=4)
        # After filtering, high-freq energy should be reduced
        # Check that variance of difference from low-freq component is small
        low_only = np.sin(2 * np.pi * 5 * t)
        # Trim edges to avoid filter transients
        trim = 50
        residual = np.std(filtered[trim:-trim] - low_only[trim:-trim])
        assert residual < 0.5, "Lowpass filter should remove 40 Hz component"
