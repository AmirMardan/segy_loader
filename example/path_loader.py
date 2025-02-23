from os import path as osp
import os
import sys
from dotenv import load_dotenv
load_dotenv()

seismic_path = os.getenv("SEISMIC_PATH")

segy_loader_path = osp.abspath(
    osp.join(
        osp.dirname(__file__), "../"
        )
    )

data_path = f"{segy_loader_path}/data"

sys.path.extend([segy_loader_path,
                 seismic_path
                 ])