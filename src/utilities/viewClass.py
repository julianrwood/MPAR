import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsPixmapItem, QGraphicsScene, QGraphicsPixmapItem, QGraphicsItem, QGraphicsRectItem, QGraphicsProxyWidget
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import Qt, QPoint, QRectF, QTimer, QUrl, pyqtSlot
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget, QGraphicsVideoItem

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
    def __init__(self, imagePath, mediaViewer, pixmap):
        """
        The init for the provided filepaths
        We first declare the global image path
        Then validate the image through the DIV utlity class (If succesful this will return our pixmap, or pixmaps if an image sequence)
        Then we add these to the QGraphics scene        
        """
        self.mediaViewer = mediaViewer
        self.pixmap = pixmap
        self.filePath = imagePath
        
        self.graphicScene = QGraphicsScene()

        # Create an instance of PaintCanvas and its associated QGraphicsItem
        self.annotationDrawings = annotationDrawings.PaintCanvas(self.mediaViewer.getImageViewer(), self.mediaViewer.annotationDockWidget)
        self.annotationDrawingsItem = MPARUtils_PI.PaintCanvasItem(self.annotationDrawings)
        
        # Add the QGraphicsItem to the scene with a higher Z-value
        self.graphicScene.addItem(self.annotationDrawingsItem)
        self.annotationDrawingsItem.setZValue(0)  # Set a higher Z-value to draw on top

        self.addPixmapToScene()

    def getDisplayType(self):
        """
        An Attribute for knowing what kind of class we have
        """
        return 'SingleImage'
    
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

    def frameItem(self, viewedItem, imageView):
        imageView.fitInView(viewedItem.getPixmapItem(), Qt.KeepAspectRatio)
        imageView.centerOn(viewedItem.getPixmapItem())

class VideoClass():
    def __init__(self, videoPath, mediaViewer):

        """
        ToDo: Need to figure out why the video doesn't display, it just plays the audio
        """
        self.mediaViewer = mediaViewer
        self.videoPath = videoPath

        # Create a QGraphicsScene
        self.graphicScene = QGraphicsScene()
        self.graphicView = QGraphicsView(self.graphicScene)

        # Create an instance of PaintCanvas and its associated QGraphicsItem
        self.annotationDrawings = annotationDrawings.PaintCanvas(self.mediaViewer.getImageViewer(), self.mediaViewer.annotationDockWidget)
        self.annotationDrawingsItem = MPARUtils_PI.PaintCanvasItem(self.annotationDrawings)
        
        # Add the QGraphicsItem to the scene with a higher Z-value
        self.graphicScene.addItem(self.annotationDrawingsItem)
        self.annotationDrawingsItem.setZValue(1)  # Set a higher Z-value to draw on top

        # Create a QGraphicsVideoItem
        self.videoItem = QGraphicsVideoItem()
        self.graphicScene.addItem(self.videoItem)

        # Create a QMediaPlayer and set the video output
        self.player = QMediaPlayer(self.graphicScene, QMediaPlayer.VideoSurface)
        self.player.setVideoOutput(self.videoItem)
        #self.player.stateChanged.connect(self.stateChanged)
        self.player.stateChanged.connect(self.stateChanged)

        # Set up the media content
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.videoPath)))

        # Create a background rectangle
        self.background = self.graphicScene.addRect(QRectF(0, 0, 128000, 128000), QPen(Qt.NoPen), QBrush(QColor("#2B2B2B")))

        # Set the position of the video item to the center of the background
        backgroundCenter = self.background.sceneBoundingRect().center()
        #self.videoItem.setPos(backgroundCenter.x() - self.videoItem.boundingRect().width() / 2, backgroundCenter.y() - self.videoItem.boundingRect().height() / 2)
        self.videoItem.setPos(backgroundCenter.x(), backgroundCenter.y())

        print('width of video is: '+ str(self.videoItem.boundingRect().width()))

        self.graphicScene.setSceneRect(self.graphicScene.itemsBoundingRect())

    def stateChanged(self, state):
        print('stateChanged')
        if state == QMediaPlayer.PlayingState:
            self.graphicView.fitInView(self.videoItem, Qt.KeepAspectRatio)

    def getDisplayType(self):
        return 'Video'

    def getFilepath(self):
        return self.videoPath

    def getMediaPlayer(self):
        return self.player

    def getGraphicsScene(self):
        return self.graphicScene

    def getBackground(self):
        return self.background

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def getAnnoationDrawings(self):
        return self.annotationDrawings
    
    def getAnnotationDrawingsItem(self):
        return self.annotationDrawingsItem
    
    def frameItem(self, viewedItem, imageView):
        print('cant frame shit yet')
        #imageView.fitInView(self.viewedItem.getPixmapItem(), Qt.KeepAspectRatio)
        #imageView.centerOn(self.viewedItem.getPixmapItem())