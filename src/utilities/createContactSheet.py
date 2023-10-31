from math import sqrt, ceil

# Standard import of Pyqt5 stuff
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsPixmapItem, QGraphicsScene, QGraphicsPixmapItem, QGraphicsItem
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import Qt, QPoint, QRectF

# Standard import of custom widgets
import src.ui.widgets.annotationDrawings as annotationDrawings

# Standard import of custom utilities
import src.utilities.droppedItemValidation as MPARUtils_DIV
import src.utilities.paintItem as MPARUtils_PI


class CreateContactSheetViewable():
    def __init__(self, processedItems, mediaViewer):
        self.processedItems = processedItems
        self.graphicScene = QGraphicsScene()
        self.mediaViewer = mediaViewer
        # Create an instance of PaintCanvas and its associated QGraphicsItem
        self.annotationDrawings = annotationDrawings.PaintCanvas(self.mediaViewer.getImageViewer(), self.mediaViewer.annotationDockWidget)
        self.annotationDrawingsItem = MPARUtils_PI.PaintCanvasItem(self.annotationDrawings)
        
        # Add the QGraphicsItem to the scene with a higher Z-value
        self.graphicScene.addItem(self.annotationDrawingsItem)
        self.annotationDrawingsItem.setZValue(0)  # Set a higher Z-value to draw on top
        
        self.createBackground()
        self.mainKickOff()
        self.autoLayoutItems()
        self.name = 'Contact Sheet'

    def mainKickOff(self):
        for item in self.processedItems:
            data = item.data(1, Qt.DisplayRole)
            imageClass = data['Class']
            pixmap = imageClass.getPixmap()
            self.pixmapItem = imageClass.getPixmapItem()
            self.addPixmap(pixmap, self.pixmapItem)

    def createBackground(self):
        # Create a larger background rectangle
        # ToDo: make the bounding rectangle be triple the size of the loaded image
        self.background = self.graphicScene.addRect(QRectF(0, 0, 32000, 32000), QPen(Qt.NoPen), QBrush(QColor("#2B2B2B")))
    
    def addPixmap(self, pixmap, pixmapItem):
        # Calculate the center of the background rectangle
        backgroundCenter = self.background.sceneBoundingRect().center()

        # Set the position of the pixmap item to the calculated center
        pixmapItem.setPos(backgroundCenter.x() - pixmap.width() / 2, backgroundCenter.y() - pixmap.height() / 2)

        # Add the image on top of the background
        self.graphicScene.addItem(pixmapItem)

    def autoLayoutItems(self):
        items = self.graphicScene.items()

        totalItems = len(items)
        if totalItems == 0:
            return

        # Calculate the number of columns based on a predefined maximum width for each item
        maxColumns = 4  # Define the maximum number of columns
        itemWidth = items[0].boundingRect().width() if items else 0  # Assuming all items have the same width

        # Calculate the number of rows and columns based on the total number of items and the maximum number of columns
        totalColumns = min(totalItems, maxColumns)
        totalRows = (totalItems + totalColumns - 1) // totalColumns

        # Calculate the total width and height of the items
        totalWidth = totalColumns * itemWidth
        totalHeight = totalRows * items[0].boundingRect().height() if items else 0

        # Calculate the starting position for the center alignment
        backgroundCenter = self.background.sceneBoundingRect().center()

        # Calculate the top-left position for the layout
        start_x = backgroundCenter.x() - totalWidth / 2
        start_y = backgroundCenter.y() - totalHeight / 2

        # Iterate through items and position them
        if totalItems > 0:
            for index, item in enumerate(items, start=1):
                itemRect = item.boundingRect()
                itemWidth = itemRect.width()
                itemHeight = itemRect.height()

                currentRow = (index - 1) // totalColumns
                currentColumn = (index - 1) % totalColumns

                xPos = start_x + currentColumn * itemWidth
                yPos = start_y + currentRow * itemHeight

                item.setPos(xPos, yPos)


    def getGraphicsScene(self):
        return self.graphicScene
    
    def setName(self, name):
        self.name = name

    def getAnnoationDrawings(self):
        return self.annotationDrawings
    
    def getAnnotationDrawingsItem(self):
        return self.annotationDrawingsItem

    def getName(self):
        return self.name
    
    def getPixmapItem(self):
        return self.pixmapItem