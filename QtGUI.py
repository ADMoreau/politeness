#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore

from politeness.helpers import set_corenlp_url
from politeness.classifier import Classifier

#Make sure you have StanfordCoreNLP downloaded
#Make sure the corenlp server is running
#example command to run -
#java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000

#Connect to StanfordCoreNLP Server
set_corenlp_url("http://localhost:9000")
cls = Classifier()

font_but = QtGui.QFont()
font_but.setFamily("Segoe UI Symbol")
font_but.setPointSize(10)
font_but.setWeight(95)

class PushBut1(QtWidgets.QPushButton):

    def __init__(self, parent=None):
        super(PushBut1, self).__init__(parent)
        self.setMouseTracking(True)
        self.setStyleSheet("margin: 1px; padding: 7px;                          \
                            background-color: rgba(1,255,0,100);                \
                            color: rgba(1,140,0,100);                           \
                            border-style: solid;                                \
                            border-radius: 3px;                                 \
                            border-width: 0.5px;                                \
                            border-color: rgba(1,140,0,100);")

    def enterEvent(self, event):
        if self.isEnabled() is True:
            self.setStyleSheet("margin: 1px; padding: 7px; background-color: rgba(1,255,255,100); color: rgba(0,230,255,255);"
                               "border-style: solid; border-radius: 3px; border-width: 0.5px; border-color: rgba(0,230,255,255);")
        if self.isEnabled() is False:
            self.setStyleSheet("margin: 1px; padding: 7px; background-color: rgba(1,255,255,100); color: rgba(0,190,255,255); border-style: solid;"
                               "border-radius: 3px; border-width: 0.5px; border-color: rgba(127,127,255,255);")


    def leaveEvent(self, event):
        self.setStyleSheet("margin: 1px; padding: 7px;                          \
                            background-color: rgba(1,255,0,100);                \
                            color: rgba(1,140,0,100);                           \
                            border-style: solid;                                \
                            border-radius: 3px; border-width: 0.5px;            \
                            border-color: rgba(1,140,0,100);")

class politenessApp(QtWidgets.QWidget):

    def getText(self, output):
        out = ''
        length = len(output)
        for i in range(0, length - 1):
            out += "Sentence " + str(i) + ":\n"
            out += "\t" + str(list(output[i].keys())[0]) + "\n"
            vals = list(output[i].values())
            out += "\tP(polite) = " + str(round(vals[0][0], 2)) + "\n"
            out += "\tP(impolite) = " + str(round(vals[0][1], 2)) + "\n"
        out += "---------------------------------------------------------------\n"
        out += "Document :\n"
        vals = list(output[length-1].values())
        out += "\tP(polite) = " + str(round(vals[0][0], 2)) + "\n"
        out += "\tP(impolite) = " + str(round(vals[0][1], 2)) + "\n"
        return out

    def on_but1(self):
        input = self.textIn.toPlainText()
        output = cls.predict(input)
        self.textOut.setText(self.getText(output))


    def on_but2(self):
        self.close()

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("Politeness Analysis")
        #self.setWindowIcon(QtGui.QIcon("Image/path"))
        self.setMinimumWidth(resolution.width() / 2)
        self.setMinimumHeight(resolution.height() / 1.5)
        self.setStyleSheet("QWidget {background-color:                          \
                            rgba(255,255,255,255);}                             \
                            QScrollBar:horizontal {                             \
                            width: 1px; height: 1px;                            \
                            background-color: rgba(0,41,59,255);}               \
                            QScrollBar:vertical { width: 1px;                   \
                            height: 1px;                                        \
                            background-color: rgba(0,41,59,255);}")

        self.textIn = QtWidgets.QTextEdit(self)
        self.textIn.setPlaceholderText("Enter Input")
        self.textIn.setStyleSheet("margin: 1px; padding: 7px;                   \
                                 background-color:                              \
                                 rgba(1,255,255,100);                           \
                                 color: rgba(1,140,255,100);                    \
                                 border-style: solid;                           \
                                 border-radius: 3px;                            \
                                 border-width: 0.5px;                           \
                                 border-color: rgba(1,140,0,100);")

        self.textOut = QtWidgets.QTextEdit(self)
        self.textOut.setPlaceholderText("Output")
        self.textOut.setStyleSheet("margin: 1px; padding: 7px;                  \
                                 background-color:                              \
                                 rgba(1,255,0,100);                             \
                                 color: rgba(1,140,0,100);                      \
                                 border-style: solid;                           \
                                 border-radius: 3px;                            \
                                 border-width: 0.5px;                           \
                                 border-color: rgba(1,140,0,100);")

        self.but1 = PushBut1(self)
        self.but1.setText("Calculate")
        self.but1.setFixedWidth(100)
        self.but1.setFont(font_but)
        self.but2 = PushBut1(self)
        self.but2.setText("Exit")
        self.but2.setFixedWidth(100)
        self.but2.setFont(font_but)
        self.but3 = PushBut1(self)
        self.but3.setText("Help")
        self.but3.setFixedWidth(100)

        self.grid1 = QtWidgets.QGridLayout()
        self.grid1.addWidget(self.textIn, 0, 0, 3, 13)
        self.grid1.addWidget(self.textOut, 4, 0, 9, 13)
        self.grid1.addWidget(self.but1, 0, 14, 1, 1)
        self.grid1.addWidget(self.but2, 1, 14, 1, 1)
        self.grid1.addWidget(self.but3, 2, 14, 1, 1)
        self.grid1.setContentsMargins(7, 7, 7, 7)
        self.setLayout(self.grid1)

        self.but1.clicked.connect(self.on_but1)

        self.but2.clicked.connect(self.on_but2)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    desktop = QtWidgets.QApplication.desktop()
    resolution = desktop.availableGeometry()
    myapp = politenessApp()
    #myapp.setWindowOpacity(0.95)
    myapp.show()
    myapp.move(resolution.center() - myapp.rect().center())
    sys.exit(app.exec())
else:
    desktop = QtWidgets.QApplication.desktop()
    resolution = desktop.availableGeometry()
