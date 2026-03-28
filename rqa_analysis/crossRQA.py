from .utils import norm_utils, plot_utils, output_io_utils
from .utils.metrics_utils import print_rqa_metrics
from .utils import rqa_utils_cpp
import os

def crossRQA(data1, data2, params):
    """
    Perform Cross Recurrence Quantification Analysis (RQA).
    Parameters:
        data1 (np.ndarray): Time series data 1.
        data2 (np.ndarray): Time series data 2.
        params (dict): Dictionary of RQA parameters:
                       - norm, eDim, tLag, rescaleNorm, radius, tmin, minl,
                         doPlots, plotMode, phaseSpace, doStatsFile
    """

    # Normalize data
    dataX1 = norm_utils.normalize_data(data1, params['norm'])
    dataX2 = norm_utils.normalize_data(data2, params['norm'])

    # Compute distance maxtrix for RQA
    ds = rqa_utils_cpp.rqa_dist(dataX1, dataX2, dim=params['eDim'], lag=params['tLag'])

    # Perform CRQA calculations
    td, rs, mats, err_code = rqa_utils_cpp.rqa_stats(ds["d"], rescale=params['rescaleNorm'], rad=params['radius'], diag_ignore=0, minl=params['minl'], rqa_mode="cross")

    # Print stats
    if err_code == 0:
        if params['showMetrics']:
            print_rqa_metrics(rs)
    else:
        print("Error in RQA computation. Check parameters and data.")

    # Plot results
    plot_mode = params.get('plotMode', 'rp')
    if plot_mode in ('rp', 'rp-timeseries'):
        save_path = None
        if params.get('saveFig', False):
            save_path = os.path.join('images', 'rqa', f"crossRQA_plot.png")

        plot_utils.plot_rqa_results(
            dataX=dataX1,
            dataY=dataX2,
            td=td,
            plot_mode=plot_mode,
            point_size=params['pointSize'],
            save_path=save_path  
        )
    # Write stats
    if params['doStatsFile']:
        output_io_utils.write_rqa_stats("CrossRQA", params, rs, err_code)

    # Return results
    return td, rs, mats, err_code