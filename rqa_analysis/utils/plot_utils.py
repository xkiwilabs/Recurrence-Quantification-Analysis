import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

def plot_rqa_results(
    dataX=None, dataY=None, td=None,
    plot_mode='rp', point_size=4,
    save_path=None):
    """
    Plot RQA or CRQA results with aligned RP and TS width.
    """

    ax_ts_x = None
    ax_ts_y = None

    N = len(dataX)
    fig = plt.figure(figsize=(8, 9))  # Squarer figure to accommodate equal width
    gs = gridspec.GridSpec(3, 2, width_ratios=[1, 12], height_ratios=[1, 12, 2], hspace=0.4, wspace=0.2)

    # === Recurrence Plot ===
    ax_rp = fig.add_subplot(gs[1, 1])
    ax_rp.set_facecolor('#b0c4de')  # Light Steel Blue, a lighter navy shade

    recur_y, recur_x = np.where(td == 1)
    ax_rp.scatter(recur_x, recur_y, c='blue', s=point_size, edgecolors='none')
    ax_rp.set_xlim([0, N])
    ax_rp.set_ylim([0, N])
    ax_rp.set_title("Cross-Recurrence Plot" if dataY is not None else "Recurrence Plot", pad=8)
    ax_rp.set_xlabel("X(i)")
    ax_rp.set_ylabel("Y(j)" if dataY is not None else "X(j)")

    # === Time Series X ===
    if 'timeseries' in plot_mode:
        ax_ts_x = fig.add_subplot(gs[2, 1], sharex=ax_rp)
        ax_ts_x.plot(np.arange(N), dataX[:N], color='tab:blue')
        ax_ts_x.set_xlim([0, N])
        ax_ts_x.set_title("Time Series X", fontsize=10)
        ax_ts_x.set_xlabel("Time")
        ax_ts_x.set_ylabel("X", rotation=0, labelpad=15)

    # === Time Series Y ===
    if dataY is not None and 'timeseries' in plot_mode:
        ax_ts_y = fig.add_subplot(gs[1, 0], sharey=ax_rp)
        ax_ts_y.plot(dataY[:N], np.arange(N), color='tab:blue')
        ax_ts_y.invert_xaxis()
        ax_ts_y.set_ylim([0, N])
        ax_ts_y.set_title("Time Series Y", fontsize=10)
        ax_ts_y.set_ylabel("Time")
        ax_ts_y.set_xlabel("Y", rotation=0, labelpad=15)

    if 'timeseries' in plot_mode:
        if ax_ts_x is not None:
            fig.align_xlabels([ax_rp, ax_ts_x])
        if ax_ts_y is not None:
            fig.align_ylabels([ax_rp, ax_ts_y])
    else:
        fig.align_xlabels([ax_rp])
        fig.align_ylabels([ax_rp])
    
    if save_path:
       import os
       os.makedirs(os.path.dirname(save_path), exist_ok=True)
       plt.savefig(save_path, dpi=300, bbox_inches='tight')
       print(f"Plot saved to: {save_path}")

    plt.show()

def plot_drp_results(
    lags,
    drp,
    point_size=4,
    save_path=None
):
    """
    Plot Diagonal Recurrence Profile (DRP).

    Parameters
    ----------
    lags : np.ndarray
        Array of lag values corresponding to the DRP.
    drp : np.ndarray
        Recurrence rate values for each lag.
    point_size : int, optional
        Marker size for the plot (default=4).
    save_path : str or None, optional
        If provided, the plot will be saved to this path.
    """
    fig, ax = plt.subplots(figsize=(8, 4))

    ax.plot(lags, drp, marker='o', ms=point_size, color='tab:blue', label="DRP")
    ax.axvline(0, color='k', linestyle='--', alpha=0.6, label="Lag=0")
    ax.set_title("Diagonal Recurrence Profile (DRP)")
    ax.set_xlabel("Lag")
    ax.set_ylabel("% Recurrence")
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="best")

    if save_path:
        import os
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")

    plt.show()
