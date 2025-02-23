from PySide6.QtWidgets import (
    # QApplication,
    QMainWindow,
    QLabel,
    QTextEdit,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QWidget,
    QStatusBar,
    QPlainTextEdit,
    QFileDialog
    )
import textwrap

import sys
import os
sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        )
from segy_loader.io.segy import (
    get_segy_header_text,
    get_segy_byte_example,
    get_segy_byte_value
)
from segy_loader.widgets import SegyByte
from segy_loader.visualization.visualziation import imshow
from segy_loader import Seis

class SegyLoader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SEGY Loader - GImage")
        self.setGeometry(100, 100, 800, 600)
        
        self._selected_file = ""
        # self.get_selected_file = self.selected_file
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.main_layout = QVBoxLayout()
        central_widget.setLayout(self.main_layout)

        self.setup_ui()

    # @property
    def selected_file(self):
        return self._selected_file
    
    # @selected_file.setter
    # def selected_file(self, value):
    #     self._selected_file = value
    
    def setup_ui(self):
        self.setup_byte_widgets()
        self.setup_header_text_box()
        self.setup_load_help_buttons()
        
        # status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready to load SEGY file.")
    
    def setup_byte_widgets(self):
        """
        Byte widgets to select the byte range of the SEGY file.
        """
        self.bytes_map = {
            "SourceX": 73,
            "SourceY": 77,
            "SourceZ": 49,
            "ReceiverX": 81,
            "ReceiverY": 85,
            "ReceiverZ": 41,
            "Offset": 37,
            "CoordinateUnits": 89,
            "TRACE_SEQUENCE_FILE": 5,
            "FieldRecord": 9,
            "TraceNumber": 13,
            "CDP": 21,
            "TraceIdentificationCode": 29,
        }
        for byte_name, byte_key in self.bytes_map.items():
            self.__dict__[byte_name] = SegyByte(name=byte_name,
                                                default_text=byte_key,
                                                segy_path=self.selected_file)
            
        # self.time_unit
        byte_layout = QGridLayout()
        # first row
        byte_layout.addWidget(self.SourceX,
                              0, 0)
        byte_layout.addWidget(self.SourceY,
                              0, 1)
        byte_layout.addWidget(self.SourceZ,
                              0, 2)
        # second row
        byte_layout.addWidget(self.ReceiverX,
                              1, 0)
        byte_layout.addWidget(self.ReceiverY,
                              1, 1)
        byte_layout.addWidget(self.ReceiverZ,
                              1, 2)
        # third row
        byte_layout.addWidget(self.Offset,
                              2, 0)
        byte_layout.addWidget(self.CoordinateUnits,
                              2, 1)
        byte_layout.addWidget(self.FieldRecord,
                                2, 2)
        
        # fourth row
        byte_layout.addWidget(self.CDP,
                              3, 0)
        byte_layout.addWidget(self.TraceIdentificationCode,
                                3, 1)
        byte_layout.addWidget(self.TraceNumber,
                                3, 2)
        
        # fifth row
        byte_layout.addWidget(self.TRACE_SEQUENCE_FILE,
                              4, 0)
        
        
        self.main_layout.addLayout(byte_layout)
    
    def update_byte_examples(self):
        for byte_name, byte_key in self.bytes_map.items():
            self.__dict__[byte_name].example_value_label.setText(str(
                get_segy_byte_example(self._selected_file,
                                      key=int(byte_key))))
            
    def setup_load_help_buttons(self):
        """
        Buttons to load and help the user load the SEGY file.
        """
        # create buttons
        exit_button = QPushButton("Exit")
        help_button = QPushButton("Help")
        help_button.setToolTip("Show help on how to work with this tool.")
        
        load_button = QPushButton("Load SEGY")
        load_button.setToolTip("Load a SEGY file.")
        
        self.display_button = QPushButton("Display")
        self.display_button.setEnabled(False)
        self.display_button.setToolTip("Display the loaded data.")
        
        self.save_button = QPushButton("Save")
        self.save_button.setEnabled(False)
        self.save_button.setToolTip("Save the seismic data to a file.")
        
        # create layout
        help_load_btn_layouts = QHBoxLayout()
        help_load_btn_layouts.addWidget(exit_button)
        help_load_btn_layouts.addWidget(help_button)
        help_load_btn_layouts.addStretch()
        help_load_btn_layouts.addWidget(load_button)
        help_load_btn_layouts.addWidget(self.display_button)
        help_load_btn_layouts.addWidget(self.save_button)
        
        # add layout to main layout
        self.main_layout.addLayout(help_load_btn_layouts)
        
        # connect buttons
        exit_button.clicked.connect(self.close)
        help_button.clicked.connect(self.show_help)
        load_button.clicked.connect(self.load_segy)
        self.display_button.clicked.connect(self.display_data)
        self.save_button.clicked.connect(self.save_seis)
        
    def show_help(self):
        help_text = """
        SEGY Loader Help
        
        1. Click the 'Load SEGY' button to load a SEGY file.
        2. Select the SEGY file from the file dialog.
        3. The header of the SEGY file will be displayed in the text box.
        4. Verify the header information and adjust the the selected bytes if necessary.
        5. Click 'Display' to display the seismic data.
        6. Click the 'Save' button to save the seismic data.
        7. Click the 'Exit' button to close the application.
        """
        self.text_edit.setPlainText(help_text)
        
    def display_data(self):
        imshow(self.data, self.dt)
    
    def save_seis(self):
            
        data = self.data
        header = {
            "dt": self.dt,
            "ffid": self.get_segy_value(self.FieldRecord.byte_spinbox.value()).astype(str),
            "samples": self.samples,
            # "s_id": 1,
            "sx": self.get_segy_value(self.SourceX.byte_spinbox.value()),
            "sy": self.get_segy_value(self.SourceY.byte_spinbox.value()),
            "sz": self.get_segy_value(self.SourceZ.byte_spinbox.value()),
            # "r_id": 1,
            "rx": self.get_segy_value(self.ReceiverX.byte_spinbox.value()),
            "ry": self.get_segy_value(self.ReceiverY.byte_spinbox.value()),
            "rz": self.get_segy_value(self.ReceiverZ.byte_spinbox.value()),
            "offset": self.get_segy_value(self.Offset.byte_spinbox.value()),
        }
        seis_data = Seis(data, header)
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self,
                                                   "Save Seis File",
                                                   "",
                                                   "Seis Files (*.seis)",
                                                   options=options)
        if file_name:
            extension = ".seis"
            if not file_name.endswith(extension):
                file_name += extension
            seis_data.write(f"{file_name}")
    
    def get_segy_value(self, key):
        return get_segy_byte_value(self._selected_file, key)
    
    def setup_header_text_box(self):
        """
        The text box to show the header of the SEGY file.
        """
        self.text_edit = QPlainTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlaceholderText(
            """
            No SEGY file selected.
            
            Click the button below to load a SEGY file...
            """
            )
        self.main_layout.addWidget(self.text_edit)
        
    def load_segy(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("SEGY Files (*.sgy *.segy)")
        
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            self._selected_file = file_path
            self.show_file_info()
            
            self.update_byte_examples()
            self.status_bar.showMessage(f"Loaded SEGY file: {file_path}")
            self.save_button.setEnabled(True)
            self.display_button.setEnabled(True)
            
    def show_file_info(self):
        header_text, data_info, self.data = get_segy_header_text(self._selected_file)
        self.dt = data_info["dt"]
        self.samples = data_info["samples"]
        
        self.text_edit.setPlainText(header_text)
        
        text_to_append = textwrap.dedent(f"""
            \n
            ========================================
            Data information
            ========================================
            
            File: {self._selected_file}
            Format: {data_info['format']}
            Sorting: {data_info['sorting']}
            Data shape: {data_info['data_shape']}
            Sampling rate: {data_info['dt']}
            Number of traces: {data_info['n_traces']}
            Number of samples: {data_info['data_shape'][0]}
            Trace length: {data_info['length']}
        """)
        self.text_edit.appendPlainText(text_to_append)
        
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    # sys.path.append(
    #     os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    #     )
    app = QApplication(sys.argv)
    window = SegyLoader()
    window.show()
    
    app.exec()