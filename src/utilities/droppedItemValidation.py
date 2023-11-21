"""
This class is used to handle any incoming dropped file. It'll then be able to process the extension correctly
and return a class of that type file. There will probably be another utility class for converting video files
into their individual Pixmap frames to be loaded when the timeline is changed
"""
import os

from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPen, QImage
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
#from PyQt5.QtWidgets import QGraphicsVideoItem

import imageio
import numpy as np

import src.utilities.viewClass as MPARUtils_SIC


class ItemDistributionAndValidation():

    def __init__(self, filePath, mediaViewer):
        self.mediaViewer = mediaViewer
        extension = self.extractExtension(filePath)
        imageClass = self.processExtension(extension, filePath)

    def extractExtension(self, filePath):
        if filePath:
            # Extract the file extension
            fileExtension = os.path.splitext(filePath)[-1].lower()
            return fileExtension
    
    def processExtension(self, fileExtension, filePath):
        # Check if the file extension is one that PyQt5 can handle natively
        if fileExtension in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tif', '.tiff']:
            # Handle the file using PyQt5's native handling for these formats
            # For example, you can use QPixmap for images
            pixmap = QPixmap(filePath)
            self.pixmap = pixmap
            self.output = 'pixmap'
            self.viewClass = MPARUtils_SIC.SingleImageClass(filePath, self.mediaViewer, self.pixmap)
            return self.viewClass

        if fileExtension in ['.mp4', '.mov', '.webm']:
            self.output = 'video'
            self.viewClass = MPARUtils_SIC.VideoClass(filePath, self.mediaViewer)
            return self.viewClass
        
        elif fileExtension in ['.exr']:
            pixmap = self.exrToPixmap(filePath)
            self.pixmap = pixmap
            self.output = 'exr'
            return pixmap
        else:
            # This is basically an auto failure and isntant software crash at the moment
            self.label.setText("Unsupported file format: "+fileExtension)
    
    def getViewClass(self):
        return self.viewClass
        
    def exrToPixmap(self, exrImage):
        """
        This doesn't work and I don't know why, it just makes pixelated shit
        """
        
        # Read the EXR image
        exrImage = imageio.imread(exrImage)

        # Create a NumPy array with float32 values
        width, height, channel = exrImage.shape
        float32_data = exrImage.astype(np.float32)  # Example data

        # Scale the float values to the 8-bit integer range (0-255)
        #scaled_data = ((float32_data - float32_data.min()) / (float32_data.max() - float32_data.min()) * 255).astype(np.uint8)

        # Create a QImage from the scaled data
        q_image = QImage(float32_data.data, width, height, QImage.Format_ARGB32)

        # Test save
        #q_image.save('C:/Users/Julian/projects/hamish/blender/output/v001/conerted.png')

        print('made a QImage')
        # Create a QPixmap from the QImage (optional)
        pixmap = QPixmap.fromImage(q_image)

        return pixmap
    
    def getPixmap(self):
        return self.pixmap