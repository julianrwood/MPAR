import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QFileDialog, QDockWidget
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import Qt, QRectF, pyqtSlot

import qdarkgraystyle

# Importing the ui elements
import src.ui.imageViewer as imageViewer
import src.ui.annotations as imageAnnotations
import src.ui.widgets.annotationDrawings as annotationDrawings
import src.ui.sources as sources
import src.ui.tools as tools
import src.ui.timeline as timeline

# Importing self utility classes
import src.utilities.viewClass as SIC

class MediaViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Media Viewer')
        self.setMinimumSize(int(1920/2), int(1080/2))
        self.setStyleSheet(qdarkgraystyle.load_stylesheet())
        self.setStyleSheet("background-color: #2B2B2B;")
        self.initUI()
        
    def initUI(self):
        """
        This is the main kick off point of the program. We build the initial docked menus
            and the menu bar.
        """
        self.buildMenuBar()
        #Create the docked tools menu
        self.toolsDock = QDockWidget("Tool Shelf", self)
        self.toolsDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea)
        self.toolsMenu = tools.ToolsMenu(self)
        self.toolsDock.setWidget(self.toolsMenu)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.toolsDock)

        # Create the docked annotations window
        self.annotationDock = QDockWidget("Annotations", self)
        self.annotationDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea)
        self.annotationDockWidget = imageAnnotations.AnnotationWidget(self)
        self.annotationDock.setWidget(self.annotationDockWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.annotationDock)

        # Create the docked sources window
        self.sourcesDock = QDockWidget("Sources", self)
        self.sourcesDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea)
        self.sourcesDockWidget = sources.SourcesWidget(self)
        self.sourcesDock.setWidget(self.sourcesDockWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.sourcesDock)

        #Create the docked timeline menu
        self.timelineDock = QDockWidget("TimeLine", self)
        self.timelineDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea)
        self.timelineMenu = timeline.MainWindow()
        self.timelineDock.setWidget(self.timelineMenu)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.timelineDock)

        # Create an instance of ImageView
        self.view = imageViewer.ImageView(self, self.sourcesDockWidget)
        self.view.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.view)

        self.toolsMenu.brushToolSelected.connect(self.enterAnnotationMode)
        self.toolsMenu.selectToolSelected.connect(self.enterSelectionMode)       
        
    def buildMenuBar(self):
        """
        The entry point for all menu bar buildings
        """
        self.menu = self.menuBar()
        self.buildFileMenu()
        self.BuildToolMenu()
    
    def buildFileMenu(self):
        """
        The entry point for our QfileBrowser window
        """
        fileMenu = self.menu.addMenu('File')
        openImageAction = QAction('Open Image', self)
        openImageAction.triggered.connect(self.openImage)
        fileMenu.addAction(openImageAction)

    def BuildToolMenu(self):
        """
        The connection and entry point for the tool shelf menu that currently doesn't 
            Add anything to the ui. It will add the annotations menu into it
        """
        fileMenu = self.menu.addMenu('Tools')
        openImageAction = QAction('Annotations', self)
        openImageAction.triggered.connect(self.anotations)
        fileMenu.addAction(openImageAction)
    
    def anotations(self):
        """
        #ToDo: We'll want to show the annotations window if 
        # it's been either closed or had it's visibility turned off
        # This function will create and dock a new instance of the annotations window when 
        # any call to create it is made. 
        """
        print('Docking annotations window')

    def openImage(self):
        """
        A simple QFileDialog viewer for browsing to PYQT native image files
        # ToDo: Once exr capibility is allowed beging to restrict the extensions 
                to only be what we support. At the moment we pretend to support everything haha? 
        """
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)", options=options)

        self.loadImage(fileName)

    def getActiveImageViewer(self):
        """
        This function allows us to retreive the viewer after it is created.
        This is important to our Sources tab as it gets created before 
        The imageView and is isn't allowed to have it parsed to it. 
        """
        return self.view

    @pyqtSlot()
    def enterAnnotationMode(self):
        """
        Allows us to tell our ImageView that we have entered annotation mode
        """
        self.view.setToolType('Brush')

    @pyqtSlot()
    def enterSelectionMode(self):
        """
        Allows us to tell ImageView that we entered selectionMode
        """
        self.view.setToolType('Select')

    def getToolMode(self):
        """
        We get our toolMode from theImageView as this is responsible for keeping track of 
        which tool type we are in
        """
        return self.view.getToolType()

    def getImageViewer(self):
        return self.view

def main():
    app = QApplication(sys.argv)
    viewer = MediaViewer()
    viewer.show()
    sys.exit(app.exec_())
