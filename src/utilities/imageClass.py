from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsPixmapItem, QGraphicsScene, QGraphicsPixmapItem, QGraphicsItem
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import Qt, QPoint, QRectF

import src.utilities.droppedItemValidation as MPARUtils_DIV


class SingleImageClass():
    def __init__(self, imagePath):
        self.filePath = imagePath
        validatedImage = MPARUtils_DIV.pixMapConversion(self.filePath)
        self.pixmap = validatedImage.getPixmap()
        self.graphicScene = QGraphicsScene()
        self.addPixmapToScene()

    def getFilepath(self):
        return self.filePath

    def getPixmap(self):
        return self.pixmap
    
    def addPixmapToScene(self):
        self.pixmapItem = QGraphicsPixmapItem(self.pixmap)

        # Create a larger background rectangle
        # ToDo: make the bounding rectangle be triple the size of the loaded image
        self.background = self.graphicScene.addRect(QRectF(0, 0, 16000, 16000), QPen(Qt.NoPen), QBrush(QColor("#2B2B2B")))
        
        # Calculate the center of the background rectangle
        backgroundCenter = self.background.sceneBoundingRect().center()

        # Set the position of the pixmap item to the calculated center
        self.pixmapItem.setPos(backgroundCenter.x() - self.pixmap.width() / 2, backgroundCenter.y() - self.pixmap.height() / 2)

        # Add the image on top of the background
        self.graphicScene.addItem(self.pixmapItem)
        #self.graphicScene(pixmapItem)

    def getGraphicsScene(self):
        return self.graphicScene
    
    def getBackground(self):
        return self.background
    
    def getPixmapItem(self):
        return self.pixmapItem
