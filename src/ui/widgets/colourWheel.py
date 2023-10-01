from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QPalette, QColor, QConicalGradient
import math

class ColorWheel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.color = QColor.fromHsv(255, 255, 255)
        self.setMouseTracking(True)
        self.setFixedSize(100, 100)  # Adjust the size as needed
        self.dot_position = QPointF()  # Initialize dot_position attribute

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        center = rect.center()
        radius = min(rect.width(), rect.height()) / 2

        gradient = QConicalGradient(center, -90)
        gradient.setColorAt(0, Qt.red)
        gradient.setColorAt(1/6, Qt.yellow)
        gradient.setColorAt(1/3, Qt.green)
        gradient.setColorAt(0.5, Qt.cyan)
        gradient.setColorAt(2/3, Qt.blue)
        gradient.setColorAt(5/6, Qt.magenta)
        gradient.setColorAt(1, Qt.red)

        painter.setBrush(gradient)
        painter.drawEllipse(rect)

        # Draw the white dot at the calculated position
        painter.setPen(Qt.NoPen)
        painter.setBrush(QPalette().color(QPalette.Background))
        painter.drawEllipse(self.dot_position, 5, 5)

    def mousePressEvent(self, event):
        wheel_size = self.size()  # Get the size of the color wheel widget

        # Calculate the center of the wheel
        center = wheel_size.width() / 2, wheel_size.height() / 2

        # Calculate the radius of the wheel (half the smaller dimension)
        radius = min(wheel_size.width(), wheel_size.height()) / 2

        # Calculate the vector from the center to the mouse click position
        vector = QPointF(event.pos()) - QPointF(*center)
        
        # Calculate the distance from the center to the click position
        distance = vector.manhattanLength()

        # Check if the click position is within the color wheel's bounds
        if distance <= radius:
            # Pass the mouse click position as a QPointF to the updateDotPosition function
            self.updateDotPosition(QPointF(event.pos()))

            # Calculate the corresponding HSV values and update the color
            self.updateColorFromDotPosition()

            self.update()

    def updateDotPosition(self, new_position):
        # Set the dot position to the new_position
        self.dot_position = new_position

    def updateColorFromDotPosition(self):
        # Calculate the new color based on the dot position within the color wheel
        rect = self.rect()
        center = rect.center()
        radius = min(rect.width(), rect.height()) / 2

        vector = self.dot_position - center
        angle = math.degrees(math.atan2(vector.y(), vector.x()))
        
        if angle < 0:
            angle += 360

        saturation = vector.manhattanLength() / radius
        value = 1.0

        self.color.setHsvF(angle / 360, saturation, value)