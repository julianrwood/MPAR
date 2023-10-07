from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPoint

class PaintCanvas(QWidget):
    def __init__(self, parent, annotationWindow):
        super().__init__(parent)
        self.active = False
        self.parent = parent
        self.annotationsWindow = annotationWindow
        
        self.annotationsWindow.clearSignal.connect(self.clearDrawings)
        self.annotationsWindow.undoSignal.connect(self.undoPrevious)
        self.annotationsWindow.redoSignal.connect(self.redo)

        self.initUI()
        self.drawing = False
        self.lastPoint = None
        self.strokes = []
        self.deletedStrokes = []
        self.toolType = "Select"
        self.setVisible(False)

        # Viewport navigation
        self.panning = False
        self.zooming = False
        self.lastDragPosition = None
        self.middleButtonPressed = False

        self.originalViewRect = None
        self.viewedItem = None
        self.altPressed = False

        # Store the original zoom factor
        self.originalZoomFactor = 1.0

    def initUI(self):
        self.setGeometry(0, 0, 16000, 16000)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(self.palette().Window)
        self.setStyleSheet("background-color: white;")

    def paintEvent(self, event):
        painter = QPainter(self)
        for stroke, pen in self.strokes:
            painter.setPen(pen)
            if len(stroke) > 1:
                painter.drawPolyline(*stroke)

        if self.drawing and self.lastPoint:
            painter.setPen(self.annotationsWindow.getPen())  # Use the selected pen for drawing
            painter.drawLine(self.lastPoint, self.currentPoint)
    
    def clearDrawings(self):
        if self.active:
            self.strokes = []
            self.update()
    
    def undoPrevious(self):
        if self.active:
            if self.strokes == []:
                return
            
            self.deletedStrokes.append(self.strokes[-1])
            self.strokes.pop()
            self.update()

    def redo(self):
        if self.active:
            if self.deletedStrokes == []:
                return
            
            self.strokes.append(self.deletedStrokes[-1])
            self.deletedStrokes.pop()
            self.update()

    def mouseMoveEvent(self, event):
        if self.active:
            if (event.buttons() & Qt.LeftButton) and self.drawing:
                self.currentPoint = event.pos()
                stroke = self.strokes[-1][0]
                stroke.append(self.currentPoint)  # Append the point to the current stroke
                self.update()
                self.lastPoint = self.currentPoint

            if self.panning:
                if self.lastDragPosition:
                    delta = event.pos() - self.lastDragPosition
                    self.parent.horizontalScrollBar().setValue(self.parent.horizontalScrollBar().value() - delta.x())
                    self.parent.verticalScrollBar().setValue(self.parent.verticalScrollBar().value() - delta.y())

                    # Update the position of the annotations by adding the delta
                    for stroke, _ in self.strokes:
                        for point in stroke:
                            point.setX(int(point.x() + delta.x()))
                            point.setY(int(point.y() + delta.y()))

                    self.lastDragPosition = event.pos()
                else:
                    self.lastDragPosition = event.pos()  # Track the initial position

            elif self.zooming:
                if self.lastDragPosition:
                    delta = event.pos() - self.lastDragPosition
                    zoomFactor = 1.0 + delta.x() / 100.0  # Adjust the factor as needed

                    # Calculate the center point for zooming (center of the widget)
                    center = self.parent.viewport().rect().center()
                    # Get the current transformation matrix for the view
                    viewTransform = self.parent.transform()
                    # Scale the view's transformation matrix
                    viewTransform.scale(zoomFactor, zoomFactor)
                    # Translate the view's transformation matrix to the center point
                    viewTransform.translate(center.x() * (1 - zoomFactor), center.y() * (1 - zoomFactor))
                    # Set the new transformation matrix for the view
                    self.parent.setTransform(viewTransform)

                    # Calculate the center point for zooming (center of the widget)
                    center = self.parent.viewport().rect().center()

                    # Scale the annotations by the same factor
                    for stroke, _ in self.strokes:
                        for point in stroke:
                            scaledX = int((point.x() - center.x()) * zoomFactor + center.x())
                            scaledY = int((point.y() - center.y()) * zoomFactor + center.y())
                            point.setX(scaledX)
                            point.setY(scaledY)

                    self.lastDragPosition = event.pos()
                else:
                    self.lastDragPosition = event.pos()

            elif self.middleButtonPressed:
                # Calculate the direction of the drag
                delta = event.pos() - self.lastDragPosition
                if delta.x() < 0:
                    zoomFactor = 0.95  # Zoom out
                else:
                    zoomFactor = 1.05  # Zoom in

                # Calculate the center point for zooming (center of the widget)
                center = self.parent.viewport().rect().center()
                # Get the current transformation matrix for the view
                viewTransform = self.parent.transform()
                # Scale the view's transformation matrix
                viewTransform.scale(zoomFactor, zoomFactor)
                # Translate the view's transformation matrix to the center point
                viewTransform.translate(center.x() * (1 - zoomFactor), center.y() * (1 - zoomFactor))
                # Set the new transformation matrix for the view
                self.parent.setTransform(viewTransform)

                # Scale the annotations by the same factor
                for stroke, _ in self.strokes:
                    for point in stroke:
                        point.setX(int(point.x() * zoomFactor))
                        point.setY(int(point.y() * zoomFactor))

                self.lastDragPosition = event.pos()
            else:
                super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if self.active:
            if event.button() == Qt.LeftButton and self.toolType == "Brush":
                self.drawing = True
                self.currentPoint = event.pos()
                self.lastPoint = event.pos()
                self.strokes.append(([], self.annotationsWindow.getPen()))  # Create a new QPen for this stroke

            if event.button() == Qt.MiddleButton:
                if self.altPressed:
                    self.zooming = True
                    self.lastDragPosition = event.pos()
                else:
                    self.panning = True
                    self.lastDragPosition = event.pos()
                    self.setCursor(Qt.ClosedHandCursor)
            else:
                super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.active:
            if event.button() == Qt.LeftButton:
                self.drawing = False
                self.lastPoint = None

            if event.button() == Qt.MiddleButton:
                if self.altPressed:
                    self.zooming = False
                else:
                    self.panning = False
                self.setCursor(Qt.ArrowCursor)
            else:
                super().mouseReleaseEvent(event)
            self.update()

    def frameViewedItem(self):
        self.fitInView(self.viewedItem, Qt.KeepAspectRatio)
        self.centerOn(self.viewedItem)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F:  # Check if the 'f' key is pressed
            self.parent.frameViewedItem()
        elif event.key() == Qt.Key_Alt:
            self.altPressed = True
        else:
            super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Alt:
            self.altPressed = False

    def setToolType(self, toolType):
        toolTypes = ['Select', 'Brush']
        if toolType in toolTypes:
            self.toolType = toolType
        else:
            return None

    def setVisible(self, visible: bool) -> None:
        if visible:
            self.setFocusPolicy(Qt.StrongFocus)
        else:
            self.setFocusPolicy(Qt.NoFocus)
        super().setVisible(visible)
    
    def setActive(self, active):
        if active:
            self.active = True
            self.setVisible(True)
        else:
            self.active = False
            self.setVisible(False)
