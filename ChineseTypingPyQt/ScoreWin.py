# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ScoreWin.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ScoreWindow(object):
    def setupUi(self, ScoreWindow):
        ScoreWindow.setObjectName("ScoreWindow")
        ScoreWindow.resize(800, 600)
        font = QtGui.QFont()
        font.setFamily("Sans")
        font.setPointSize(12)
        ScoreWindow.setFont(font)
        self.gridLayout_2 = QtWidgets.QGridLayout(ScoreWindow)
        self.gridLayout_2.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.resultText = QtWidgets.QPlainTextEdit(ScoreWindow)
        font = QtGui.QFont()
        font.setFamily("Sans")
        font.setPointSize(18)
        self.resultText.setFont(font)
        self.resultText.setReadOnly(True)
        self.resultText.setObjectName("resultText")
        self.verticalLayout.addWidget(self.resultText)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.saveBtn = QtWidgets.QPushButton(ScoreWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveBtn.sizePolicy().hasHeightForWidth())
        self.saveBtn.setSizePolicy(sizePolicy)
        self.saveBtn.setObjectName("saveBtn")
        self.horizontalLayout.addWidget(self.saveBtn)
        self.discardBtn = QtWidgets.QPushButton(ScoreWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.discardBtn.sizePolicy().hasHeightForWidth())
        self.discardBtn.setSizePolicy(sizePolicy)
        self.discardBtn.setObjectName("discardBtn")
        self.horizontalLayout.addWidget(self.discardBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(ScoreWindow)
        QtCore.QMetaObject.connectSlotsByName(ScoreWindow)

    def retranslateUi(self, ScoreWindow):
        _translate = QtCore.QCoreApplication.translate
        ScoreWindow.setWindowTitle(_translate("ScoreWindow", "評分結果"))
        self.saveBtn.setText(_translate("ScoreWindow", "成績存檔"))
        self.discardBtn.setText(_translate("ScoreWindow", "放棄成績"))

