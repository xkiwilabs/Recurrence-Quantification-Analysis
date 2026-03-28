"""Tests for plot utilities (non-visual, just ensure no errors)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for testing
from rqa_analysis.utils.plot_utils import plot_rqa_results, plot_drp_results


class TestPlotRqaResults:
    """Smoke tests for plot_rqa_results (no visual verification)."""

    def test_auto_rqa_plot_no_error(self):
        n = 50
        td = np.random.randint(0, 2, (n, n)).astype(np.int8)
        data = np.random.randn(n)
        plot_rqa_results(dataX=data, td=td, plot_mode="rp")

    def test_cross_rqa_plot_no_error(self):
        n = 50
        td = np.random.randint(0, 2, (n, n)).astype(np.int8)
        dataX = np.random.randn(n)
        dataY = np.random.randn(n)
        plot_rqa_results(dataX=dataX, dataY=dataY, td=td, plot_mode="rp")

    def test_timeseries_mode_no_error(self):
        n = 50
        td = np.random.randint(0, 2, (n, n)).astype(np.int8)
        data = np.random.randn(n)
        plot_rqa_results(dataX=data, td=td, plot_mode="rp-timeseries")

    def test_cross_timeseries_mode_no_error(self):
        n = 50
        td = np.random.randint(0, 2, (n, n)).astype(np.int8)
        dataX = np.random.randn(n)
        dataY = np.random.randn(n)
        plot_rqa_results(dataX=dataX, dataY=dataY, td=td, plot_mode="rp-timeseries")

    def test_save_to_file(self, tmp_path):
        n = 50
        td = np.random.randint(0, 2, (n, n)).astype(np.int8)
        data = np.random.randn(n)
        save_path = str(tmp_path / "test_plot.png")
        plot_rqa_results(dataX=data, td=td, plot_mode="rp", save_path=save_path)
        import os
        assert os.path.exists(save_path)


class TestPlotDrpResults:
    """Smoke tests for plot_drp_results."""

    def test_drp_plot_no_error(self):
        lags = np.arange(-20, 21)
        drp = np.random.rand(41) * 10
        plot_drp_results(lags=lags, drp=drp)

    def test_save_to_file(self, tmp_path):
        lags = np.arange(-10, 11)
        drp = np.random.rand(21) * 10
        save_path = str(tmp_path / "test_drp.png")
        plot_drp_results(lags=lags, drp=drp, save_path=save_path)
        import os
        assert os.path.exists(save_path)
