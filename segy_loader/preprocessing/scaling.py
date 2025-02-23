'''
Tools for scale seismic data.

'''
from typing import Union
import numpy as np

def scale(data: np.ndarray,
          method: str = "trace") -> np.ndarray:
    """Scale data.

    Parameters
    ----------
    data : np.ndarray
        Data to scale.
    method : str, optional
        Method for scaling, by default `"trace"`. Options are:
        - `"trace"`: Scale data by trace.
        - `"global"`: Scale data globally.

    Returns
    -------
    np.ndarray
        Scaled data.
    """
    if method == "trace":
        return data / np.max(np.abs(data), axis=0)
    if method == "global":
        return data / np.max(np.abs(data))