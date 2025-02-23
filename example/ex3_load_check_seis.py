"""
In this example, we will show how to use convert segy data to
seis data, save, load and visualize it using shot_viewer
"""
from os import path as osp
import matplotlib.pyplot as plt
from path_loader import data_path # noqa: F401

from segy_loader.io import load_seis
from seismic.viewers import shot_viewer

path = osp.abspath(osp.join(osp.dirname(__file__), "../data/seis/42.seis"))

data = load_seis(path)
data.time_cut(0, 0.32)

# data.write(path) 

shot_viewer(key="ffid",
            clip=0.9,
            direction='x')

plt.show()