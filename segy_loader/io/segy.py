import numpy as np
from typing import Tuple
from pandas import DataFrame

import segyio 

def load_segy(file: str,
              verbose: bool=False) -> Tuple[np.ndarray, 
                                            dict]:
    """Load a segy file using segyio

    Parameters
    ----------
    file : str
        file path to be loaded
    verbose : bool
        print header information

    Returns
    -------
    data : np.ndarray
        data loaded from the segy file
    
    header : dict
        header information of the segy file
        
    References
    ----------
    - https://segyio.readthedocs.io/en/latest/segyio.html#segyio.open
    - https://github.com/equinor/segyio/blob/master/python/test/segy.py#L1089-L1120
    """
    
    with segyio.open(filename=file, ignore_geometry=True) as f:
        data = f.trace.raw[:].T
        format = int(f.format)
        sorting = f.sorting
        samples = f.samples
        dt = segyio.tools.dt(f) / 1e6 # mus -> s
        n_traces = f.tracecount
        inline = f.ilines
        xlines = f.xlines
        sx = f.attributes(segyio.TraceField.SourceX)[:]
        sy = f.attributes(segyio.TraceField.SourceY)[:]
        sz = f.attributes(segyio.TraceField.SourceDepth)[:]
        
        gx = f.attributes(segyio.TraceField.GroupX)[:]
        gy = f.attributes(segyio.TraceField.GroupY)[:]
        gz =  f.attributes(segyio.TraceField.ReceiverGroupElevation)[:]
        
        reel = f.attributes(segyio.TraceField.TRACE_SEQUENCE_FILE)[:]
        ffid = f.attributes(segyio.TraceField.FieldRecord)[:]
        
        # example of how to get value from header
        # f.header[5][37]
        
        to_verbose = segyio.tools.wrap(f.text[0])
        
    if verbose:
        print(to_verbose)
    
    header = {
        "dt": dt,
        "reel": reel,
        "ffid": ffid,
        "inline": inline,
        "xline": xlines,
        "format": format,
        "sorting": sorting,
        "samples": samples, # ms
        "n_traces": n_traces,
        "trace_length": max(samples),
        "offset": distance([sx, sy], [gx, gy]),
        "sx": sx,
        "sy": sy,
        "sz": sz,
        "gx": gx,
        "gy": gy,
        "gz": gz
    }
    
    return data, header
    
def get_segy_header_text(file: str):
    '''
    Get the text header of a segy file
    '''
    with segyio.open(file, ignore_geometry=True) as f:
        return (segyio.tools.wrap(f.text[0]), 
                {
                    'data_shape': f.trace.raw[:].T.shape,
                    'format': f.format,
                    'sorting': f.sorting,
                    'dt': f.samples[1] - f.samples[0],
                    'samples': f.samples,
                    'n_traces': f.tracecount,
                    'length': f.samples[-1]
                    }, 
                f.trace.raw[:].T)


def get_segy_byte_value(file: str,
                        key: str) -> np.ndarray:
    '''
    Get the byte value of a segy file
    '''
    
    with segyio.open(file, 
                     ignore_geometry=True) as f:
        return f.attributes(key)[:]
    
def get_segy_byte_example(file: str,
                          key: str) -> str:
    '''
    Get an example of the byte value of a segy file
    '''
    d = get_segy_byte_value(file, key)
    if np.issubdtype(d.dtype, np.number):
        return f"{d.min()} - {d.max()}"
    else:
        return d[0].decode("utf-8")
        
def parse_header(file: str)-> DataFrame:
    '''
    Parse the segy file trace headers into a pandas dataframe.
    Column names are defined from segyio internal tracefield
    One row per trace
    '''
    headers = segyio.tracefield.keys
    with segyio.open(filename=file, 
                     ignore_geometry=True) as f:
        n_traces = f.tracecount
        
        # Initialize dataframe with trace id as index and headers as columns
        df = DataFrame(index=range(1, n_traces + 1),
                        columns=headers.keys())
        # Fill dataframe with all header values
        for k, v in headers.items():
            df[k] = f.attributes(v)[:]
    return df


def distance(x1: np.ndarray,
             x2: np.ndarray) -> np.ndarray:
    '''
    Calculate the distance between two points
    '''
    return np.sqrt((x1[0]-x2[0])**2 + (x1[1]-x2[1])**2)


def get_segy_header(file: str,
                    trace: int,
                    line: int) -> dict:
    '''
    Get the header of a segy file
    '''
    if isinstance(trace, int):
        with segyio.open(file, ignore_geometry=True) as f:
            header = f.header[trace][line]
        return header
    elif isinstance(trace, list):
        n = np.arange(trace[0], trace[1]).astype(int)
        with segyio.open(file, ignore_geometry=True) as f:
            header = [f.header[t][line] for t in n]
        header = np.array(header)
        return header

def save_segy(file_name: str,
              data: np.ndarray,
              header: dict,
              verbose: bool=False) -> None:
    """Save segy file using segyio

    Parameters
    ----------
    file_name : str
        File path
    data : np.ndarray
        data to be saved
    header : dict
        Header of the segy file
    verbose : bool, optional, default False
        Print the text header of the segy file
        
    References
    ----------
    - https://segyio.readthedocs.io/en/latest/segyio.html#segyio.create
    - https://github.com/equinor/segyio/blob/master/python/test/segy.py#L1089-L1120
    """
    
    spec = segyio.spec()
    spec.tracecount = data.shape[1]
    if "format" in header:
        spec.format = int(header["format"])
    else:
        spec.format = 1
        
    if header["sorting"] is None:
        spec.sorting = None
    else:
        spec.sorting = int(header["sorting"])
    
    if "samples" in header:  
        spec.samples = header["samples"]
    else:
        spec.samples = header["dt"] * np.arange(data.shape[0]) * 1e3 # mus -> ms
    
    if "inline" in header:
        spec.ilines = header["inline"]
    else:
        spec.ilines = None
        
    if "xline" in header:
        spec.xlines = header["xline"]
    else:
        spec.xlines = None
        
    spec.dt = header["dt"] * 1e6 # s -> mus
        
    with segyio.create(file_name, spec) as f:
        for trace_ind in range(data.shape[1]):
            f.trace[trace_ind] = data[:, trace_ind]
    
    if verbose:
        with segyio.open(file_name, ignore_geometry=True) as f:
            print(segyio.tools.wrap(f.text[0]))
        
if __name__ == "__main__":
    pass