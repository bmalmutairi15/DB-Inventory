'''
MIT License
Copyright (c) 2017 Gerard Marull-Paretas <gerardmarull@gmail.com>
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
from os.path import join, dirname, abspath

from PySide2.QtCore import Qt, QMetaObject, Signal, Slot, QEvent
from PySide2.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QToolButton,
                            QLabel, QSizePolicy)
from PySide2.QtGui import QIcon

class WindowDragger(QWidget):
    """ Window dragger.

        Args:
            window (QWidget): Associated window.
            parent (QWidget, optional): Parent widget.
    """

    doubleClicked = Signal()

    def __init__(self, window, parent=None):
        QWidget.__init__(self, parent)

        self._window = window
        self._mousePressed = False

    def mousePressEvent(self, event):
        self._mousePressed = True
        self._mousePos = event.globalPos()
        self._windowPos = self._window.pos()

    def mouseMoveEvent(self, event):
        if self._mousePressed:
            self._window.move(self._windowPos +
                              (event.globalPos() - self._mousePos))

    def mouseReleaseEvent(self, event):
        self._mousePressed = False

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()


class ModernWindow(QWidget):
    """ Modern window.

        Args:
            w (QWidget): Main widget.
            parent (QWidget, optional): Parent widget.
    """

    def __init__(self, w, parent=None,theme=None):
        QWidget.__init__(self, parent)
        global _FL_STYLESHEET
        global iconclose
        global iconminimize
        global iconmaximize
        global iconrestore
        
        if theme == 'dark':

            _FL_STYLESHEET = join(dirname(abspath(__file__)), 'resources/frameless.qss')
            iconclose = join(dirname(abspath(__file__)), 'resources/icon_close.png')
            iconminimize = join(dirname(abspath(__file__)), 'resources/icon_minimize.png')
            iconmaximize = join(dirname(abspath(__file__)), 'resources/icon_maximize.png')
            iconrestore = join(dirname(abspath(__file__)), 'resources/icon_restore.png')
        elif theme == 'light':

            _FL_STYLESHEET = join(dirname(abspath(__file__)), 'resources/frameless.qss')
            iconclose = join(dirname(abspath(__file__)), 'resources/icon_close1.png')
            iconminimize = join(dirname(abspath(__file__)), 'resources/icon_minimize1.png')
            iconmaximize = join(dirname(abspath(__file__)), 'resources/icon_maximize1.png')
            iconrestore = join(dirname(abspath(__file__)), 'resources/icon_restore1.png')
        elif theme == 'darkblue':

            _FL_STYLESHEET = join(dirname(abspath(__file__)), 'resources/windows.qss')
            iconclose = join(dirname(abspath(__file__)), 'resources/icon_close.png')
            iconminimize = join(dirname(abspath(__file__)), 'resources/icon_minimize.png')
            iconmaximize = join(dirname(abspath(__file__)), 'resources/icon_maximize.png')
            iconrestore = join(dirname(abspath(__file__)), 'resources/icon_restore.png')
        elif theme == 'darkorange':
            _FL_STYLESHEET = join(dirname(abspath(__file__)), 'resources/windows.qss')
            iconclose = join(dirname(abspath(__file__)), 'resources/icon_close.png')
            iconminimize = join(dirname(abspath(__file__)), 'resources/icon_minimize.png')
            iconmaximize = join(dirname(abspath(__file__)), 'resources/icon_maximize.png')
            iconrestore = join(dirname(abspath(__file__)), 'resources/icon_restore.png')
        #print(theme,_FL_STYLESHEET)
        self._w = w
        self.setupUi()

        contentLayout = QHBoxLayout()
        contentLayout.setContentsMargins(0, 0, 0, 0)
        contentLayout.addWidget(w)

        self.windowContent.setLayout(contentLayout)

        self.setWindowTitle(w.windowTitle())
        self.setGeometry(w.geometry())

        # Adding attribute to clean up the parent window when the child is closed
        self._w.setAttribute(Qt.WA_DeleteOnClose, True)
        self._w.destroyed.connect(self.__child_was_closed)

    def setupUi(self):
        # create title bar, content
        self.vboxWindow = QVBoxLayout(self)
        self.vboxWindow.setContentsMargins(0, 0, 0, 0)

        self.windowFrame = QWidget(self)
        self.windowFrame.setObjectName('windowFrame')

        self.vboxFrame = QVBoxLayout(self.windowFrame)
        self.vboxFrame.setContentsMargins(0, 0, 0, 0)

        self.titleBar = WindowDragger(self, self.windowFrame)
        self.titleBar.setObjectName('titleBar')
        self.titleBar.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,
                                                QSizePolicy.Fixed))

        self.hboxTitle = QHBoxLayout(self.titleBar)
        self.hboxTitle.setContentsMargins(0, 0, 0, 0)
        self.hboxTitle.setSpacing(0)

        self.lblTitle = QLabel('Title')
        self.lblTitle.setObjectName('lblTitle')
        self.lblTitle.setAlignment(Qt.AlignCenter)

        spButtons = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.btnMinimize = QToolButton(self.titleBar)
        self.btnMinimize.setObjectName('btnMinimize')
        self.btnMinimize.setSizePolicy(spButtons)
        self.btnMinimize.setIcon(QIcon(iconminimize))

        self.btnRestore = QToolButton(self.titleBar)
        self.btnRestore.setObjectName('btnRestore')
        self.btnRestore.setSizePolicy(spButtons)
        self.btnRestore.setVisible(False)
        self.btnRestore.setIcon(QIcon(iconrestore))

        self.btnMaximize = QToolButton(self.titleBar)
        self.btnMaximize.setObjectName('btnMaximize')
        self.btnMaximize.setSizePolicy(spButtons)
        self.btnMaximize.setIcon(QIcon(iconmaximize))

        self.btnClose = QToolButton(self.titleBar)
        self.btnClose.setObjectName('btnClose')
        self.btnClose.setSizePolicy(spButtons)
        self.btnClose.setIcon(QIcon(iconclose))

        self.vboxFrame.addWidget(self.titleBar)

        self.windowContent = QWidget(self.windowFrame)
        self.vboxFrame.addWidget(self.windowContent)

        self.vboxWindow.addWidget(self.windowFrame)

        
        self.hboxTitle.addWidget(self.lblTitle)
        self.hboxTitle.addWidget(self.btnMinimize)
        self.hboxTitle.addWidget(self.btnRestore)
        self.hboxTitle.addWidget(self.btnMaximize)
        self.hboxTitle.addWidget(self.btnClose)

        # set window flags
        self.setWindowFlags(
                Qt.Window | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)

        self.setAttribute(Qt.WA_TranslucentBackground)

        # set stylesheet
        with open(_FL_STYLESHEET) as stylesheet:
            self.setStyleSheet(stylesheet.read())

        # automatically connect slots
        QMetaObject.connectSlotsByName(self)

    def __child_was_closed(self):
        self._w = None  # The child was deleted, remove the reference to it and close the parent window
        self.close()

    def closeEvent(self, event):
        if not self._w:
            event.accept()
        else:
            self._w.close()
            event.setAccepted(self._w.isHidden())

    def setWindowTitle(self, title):
        """ Set window title.

            Args:
                title (str): Title.
        """

        super(ModernWindow, self).setWindowTitle(title)
        self.lblTitle.setText(title)

    @Slot()
    def on_btnMinimize_clicked(self):
        self.setWindowState(Qt.WindowMinimized)

    @Slot()
    def on_btnRestore_clicked(self):
        self.btnRestore.setVisible(False)
        self.btnMaximize.setVisible(True)

        self.setWindowState(Qt.WindowNoState)

    @Slot()
    def on_btnMaximize_clicked(self):
        self.btnRestore.setVisible(True)
        self.btnMaximize.setVisible(False)

        self.setWindowState(Qt.WindowMaximized)

    @Slot()
    def on_btnClose_clicked(self):
        self.close()

    @Slot()
    def on_titleBar_doubleClicked(self):
        if self.btnMaximize.isVisible():
            self.on_btnMaximize_clicked()
        else:
            self.on_btnRestore_clicked()
