import os

# Function: Write stats to file
def write_rqa_stats(filename, params, rs, err_code):
    stats_file = "RQA_Stats.csv"

    # Write header only if the file doesn't exist
    if not os.path.exists(stats_file):
        with open(stats_file, "w") as f:
            f.write("filename,eDim,tLag,rescale,radius,perc_recur,perc_determ,maxl_found,"
                    "mean_line,std_line,count_line,entropy,laminarity,trapping_time,"
                    "vmax,divergence,trend_lower_diag,trend_upper_diag\n")

    # Append results
    with open(stats_file, "a") as f:
        f.write(f"{filename}, {params['eDim']}, {params['tLag']}, {params['rescaleNorm']}, {params['radius'] * 100}, ")
        if err_code == 0:
            f.write(
                f"{rs['perc_recur']:.3f}, {rs['perc_determ']:.3f}, {rs['maxl_found']:.2f}, "
                f"{rs['mean_line_length']:.2f}, {rs['std_line_length']:.2f}, {rs['count_line']:.0f}, "
                f"{rs['entropy']:.3f}, {rs['laminarity']:.3f}, {rs['trapping_time']:.3f}, "
                f"{rs['vmax']:.2f}, {rs['divergence']:.3f}, "
                f"{rs['trend_lower_diag']:.3f}, {rs['trend_upper_diag']:.3f}\n"
            )
        else:
            f.write("0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0\n")

def write_drp_profile(filename, params, lags, drp):
    """
    Save full DRP profile (lags + %REC values) to CSV,
    with metadata written into each row.
    """
    import os
    stats_file = "DRP_Profile.csv"
    file_exists = os.path.exists(stats_file)

    if not file_exists:
        with open(stats_file, "w") as f:
            f.write("filename,eDim,tLag,rescale,radius,lag,perc_recur\n")

    with open(stats_file, "a") as f:
        for lag, val in zip(lags, drp):
            f.write(
                f"{filename}, {params['eDim']}, {params['tLag']}, "
                f"{params['rescaleNorm']}, {params['radius'] * 100}, "
                f"{lag}, {val:.6f}\n"
            )

    print(f"DRP profile written to {stats_file}")

