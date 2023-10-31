from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsPixmapItem, QGraphicsScene, QGraphicsPixmapItem, QGraphicsItem
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import Qt, QPoint, QRectF

# Standard import of custom widgets
import src.ui.widgets.annotationDrawings as annotationDrawings

# Standard import of custom utilities
import src.utilities.droppedItemValidation as MPARUtils_DIV
import src.utilities.paintItem as MPARUtils_PI
 
class SingleImageClass():
    """
    Pretty much anything that wants to be opened in the ImageViewer should come through here.
    At the moment it just supports single images but this will change once we have sequence support.
    We will also support any filetype essentially through here. The validation will bounce the class if
    it detects a file type that we don't read.  
    """
    def __init__(self, imagePath, mediaViewer):
        """
        The init for the provided filepaths
        We first declare the global image path
        Then validate the image through the DIV utlity class (If succesful this will return our pixmap, or pixmaps if an image sequence)
        Then we add these to the QGraphics scene        
        """
        self.mediaViewer = mediaViewer
        self.filePath = imagePath
        validatedImage = MPARUtils_DIV.pixMapConversion(self.filePath)
        
        # Early return incase the validator does it job and fails
        if validatedImage is None:
            return None
        
        self.pixmap = validatedImage.getPixmap()
        self.graphicScene = QGraphicsScene()

        # Create an instance of PaintCanvas and its associated QGraphicsItem
        self.annotationDrawings = annotationDrawings.PaintCanvas(self.mediaViewer.getImageViewer(), self.mediaViewer.annotationDockWidget)
        self.annotationDrawingsItem = MPARUtils_PI.PaintCanvasItem(self.annotationDrawings)
        
        # Add the QGraphicsItem to the scene with a higher Z-value
        self.graphicScene.addItem(self.annotationDrawingsItem)
        self.annotationDrawingsItem.setZValue(0)  # Set a higher Z-value to draw on top

        self.addPixmapToScene()

    def getFilepath(self):
        """
        Returns the filepath of the imageClass

        returns
        -------------
        self.filePath: str(): A string of the filepath related tot his class
        """
        return self.filePath

    def getPixmap(self):
        """
        Returns the generated pixmap

        returns:
        ------------
        self.pixmap: The generated pixmap of the provided image
        None: Returns if there is no pixmap
        """
        if self.pixmap:
            return self.pixmap
        else:
            return None
    
    def addPixmapToScene(self):
        """
        In this function we add the image path to the created QGraphics scene. 
        We also generate the background for the QGraphics scene and set the 
        pixmap to be in the centre of this background
        """
        self.pixmapItem = QGraphicsPixmapItem(self.pixmap)

        # Create a larger background rectangle
        # ToDo: make the bounding rectangle be triple the size of the loaded image
        self.background = self.graphicScene.addRect(QRectF(0, 0, 128000, 128000), QPen(Qt.NoPen), QBrush(QColor("#2B2B2B")))
        
        # Calculate the center of the background rectangle
        backgroundCenter = self.background.sceneBoundingRect().center()

        # Set the position of the pixmap item to the calculated center
        self.pixmapItem.setPos(backgroundCenter.x() - self.pixmap.width() / 2, backgroundCenter.y() - self.pixmap.height() / 2)

        # Add the image on top of the background
        self.graphicScene.addItem(self.pixmapItem)
        #self.graphicScene(pixmapItem)

    def getGraphicsScene(self):
        """
        Returns the graphics scene we're using
        
        returns
        ----------------
        self.graphicsScene: QGraphicsScene() Returns a QGraphics scene object
        """

        return self.graphicScene
    
    def getBackground(self):
        """
        Returns the Background that we created
        
        returns
        ----------------
        self.background: self.graphicScene.addRect() Returns a QGraphicsScene background object
        """
        return self.background
    
    def getPixmapItem(self):
        """
        Returns the generated pixmapItem for a time in the view ( Usually this will be requested and handled automatically)
        
        returns
        ----------
        self.pixmapItem: QGraphicsPixmapItem() The actual Itme of the pixmap once generated into the main QGraphics scene
        """
        return self.pixmapItem
    
    def getAnnoationDrawings(self):
        return self.annotationDrawings
    
    def getAnnotationDrawingsItem(self):
        return self.annotationDrawingsItem
