from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QColorDialog, QLabel
from PyQt5.QtGui import QPainter, QColor, QPen, QPainter, QPalette, QColor, QConicalGradient, QIcon
from PyQt5.QtCore import Qt, QPointF, pyqtSignal

import src.ui.widgets.colourWheel as colourWheel

class AnnotationWidget(QWidget):
    clearSignal = pyqtSignal()
    undoSignal = pyqtSignal()
    redoSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Annotations')
        self.setMaximumHeight(300)
        #self.setSize(300, 300)
        # Create layout for the annotation widget
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        
        # Create layout for color Picking controls
        colorPickerLayout = QHBoxLayout()

        # Color picker (integrate the color wheel here)
        self.colourWheel = colourWheel.ColorWheel()

        # Create a vertical slider
        self.valueSlider = QSlider(Qt.Vertical)
        self.valueSlider.setRange(1, 255)  # Set the range (adjust as needed)
        self.valueSlider.setValue(255)  # Set the initial value to maximum
        self.value = 255
        self.valueSlider.setStyleSheet(
            "QSlider::groove:vertical { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 white, stop:1 black); }"
        )  # Style the slider to be a white-to-black gradient
        self.valueSlider.valueChanged.connect(self.setValue)

        # Adding the colorwheel and value slider to the layout
        colorPickerLayout.addWidget(self.colourWheel)
        colorPickerLayout.addWidget(self.valueSlider)

        # Create layout for brush controls
        brush_layout = QHBoxLayout()

        # Brush size slider
        self.brush_size_label = QLabel("Brush Size:")
        self.brush_size_slider = QSlider(Qt.Horizontal)
        self.brush_size_slider.setMinimum(1)
        self.brush_size_slider.setMaximum(20)
        self.brush_size_slider.setValue(3)
        self.brush_size_label.setBuddy(self.brush_size_slider)
        brush_layout.addWidget(self.brush_size_label)
        brush_layout.addWidget(self.brush_size_slider)

        # Create layout for brush controls
        opacityLayout = QHBoxLayout()

        # Opacity slider
        self.opacity_label = QLabel("Opacity:")
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.valueChanged.connect(self.set_opacity)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(255)
        self.opacity_slider.setValue(255)
        self.opacity = 255
        self.opacity_label.setBuddy(self.opacity_slider)
        opacityLayout.addWidget(self.opacity_label)
        opacityLayout.addWidget(self.opacity_slider)

        # clear and undo button layout
        toolButtonLayout = QHBoxLayout()

        # Clear and Undo buttons
        self.clearButton = QPushButton()
        self.undoButton = QPushButton()
        self.redoButton = QPushButton()

        # Set icons for undo and redo buttons
        self.clearButton.setIcon(QIcon("C:/Users/Julian/projects/python/mediaPlayer/src/ui/icons/clear.png"))  # Replace with your clear icon file
        self.undoButton.setIcon(QIcon("C:/Users/Julian/projects/python/mediaPlayer/src/ui/icons/undo.png"))    # Replace with your undo icon file
        self.redoButton.setIcon(QIcon("C:/Users/Julian/projects/python/mediaPlayer/src/ui/icons/redo.png"))    # Replace with your redo icon file

        # hook in the annotation buttons
        self.clearButton.clicked.connect(self.clear)
        self.undoButton.clicked.connect(self.undo)
        self.redoButton.clicked.connect(self.redo)

        # Adding the tools tot he layout
        toolButtonLayout.addWidget(self.clearButton)
        toolButtonLayout.addWidget(self.undoButton)
        toolButtonLayout.addWidget(self.redoButton)

        # Add opacity slider and buttons to the main layout
        layout.addLayout(colorPickerLayout)
        layout.addLayout(brush_layout)
        layout.addLayout(opacityLayout)
        layout.addLayout(toolButtonLayout)

        # Set the layout for the widget
        self.setLayout(layout)

    def clear(self):
        self.clearSignal.emit()

    def undo(self):
        self.undoSignal.emit()

    def redo(self):
        self.redoSignal.emit()

    def set_brush_size(self, size):
        self.brush_size = size

    def set_opacity(self):
        self.opacity = self.opacity_slider.value()

    def setValue(self):
        self.value = self.valueSlider.value()

    def clear_annotations(self):
        # Implement logic to clear annotations
        pass

    def undo_annotation(self):
        # Implement logic to undo the last annotation
        pass

    def calculateAdjustedColor(self, annotationColor):
        #annotationColor.getRgb()

        red = annotationColor.red() * self.value // 255 
        green = annotationColor.green() * self.value // 255
        blue = annotationColor.blue() * self.value // 255

        pen = QColor(int(red), int(green), int(blue))
        pen.setAlpha(self.opacity)

        return pen
        
    def getPen(self):
        annotation_color = self.colourWheel.color  # Get the selected color from the color wheel
        adjustedPen = self.calculateAdjustedColor(annotation_color)
        pen = QPen(adjustedPen, self.getBrushSize(), Qt.SolidLine)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        
        return pen
    
    def getColor(self):
        return self.colourWheel.color

    def getOpacity(self):
        return self.opacity_slider.value()

    def getBrushSize(self):
        return self.brush_size_slider.value()