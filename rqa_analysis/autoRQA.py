from .utils import norm_utils, plot_utils, output_io_utils
from .utils.metrics_utils import print_rqa_metrics
from .utils import rqa_utils_cpp
import os

def autoRQA(data, params):
    """ Auto Recurrence Quantification Analysis """
    # Normalize data
    dataX = norm_utils.normalize_data(data, params['norm'])

    # Perform RQA computations
    ds = rqa_utils_cpp.rqa_dist(dataX, dataX, dim=params['eDim'], lag=params['tLag'])

    # Similarly, you can call xRQA_stats:
    td, rs, mats, err_code = rqa_utils_cpp.rqa_stats(
        ds["d"], rescale=params['rescaleNorm'], rad=params['radius'], 
        diag_ignore=params['tw'], minl=params['minl'], rqa_mode="auto"
        )

    ## Print stats
    if err_code == 0:
        if params['showMetrics']:
            print_rqa_metrics(rs)
    else:
        print("Error in RQA computation. Check parameters and data.")

    # Plot results
    # plotMode: 'none', 'rp', 'rp_timeseries',
    plot_mode = params.get('plotMode', 'rp')
    if plot_mode in ('rp', 'rp-timeseries'):
        save_path = None
        if params.get('saveFig', False):
            save_path = os.path.join('images', 'rqa', f"autoRQA_plot.png")
        

        plot_utils.plot_rqa_results(
            dataX=dataX,
            td=td,
            plot_mode=plot_mode,
            point_size=params['pointSize'],
            save_path=save_path 
        )

    # Write stats
    if params['doStatsFile']:
        output_io_utils.write_rqa_stats("AutoRQA", params, rs, err_code)

    # Return results
    return td, rs, mats, err_code