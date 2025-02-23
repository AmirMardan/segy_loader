import matplotlib.pyplot as plt
import numpy as np

import segy_loader as sl
from segy_loader.preprocessing import scale

def imshow(data: sl.Seis,
           ffid) -> None:
    fig, ax = plt.subplots(1, 1,
                           figsize=(10, 6))

    ax.imshow(scale(data.data,
                method="trace"), 
          cmap="seismic", 
          aspect="auto",
          extent=[0, data.data.shape[1], 
                  data.n_samples*data.dt, 0])
    ax.set_title("All shots")
    ax.set_ylabel("Time [s]")
    
    ax.set_xticklabels(data.recs.index[sl.int32(ax.get_xticks())[:-1]])
    ax.set_xlabel("Trace number")
    ax.set_title(f"Shot {ffid}")
    ax1 = ax.twiny()
    ax1.set_xticks(np.linspace(0, data.data.shape[1]-1, 8))
    ax1.set_xticklabels(data.offset[sl.int32(ax1.get_xticks())])
    ax1.set_xlabel("Offset (m)")
    plt.show()