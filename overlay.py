from PyQt5 import QtCore, QtGui, QtWidgets

class Overlay(QtWidgets.QWidget):
    def __init__(self, monitor, targets):
        super().__init__()

        self.monitor = monitor
        self.targets = targets

        self.setGeometry(
            monitor["left"],
            monitor["top"],
            monitor["width"],
            monitor["height"]
        )

        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.Tool
        )

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        self.show()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        font = QtGui.QFont()
        font.setPointSize(12)
        painter.setFont(font)

        colors = {
            "START": QtGui.QColor(0, 255, 0),
            "DEATH": QtGui.QColor(255, 0, 0)
        }

        for name, target in self.targets:
            region = target["region"]

            x = int(region["left"] * self.monitor["width"])
            y = int(region["top"] * self.monitor["height"])
            w = int(region["width"] * self.monitor["width"])
            h = int(region["height"] * self.monitor["height"])

            color = colors.get(name, QtGui.QColor(255, 255, 0))

            pen = QtGui.QPen(color)
            pen.setWidth(3)
            painter.setPen(pen)

            painter.drawRect(x, y, w, h)

        if name == "START":
            painter.drawText(x, y + h, name)
        else:
            painter.drawText(x, y - 5, name)