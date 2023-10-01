import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsPixmapItem, QGraphicsScene, QGraphicsPixmapItem, QGraphicsItem
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPoint, QRectF

import src.ui.widgets.annotationDrawings as annotationDrawings

# Importing self utility classes
import src.utilities.imageClass as SIC

class PaintCanvasItem(QGraphicsItem):
    def __init__(self, paintCanvas):
        super().__init__()
        self.paintCanvas = paintCanvas

    def boundingRect(self):
        return QRectF(self.paintCanvas.rect())  # Create a QRectF from the QRect

    def paint(self, painter, option, widget):
        # Forward the paint call to the PaintCanvas
        self.paintCanvas.paintEvent(None)

class ImageView(QGraphicsView):
    def __init__(self, MediaViewer):
        super().__init__()
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setInteractive(True)

        self.panning = False
        self.lastDragPosition = None
        self.middleButtonPressed = False

        self.originalViewRect = None
        self.viewedItem = None
        self.altPressed = False

        self.MediaViewer = MediaViewer
        self.toolType = 'Select'  # Default tool is 'Select'

        # Create a QGraphicsScene to manage the items in the view
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        # Create an instance of PaintCanvas and its associated QGraphicsItem
        self.annotationDrawings = annotationDrawings.PaintCanvas(self, self.MediaViewer.annotationDockWidget)
        self.annotationDrawingsItem = PaintCanvasItem(self.annotationDrawings)
        
        # Add the QGraphicsItem to the scene with a higher Z-value
        self.scene.addItem(self.annotationDrawingsItem)
        self.annotationDrawingsItem.setZValue(0)  # Set a higher Z-value to draw on top
        
        self.setAcceptDrops(True)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()

            selfImage = SIC.SingleImageClass(file_path)

            # Load the dropped image using the file_path
            self.MediaViewer.loadImage(selfImage.getFilepath())

    def setViewedItem(self, pixmap):
        self.viewedItem = pixmap

    def wheelEvent(self, event):
        zoomInFactor = 1.25
        zoomOutFactor = 0.8

        if event.angleDelta().y() > 0:
            self.scale(zoomInFactor, zoomInFactor)
        else:
            self.scale(zoomOutFactor, zoomOutFactor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            if self.altPressed:
                self.middleButtonPressed = True
                self.lastDragPosition = event.pos()
            else:
                self.panning = True
                self.lastDragPosition = event.pos()
                self.setCursor(Qt.ClosedHandCursor)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.panning:
            if self.lastDragPosition:
                delta = event.pos() - self.lastDragPosition
                self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
                self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
                self.lastDragPosition = event.pos()
        elif self.middleButtonPressed:
            # Calculate the direction of the drag
            delta = event.pos() - self.lastDragPosition
            if delta.x() < 0:
                zoomFactor = 0.95  # Zoom out
            else:
                zoomFactor = 1.05  # Zoom in

            self.scale(zoomFactor, zoomFactor)
            self.lastDragPosition = event.pos()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleButtonPressed = False
            self.panning = False
            self.setCursor(Qt.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)

    def frameViewedItem(self):
        self.fitInView(self.viewedItem, Qt.KeepAspectRatio)
        self.centerOn(self.viewedItem)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F:  # Check if the 'f' key is pressed
            if self.viewedItem is not None:
                self.frameViewedItem()
        elif event.key() == Qt.Key_Alt:
            self.altPressed = True
        else:
            super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Alt:
            self.altPressed = False
    
    def decideVisible(self):
        if self.toolType == 'Brush':
            self.enableAnnotations()
        elif self.toolType == 'Select':
            self.disableAnnotations()

    def enableAnnotations(self):
        self.annotationDrawings.setVisible(True)
    
    def disableAnnotations(self):
        self.annotationDrawings.setVisible(False)

    def setToolType(self, toolType):
        toolTypes = ['Select', 'Brush']
        if toolType in toolTypes:
            self.toolType = toolType
            self.annotationDrawings.setToolType(toolType)
            self.decideVisible()
        else:
            return None
