from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QGridLayout,
    QSpinBox
)
from PySide6.QtGui import QValidator

from segy_loader.io.segy import get_segy_byte_example
from segy_loader.data.segyio_keys import segyio_keys

class CustomSpinBox(QSpinBox):
    '''
    Custom spinbox for segy byte to be sure that the value is in the allowed values
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        allowed_values = list(segyio_keys.values())
        self.allowed_values = allowed_values
        self.setRange(min(allowed_values), max(allowed_values))
        self.setSingleStep(4)
        
    def validate(self, text, pos):
        if text.isdigit() and int(text) in self.allowed_values:
            return QValidator.Acceptable, text, pos
        return QValidator.Invalid, text, pos

    def fixup(self, text):
        if text.isdigit():
            value = int(text)
            closest_value = min(self.allowed_values, key=lambda x: abs(x - value))
            self.setValue(closest_value)

    def valueFromText(self, text):
        return int(text)

    def textFromValue(self, value):
        return str(value)
    
    
class SegyByte(QWidget):
    def __init__(self, name: str,
                 default_text: str,
                 single_step: int=4,
                 segy_path: str=None,
                 parent=None):
        
        super().__init__(parent)
        self.segy_path = segy_path
        
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        self.setup_ui(name, default_text,
                      single_step)
        
    def setup_ui(self, name: str,
                 default_text: str,
                 single_step: int):
        self.byte_layout = QGridLayout()
        self.main_layout.addLayout(self.byte_layout)
        
        label = QLabel(f"{name}:")
        self.byte_layout.addWidget(label, 0, 0)
        
        self.example_value_label = QLabel("")
        self.byte_layout.addWidget(self.example_value_label, 0, 1)
        
        self.byte_spinbox = CustomSpinBox()
        # self.byte_spinbox.setSingleStep(single_step)
        # self.byte_spinbox.setRange(1, 1000)
        self.byte_layout.addWidget(self.byte_spinbox, 1, 0,
                                   1, 2)
        self.byte_spinbox.setValue(default_text)
        self.byte_spinbox.valueChanged.connect(
            self.update_example_value)
        
    def update_example_value(self):
        self.example_value_label.setText(
            get_segy_byte_example(self.segy_path(),
                                  key=int(self.byte_spinbox.value())))
        
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication([])
    widget = SegyByte(name="SourceX",
                      default_text=73)
    widget.show()
    app.exec()