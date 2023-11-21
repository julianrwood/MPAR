import os
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets

class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)

        self._scene = QtWidgets.QGraphicsScene()
        self._gv = QtWidgets.QGraphicsView(self._scene)

        self._videoitem = QtMultimediaWidgets.QGraphicsVideoItem()
        self._scene.addItem(self._videoitem)

        self._player = QtMultimedia.QMediaPlayer(self, QtMultimedia.QMediaPlayer.VideoSurface)
        self._player.stateChanged.connect(self.on_stateChanged)
        self._player.setVideoOutput(self._videoitem)

        self._player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile('C:/Users/Julian/Downloads/hotMilk_awfullEverAFter.mp4')))
        button = QtWidgets.QPushButton("Play")
        button.clicked.connect(self._player.play)

        self.resize(640, 480)
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self._gv)
        lay.addWidget(button)

    @QtCore.pyqtSlot(QtMultimedia.QMediaPlayer.State)
    def on_stateChanged(self, state):
        print('stateChanged')
        if state == QtMultimedia.QMediaPlayer.PlayingState:
            self._gv.fitInView(self._videoitem, QtCore.Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        bounds = QtCore.QRectF(self._scene.sceneRect())
        self._gv.fitInView(bounds, QtCore.Qt.KeepAspectRatio)
        self._gv.centerOn(bounds.center())

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())