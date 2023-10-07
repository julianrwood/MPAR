from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import Qt, QPoint, QRectF

class PaintCanvasItem(QGraphicsItem):
    def __init__(self, paintCanvas):
        super().__init__()
        self.paintCanvas = paintCanvas

    def boundingRect(self):
        return QRectF(self.paintCanvas.rect())  # Create a QRectF from the QRect

    def paint(self, painter, option, widget):
        # Forward the paint call to the PaintCanvas
        self.paintCanvas.paintEvent(None)