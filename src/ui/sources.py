from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QColorDialog, QLabel, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QPainter, QColor, QPen, QPainter, QPalette, QColor, QConicalGradient, QIcon
from PyQt5.QtCore import Qt, QPointF, pyqtSignal, QVariant

class SourcesWidget(QWidget):

    def __init__(self, mediaPlayer, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Sources')
        self.setMaximumHeight(300)
        #self.setSize(300, 300)
        # Create layout for the annotation widget
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.mediaPlayer = mediaPlayer

        self.tree_widget = QTreeWidget(self)
        #self.setCentralWidget(self.tree_widget)

        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.itemDoubleClicked.connect(self.childClicked)

        self.populateTreeWidget()

        # Add opacity slider and buttons to the main layout
        layout.addWidget(self.tree_widget)

        # Set the layout for the widget
        self.setLayout(layout)

    def populateTreeWidget(self):
        self.fileParent = QTreeWidgetItem(self.tree_widget, ['Files'])
        self.contactSheetsParent = QTreeWidgetItem(self.tree_widget, ['Contact sheets'])
        self.sequencesParent = QTreeWidgetItem(self.tree_widget, ['Sequences'])

    def addFileChild(self, imageClass):
        child = QTreeWidgetItem(self.fileParent, [imageClass.getFilepath().split('/')[-1]])

        # Here we actually establish the link between the viewer and the sources window. 
        # It's kind of shit actually. I'd rather be able to parse the viewer to the class. 
        # I might be able to put a function in that requests the Image viewer from the main ui
        self.imageViewer = self.mediaPlayer.getActiveImageViewer()

        # Set dictionary as data on an item
        data_dict = {'type':'Image','imageClass': imageClass}
        child.setData(1, Qt.DisplayRole, QVariant(data_dict))

        return child
    
    def childClicked(self, item):
        data = item.data(1, Qt.DisplayRole)

        if data['type'] == 'Image':
            self.imageViewer.setViewedItem(data['imageClass'])






