import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
import imageio
import numpy as np

class EXRViewer(QMainWindow):
    def __init__(self, exr_filename):
        super().__init__()
        self.setWindowTitle("EXR Viewer")

        # Load EXR Image
        exr_data = imageio.imread(exr_filename)
        q_img = self.numpy_array_to_qpixmap(exr_data)

        # Create QLabel to display the image
        label = QLabel()
        label.setPixmap(q_img)

        # Set up the main layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(label)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def numpy_array_to_qpixmap(self, arr):
        height, width, channel = arr.shape
        bytes_per_line = 3 * width
        q_img = QPixmap.fromImage(QImage(arr.data, width, height, bytes_per_line, QImage.Format_RGB888))
        return q_img

if __name__ == '__main__':
    app = QApplication(sys.argv)
    exr_file_path = 'C:/Users/Julian/projects/hamish/blender/output/v001/room_1_v001_####.exr'
    viewer = EXRViewer(exr_file_path)
    viewer.show()
    sys.exit(app.exec_())