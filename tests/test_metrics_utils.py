"""Tests for metrics printing utility."""
from rqa_analysis.utils.metrics_utils import print_rqa_metrics


class TestPrintRqaMetrics:
    """Tests for print_rqa_metrics."""

    def test_prints_without_error(self, capsys):
        rs = {
            "perc_recur": 5.123,
            "perc_determ": 82.456,
            "maxl_found": 150.0,
            "mean_line_length": 4.56,
            "std_line_length": 2.34,
            "count_line": 100.0,
            "entropy": 2.345,
            "laminarity": 0.678,
            "trapping_time": 3.456,
            "vmax": 25.0,
            "divergence": 0.007,
            "trend_lower_diag": -0.123,
            "trend_upper_diag": 0.456,
        }
        print_rqa_metrics(rs)
        captured = capsys.readouterr()
        assert "%REC:" in captured.out
        assert "%DET:" in captured.out
        assert "ENTR:" in captured.out
        assert "LAM:" in captured.out

    def test_prints_extra_info(self, capsys):
        rs = {
            "perc_recur": 0.0, "perc_determ": 0.0, "maxl_found": 0.0,
            "mean_line_length": 0.0, "std_line_length": 0.0, "count_line": 0.0,
            "entropy": 0.0, "laminarity": 0.0, "trapping_time": 0.0,
            "vmax": 0.0, "divergence": 0.0,
            "trend_lower_diag": 0.0, "trend_upper_diag": 0.0,
        }
        print_rqa_metrics(rs, extra_info="Dimensions: 3 | Analysis: MultivariateRQA")
        captured = capsys.readouterr()
        assert "Dimensions: 3" in captured.out
