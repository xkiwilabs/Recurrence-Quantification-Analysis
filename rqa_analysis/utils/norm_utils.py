import numpy as np

def normalize_data(data, norm="none"):
    """
    Normalise data according to the specified method.

    Parameters
    ----------
    data : np.ndarray
        Input array (1D or 2D).
    norm : str or int
        Normalisation method:
            - "minmax" or 1 : rescale to [0, 1]
            - "zscore" or 2 : mean=0, std=1
            - "center" or 3 : subtract mean
            - "none"        : no normalisation

    Returns
    -------
    np.ndarray
        Normalised array.

    Raises
    ------
    ValueError
        If `norm` is not recognised.
    """
    
    # Map numeric codes to strings
    mapping = {1: "minmax", 2: "zscore", 3: "center"}
    if isinstance(norm, int):
        norm = mapping.get(norm, f"INVALID_INT_{norm}")

    if norm == "minmax":
        if data.ndim == 1:
            return (data - np.min(data)) / (np.max(data) - np.min(data))
        else:
            return (data - np.min(data, axis=0)) / (np.max(data, axis=0) - np.min(data, axis=0))
    elif norm == "zscore":
        if data.ndim == 1:
            return (data - np.mean(data)) / np.std(data)
        else:
            return (data - np.mean(data, axis=0)) / np.std(data, axis=0)
    elif norm == "center":
        if data.ndim == 1:
            return data - np.mean(data)
        else:
            return data - np.mean(data, axis=0)
    elif norm == "none":
        return data
    else:
        raise ValueError(
            f"Invalid norm option '{norm}'. "
            "Choose from: 'minmax', 'zscore', 'center', 'none' "
            "or numeric codes {1, 2, 3}."
        )