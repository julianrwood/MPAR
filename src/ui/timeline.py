from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QLabel

class QTimeLine(QWidget):
    positionChanged = pyqtSignal(int)

    def __init__(self, duration, parent=None):
        super().__init__(parent)
        self.duration = duration
        self.slider_position = 0
        self.setMinimumHeight(25)
        self.setMaximumHeight(250)

        self.backgroundColor = QColor(60, 63, 65)
        self.textColor = QColor(187, 187, 187)
        self.font = None  # Use default font

        self.setMouseTracking(True)
        self.setAutoFillBackground(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background
        painter.setBrush(self.backgroundColor)
        painter.drawRect(self.rect())

        # Calculate the interval for frame numbers based on available width
        interval = self.duration
        if self.width() > 0:
            interval = max(1, int(self.duration / (self.width() / 100)))

        # Draw timeline
        scale = self.width() / self.duration
        for frame in range(0, self.duration + 1, interval):
            x = int(frame * scale)
            painter.setPen(QPen(self.textColor))
            painter.drawLine(x, 40, x, 60)
            painter.drawText(x - 10, 25, str(frame))  # Display frame number

        # Draw white lines for the beginning of frames
        painter.setPen(QPen(Qt.white))  # White color for lines
        for frame in range(0, self.duration + 1, interval):
            x = int(frame * scale)
            if frame > 0:
                painter.drawLine(x, 0, x, 40)

        # Draw slider
        slider_width = 10
        slider_height = self.height()
        slider_x = int(self.slider_position - slider_width / 2)  # Convert to integer
        painter.setBrush(QColor(255, 165, 0))  # Orange color for the slider
        painter.drawRect(slider_x, 10, slider_width, slider_height)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.moveSlider(event.x())

    def moveSlider(self, x):
        x = max(0, min(x, self.width()))  # Ensure x is within the widget boundaries
        self.slider_position = x
        frame = int((x / self.width()) * self.duration)
        self.positionChanged.emit(frame)
        self.snapSlider(frame)

    def snapSlider(self, position):
        slider_width = 10
        scale = self.width() / self.duration
        x = int(position * scale)  # Calculate the slider position based on the frame
        x = max(0, min(x, self.width() - slider_width))  # Ensure x is within the widget boundaries
        self.slider_position = x
        self.update()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)

        self.timeline = QTimeLine(50)
        self.timeline.positionChanged.connect(self.onPositionChanged)

        self.current_frame_label = QLabel(self)
        self.current_frame_label.setText("0")  # Initial text
        self.current_frame_label.setMaximumWidth(30)

        layout = QHBoxLayout()  # Use QHBoxLayout
        layout.addWidget(self.timeline, stretch=1)
        layout.addWidget(self.current_frame_label, alignment=Qt.AlignRight)  # Align the label to the left
        self.setLayout(layout)

    def onPositionChanged(self, position):
        self.current_frame_label.setText(str(position))

    def setVisible(self, visible: bool) -> None:
        return super().setVisible(visible)