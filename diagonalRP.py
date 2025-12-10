from .utils import norm_utils, plot_utils, output_io_utils
from .utils import rqa_utils_cpp
import numpy as np
import os


def DRP(data, params, mode="auto"):
    """
    Perform Diagonal Recurrence Profile (DRP) analysis.

    Parameters
    ----------
    data : array-like or list of two arrays
        - For mode="auto": a single 1D array (time series).
        - For mode="cross": list/tuple of two 1D arrays [data1, data2].
    params : dict
        Dictionary of DRP parameters:
            'norm'         : normalization flag (see norm_utils)
            'eDim'         : embedding dimension
            'tLag'         : embedding lag
            'rescaleNorm'  : rescale mode (0=none, 1=mean, 2=max)
            'radius'       : recurrence threshold
            'tw'           : Theiler window (ignored diagonals for auto mode)
            'maxLag'       : maximum lag to return (optional)
            'plotMode'     : 'none' or 'drp'
            'saveFig'      : whether to save figure
            'pointSize'    : marker size for plot
            'showMetrics'  : whether to print DRP metrics to console
            'doStatsFile'  : whether to write profile to file
    mode : str
        "auto" (default) or "cross".

    Returns
    -------
    drp : np.ndarray
        Diagonal recurrence profile (possibly truncated).
    lags : np.ndarray
        Array of lag values corresponding to drp.
    """
    if mode == "cross":
        if not isinstance(data, (list, tuple)) or len(data) != 2:
            raise ValueError("Cross DRP requires a list/tuple of two time series.")
        dataX = norm_utils.normalize_data(data[0], params['norm'])
        dataY = norm_utils.normalize_data(data[1], params['norm'])
    else:
        dataX = norm_utils.normalize_data(data, params['norm'])
        dataY = dataX

    # Distance & recurrence
    ds = rqa_utils_cpp.rqa_dist(dataX, dataY, dim=params['eDim'], lag=params['tLag'])
    diag_ignore = params.get('tw', 0) if mode == "auto" else 0
    td = rqa_utils_cpp.rqa_radius(ds["d"], params['rescaleNorm'], params['radius'], diag_ignore)

    # DRP
    drp = rqa_utils_cpp.rqa_drp(td)
    lags = np.arange(-(td.shape[0] - 1), td.shape[0])

    # Truncate if maxLag is set
    maxLag = params.get('maxLag', None)
    if maxLag is not None:
        mask = np.abs(lags) <= maxLag
        lags = lags[mask]
        drp = drp[mask]

    # Show metrics
    if params.get('showMetrics', False) and len(drp) > 0:
        max_idx = np.argmax(drp)
        max_val = drp[max_idx]
        max_lag = lags[max_idx]
        mean_val = np.mean(drp)

        print(f"[DRP Metrics] Mean recurrence rate = {mean_val:.4f}")
        print(f"[DRP Metrics] Max recurrence rate  = {max_val:.4f} at lag = {max_lag}")

    # Plot
    if params.get('plotMode', 'drp') == 'drp':
        save_path = None
        if params.get('saveFig', False):
            os.makedirs("images/drp", exist_ok=True)
            save_path = os.path.join("images", "drp", f"drp_{mode}.png")

        plot_utils.plot_drp_results(
            lags=lags, drp=drp, point_size=params.get('pointSize', 2), save_path=save_path
        )

    # Write full profile
    if params.get('doStatsFile', False):
        output_io_utils.write_drp_profile(f"DRP-{mode}", params, lags, drp)

    return drp, lags

def crossDRP(data1, data2, params):
    """
    Convenience function for Cross-DRP.
    """
    return DRP([data1, data2], params, mode="cross")
