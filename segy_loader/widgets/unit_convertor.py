from PySide6.QtWidgets import (
    QWidget,
    QSpinBox,
    QLabel,
    QHBoxLayout
)

class UnitConvertor(QWidget):
    
    def __init__(self, label: str,
                 parent=None):
        super(UnitConvertor, self).__init__(parent)
        
        self.init_ui(label)
        
    def init_ui(self, label: str):
        dt_label = QLabel(label)
        self.ex_label = QLabel("")
        self.unit = QSpinBox()
        self.unit.setRange(-10, 10)
        self.unit.setPrefix("10^")
        self.unit.setValue(0)        
        
        self.layout = QHBoxLayout()
        
        self.layout.addWidget(dt_label)
        self.layout.addWidget(self.ex_label)
        self.layout.addWidget(self.unit)
        
        self.setLayout(self.layout)
    
    def setExample(self, example: str):
        self.ex_label.setText(example)
        
    def setRange(self, min_val: int, max_val: int):
        self.unit.setRange(min_val, max_val)
        
    def setPrefix(self, prefix: str):
        self.unit.setPrefix(prefix)
        
    def setValue(self, value: int):
        self.unit.setValue(value)
        
    def setLabel(self, label: str):
        self.ex_label.setText(label)
        
    def setEnabled(self, enabled: bool):
        self.unit.setEnabled(enabled)
        
    def setReadOnly(self, read_only: bool):
        self.unit.setReadOnly(read_only)
        
    def setToolTip(self, tooltip: str):
        self.unit.setToolTip(tooltip)
        
    def setObjectName(self, name: str):
        self.unit.setObjectName(name)
        
    def setSingleStep(self, step: int):
        self.unit.setSingleStep(step)
        
    def setFocus(self):
        self.unit.setFocus()
    
    def setMinimum(self, min_val: int):
        self.unit.setMinimum(min_val)
        
    def setMaximum(self, max_val: int):
        self.unit.setMaximum(max_val)
    
    def value(self) -> int:
        return self.unit.value()
    