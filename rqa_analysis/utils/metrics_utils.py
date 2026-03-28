def print_rqa_metrics(rs, extra_info=None):
    """Print standard RQA metrics to console.

    Parameters
    ----------
    rs : dict
        Results dictionary from rqa_stats.
    extra_info : str, optional
        Additional line to print after metrics (e.g. dimension info).
    """
    print(f"%REC: {float(rs['perc_recur']):.3f} | %DET: {float(rs['perc_determ']):.3f} | MaxLine: {float(rs['maxl_found']):.2f}")
    print(f"Mean Line Length: {float(rs['mean_line_length']):.2f} | SD Line Length: {float(rs['std_line_length']):.2f} | Line Count: {float(rs['count_line']):.2f}")
    print(f"ENTR: {float(rs['entropy']):.3f} | LAM: {float(rs['laminarity']):.3f} | TT: {float(rs['trapping_time']):.3f}")
    print(f"Vmax: {float(rs['vmax']):.2f} | Divergence: {float(rs['divergence']):.3f}")
    print(f"Trend_Lower: {float(rs['trend_lower_diag']):.3f} | Trend_Upper {float(rs['trend_upper_diag']):.3f}")
    if extra_info:
        print(extra_info)
