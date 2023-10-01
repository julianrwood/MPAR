import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QAction, QFileDialog
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap
from PyQt5.QtCore import Qt, QPoint


class PaintCanvas(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()
        self.drawing = False
        self.lastPoint = None
        self.strokes = []

    def initUI(self):
        self.setGeometry(0, 0, self.parent.width(), self.parent.height())
        self.setAutoFillBackground(True)
        self.setBackgroundRole(self.palette().Window)
        self.setStyleSheet("background-color: white;")

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor(0, 0, 0), 50, Qt.SolidLine)
        painter.setPen(pen)

        for stroke in self.strokes:
            painter.drawPolyline(stroke)

        if self.drawing and self.lastPoint:
            painter.drawLine(self.lastPoint, self.currentPoint)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()
            self.strokes.append([self.lastPoint])

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.drawing:
            self.currentPoint = event.pos()
            self.strokes[-1].append(self.currentPoint)
            self.update()
            self.lastPoint = self.currentPoint

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            self.lastPoint = None
