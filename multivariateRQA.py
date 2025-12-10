from .utils import norm_utils, plot_utils, output_io_utils
from .utils import rqa_utils_cpp
import numpy as np
import os

def multivariateRQA(data, params, mode="auto"):
    """
    Perform Multivariate Recurrence Quantification Analysis (RQA).
    
    Parameters:
        data (np.ndarray): 2D array of shape (time_points, dimensions) or 
                          list of 1D arrays for each dimension
        params (dict): Dictionary of RQA parameters:
                       - norm, rescaleNorm, radius, tw, minl,
                         showMetrics, plotMode, pointSize, saveFig, doStatsFile
        mode (str): "auto" for auto-RQA or "cross" for cross-RQA (requires data to be [data1, data2])
    
    Returns:
        tuple: (td, rs, mats, err_code) - thresholded matrix, results, matrices, error code
    """
    
    # Handle different input formats
    if isinstance(data, list):
        if len(data) < 2:
            raise ValueError("Multivariate RQA requires at least 2 dimensions.")
        
        if mode == "cross":
            if len(data) != 2:
                raise ValueError("Cross multivariate RQA requires exactly 2 datasets.")
            data1, data2 = data
            if isinstance(data1, list):
                data1 = np.column_stack(data1)
            if isinstance(data2, list):
                data2 = np.column_stack(data2)
        else:
            # Convert list of 1D arrays to 2D array
            data = np.column_stack(data)
    else:
        if data.ndim != 2:
            raise ValueError("Multivariate data must be 2D array (time x dimensions).")
        if data.shape[1] < 2:
            raise ValueError("Multivariate RQA requires at least 2 dimensions.")
    
    if mode == "cross":
        # Normalize data separately
        dataX1 = norm_utils.normalize_data(data1, params['norm'])
        dataX2 = norm_utils.normalize_data(data2, params['norm'])
        
        # Ensure 2D format
        if dataX1.ndim == 1:
            dataX1 = dataX1.reshape(-1, 1)
        if dataX2.ndim == 1:
            dataX2 = dataX2.reshape(-1, 1)
        
        # Compute multivariate distance matrix
        ds = rqa_utils_cpp.rqa_dist_multivariate(dataX1.astype(np.float32), dataX2.astype(np.float32))
        
        # Perform CRQA calculations
        td, rs, mats, err_code = rqa_utils_cpp.rqa_stats(
            ds["d"], rescale=params['rescaleNorm'], rad=params['radius'], 
            diag_ignore=0, minl=params['minl'], rqa_mode="cross"
        )
        
        analysis_type = "MultivariateX-RQA"
        plot_data = [dataX1, dataX2]
        
    else:  # auto mode
        # Normalize data
        dataX = norm_utils.normalize_data(data, params['norm'])
        
        # Ensure 2D format
        if dataX.ndim == 1:
            dataX = dataX.reshape(-1, 1)
        
        # Compute multivariate distance matrix
        ds = rqa_utils_cpp.rqa_dist_multivariate(dataX.astype(np.float32), dataX.astype(np.float32))
        
        # Perform RQA calculations
        tw = params.get('tw', 1)  # Default theiler window
        td, rs, mats, err_code = rqa_utils_cpp.rqa_stats(
            ds["d"], rescale=params['rescaleNorm'], rad=params['radius'], 
            diag_ignore=tw, minl=params['minl'], rqa_mode="auto"
        )
        
        analysis_type = "MultivariateRQA"
        plot_data = [dataX]
    
    # Print stats
    if err_code == 0:
        if params.get('showMetrics', True):
            print(f"%REC: {float(rs['perc_recur']):.3f} | %DET: {float(rs['perc_determ']):.3f} | MaxLine: {float(rs['maxl_found']):.2f}")
            print(f"Mean Line Length: {float(rs['mean_line_length']):.2f} | SD Line Length: {float(rs['std_line_length']):.2f} | Line Count: {float(rs['count_line']):.2f}")
            print(f"ENTR: {float(rs['entropy']):.3f} | LAM: {float(rs['laminarity']):.3f} | TT: {float(rs['trapping_time']):.3f}")
            print(f"Vmax: {float(rs['vmax']):.2f} | Divergence: {float(rs['divergence']):.3f}") 
            print(f"Trend_Lower: {float(rs['trend_lower_diag']):.3f} | Trend_Upper {float(rs['trend_upper_diag']):.3f}")
            print(f"Dimensions: {ds['dim']} | Analysis: {analysis_type}")
    else:
        print("Error in multivariate RQA computation. Check parameters and data.")
    
    # Plot results
    plot_mode = params.get('plotMode', 'rp')
    if plot_mode in ('rp', 'rp-timeseries'):
        save_path = None
        if params.get('saveFig', False):
            save_path = os.path.join('images', 'rqa', f"{analysis_type.lower()}_plot.png")
        
        # For multivariate plotting, we'll use the first two dimensions if available
        if mode == "cross":
            plot_utils.plot_rqa_results(
                dataX=plot_data[0][:, 0],  # First dimension of first dataset
                dataY=plot_data[1][:, 0],  # First dimension of second dataset  
                td=td,
                plot_mode=plot_mode,
                point_size=params.get('pointSize', 1),
                save_path=save_path
            )
        else:
            plot_utils.plot_rqa_results(
                dataX=plot_data[0][:, 0],  # First dimension
                td=td,
                plot_mode=plot_mode,
                point_size=params.get('pointSize', 1),
                save_path=save_path
            )
    
    # Write stats
    if params.get('doStatsFile', False):
        output_io_utils.write_rqa_stats(analysis_type, params, rs, err_code)
    
    return td, rs, mats, err_code


def multivariateCrossRQA(data1, data2, params):
    """
    Convenience function for multivariate cross-RQA.
    
    Parameters:
        data1, data2: Multivariate time series datasets
        params: RQA parameters
    
    Returns:
        Results from multivariateRQA with mode="cross"
    """
    return multivariateRQA([data1, data2], params, mode="cross")