from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal


class ToolsMenu(QWidget):
    
    brushToolSelected = pyqtSignal()
    selectToolSelected = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a horizontal layout for the base menu
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignTop) 
        self.setMaximumHeight(150)
        # Create tool buttons
        select_button = QPushButton()
        annotation_button = QPushButton()

        annotation_button.clicked.connect(self.emitBrushToolSelected)
        select_button.clicked.connect(self.emitSelectToolSelected)
        
        #Set their icons
        selfLocation = __file__
        iconLocation = selfLocation.replace('tools.py','icons')

        select_button.setIcon(QIcon(iconLocation+"/select.png"))  # Replace with your clear icon file
        annotation_button.setIcon(QIcon(iconLocation+"/brush.png"))    # Replace with your undo icon file

        # Add tool buttons to the layout
        layout.addWidget(select_button)
        layout.addWidget(annotation_button)
        # Add any other tool buttons to the layout as needed

        # Set the layout for the base menu
        self.setLayout(layout)
    
    def emitBrushToolSelected(self):
        # Emit the custom signal when the brush tool is selected
        self.brushToolSelected.emit()

    def emitSelectToolSelected(self):
        # Emit the custom signal when the brush tool is selected
        self.selectToolSelected.emit()