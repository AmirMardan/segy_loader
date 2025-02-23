"""
In this example, we will show how to use convert segy data to
seis data, save, load and visualize it using shot_viewer
"""
from os import path as osp
import matplotlib.pyplot as plt
import numpy as np
from path_loader import data_path

import segy_loader as sl
from segy_loader.io import load_segy, load_seis
# from seismic.viewers import shot_viewer
from segy_loader.preprocessing import scale

path = osp.abspath(osp.join(osp.dirname(__file__), "../../"))

dat_shots = ["1.cat", "2.cat", "3.cat", "4.cat", "5.cat", "6.cat"]
segy_shots = ["2.segy", "24.segy", "42.segy"]
sgy_shots = ["1006.sgy", "1007.sgy", "1013.sgy", "1027.sgy"]

data = sl.Seis()
for i, shot in enumerate(sgy_shots):
    shot_name = shot.split(".")[0]
    d1, h1 = load_segy(f"{data_path}/segy/{shot}", False)

    h1['ffid'] = int(shot_name)
    data.extend(d1, h1)
    
data.time_cut(0, 0.8)

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

ax1 = ax.twiny()
ax1.set_xticks(np.linspace(0, data.data.shape[1]-1, 8))
ax1.set_xticklabels(data.offset[sl.int32(ax1.get_xticks())])
# ax1.set_xticklabels(data.offset[sl.int32(ax.get_xticks())[:-1]])
ax1.set_xlabel("Offset (m)")

a = 1
# shot_viewer(data, 
#             key="ffid",
#             clip=0.9,
#             direction='x')
# data.write(f"{data_path}/seis/merged.seis")

# laoded_data = load_seis(f"{data_path}/seis/merged.seis")
# shot_viewer(laoded_data,
#             clip=0.9, 
#             key="ffid")
plt.show()