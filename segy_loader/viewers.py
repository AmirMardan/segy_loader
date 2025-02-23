from PySide6.QtWidgets import QApplication
import sys

from .windows import SegyLoader

def load_segy():
    app = QApplication(sys.argv)
    window = SegyLoader()
    window.show()
    
    app.exec()