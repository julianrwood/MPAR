from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QColorDialog, QLabel, QTreeWidget, QTreeWidgetItem, QMenu, QTreeView
from PyQt5.QtGui import QPainter, QColor, QPen, QPainter, QPalette, QColor, QConicalGradient, QIcon
from PyQt5.QtCore import Qt, QPointF, pyqtSignal, QVariant

from src.utilities.createContactSheet import CreateContactSheetViewable

class SourcesWidget(QWidget):

    def __init__(self, mediaPlayer, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Sources')
        self.setMaximumHeight(500)
        # Create layout for the annotation widget
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.mediaPlayer = mediaPlayer

        self.tree_widget = QTreeWidget(self)
        #self.setCentralWidget(self.tree_widget)

        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.itemDoubleClicked.connect(self.childClicked)

        self.tree_widget.setContextMenuPolicy(3)  # CustomContextMenu
        self.tree_widget.customContextMenuRequested.connect(self.customContextMenu)

        self.tree_widget.setSelectionMode(QTreeView.ExtendedSelection)

        self.populateTreeWidget()

        # Add opacity slider and buttons to the main layout
        layout.addWidget(self.tree_widget)

        # Set the layout for the widget
        self.setLayout(layout)

    def customContextMenu(self, point):
        index = self.tree_widget.indexAt(point)
        if not index.isValid():
            return

        # Call the correct context menu creation script depending on what was selected
        item = self.tree_widget.itemFromIndex(index)
        data = item.data(1, Qt.DisplayRole)

        # Quick return in case we tried to call a submenu for a none object
        if data is None:
            return
        
        if data['type'] == 'Image':
            self.createViewablesContextMenu(item, point)

    def createViewablesContextMenu(self, item, point):
        # Create the main context menu
        menu = QMenu(self)
        viewablesSubmenu = QMenu("Viewables")
        menu.addMenu(viewablesSubmenu)

        actionCreateContactSheets = viewablesSubmenu.addAction("Create Contact Sheet viewable")
        ationStackSequenceViewable = viewablesSubmenu.addAction("Create Stack viewable")

        actionCreateContactSheets.triggered.connect(self.createContactSheetViewable)

        action = menu.exec_(self.tree_widget.viewport().mapToGlobal(point))

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
        data_dict = {'type':'Image','Class': imageClass}
        child.setData(1, Qt.DisplayRole, QVariant(data_dict))

        return child
    
    def childClicked(self, item):
        data = item.data(1, Qt.DisplayRole)

        if data['type'] == 'Image' or data['type'] == 'ContactSheet':
            self.imageViewer.setViewedItem(data['Class'])

    def getSelectedItems(self):
        selectedItems = self.tree_widget.selectedItems()
        return selectedItems

    def processSelectedItems(self, searchableClass, selectedItems):
        """
        A function for processing the items to make sure that we have only gathered the requested items and exclude anything we can't use in the main fuction
            that called us.

        searchableClass: str(): The name of the class you want to gather seected items from you can use, Image, ContactSheet, Stack
        selectedItems: list(): Get selected items using self.getSelectedItems() and pass it to this function
        """
        listOfRequestedItems = []

        for item in selectedItems:
            data = item.data(1, Qt.DisplayRole)
            if data['type'] == searchableClass:
                listOfRequestedItems.append(item)

        return listOfRequestedItems

    def createContactSheetViewable(self):
        selectedItems = self.getSelectedItems()
        processedElements = self.processSelectedItems('Image', selectedItems)

        contactSheetViewable = CreateContactSheetViewable(processedElements, self.mediaPlayer)
        self.addContactSheetViewableChild(contactSheetViewable)

    def addContactSheetViewableChild(self, contactSheetViewable):
        child = QTreeWidgetItem(self.contactSheetsParent, [contactSheetViewable.getName()])

        # Here we actually establish the link between the viewer and the sources window. 
        # It's kind of shit actually. I'd rather be able to parse the viewer to the class. 
        # I might be able to put a function in that requests the Image viewer from the main ui
        self.imageViewer = self.mediaPlayer.getActiveImageViewer()

        # Set dictionary as data on an item
        data_dict = {'type':'ContactSheet','Class': contactSheetViewable}
        child.setData(1, Qt.DisplayRole, QVariant(data_dict))

        return child





