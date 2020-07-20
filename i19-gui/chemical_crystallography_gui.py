# coding: utf-8

"""
TODO
 * fix "QObject::connect: Cannot queue arguments of type 'QTextCursor'" error
 * add image ranges
 * add HP functionality
 * add manual input commands
"""

import fnmatch
import glob
import os
import subprocess
from datetime import datetime
from time import sleep

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.dialVersion = ""
        self.datasetPath = ""
        global datasetINPUT
        datasetINPUT = self.datasetPath
        self.processingPath = ""
        self.openingVisit = "/dls/i19-2/data/2020/"
        self.multipleDataset = {}
        self.dataset = ""
        self.visit = ""
        self.runList = []
        global runImageSelector
        runImageSelector = False
        global runSelection
        runSelection = []
        global imageSelection
        imageSelection = {}

        global computingLocation
        computingLocation = "Cluster"

        self.prefix = ""
        global xia2OptionsList
        xia2OptionsList = " small_molecule=true"
        self.xia2command = "xia2 "
        self.tabs = ["tab1", "tab2", "tab3", "tab4", "tab5", "tab6", "tab7", "tab8"]
        self.tabstxt = [
            "tab1t",
            "tab2t",
            "tab3t",
            "tab4t",
            "tab5t",
            "tab6t",
            "tab7t",
            "tab8t",
        ]
        self.tabsIV = ["IV_1", "IV_2", "IV_3", "IV_4", "IV_5", "IV_6", "IV_7", "IV_8"]
        self.tabsRLV = [
            "RLV_1",
            "RLV_2",
            "RLV_3",
            "RLV_4",
            "RLV_5",
            "RLV_6",
            "RLV_7",
            "RLV_8",
        ]
        self.tabsHTML = [
            "HTML_1",
            "HTML_2",
            "HTML_3",
            "HTML_4",
            "HTML_5",
            "HTML_6",
            "HTML_7",
            "HTML_8",
        ]
        self.tabsProcessingPath = [
            "none",
            "none",
            "none",
            "none",
            "none",
            "none",
            "none",
            "none",
        ]
        self.tabsNum = 0

        self.fontSize14B = QtGui.QFont()
        self.fontSize14B.setPointSize(14)
        self.fontSize14B.setBold(True)
        self.fontSize14B.setWeight(75)

        self.fontSize12B = QtGui.QFont()
        self.fontSize12B.setPointSize(10)
        self.fontSize12B.setBold(True)
        self.fontSize12B.setWeight(75)

        self.fontSize10B = QtGui.QFont()
        self.fontSize10B.setPointSize(10)
        self.fontSize10B.setBold(True)
        self.fontSize10B.setWeight(75)

        self.fontSize10 = QtGui.QFont()
        self.fontSize10.setPointSize(10)

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(764, 720)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        # menubar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        ##########################################################################################
        # menu File
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menubar.addAction(self.menuFile.menuAction())
        #
        self.menuFile_Open = QtWidgets.QAction(MainWindow)
        self.menuFile_Open.setObjectName("menuFile_Open")
        self.menuFile.addAction(self.menuFile_Open)
        self.menuFile_Open.triggered.connect(self.selectDataset)
        self.menuFile_Open_Multiple = QtWidgets.QAction(MainWindow)
        self.menuFile_Open_Multiple.setObjectName("menuFile_Open_Multiple")
        self.menuFile.addAction(self.menuFile_Open_Multiple)
        self.menuFile_Open_Multiple.triggered.connect(self.openMultiple)
        self.menuFile_Close_GUI = QtWidgets.QAction(MainWindow)
        self.menuFile_Close_GUI.setObjectName("menuFile_Close_GUI")
        self.menuFile.addAction(self.menuFile_Close_GUI)
        self.menuFile_Close_GUI.triggered.connect(self.closeGUI)
        # menu Edit
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menubar.addAction(self.menuEdit.menuAction())
        #
        self.menuEdit_CopyCommand = QtWidgets.QAction(MainWindow)
        self.menuEdit_CopyCommand.setObjectName("menuEdit_CopyCommand")
        self.menuEdit.addAction(self.menuEdit_CopyCommand)
        self.menuEdit_SaveSettings = QtWidgets.QAction(MainWindow)
        self.menuEdit_SaveSettings.setObjectName("menuEdit_SaveSettings")
        self.menuEdit.addAction(self.menuEdit_SaveSettings)
        self.menuEdit_LoadSettings = QtWidgets.QAction(MainWindow)
        self.menuEdit_LoadSettings.setObjectName("menuEdit_LoadSettings")
        self.menuEdit.addAction(self.menuEdit_LoadSettings)
        # menu View
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menubar.addAction(self.menuView.menuAction())
        # menu Settings
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menubar.addAction(self.menuSettings.menuAction())
        # menu Version
        self.menuVersion = QtWidgets.QMenu(self.menubar)
        self.menuVersion.setObjectName("menuVersion")
        self.menubar.addAction(self.menuVersion.menuAction())
        #
        self.menuVersion_current = QtWidgets.QAction(MainWindow)
        self.menuVersion_current.setObjectName("menuVersion_current")
        self.menuVersion.addAction(self.menuVersion_current)
        self.menuVersion_current.triggered.connect(self.versionCurrent)
        self.menuVersion_latest = QtWidgets.QAction(MainWindow)
        self.menuVersion_latest.setObjectName("menuVersion_latest")
        self.menuVersion.addAction(self.menuVersion_latest)
        self.menuVersion_latest.triggered.connect(self.versionLatest)
        self.menuVersion_now = QtWidgets.QAction(MainWindow)
        self.menuVersion_now.setObjectName("menuVersion_now")
        self.menuVersion.addAction(self.menuVersion_now)
        self.menuVersion_now.triggered.connect(self.VersionNow)
        self.menuVersion_1_4 = QtWidgets.QAction(MainWindow)
        self.menuVersion_1_4.setObjectName("menuVersion_1_4")
        self.menuVersion.addAction(self.menuVersion_1_4)
        self.menuVersion_1_4.triggered.connect(self.Version1_4)
        self.menuVersion_2_1 = QtWidgets.QAction(MainWindow)
        self.menuVersion_2_1.setObjectName("menuVersion_2_1")
        self.menuVersion.addAction(self.menuVersion_2_1)
        self.menuVersion_2_1.triggered.connect(self.Version2_1)

        ##########################################################################################
        self.labelsDataset = QtWidgets.QLabel(self.centralwidget)
        self.labelsDataset.setGeometry(QtCore.QRect(0, 0, 55, 16))
        self.labelsDataset.setObjectName("labelsDataset")
        self.labelsPrefix = QtWidgets.QLabel(self.centralwidget)
        self.labelsPrefix.setGeometry(QtCore.QRect(250, 0, 55, 16))
        self.labelsPrefix.setObjectName("labelsPrefix")
        self.labelsImages = QtWidgets.QLabel(self.centralwidget)
        self.labelsImages.setGeometry(QtCore.QRect(500, 0, 100, 16))
        self.labelsImages.setObjectName("labelsImages")
        self.labelsVersion = QtWidgets.QLabel(self.centralwidget)
        self.labelsVersion.setGeometry(QtCore.QRect(650, 0, 81, 16))
        self.labelsVersion.setObjectName("labelsVersion")

        self.datasetInfo_dataset = QtWidgets.QLabel(self.centralwidget)
        self.datasetInfo_dataset.setGeometry(QtCore.QRect(0, 17, 250, 28))
        self.datasetInfo_dataset.setFont(self.fontSize12B)
        self.datasetInfo_dataset.setObjectName("datasetInfo_dataset")
        self.datasetInfo_prefix = QtWidgets.QLabel(self.centralwidget)
        self.datasetInfo_prefix.setGeometry(QtCore.QRect(250, 17, 151, 28))
        self.datasetInfo_prefix.setFont(self.fontSize12B)
        self.datasetInfo_prefix.setObjectName("datasetInfo_prefix")
        self.datasetInfo_images = QtWidgets.QLabel(self.centralwidget)
        self.datasetInfo_images.setGeometry(QtCore.QRect(500, 17, 300, 28))
        self.datasetInfo_images.setFont(self.fontSize12B)
        self.datasetInfo_images.setObjectName("datasetInfo_images")

        self.datasetInfo_line = QtWidgets.QFrame(self.centralwidget)
        self.datasetInfo_line.setGeometry(QtCore.QRect(0, 43, 761, 16))
        self.datasetInfo_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.datasetInfo_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.datasetInfo_line.setObjectName("datasetInfo_line")

        ##########################################################################################

        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(213, 234, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(149, 202, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(42, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(56, 113, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 212, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(213, 234, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(149, 202, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(42, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(56, 113, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 212, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(42, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(213, 234, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(149, 202, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(42, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(56, 113, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(42, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(42, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)

        self.viewButtons_xia2 = QtWidgets.QPushButton(self.centralwidget)
        self.viewButtons_xia2.setGeometry(QtCore.QRect(5, 60, 151, 31))
        self.viewButtons_xia2.setPalette(palette)
        self.viewButtons_xia2.setFont(self.fontSize10B)
        self.viewButtons_xia2.setObjectName("viewButtons_xia2")
        self.viewButtons_xia2.clicked.connect(self.runXia2)

        self.viewButtons_screen19 = QtWidgets.QPushButton(self.centralwidget)
        self.viewButtons_screen19.setGeometry(QtCore.QRect(165, 60, 151, 31))
        self.viewButtons_screen19.setPalette(palette)
        self.viewButtons_screen19.setFont(self.fontSize10B)
        self.viewButtons_screen19.setObjectName("viewButtons_screen19")
        self.viewButtons_screen19.clicked.connect(self.runScreen19)

        self.viewButtons_options = QtWidgets.QPushButton(self.centralwidget)
        self.viewButtons_options.setGeometry(QtCore.QRect(325, 60, 151, 31))
        self.viewButtons_options.setFont(self.fontSize10)
        self.viewButtons_options.setObjectName("viewButtons_options")
        self.viewButtons_options.clicked.connect(self.openOptions)

        self.viewButtons_albula = QtWidgets.QPushButton(self.centralwidget)
        self.viewButtons_albula.setGeometry(QtCore.QRect(485, 60, 151, 31))
        self.viewButtons_albula.setFont(self.fontSize10)
        self.viewButtons_albula.setObjectName("viewButtons_albula")
        self.viewButtons_albula.clicked.connect(self.runAlbula)

        self.viewButtons_line = QtWidgets.QFrame(self.centralwidget)
        self.viewButtons_line.setGeometry(QtCore.QRect(0, 93, 761, 16))
        self.viewButtons_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.viewButtons_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.viewButtons_line.setObjectName("viewButtons_line")

        ##########################################################################################

        self.processingPath_label = QtWidgets.QLabel(self.centralwidget)
        self.processingPath_label.setGeometry(QtCore.QRect(2, 101, 191, 16))
        self.processingPath_label.setObjectName("processingPath_label")

        self.processingPath__path = QtWidgets.QLabel(self.centralwidget)
        self.processingPath__path.setGeometry(QtCore.QRect(2, 115, 761, 21))
        self.processingPath__path.setFont(self.fontSize10B)
        self.processingPath__path.setObjectName("processingPath__path")

        self.processingPath__line = QtWidgets.QFrame(self.centralwidget)
        self.processingPath__line.setGeometry(QtCore.QRect(-1, 132, 761, 16))
        self.processingPath__line.setFrameShape(QtWidgets.QFrame.HLine)
        self.processingPath__line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.processingPath__line.setObjectName("processingPath__line")

        ##########################################################################################

        self.command_label = QtWidgets.QLabel(self.centralwidget)
        self.command_label.setGeometry(QtCore.QRect(2, 142, 91, 16))
        self.command_label.setObjectName("command_label")

        self.command_command = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.command_command.setGeometry(QtCore.QRect(0, 160, 761, 61))
        self.command_command.setFont(self.fontSize10B)
        self.command_command.setObjectName("command_command")

        self.command_line = QtWidgets.QFrame(self.centralwidget)
        self.command_line.setGeometry(QtCore.QRect(0, 220, 761, 16))
        self.command_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.command_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.command_line.setObjectName("command_line")

        ##########################################################################################
        # xia2 output tabs

        self.xia2output = QtWidgets.QTabWidget(self.centralwidget)
        # self.xia2output.setGeometry(QtCore.QRect(0, 180, 761, 331))
        self.xia2output.setGeometry(QtCore.QRect(0, 230, 761, 441))
        self.xia2output.setObjectName("xia2output")
        self.xia2output.setTabsClosable(True)
        self.xia2output.tabCloseRequested.connect(self.close_handler)

        self.mainTab = QtWidgets.QWidget()
        self.mainTab.setObjectName("mainTab")
        self.mainTab_txt = QtWidgets.QPlainTextEdit(self.mainTab)
        self.mainTab_txt.setGeometry(QtCore.QRect(0, 0, 756, 372))
        self.mainTab_txt.setObjectName("mainTab_txt")
        self.xia2output.addTab(self.mainTab, "")
        self.xia2output.setTabText(self.xia2output.indexOf(self.mainTab), "Main")

        ##########################################################################################

        self.retranslateUi(MainWindow)
        self.xia2output.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        ####################################################

    ####################################################
    ### functions ######

    def appendOutput(self, tabName, newLinesPrint):
        try:
            tabName.appendPlainText(newLinesPrint)
            tabName.moveCursor(QtGui.QTextCursor.End)
        except Exception:
            print("\n\n *** Error with updating tab text *** \n\n")
        finally:
            pass

    def getDialsVersion(self):
        return os.popen("dials.version").read().split("-")[0]

    def selectDataset(self):
        try:
            path = self.openingVisit
            self.datasetPath = QFileDialog.getExistingDirectory(
                None, "Select a dataset folder", path, QFileDialog.ShowDirsOnly
            )
            global datasetINPUT
            datasetINPUT = self.datasetPath
            if self.datasetPath:
                self.multipleDataset = {}
                self.appendOutput(
                    self.mainTab_txt, "\n	Dataset Path:		" + self.datasetPath
                )
                self.dataset = self.datasetPath.split("/")[-1]  # dataset name
                self.visit = "/".join(self.datasetPath.split("/")[:6]) + "/"
                self.openingVisit = str(self.visit)
            self.appendOutput(self.mainTab_txt, "	Dataset:		" + self.dataset)
            for cbfFile in os.listdir(self.datasetPath):  # prefix
                if cbfFile.endswith("_00001.cbf"):
                    self.prefix = cbfFile[:-12]
                    break
                else:
                    continue
                break

            self.appendOutput(self.mainTab_txt, "	Prefix:			" + self.prefix)
            self.runList = []
            runImagesDict = {}
            for cbfFiles in os.listdir(self.datasetPath):  # runs in dataset
                if cbfFiles.endswith("_00001.cbf"):
                    if cbfFiles[:-12] == self.prefix:
                        run = int(cbfFiles[-12:-10])
                        self.runList.append(run)

            self.runList.sort()
            self.appendOutput(
                self.mainTab_txt,
                "	Number of runs:		" + str(len(self.runList)) + " " + str(self.runList),
            )
            for run in self.runList:  # number of images per run
                basenameMatch = self.prefix + "%02d" % (run) + "_*.cbf"
                numCbfRun = len(
                    fnmatch.filter(os.listdir(self.datasetPath), basenameMatch)
                )
                runImagesDict[run] = numCbfRun
            self.appendOutput(
                self.mainTab_txt, "	Images per run: 	" + str(runImagesDict)
            )
            totalNumImages = sum(runImagesDict.values())  # total number of imagess
            self.appendOutput(
                self.mainTab_txt,
                "	Total number of images:	" + str(totalNumImages) + "\n",
            )
            # update lables
            self.datasetInfo_dataset.setText(self.dataset)
            self.datasetInfo_prefix.setText(self.prefix)
            self.datasetInfo_images.setText(str(runImagesDict).strip("{}"))
            self.command_command.setPlainText(
                self.xia2command + datasetINPUT + xia2OptionsList
            )
        except Exception:
            self.appendOutput(self.mainTab_txt, "\n	*** unable to load dataset ***	\n")

    #### file menu, open-> select dataset ####
    def openMultiple(self):
        # try:
        path = self.openingVisit
        newDatasetPath = QFileDialog.getExistingDirectory(
            None, "Select a dataset folder", path, QFileDialog.ShowDirsOnly
        )

        global datasetINPUT
        datasetINPUT = "MULTIPLE"

        if newDatasetPath:
            self.appendOutput(
                self.mainTab_txt, "\n	New Dataset Path:		" + newDatasetPath
            )

            dataset = newDatasetPath.split("/")[-1]  # dataset name
            self.visit = "/".join(newDatasetPath.split("/")[:6]) + "/"
            self.openingVisit = str(self.visit)
        self.appendOutput(self.mainTab_txt, "	New Dataset:		" + dataset)
        for cbfFile in os.listdir(newDatasetPath):  # prefix
            if cbfFile.endswith("_00001.cbf"):
                prefix = cbfFile[:-12]
                break
            else:
                continue
            break

        self.appendOutput(self.mainTab_txt, "	New Prefix:			" + prefix)
        runList = []
        runImagesDict = {}
        for cbfFiles in os.listdir(newDatasetPath):  # runs in dataset
            if cbfFiles.endswith("_00001.cbf"):
                if cbfFiles[:-12] == prefix:
                    run = int(cbfFiles[-12:-10])
                    runList.append(run)

        runList.sort()
        self.appendOutput(
            self.mainTab_txt,
            "	New Number of runs:		" + str(len(runList)) + " " + str(runList),
        )
        for run in runList:  # number of images per run
            basenameMatch = prefix + "%02d" % (run) + "_*.cbf"
            numCbfRun = len(fnmatch.filter(os.listdir(newDatasetPath), basenameMatch))
            runImagesDict[run] = numCbfRun
        self.appendOutput(
            self.mainTab_txt, "	New Images per run: 	" + str(runImagesDict)
        )
        totalNumImages = sum(runImagesDict.values())  # total number of imagess
        self.appendOutput(
            self.mainTab_txt,
            "	New Total number of images:	" + str(totalNumImages) + "\n",
        )
        # update lables
        self.datasetInfo_dataset.setText(dataset)
        self.datasetInfo_prefix.setText(prefix)
        self.datasetInfo_images.setText(str(runImagesDict).strip("{}"))
        self.command_command.setPlainText(
            self.xia2command + datasetINPUT + xia2OptionsList
        )

        self.multipleDataset[dataset] = [newDatasetPath, prefix, runList]
        self.appendOutput(
            self.mainTab_txt, "	Multiple runs:\n	" + str(self.multipleDataset)
        )

    # except Exception:
    # self.appendOutput(self.mainTab_txt,"\n	*** unable to load datasets ***	\n")

    #### file menu, close -> close GUI ####
    def closeGUI(self):
        self.appendOutput(self.mainTab_txt, "\n\nClosing GUI\n\n")
        QtCore.QCoreApplication.instance().quit()

    #### open albula ####
    def runAlbula(self):
        self.appendOutput(self.mainTab_txt, self.datasetPath)
        if self.datasetPath == "":
            subprocess.Popen(
                ["sh", "/dls_sw/i19/scripts/MarkWarren/PyQT/1_basic/albula.sh"]
            )
        else:
            self.appendOutput(self.mainTab_txt, "opening albula with first image")
            image = (
                self.datasetPath
                + "/"
                + self.prefix
                + "%02d" % (self.runList[0])
                + "_00001.cbf"
            )
            subprocess.Popen(
                ["sh", "/dls_sw/i19/scripts/MarkWarren/PyQT/1_basic/albula.sh", image]
            )

    #### open options window #####################################################################################################################
    def openOptions(self):
        self.appendOutput(self.mainTab_txt, "Opeining Optioins window")
        self.secondWindow = QtWidgets.QMainWindow()
        self.ui = Ui_Xia2Options(
            self.xia2command,
            self.datasetPath,
            self.command_command,
            self.visit,
            self.mainTab_txt,
            self.runList,
            self.prefix,
            self.openingVisit,
        )
        self.ui.setupUi(self.secondWindow)
        self.secondWindow.show()

    def updateOptionsFunction(xia2command, datasetPath, command_command):
        command_command.setPlainText(xia2command + datasetPath + xia2OptionsList)

    def runXia2(self):
        self.appendOutput(self.mainTab_txt, "\nRunning xia2\n")
        ###### single datasets ###########
        if not datasetINPUT == "MULTIPLE":
            self.appendOutput(self.mainTab_txt, "Single Dataset")
            if self.prefix == "":
                self.appendOutput(
                    self.mainTab_txt,
                    "\n\n " "########################################################a",
                )
                self.appendOutput(
                    self.mainTab_txt,
                    "	No cbf images found in directory, "
                    "please select dataset directory",
                )
                return
            self.runXia2dataset(self.dataset, datasetINPUT)
        ###### multiple datasets ###########
        if datasetINPUT == "MULTIPLE":  # if multiple input has been utilised
            self.appendOutput(self.mainTab_txt, "\n Multiple dataset proocessing\n")
            # {'01_Prot1_21': ['/dls/i19-2/data/2020/cy23401-1/01_Prot1_21', 'Prot1_21_', [1, 2, 3]]}
            # {dataset: [datasetPath, prefix, runs]}
            if not runImageSelector:
                for datasetKey in self.multipleDataset:
                    datasetPath = self.multipleDataset[datasetKey][0]
                    prefix = self.multipleDataset[datasetKey][1]
                    if prefix == "":
                        self.appendOutput(
                            self.mainTab_txt,
                            "\n\n "
                            "########################################################b",
                        )
                        self.appendOutput(
                            self.mainTab_txt,
                            "	No cbf images found in directory, "
                            "please select dataset directory",
                        )
                        return
                    self.runXia2dataset(datasetKey, datasetPath)
            else:
                for datasetKey in self.multipleDataset:
                    dataset = datasetKey
                    datasetPath = self.multipleDataset[datasetKey][0] + "/"
                    prefix = self.multipleDataset[datasetKey][1]
                    runs = self.multipleDataset[datasetKey][2]
                    if prefix == "":
                        self.appendOutput(
                            self.mainTab_txt,
                            "\n\n "
                            "########################################################c",
                        )
                        self.appendOutput(
                            self.mainTab_txt,
                            "	No cbf images found in directory, "
                            "please select dataset directory",
                        )
                        return
                    else:
                        xia2Input = ""
                        if runSelection:
                            for entry in runSelection:
                                xia2Input = (
                                    xia2Input
                                    + " image="
                                    + datasetPath
                                    + prefix
                                    + str("%02d_00001.cbf" % int(entry))
                                )
                                if entry in imageSelection:
                                    xia2Input = xia2Input + ":" + imageSelection[entry]
                        else:  # runs have NOT been selected
                            for run in runs:
                                xia2Input = (
                                    xia2Input
                                    + " image="
                                    + datasetPath
                                    + prefix
                                    + str("%02d_00001.cbf" % int(run))
                                )
                                if (run - 1) in imageSelection:
                                    xia2Input = (
                                        xia2Input + ":" + imageSelection[run - 1]
                                    )
                    self.runXia2dataset(dataset, xia2Input)

    def runXia2dataset(self, inputDataset, xia2Input):  # prefix # visit # dataset
        # create processing path
        timeDate = str(datetime.utcnow().strftime("%Y%m%d_%H%M"))
        self.processingPath = (
            self.visit + "processing/xia2GUI/" + inputDataset + "_" + timeDate + "/"
        )
        if not os.path.exists(self.visit + "processing/xia2GUI/"):
            os.makedirs(self.visit + "processing/xia2GUI/")
        if not os.path.exists(self.processingPath):
            os.makedirs(self.processingPath)

        self.processingPath__path.setText(self.processingPath)
        self.tabsProcessingPath[self.tabsNum] = self.processingPath

        self.appendOutput(self.mainTab_txt, "Xia2 command:")
        inputXia2Command = (
            self.xia2command + xia2Input + xia2OptionsList
        )  # this is the bit I think i need to change!!! # dataset and prefix I would guess is required
        self.appendOutput(self.mainTab_txt, "	" + inputXia2Command)

        # create job file

        jobFile = self.processingPath + "job.sh"
        with open(jobFile, "a") as jF:
            jF.write(str("cd " + self.processingPath) + "\n")
            jF.write(str("module load dials" + self.dialVersion) + "\n")
            jF.write(str(inputXia2Command) + "\n")

        ###################################################################################################################
        ### open new tab with dataset and date
        self.tabs[self.tabsNum] = QtWidgets.QWidget()
        self.tabs[self.tabsNum].setObjectName("tabs[tabNum]")

        # plain text
        # clear previous??
        self.tabstxt[self.tabsNum] = QtWidgets.QPlainTextEdit(self.tabs[self.tabsNum])
        self.tabstxt[self.tabsNum].setGeometry(QtCore.QRect(0, 32, 756, 372))
        self.tabstxt[self.tabsNum].setObjectName("tabstxt[tabNum]")

        # buttons
        tabNum = int(self.tabsNum)

        self.tabsIV[self.tabsNum] = QtWidgets.QPushButton(self.tabs[self.tabsNum])
        self.tabsIV[self.tabsNum].setGeometry(QtCore.QRect(120, 0, 151, 31))
        self.tabsIV[self.tabsNum].setFont(self.fontSize10)
        self.tabsIV[self.tabsNum].setObjectName("xia2output_dialsImage")
        self.tabsIV[self.tabsNum].setText("Image Viewer")
        self.tabsIV[self.tabsNum].clicked.connect(
            lambda: self.runDialsImageViewer(tabNum)
        )

        self.tabsRLV[self.tabsNum] = QtWidgets.QPushButton(self.tabs[self.tabsNum])
        self.tabsRLV[self.tabsNum].setGeometry(QtCore.QRect(270, 0, 151, 31))
        self.tabsRLV[self.tabsNum].setFont(self.fontSize10)
        self.tabsRLV[self.tabsNum].setObjectName("xia2output_reciprocal")
        self.tabsRLV[self.tabsNum].setText("Reciprocal Lattice")
        self.tabsRLV[self.tabsNum].clicked.connect(
            lambda: self.runDialsReciprocalLattice(tabNum)
        )

        self.tabsHTML[self.tabsNum] = QtWidgets.QPushButton(self.tabs[self.tabsNum])
        self.tabsHTML[self.tabsNum].setGeometry(QtCore.QRect(420, 0, 151, 31))
        self.tabsHTML[self.tabsNum].setFont(self.fontSize10)
        self.tabsHTML[self.tabsNum].setObjectName("xia2output_html")
        self.tabsHTML[self.tabsNum].setText("HTML")
        self.tabsHTML[self.tabsNum].clicked.connect(lambda: self.runDialsHTML(tabNum))

        self.xia2output.addTab(self.tabs[self.tabsNum], "")
        self.xia2output.setTabText(
            self.xia2output.indexOf(self.tabs[self.tabsNum]),
            inputDataset + "_" + timeDate,
        )

        # edit plain text
        self.tabstxt[self.tabsNum].appendPlainText("\nRunning xia2\n")
        self.tabstxt[self.tabsNum].appendPlainText("Xia2 command:")
        self.tabstxt[self.tabsNum].appendPlainText("	" + inputXia2Command + "\n")

        ###################################################################################################################
        # run xia2

        if inputDataset == "":
            tabName = self.tabstxt[self.tabsNum]
            datasetErrorStatment = "\n\n Dataset has not be selected (File>Open) \n\n"
            self.appendOutput(self.mainTab_txt, datasetErrorStatment)
            self.appendOutput(tabName, datasetErrorStatment)
        else:
            if computingLocation == "Local":
                # run xai2 locally
                subprocess.Popen(["sh", jobFile])
            else:
                # run xia2 on cluster?
                # module load global/cluster
                # "qsub -pe smp 1 -q medium.q " + jobFile
                # module load global/hamilton
                # qsub -pe smp 20 -cwd -q all.q -P i19-2 -o /dev/null -e /dev/null job.sh
                os.system(
                    "module load global/hamilton && qsub -pe smp 20 -q all.q -P i19-2 -o /dev/null -e /dev/null "
                    + jobFile
                )

            ###################################################################################################################
            # output xia2.txt into tab
            self.thread = mythread2(
                self.processingPath,
                inputDataset,
                self.tabstxt,
                self.tabsNum,
                self.mainTab_txt,
                "xia2.txt",
            )

            self.thread.finished.connect(self.threadFinished)
            self.thread.started.connect(self.threadStarted)
            # self.thread.terminated.connect(self.threadTerminated)

            self.thread.start()

        ###################################################################################################################
        self.tabsNum += 1
        if self.tabsNum > 8:
            self.tabsNum = 0

    def runScreen19(self):
        self.appendOutput(self.mainTab_txt, "\nRunning screen19\n")
        if self.prefix == "":
            self.appendOutput(
                self.mainTab_txt,
                "\n\n ########################################################a",
            )
            self.appendOutput(
                self.mainTab_txt,
                "	No cbf images found in directory, please select dataset directory",
            )
            return
        else:
            # create processing path
            timeDate = str(datetime.utcnow().strftime("%Y%m%d_%H%M"))
            self.processingPath = (
                self.visit
                + "processing/xia2GUI/"
                + self.dataset
                + "_s19_"
                + timeDate
                + "/"
            )
            if not os.path.exists(self.visit + "processing/xia2GUI/"):
                os.makedirs(self.visit + "processing/xia2GUI/")
            if not os.path.exists(self.processingPath):
                os.makedirs(self.processingPath)

            self.processingPath__path.setText(self.processingPath)
            self.tabsProcessingPath[self.tabsNum] = self.processingPath

            self.appendOutput(self.mainTab_txt, "screen19 command:")

            # remove unwanted xia2 commands
            screen19OptionsList = ""
            for command in xia2OptionsList.split(" "):
                if command == "small_molecule=true":
                    pass
                else:
                    screen19OptionsList = screen19OptionsList + command + " "

            inputScreen19Command = "screen19 " + self.datasetPath + screen19OptionsList
            self.appendOutput(self.mainTab_txt, "	" + inputScreen19Command)

            # create job file
            jobFile = self.processingPath + "job.sh"
            with open(jobFile, "a") as jF:
                jF.write(str("cd " + self.processingPath) + "\n")
                jF.write(str("module load dials" + self.dialVersion) + "\n")
                jF.write(str(inputScreen19Command) + "\n")

            ###################################################################################################################
            ### open new tab with dataset and date
            self.tabs[self.tabsNum] = QtWidgets.QWidget()

            self.tabs[self.tabsNum].setObjectName("tabs[tabNum]")

            # plain text
            # clear previous??
            self.tabstxt[self.tabsNum] = QtWidgets.QPlainTextEdit(
                self.tabs[self.tabsNum]
            )
            self.tabstxt[self.tabsNum].setGeometry(QtCore.QRect(0, 32, 756, 372))
            self.tabstxt[self.tabsNum].setObjectName("tabstxt[tabNum]")

            # buttons
            tabNum = int(self.tabsNum)

            self.tabsIV[self.tabsNum] = QtWidgets.QPushButton(self.tabs[self.tabsNum])
            self.tabsIV[self.tabsNum].setGeometry(QtCore.QRect(120, 0, 151, 31))
            self.tabsIV[self.tabsNum].setFont(self.fontSize10)
            self.tabsIV[self.tabsNum].setObjectName("xia2output_dialsImage")
            self.tabsIV[self.tabsNum].setText("Image Viewer")
            self.tabsIV[self.tabsNum].clicked.connect(
                lambda: self.runDialsImageViewer(tabNum)
            )

            self.tabsRLV[self.tabsNum] = QtWidgets.QPushButton(self.tabs[self.tabsNum])
            self.tabsRLV[self.tabsNum].setGeometry(QtCore.QRect(270, 0, 151, 31))
            self.tabsRLV[self.tabsNum].setFont(self.fontSize10)
            self.tabsRLV[self.tabsNum].setObjectName("xia2output_reciprocal")
            self.tabsRLV[self.tabsNum].setText("Reciprocal Lattice")
            self.tabsRLV[self.tabsNum].clicked.connect(
                lambda: self.runDialsReciprocalLattice(tabNum)
            )

            self.tabsHTML[self.tabsNum] = QtWidgets.QPushButton(self.tabs[self.tabsNum])
            self.tabsHTML[self.tabsNum].setGeometry(QtCore.QRect(420, 0, 151, 31))
            self.tabsHTML[self.tabsNum].setFont(self.fontSize10)
            self.tabsHTML[self.tabsNum].setObjectName("xia2output_html")
            self.tabsHTML[self.tabsNum].setText("HTML")
            self.tabsHTML[self.tabsNum].clicked.connect(
                lambda: self.runDialsHTML(tabNum)
            )

            self.xia2output.addTab(self.tabs[self.tabsNum], "")
            self.xia2output.setTabText(
                self.xia2output.indexOf(self.tabs[self.tabsNum]),
                self.dataset + "_s19_" + timeDate,
            )

            # edit plain text
            self.tabstxt[self.tabsNum].appendPlainText("\nRunning screen19\n")
            self.tabstxt[self.tabsNum].appendPlainText("screen19 command:")
            self.tabstxt[self.tabsNum].appendPlainText(
                "	" + inputScreen19Command + "\n"
            )

            ###################################################################################################################
            # run screen19

            if self.dataset == "":
                tabName = self.tabstxt[self.tabsNum]
                datasetErrorStatment = (
                    "\n\n Dataset has not be selected (File>Open) \n\n"
                )
                self.appendOutput(self.mainTab_txt, datasetErrorStatment)
                self.appendOutput(tabName, datasetErrorStatment)
            else:
                if computingLocation == "Local":
                    # run screen19 locally
                    subprocess.Popen(["sh", jobFile])
                else:
                    os.system(
                        "module load global/hamilton && qsub -pe smp 20 -q all.q -P i19-2 -o /dev/null -e /dev/null "
                        + jobFile
                    )

                ###################################################################################################################
                # output xia2.txt into tab
                self.thread = mythread2(
                    self.processingPath,
                    self.dataset,
                    self.tabstxt,
                    self.tabsNum,
                    self.mainTab_txt,
                    "screen19.log",
                )

                self.thread.finished.connect(self.threadFinished)
                self.thread.started.connect(self.threadStarted)
                # self.thread.terminated.connect(self.threadTerminated)

                self.thread.start()

            ###################################################################################################################
            self.tabsNum += 1
            if self.tabsNum > 8:
                self.tabsNum = 0

    def threadStarted(self):
        self.appendOutput(self.mainTab_txt, "\n*** Thread Started ***\n")

    def threadFinished(self):
        self.appendOutput(self.mainTab_txt, "\n*** Thread Finished ***\n")

    def stopThread(self):
        self.appendOutput(self.mainTab_txt, "\n*** Stopping Thead ***\n")
        # self.mythread2.stop()
        # self.mythread2.quit()

    #### open run dials Reciprocal Lattice viewer ####
    def runDialsReciprocalLattice(self, tabsNum):
        self.appendOutput(self.mainTab_txt, "Opening dials reciprocal lattice viewer")
        self.appendOutput(
            self.mainTab_txt, "Processing path:" + self.tabsProcessingPath[tabsNum]
        )

        latestExpt = ""
        latestExptTime = ""
        latestRefl = ""
        latestReflTime = ""

        exptFiles = glob.glob(
            self.tabsProcessingPath[tabsNum] + "/**/*.expt", recursive=True
        )
        reflFiles = glob.glob(
            self.tabsProcessingPath[tabsNum] + "/**/*.refl", recursive=True
        )
        for exptFile in exptFiles:
            fileTime = os.path.getmtime(exptFile)
            if latestExptTime == "":
                latestExpt = exptFile
                latestExptTime = fileTime
            else:
                if fileTime > latestExptTime:
                    latestExpt = exptFile
                    latestExptTime = fileTime
        for reflFile in reflFiles:
            fileTime = os.path.getmtime(reflFile)
            if latestReflTime == "":
                latestRefl = reflFile
                latestReflTime = fileTime
            else:
                if fileTime > latestReflTime:
                    latestRefl = reflFile
                    latestReflTime = fileTime
        if latestExpt == "":
            self.appendOutput(
                self.mainTab_txt,
                "\n\n *** Expt was not present in processing path, please wait unit after inital importing *** \n\n",
            )
            return
        if latestRefl == "":
            self.appendOutput(
                self.mainTab_txt,
                "\n\n ***Refl was not present in processing path, please wait unit after inital spot finding *** \n\n",
            )
            return
        else:
            try:
                self.appendOutput(
                    self.mainTab_txt, "\nReflection file: " + str(latestRefl)
                )
                self.appendOutput(
                    self.mainTab_txt, "Experiment file: " + str(latestExpt) + "\n"
                )
                subprocess.Popen(
                    [
                        "sh",
                        "/dls_sw/i19/scripts/MarkWarren/PyQT/1_basic/dialsReciprocalLatticeViewer.sh",
                        latestExpt,
                        latestRefl,
                    ]
                )
            except Exception:
                self.appendOutput(self.mainTab_txt, "Running dials image viewer failed")

    def runDialsImageViewer(self, tabsNum):
        self.appendOutput(self.mainTab_txt, "Opening dials image viewer")
        self.appendOutput(
            self.mainTab_txt, "Processing path:" + self.tabsProcessingPath[tabsNum]
        )

        latestExpt = ""
        latestExptTime = ""
        latestRefl = ""
        latestReflTime = ""

        exptFiles = glob.glob(
            self.tabsProcessingPath[tabsNum] + "/**/*.expt", recursive=True
        )
        reflFiles = glob.glob(
            self.tabsProcessingPath[tabsNum] + "/**/*.refl", recursive=True
        )
        for exptFile in exptFiles:
            fileTime = os.path.getmtime(exptFile)
            if latestExptTime == "":
                latestExpt = exptFile
                latestExptTime = fileTime
            else:
                if fileTime > latestExptTime:
                    latestExpt = exptFile
                    latestExptTime = fileTime
        for reflFile in reflFiles:
            fileTime = os.path.getmtime(reflFile)
            if latestReflTime == "":
                latestRefl = reflFile
                latestReflTime = fileTime
            else:
                if fileTime > latestReflTime:
                    latestRefl = reflFile
                    latestReflTime = fileTime
        if latestExpt == "":
            self.appendOutput(
                self.mainTab_txt,
                "\n\n ***Expt was not present in processing path, please wait unit after inital importing *** \n\n",
            )
        else:
            try:
                self.appendOutput(
                    self.mainTab_txt, "\nReflection file: " + str(latestRefl)
                )
                self.appendOutput(
                    self.mainTab_txt, "Experiment file: " + str(latestExpt) + "\n"
                )
                subprocess.Popen(
                    [
                        "sh",
                        "/dls_sw/i19/scripts/MarkWarren/PyQT/1_basic/dialsImageViewer.sh",
                        latestExpt,
                        latestRefl,
                    ]
                )
            except Exception:
                self.appendOutput(
                    self.mainTab_txt,
                    "\n\n ***Running dials image viewer failed *** \n\n",
                )

    def runDialsHTML(self, tabsNum):
        self.appendOutput(self.mainTab_txt, "Opening HTML")
        self.appendOutput(
            self.mainTab_txt, "Processing path:" + self.tabsProcessingPath[tabsNum]
        )

        latestHTML = ""
        latestHTMLTime = ""

        htmlFiles = glob.glob(
            self.tabsProcessingPath[tabsNum] + "/**/*.html", recursive=True
        )
        for htmlFile in htmlFiles:
            fileTime = os.path.getmtime(htmlFile)
            if latestHTMLTime == "":
                latestHTML = htmlFile
                latestHTMLTime = fileTime
            else:
                if fileTime > latestHTMLTime:
                    latestHTML = htmlFile
                    latestHTMLTime = fileTime

        if latestHTML == "":
            self.appendOutput(
                self.mainTab_txt,
                (
                    "\n\n *** html file was not present in processing path, please wait unit after inital importing *** \n\n"
                ),
            )
        else:
            self.appendOutput(self.mainTab_txt, "HTML file: " + str(latestHTML))
            try:
                subprocess.Popen(
                    [
                        "sh",
                        "/dls_sw/i19/scripts/MarkWarren/PyQT/1_basic/html.sh",
                        latestHTML,
                    ]
                )
            except Exception:
                self.appendOutput(self.mainTab_txt, "Running dials image viewer failed")

    ### version menu, change version
    def versionCurrent(self):
        self.appendOutput(self.mainTab_txt, "Changing to dials version to current.")
        dialVersionPop = (
            os.popen("module unload dials; module load dials; dials.version")
            .read()
            .split("-")[0]
            .split(" ")[1]
        )
        self.dialVersion = ""
        # updata version lable
        self.menuVersion.setTitle("Version(" + dialVersionPop + ")")
        self.appendOutput(self.mainTab_txt, "	Version(" + dialVersionPop + ")")

    ### version menu, change version to latest
    def versionLatest(self):
        self.appendOutput(self.mainTab_txt, "Changing to dials version to latest.")
        dialVersionPop = (
            os.popen("module unload dials; module load dials/latest; dials.version")
            .read()
            .split("-")[0]
            .split(" ")[1]
        )
        self.dialVersion = "/latest"
        # updata version lable
        self.menuVersion.setTitle("Version(" + dialVersionPop + ")")
        self.appendOutput(self.mainTab_txt, "	Version(" + dialVersionPop + ")")

    ### version menu, change version to now
    def VersionNow(self):
        self.appendOutput(self.mainTab_txt, "Changing to dials version to Now.")
        dialVersionPop = (
            os.popen("module unload dials; module load dials/now; dials.version")
            .read()
            .split("-")[0]
            .split(" ")[1]
        )
        self.dialVersion = "/now"
        # updata version lable
        self.menuVersion.setTitle("Version(" + dialVersionPop + ")")
        self.appendOutput(self.mainTab_txt, "	Version(" + dialVersionPop + ")")

    ### version menu, change version to 1.4
    def Version1_4(self):
        self.appendOutput(self.mainTab_txt, "Changing to dials version to 1.4.")
        dialVersionPop = (
            os.popen("module unload dials; module load dials/1.4; dials.version")
            .read()
            .split("-")[0]
            .split(" ")[1]
        )
        self.dialVersion = "/1.4"
        # updata version lable
        self.menuVersion.setTitle("Version(" + dialVersionPop + ")")
        self.appendOutput(self.mainTab_txt, "	Version(" + dialVersionPop + ")")

    ### version menu, change version to 2.1
    def Version2_1(self):
        self.appendOutput(self.mainTab_txt, "Changing to dials version to 2.1.")
        dialVersionPop = (
            os.popen("module unload dials; module load dials/2.1; dials.version")
            .read()
            .split("-")[0]
            .split(" ")[1]
        )
        self.dialVersion = "/2.1"
        # updata version lable
        self.menuVersion.setTitle("Version(" + dialVersionPop + ")")
        self.appendOutput(self.mainTab_txt, "	Version(" + dialVersionPop + ")")

    ### close tabs ######
    def close_handler(self, index):
        self.appendOutput(self.mainTab_txt, "close_handler called, index = %s" % index)
        self.xia2output.removeTab(index)

    ####################################################
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        # main window tile
        MainWindow.setWindowTitle(
            _translate("MainWindow", "Chemical Crystallography Xia2 GUI")
        )
        # File menu
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuFile_Open.setText(_translate("MainWindow", "Open"))
        self.menuFile_Open.setStatusTip(
            _translate("MainWindow", "Open the dataset - select dataset folder")
        )
        self.menuFile_Open.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.menuFile_Open_Multiple.setText(_translate("MainWindow", "Open Multiple"))
        self.menuFile_Open_Multiple.setStatusTip(
            _translate(
                "MainWindow",
                "Open multiple datasets - selected multiple datasets uning the Ctrl button",
            )
        )
        self.menuFile_Open_Multiple.setShortcut(_translate("MainWindow", "Ctrl+M"))
        self.menuFile_Close_GUI.setText(_translate("MainWindow", "Close GUI"))
        self.menuFile_Close_GUI.setStatusTip(
            _translate("MainWindow", "This will close the GUI")
        )
        self.menuFile_Close_GUI.setShortcut(_translate("MainWindow", "Ctrl+C"))
        # Edit menu
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuEdit_CopyCommand.setText(_translate("MainWindow", "Copy Command #"))
        self.menuEdit_SaveSettings.setText(_translate("MainWindow", "Save Settings #"))
        self.menuEdit_SaveSettings.setStatusTip(
            _translate("MainWindow", "Save all the GUI settings to a .txt file")
        )
        self.menuEdit_LoadSettings.setText(_translate("MainWindow", "Load Settings #"))
        self.menuEdit_LoadSettings.setStatusTip(
            _translate("MainWindow", "Load previous save GUI settings")
        )
        # View menu
        self.menuView.setTitle(_translate("MainWindow", "View"))
        # Settings menu
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        # Version menu
        dialVersionPop = os.popen("dials.version").read().split("-")[0].split(" ")[1]
        self.menuVersion.setTitle(
            _translate("MainWindow", "Version(" + dialVersionPop + ")")
        )
        self.menuVersion_current.setText(_translate("MainWindow", "dials_current"))
        self.menuVersion_latest.setText(_translate("MainWindow", "dials_latest"))
        self.menuVersion_now.setText(_translate("MainWindow", "dials_now"))
        self.menuVersion_1_4.setText(_translate("MainWindow", "dials_1.4 #"))
        self.menuVersion_2_1.setText(_translate("MainWindow", "dials_2.1 #"))
        # Dataset lables info
        self.labelsDataset.setText(_translate("MainWindow", "Dataset"))
        self.labelsPrefix.setText(_translate("MainWindow", "Prefix"))
        self.labelsImages.setText(_translate("MainWindow", "Run images"))
        self.datasetInfo_dataset.setText(_translate("MainWindow", "none"))
        self.datasetInfo_prefix.setText(_translate("MainWindow", "none"))
        self.datasetInfo_images.setText(_translate("MainWindow", "0"))
        # view buttons
        self.viewButtons_xia2.setText(_translate("MainWindow", "Run Xia2"))
        self.viewButtons_xia2.setStatusTip(
            _translate("MainWindow", "Run Xia2 with current dataset and options")
        )

        self.viewButtons_screen19.setText(_translate("MainWindow", "Run screen19"))
        self.viewButtons_screen19.setStatusTip(
            _translate("MainWindow", "Run screen with current dataset and options")
        )

        self.viewButtons_options.setText(_translate("MainWindow", "Xia2 Options"))
        self.viewButtons_options.setStatusTip(
            _translate(
                "MainWindow",
                "Opens a second window with all additional xia2 processing options",
            )
        )
        self.viewButtons_albula.setText(_translate("MainWindow", "Open Albula"))
        self.viewButtons_albula.setStatusTip(
            _translate(
                "MainWindow", "Open Albula which is image viewing program from Detris"
            )
        )
        # processing path
        self.processingPath__path.setText(_translate("MainWindow", "none"))
        self.processingPath_label.setText(_translate("MainWindow", "Processing Path"))
        # xia2 command
        self.command_label.setText(_translate("MainWindow", "xia2 Command"))
        self.command_command.setPlainText(
            _translate("MainWindow", "xia2 small_molecule=true dataset_path")
        )
        self.command_command.setStatusTip(
            _translate("MainWindow", "Current xia2 command (do not manually edit)")
        )

        # self.mainTab_txt.setText(_translate("MainWindow", "Main"))


###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################


class mythread2(QThread):
    # finished = pyqtSignal(object)
    finished = pyqtSignal()

    def __init__(self, processingPath, dataset, tabstxt, tabsNum, mainTab_txt, logFile):
        QThread.__init__(self)
        self.processingPath = processingPath
        self.tabstxt = tabstxt
        self.tabsNum = tabsNum
        self.dataset = dataset
        self.mainTab_txt = mainTab_txt
        self.logFile = logFile

    def __del__(self):
        self.wait()

    def run(self):
        tabName = self.tabstxt[self.tabsNum]
        mainTab_txt = self.mainTab_txt
        xia2txtlinesNumPrevious = 0
        isRunning = "Yes"
        sleep(3)
        while isRunning == "Yes":
            xia2txt = self.processingPath + self.logFile
            if os.path.isfile(xia2txt):
                xia2txtlines = [line.strip() for line in open(xia2txt)]
                newLines = xia2txtlines[xia2txtlinesNumPrevious:]
                if len(newLines) == 0:
                    pass
                else:
                    newLinesPrint = "\n".join(newLines)
                    xia2txtlinesNumPrevious = len(xia2txtlines)
                    try:
                        tabName.appendPlainText(newLinesPrint)
                        tabName.moveCursor(QtGui.QTextCursor.End)
                    except Exception:
                        mainTab_txt.appendPlainText("Unable to update new lines to txt")
                        mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                    if "Status: normal termination" in xia2txtlines:
                        outputMessage = "\n\nEnd of xia2 processing detected.\nStopping output to tab\n\n"
                        mainTab_txt.appendPlainText(outputMessage)
                        mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                        sleep(0.1)
                        tabName.appendPlainText(outputMessage)
                        tabName.moveCursor(QtGui.QTextCursor.End)
                    if "xia2.support@gmail.com" in xia2txtlines:
                        outputMessage = "\n\nEnd of xia2 processing detected.\nStopping output to tab\n\n"
                        mainTab_txt.appendPlainText(outputMessage)
                        mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                        sleep(0.1)
                        tabName.appendPlainText(outputMessage)
                        tabName.moveCursor(QtGui.QTextCursor.End)
            else:
                mainTab_txt.appendPlainText("xia2.txt file does not exist yet")
                mainTab_txt.moveCursor(QtGui.QTextCursor.End)
            sleep(5)
        mainTab_txt.appendPlainText("finishing")
        mainTab_txt.moveCursor(QtGui.QTextCursor.End)
        self.finished.emit()


###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################


def handle_results(result_queue):
    # while True:
    #    result = result_queue.get()
    #    Ui_MainWindow.appendOutput(self.mainTab_txt,"Got result {}".format(result))
    pass


###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################


class Ui_Xia2Options:
    def __init__(
        self,
        xia2command,
        datasetPath,
        command_command,
        visit,
        mainTab_txt,
        runList,
        prefix,
        openingVisit,
    ):
        self.xia2command = xia2command
        self.datasetPath = datasetPath
        self.runList = runList
        self.command_command = command_command
        self.refGeometryPath = ""
        self.visit = visit
        self.mainTab_txt = mainTab_txt
        global runImageSelector
        runImageSelector = False
        global runSelection
        runSelection = []
        global imageSelection
        imageSelection = {}
        self.prefix = prefix
        self.openingVisit = openingVisit

    def setupUi(self, Xia2Options):

        Xia2Options.setObjectName("Xia2Options")
        # Xia2Options.resize(613, 454)
        Xia2Options.resize(613, 600)
        self.centralwidget = QtWidgets.QWidget(Xia2Options)
        self.centralwidget.setObjectName("centralwidget")

        # update button
        self.updateButton = QtWidgets.QPushButton(self.centralwidget)
        self.updateButton.setGeometry(QtCore.QRect(10, 0, 131, 28))
        self.updateButton.setObjectName("updateButton")
        self.updateButton.clicked.connect(self.updateOptions)

        # reset button
        self.resetButton = QtWidgets.QPushButton(self.centralwidget)
        self.resetButton.setGeometry(QtCore.QRect(150, 0, 131, 28))
        self.resetButton.setObjectName("resetButton")
        self.resetButton.clicked.connect(self.resetOptions)

        # save button
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(290, 0, 131, 28))
        self.saveButton.setObjectName("saveButton")
        self.saveButton.clicked.connect(self.saveOptions)

        # load button
        self.loadButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadButton.setGeometry(QtCore.QRect(430, 0, 131, 28))
        self.loadButton.setObjectName("loadButton")
        self.loadButton.clicked.connect(self.loadOptions)

        self.xia2options = QtWidgets.QTabWidget(self.centralwidget)
        self.xia2options.setGeometry(QtCore.QRect(0, 30, 601, 520))
        self.xia2options.setObjectName("xia2options")

        ###############################################################################################
        # dials import

        self.xia2options_Import = QtWidgets.QWidget()
        self.xia2options_Import.setObjectName("xia2options_Import")
        self.xia2options.addTab(self.xia2options_Import, "")

        self.import_TrustBeamCentre = QtWidgets.QCheckBox(self.xia2options_Import)
        self.import_TrustBeamCentre.setGeometry(QtCore.QRect(10, 20, 141, 20))
        self.import_TrustBeamCentre.setObjectName("import_TrustBeamCentre")

        self.import_ReferenceGeometry = QtWidgets.QCheckBox(self.xia2options_Import)
        self.import_ReferenceGeometry.setGeometry(QtCore.QRect(10, 50, 161, 20))
        self.import_ReferenceGeometry.setObjectName("import_ReferenceGeometry")
        self.import_ReferenceGeometry_browse = QtWidgets.QPushButton(
            self.xia2options_Import
        )
        self.import_ReferenceGeometry_browse.setGeometry(QtCore.QRect(160, 45, 93, 28))
        self.import_ReferenceGeometry_browse.setObjectName(
            "import_ReferenceGeometry_browse"
        )
        self.import_ReferenceGeometry_browse.clicked.connect(
            self.browseForReferenceModel
        )
        self.import_ReferenceGeometry_path = QtWidgets.QLabel(self.xia2options_Import)
        self.import_ReferenceGeometry_path.setGeometry(QtCore.QRect(260, 50, 271, 16))
        self.import_ReferenceGeometry_path.setObjectName(
            "import_ReferenceGeometry_path"
        )

        self.import_DD = QtWidgets.QCheckBox(self.xia2options_Import)
        self.import_DD.setGeometry(QtCore.QRect(10, 80, 161, 21))
        self.import_DD.setObjectName("import_DD")
        self.import_DD_lineEdit = QtWidgets.QLineEdit(self.xia2options_Import)
        self.import_DD_lineEdit.setGeometry(QtCore.QRect(160, 80, 100, 22))
        self.import_DD_lineEdit.setObjectName("import_DD_lineEdit")
        self.import_DD_lineEdit.setStatusTip("e.g. 85.19")

        self.import_BeamCentre = QtWidgets.QCheckBox(self.xia2options_Import)
        self.import_BeamCentre.setGeometry(QtCore.QRect(10, 110, 161, 21))
        self.import_BeamCentre.setObjectName("import_BeamCentre")
        self.import_BeamCentre_X_label = QtWidgets.QLabel(self.xia2options_Import)
        self.import_BeamCentre_X_label.setGeometry(QtCore.QRect(180, 110, 16, 16))
        self.import_BeamCentre_X_label.setObjectName("import_BeamCentre_X_label")
        self.import_BeamCentre_X_lineEdit = QtWidgets.QLineEdit(self.xia2options_Import)
        self.import_BeamCentre_X_lineEdit.setGeometry(QtCore.QRect(200, 110, 61, 22))
        self.import_BeamCentre_X_lineEdit.setObjectName("import_BeamCentre_X_lineEdit")
        self.import_BeamCentre_X_lineEdit.setStatusTip("e.g. 54.3")
        self.import_BeamCentre_Y_label = QtWidgets.QLabel(self.xia2options_Import)
        self.import_BeamCentre_Y_label.setGeometry(QtCore.QRect(270, 110, 16, 16))
        self.import_BeamCentre_Y_label.setObjectName("import_BeamCentre_Y_label")
        self.import_BeamCentre_Y_lineEdit = QtWidgets.QLineEdit(self.xia2options_Import)
        self.import_BeamCentre_Y_lineEdit.setGeometry(QtCore.QRect(290, 110, 61, 22))
        self.import_BeamCentre_Y_lineEdit.setObjectName("import_BeamCentre_Y_lineEdit")
        self.import_BeamCentre_Y_lineEdit.setStatusTip("e.g. 43.3")

        self.import_Wavelengh = QtWidgets.QCheckBox(self.xia2options_Import)
        self.import_Wavelengh.setGeometry(QtCore.QRect(10, 140, 161, 21))
        self.import_Wavelengh.setObjectName("import_Wavelengh")
        self.import_wavelength_lineEdit = QtWidgets.QLineEdit(self.xia2options_Import)
        self.import_wavelength_lineEdit.setGeometry(QtCore.QRect(160, 140, 101, 22))
        self.import_wavelength_lineEdit.setObjectName("import_wavelength_lineEdit")
        self.import_wavelength_lineEdit.setStatusTip("e.g. 0.6889")

        self.Import_FixBeamDetector_checkBox = QtWidgets.QCheckBox(
            self.xia2options_Import
        )
        self.Import_FixBeamDetector_checkBox.setGeometry(QtCore.QRect(10, 170, 151, 20))
        self.Import_FixBeamDetector_checkBox.setObjectName(
            "Import_FixBeamDetector_checkBox"
        )

        self.Import_RunSelector_checkBox = QtWidgets.QCheckBox(self.xia2options_Import)
        self.Import_RunSelector_checkBox.setGeometry(QtCore.QRect(10, 200, 91, 20))
        self.Import_RunSelector_checkBox.setObjectName("Import_RunSelector_checkBox")
        self.Import_RunSelector_checkBox_1 = QtWidgets.QCheckBox(
            self.xia2options_Import
        )
        self.Import_RunSelector_checkBox_1.setGeometry(QtCore.QRect(110, 200, 31, 20))
        self.Import_RunSelector_checkBox_1.setObjectName(
            "Import_RunSelector_checkBox_1"
        )
        self.Import_RunSelector_checkBox_2 = QtWidgets.QCheckBox(
            self.xia2options_Import
        )
        self.Import_RunSelector_checkBox_2.setGeometry(QtCore.QRect(150, 200, 31, 20))
        self.Import_RunSelector_checkBox_2.setObjectName(
            "Import_RunSelector_checkBox_2"
        )
        self.Import_RunSelector_checkBox_3 = QtWidgets.QCheckBox(
            self.xia2options_Import
        )
        self.Import_RunSelector_checkBox_3.setGeometry(QtCore.QRect(190, 200, 31, 20))
        self.Import_RunSelector_checkBox_3.setObjectName(
            "Import_RunSelector_checkBox_3"
        )
        self.Import_RunSelector_checkBox_4 = QtWidgets.QCheckBox(
            self.xia2options_Import
        )
        self.Import_RunSelector_checkBox_4.setGeometry(QtCore.QRect(230, 200, 31, 20))
        self.Import_RunSelector_checkBox_4.setObjectName(
            "Import_RunSelector_checkBox_4"
        )
        self.Import_RunSelector_checkBox_5 = QtWidgets.QCheckBox(
            self.xia2options_Import
        )
        self.Import_RunSelector_checkBox_5.setGeometry(QtCore.QRect(270, 200, 31, 20))
        self.Import_RunSelector_checkBox_5.setObjectName(
            "Import_RunSelector_checkBox_5"
        )
        self.Import_RunSelector_checkBox_6 = QtWidgets.QCheckBox(
            self.xia2options_Import
        )
        self.Import_RunSelector_checkBox_6.setGeometry(QtCore.QRect(310, 200, 31, 20))
        self.Import_RunSelector_checkBox_6.setObjectName(
            "Import_RunSelector_checkBox_6"
        )
        self.Import_RunSelector_checkBox_7 = QtWidgets.QCheckBox(
            self.xia2options_Import
        )
        self.Import_RunSelector_checkBox_7.setGeometry(QtCore.QRect(350, 200, 31, 20))
        self.Import_RunSelector_checkBox_7.setObjectName(
            "Import_RunSelector_checkBox_7"
        )
        self.Import_RunSelector_checkBox_8 = QtWidgets.QCheckBox(
            self.xia2options_Import
        )
        self.Import_RunSelector_checkBox_8.setGeometry(QtCore.QRect(390, 200, 31, 20))
        self.Import_RunSelector_checkBox_8.setObjectName(
            "Import_RunSelector_checkBox_8"
        )
        self.Import_RunSelector_checkBox_9 = QtWidgets.QCheckBox(
            self.xia2options_Import
        )
        self.Import_RunSelector_checkBox_9.setGeometry(QtCore.QRect(430, 200, 31, 20))
        self.Import_RunSelector_checkBox_9.setObjectName(
            "Import_RunSelector_checkBox_9"
        )
        self.Import_RunSelector_checkBox_10 = QtWidgets.QCheckBox(
            self.xia2options_Import
        )
        self.Import_RunSelector_checkBox_10.setGeometry(QtCore.QRect(470, 200, 41, 20))
        self.Import_RunSelector_checkBox_10.setObjectName(
            "Import_RunSelector_checkBox_10"
        )
        self.Import_RunSelector_checkBox_11 = QtWidgets.QCheckBox(
            self.xia2options_Import
        )
        self.Import_RunSelector_checkBox_11.setGeometry(QtCore.QRect(510, 200, 41, 20))
        self.Import_RunSelector_checkBox_11.setObjectName(
            "Import_RunSelector_checkBox_11"
        )
        self.Import_RunSelector_checkBox_12 = QtWidgets.QCheckBox(
            self.xia2options_Import
        )
        self.Import_RunSelector_checkBox_12.setGeometry(QtCore.QRect(550, 200, 41, 20))
        self.Import_RunSelector_checkBox_12.setObjectName(
            "Import_RunSelector_checkBox_12"
        )

        self.Import_type_checkBox = QtWidgets.QCheckBox(self.xia2options_Import)
        self.Import_type_checkBox.setGeometry(QtCore.QRect(10, 230, 121, 20))
        self.Import_type_checkBox.setObjectName("Import_type_checkBox")
        self.Import_type_checkBox.setChecked(True)
        self.Import_type_comboBox = QtWidgets.QComboBox(self.xia2options_Import)
        self.Import_type_comboBox.setGeometry(QtCore.QRect(130, 230, 171, 22))
        self.Import_type_comboBox.setObjectName("Import_type_comboBox")
        self.Import_type_comboBox.addItem("")
        self.Import_type_comboBox.addItem("")

        ###############################################################################################
        # spotFinding
        self.xia2options_SpotFinding = QtWidgets.QWidget()
        self.xia2options_SpotFinding.setObjectName("xia2options_SpotFinding")
        self.xia2options.addTab(self.xia2options_SpotFinding, "")

        self.findSpots_sigmaStrong = QtWidgets.QCheckBox(self.xia2options_SpotFinding)
        self.findSpots_sigmaStrong.setGeometry(QtCore.QRect(10, 10, 111, 20))
        self.findSpots_sigmaStrong.setObjectName("findSpots_sigmaStrong")
        self.findSpots_sigmaStrong_lineEdit = QtWidgets.QLineEdit(
            self.xia2options_SpotFinding
        )
        self.findSpots_sigmaStrong_lineEdit.setGeometry(QtCore.QRect(130, 10, 113, 22))
        self.findSpots_sigmaStrong_lineEdit.setObjectName(
            "findSpots_sigmaStrong_lineEdit"
        )
        self.findSpots_sigmaStrong_lineEdit.setStatusTip("e.g. 6 (default=3)")

        self.findSpots_minSpot = QtWidgets.QCheckBox(self.xia2options_SpotFinding)
        self.findSpots_minSpot.setGeometry(QtCore.QRect(10, 40, 111, 20))
        self.findSpots_minSpot.setObjectName("findSpots_minSpot")
        self.findSpots_minSpot_lineEdit = QtWidgets.QLineEdit(
            self.xia2options_SpotFinding
        )
        self.findSpots_minSpot_lineEdit.setGeometry(QtCore.QRect(130, 40, 113, 22))
        self.findSpots_minSpot_lineEdit.setObjectName("findSpots_minSpot_lineEdit")
        self.findSpots_minSpot_lineEdit.setStatusTip("e.g. 2")

        self.findSpots_maxSpot = QtWidgets.QCheckBox(self.xia2options_SpotFinding)
        self.findSpots_maxSpot.setGeometry(QtCore.QRect(10, 70, 111, 20))
        self.findSpots_maxSpot.setObjectName("findSpots_maxSpot")
        self.findSpots_maxSpot_lineEdit = QtWidgets.QLineEdit(
            self.xia2options_SpotFinding
        )
        self.findSpots_maxSpot_lineEdit.setGeometry(QtCore.QRect(130, 70, 113, 22))
        self.findSpots_maxSpot_lineEdit.setObjectName("findSpots_maxSpot_lineEdit")
        self.findSpots_maxSpot_lineEdit.setStatusTip("e.g. 20 (default=1000)")

        self.findSpots_dmin = QtWidgets.QCheckBox(self.xia2options_SpotFinding)
        self.findSpots_dmin.setGeometry(QtCore.QRect(10, 100, 111, 20))
        self.findSpots_dmin.setObjectName("findSpots_dmin")
        self.findSpots_dmin_lineEdit = QtWidgets.QLineEdit(self.xia2options_SpotFinding)
        self.findSpots_dmin_lineEdit.setGeometry(QtCore.QRect(130, 100, 113, 22))
        self.findSpots_dmin_lineEdit.setObjectName("findSpots_dmin_lineEdit")
        self.findSpots_dmin_lineEdit.setStatusTip("e.g. 0.84")

        self.findSpots_dmax = QtWidgets.QCheckBox(self.xia2options_SpotFinding)
        self.findSpots_dmax.setGeometry(QtCore.QRect(10, 130, 111, 20))
        self.findSpots_dmax.setObjectName("findSpots_dmax")
        self.findSpots_dmax_lineEdit = QtWidgets.QLineEdit(self.xia2options_SpotFinding)
        self.findSpots_dmax_lineEdit.setGeometry(QtCore.QRect(130, 130, 113, 22))
        self.findSpots_dmax_lineEdit.setObjectName("findSpots_dmax_lineEdit")
        self.findSpots_dmax_lineEdit.setStatusTip("e.g. 15")

        self.findSpots_iceRings = QtWidgets.QCheckBox(self.xia2options_SpotFinding)
        self.findSpots_iceRings.setGeometry(QtCore.QRect(10, 160, 111, 20))
        self.findSpots_iceRings.setObjectName("findSpots_iceRings")

        self.findSpots_powderRings = QtWidgets.QCheckBox(self.xia2options_SpotFinding)
        self.findSpots_powderRings.setGeometry(QtCore.QRect(10, 190, 111, 20))
        self.findSpots_powderRings.setObjectName("findSpots_powderRings")
        self.findSpots_powderRingsUC_lineEdit = QtWidgets.QLineEdit(
            self.xia2options_SpotFinding
        )
        self.findSpots_powderRingsUC_lineEdit.setGeometry(
            QtCore.QRect(130, 190, 241, 22)
        )
        self.findSpots_powderRingsUC_lineEdit.setObjectName(
            "findSpots_powderRingsUC_lineEdit"
        )
        self.findSpots_powderRingsUC_lineEdit.setStatusTip(
            "e.g. 5.6,5.7,12.4,90,105.2,90"
        )
        self.findSpots_powderRingsUC_label = QtWidgets.QLabel(
            self.xia2options_SpotFinding
        )
        self.findSpots_powderRingsUC_label.setGeometry(QtCore.QRect(200, 170, 55, 16))
        self.findSpots_powderRingsUC_label.setObjectName(
            "findSpots_powderRingsUC_label"
        )
        self.findSpots_powderRingsSG_lineEdit = QtWidgets.QLineEdit(
            self.xia2options_SpotFinding
        )
        self.findSpots_powderRingsSG_lineEdit.setGeometry(
            QtCore.QRect(380, 190, 71, 22)
        )
        self.findSpots_powderRingsSG_lineEdit.setObjectName(
            "findSpots_powderRingsSG_lineEdit"
        )
        self.findSpots_powderRingsSG_lineEdit.setStatusTip("e.g. P21/c")
        self.findSpots_powderRingsSG_label = QtWidgets.QLabel(
            self.xia2options_SpotFinding
        )
        self.findSpots_powderRingsSG_label.setGeometry(QtCore.QRect(380, 170, 81, 16))
        self.findSpots_powderRingsSG_label.setObjectName(
            "findSpots_powderRingsSG_label"
        )
        self.findSpots_powderRingsW_lineEdit = QtWidgets.QLineEdit(
            self.xia2options_SpotFinding
        )
        self.findSpots_powderRingsW_lineEdit.setGeometry(QtCore.QRect(460, 190, 71, 22))
        self.findSpots_powderRingsW_lineEdit.setObjectName(
            "findSpots_powderRingsW_lineEdit"
        )
        self.findSpots_powderRingsW_lineEdit.setStatusTip("e.g. 0.04 (default=0.002)")
        self.findSpots_powderRingsW_label = QtWidgets.QLabel(
            self.xia2options_SpotFinding
        )
        self.findSpots_powderRingsW_label.setGeometry(QtCore.QRect(480, 170, 41, 16))
        self.findSpots_powderRingsW_label.setObjectName("findSpots_powderRingsW_label")

        self.findSpots_resolutionRange = QtWidgets.QCheckBox(
            self.xia2options_SpotFinding
        )
        self.findSpots_resolutionRange.setGeometry(QtCore.QRect(10, 220, 121, 20))
        self.findSpots_resolutionRange.setObjectName("findSpots_resolutionRange")
        self.findSpots_resolutionRange_lineEdit_1 = QtWidgets.QLineEdit(
            self.xia2options_SpotFinding
        )
        self.findSpots_resolutionRange_lineEdit_1.setGeometry(
            QtCore.QRect(130, 220, 71, 22)
        )
        self.findSpots_resolutionRange_lineEdit_1.setObjectName(
            "findSpots_resolutionRange_lineEdit_1"
        )
        self.findSpots_resolutionRange_lineEdit_1.setStatusTip("e.g. 1.02,0.98")
        self.findSpots_resolutionRange_lineEdit_2 = QtWidgets.QLineEdit(
            self.xia2options_SpotFinding
        )
        self.findSpots_resolutionRange_lineEdit_2.setGeometry(
            QtCore.QRect(210, 220, 71, 22)
        )
        self.findSpots_resolutionRange_lineEdit_2.setObjectName(
            "findSpots_resolutionRange_lineEdit_2"
        )
        self.findSpots_resolutionRange_lineEdit_3 = QtWidgets.QLineEdit(
            self.xia2options_SpotFinding
        )
        self.findSpots_resolutionRange_lineEdit_3.setGeometry(
            QtCore.QRect(290, 220, 71, 22)
        )
        self.findSpots_resolutionRange_lineEdit_3.setObjectName(
            "findSpots_resolutionRange_lineEdit_3"
        )
        self.findSpots_resolutionRange_lineEdit_4 = QtWidgets.QLineEdit(
            self.xia2options_SpotFinding
        )
        self.findSpots_resolutionRange_lineEdit_4.setGeometry(
            QtCore.QRect(370, 220, 71, 22)
        )
        self.findSpots_resolutionRange_lineEdit_4.setObjectName(
            "findSpots_resolutionRange_lineEdit_4"
        )
        self.findSpots_resolutionRange_lineEdit_5 = QtWidgets.QLineEdit(
            self.xia2options_SpotFinding
        )
        self.findSpots_resolutionRange_lineEdit_5.setGeometry(
            QtCore.QRect(450, 220, 71, 22)
        )
        self.findSpots_resolutionRange_lineEdit_5.setObjectName(
            "findSpots_resolutionRange_lineEdit_5"
        )
        self.findSpots_resolutionRange_lineEdit_6 = QtWidgets.QLineEdit(
            self.xia2options_SpotFinding
        )
        self.findSpots_resolutionRange_lineEdit_6.setGeometry(
            QtCore.QRect(130, 250, 71, 22)
        )
        self.findSpots_resolutionRange_lineEdit_6.setObjectName(
            "findSpots_resolutionRange_lineEdit_6"
        )
        self.findSpots_resolutionRange_lineEdit_7 = QtWidgets.QLineEdit(
            self.xia2options_SpotFinding
        )
        self.findSpots_resolutionRange_lineEdit_7.setGeometry(
            QtCore.QRect(210, 250, 71, 22)
        )
        self.findSpots_resolutionRange_lineEdit_7.setObjectName(
            "findSpots_resolutionRange_lineEdit_7"
        )
        self.findSpots_resolutionRange_lineEdit_8 = QtWidgets.QLineEdit(
            self.xia2options_SpotFinding
        )
        self.findSpots_resolutionRange_lineEdit_8.setGeometry(
            QtCore.QRect(290, 250, 71, 22)
        )
        self.findSpots_resolutionRange_lineEdit_8.setObjectName(
            "findSpots_resolutionRange_lineEdit_8"
        )
        self.findSpots_resolutionRange_lineEdit_9 = QtWidgets.QLineEdit(
            self.xia2options_SpotFinding
        )
        self.findSpots_resolutionRange_lineEdit_9.setGeometry(
            QtCore.QRect(370, 250, 71, 22)
        )
        self.findSpots_resolutionRange_lineEdit_9.setObjectName(
            "findSpots_resolutionRange_lineEdit_9"
        )
        self.findSpots_resolutionRange_lineEdit_10 = QtWidgets.QLineEdit(
            self.xia2options_SpotFinding
        )
        self.findSpots_resolutionRange_lineEdit_10.setGeometry(
            QtCore.QRect(450, 250, 71, 22)
        )
        self.findSpots_resolutionRange_lineEdit_10.setObjectName(
            "findSpots_resolutionRange_lineEdit_10"
        )

        self.findSpots_circleMask = QtWidgets.QCheckBox(self.xia2options_SpotFinding)
        self.findSpots_circleMask.setGeometry(QtCore.QRect(10, 280, 111, 20))
        self.findSpots_circleMask.setObjectName("findSpots_circleMask")
        self.findSpots_circleMask_lineEdit = QtWidgets.QLineEdit(
            self.xia2options_SpotFinding
        )
        self.findSpots_circleMask_lineEdit.setGeometry(QtCore.QRect(130, 280, 113, 22))
        self.findSpots_circleMask_lineEdit.setObjectName(
            "findSpots_circleMask_lineEdit"
        )
        self.findSpots_circleMask_lineEdit.setStatusTip("e.g. 620,851,27 (xc,yc,r)")

        self.findSpots_recMask = QtWidgets.QCheckBox(self.xia2options_SpotFinding)
        self.findSpots_recMask.setGeometry(QtCore.QRect(10, 310, 121, 20))
        self.findSpots_recMask.setObjectName("findSpots_recMask")
        self.findSpots_recMask_lineEdit = QtWidgets.QLineEdit(
            self.xia2options_SpotFinding
        )
        self.findSpots_recMask_lineEdit.setGeometry(QtCore.QRect(130, 310, 113, 22))
        self.findSpots_recMask_lineEdit.setObjectName("findSpots_recMask_lineEdit")
        self.findSpots_recMask_lineEdit.setStatusTip(
            "e.g. 0,612,824,858 (x0, x1, y0, y1)"
        )

        ###############################################################################################
        # indexing
        self.xia2options_Indexing = QtWidgets.QWidget()
        self.xia2options_Indexing.setObjectName("xia2options_Indexing")
        self.xia2options.addTab(self.xia2options_Indexing, "")

        self.Index_method_comboBox = QtWidgets.QComboBox(self.xia2options_Indexing)
        self.Index_method_comboBox.setGeometry(QtCore.QRect(130, 10, 171, 22))
        self.Index_method_comboBox.setObjectName("Index_method_comboBox")
        self.Index_method_comboBox.addItem("")
        self.Index_method_comboBox.addItem("")
        self.Index_method_comboBox.addItem("")
        self.Index_method_comboBox.addItem("")
        self.Index_method_checkBox = QtWidgets.QCheckBox(self.xia2options_Indexing)
        self.Index_method_checkBox.setGeometry(QtCore.QRect(10, 10, 121, 20))
        self.Index_method_checkBox.setObjectName("Index_method_checkBox")
        self.Index_scanVarying_checkBox = QtWidgets.QCheckBox(self.xia2options_Indexing)
        self.Index_scanVarying_checkBox.setGeometry(QtCore.QRect(10, 40, 121, 20))
        self.Index_scanVarying_checkBox.setObjectName("Index_scanVarying_checkBox")
        self.Index_UN_SG_checkBox = QtWidgets.QCheckBox(self.xia2options_Indexing)
        self.Index_UN_SG_checkBox.setGeometry(QtCore.QRect(10, 70, 181, 20))
        self.Index_UN_SG_checkBox.setObjectName("Index_UN_SG_checkBox")
        self.Index_UN_lineEdit = QtWidgets.QLineEdit(self.xia2options_Indexing)
        self.Index_UN_lineEdit.setGeometry(QtCore.QRect(190, 70, 211, 22))
        self.Index_UN_lineEdit.setObjectName("Index_UN_lineEdit")
        self.Index_UN_lineEdit.setStatusTip("e.g. 5.1,6.2,7.3,90,95.1,90")
        self.Index_UN_label = QtWidgets.QLabel(self.xia2options_Indexing)
        self.Index_UN_label.setGeometry(QtCore.QRect(260, 50, 51, 20))
        self.Index_UN_label.setObjectName("Index_UN_label")

        self.Index_SG_lineEdit = QtWidgets.QLineEdit(self.xia2options_Indexing)
        self.Index_SG_lineEdit.setGeometry(QtCore.QRect(410, 70, 91, 22))
        self.Index_SG_lineEdit.setObjectName("Index_SG_lineEdit")
        self.Index_SG_lineEdit.setStatusTip("e.g. P21/c")
        # Index_SG_lineEdit
        self.Index_SG_label = QtWidgets.QLabel(self.xia2options_Indexing)
        self.Index_SG_label.setGeometry(QtCore.QRect(420, 50, 81, 20))
        self.Index_SG_label.setObjectName("Index_SG_label")
        self.Index_minCell_checkBox = QtWidgets.QCheckBox(self.xia2options_Indexing)
        self.Index_minCell_checkBox.setGeometry(QtCore.QRect(10, 100, 151, 20))
        self.Index_minCell_checkBox.setObjectName("Index_minCell_checkBox")
        self.Index_maxCell_checkBox = QtWidgets.QCheckBox(self.xia2options_Indexing)
        self.Index_maxCell_checkBox.setGeometry(QtCore.QRect(10, 130, 151, 20))
        self.Index_maxCell_checkBox.setObjectName("Index_maxCell_checkBox")

        self.Index_minCell_lineEdit = QtWidgets.QLineEdit(self.xia2options_Indexing)
        self.Index_minCell_lineEdit.setGeometry(QtCore.QRect(170, 100, 91, 22))
        self.Index_minCell_lineEdit.setObjectName("Index_minCell_lineEdit")
        self.Index_minCell_lineEdit.setStatusTip("e.g. 6.0 (default=3)")
        # Index_maxCell_lineEdit
        self.Index_maxCell_lineEdit = QtWidgets.QLineEdit(self.xia2options_Indexing)
        self.Index_maxCell_lineEdit.setGeometry(QtCore.QRect(170, 130, 91, 22))
        self.Index_maxCell_lineEdit.setObjectName("Index_maxCell_lineEdit")
        self.Index_maxCell_lineEdit.setStatusTip("e.g. 30.0")
        self.Index_multiprocessing_checkBox = QtWidgets.QCheckBox(
            self.xia2options_Indexing
        )
        self.Index_multiprocessing_checkBox.setGeometry(QtCore.QRect(10, 160, 261, 20))
        self.Index_multiprocessing_checkBox.setObjectName(
            "Index_multiprocessing_checkBox"
        )
        self.Index_multiSweepRefine_checkBox = QtWidgets.QCheckBox(
            self.xia2options_Indexing
        )
        self.Index_multiSweepRefine_checkBox.setGeometry(QtCore.QRect(10, 190, 261, 20))
        self.Index_multiSweepRefine_checkBox.setObjectName(
            "Index_multiSweepRefine_checkBox"
        )
        self.Index_outliers_checkBox = QtWidgets.QCheckBox(self.xia2options_Indexing)
        self.Index_outliers_checkBox.setGeometry(QtCore.QRect(10, 220, 261, 20))
        self.Index_outliers_checkBox.setObjectName("Index_outliers_checkBox")

        ###############################################################################################
        # dials integrate
        self.xia2options_integrate = QtWidgets.QWidget()
        self.xia2options_integrate.setObjectName("xia2options_integrate")
        self.xia2options.addTab(self.xia2options_integrate, "")

        self.Integrate_keepAllReflections_checkBox = QtWidgets.QCheckBox(
            self.xia2options_integrate
        )
        self.Integrate_keepAllReflections_checkBox.setGeometry(
            QtCore.QRect(10, 10, 141, 20)
        )
        self.Integrate_keepAllReflections_checkBox.setObjectName(
            "Integrate_keepAllReflections_checkBox"
        )
        self.Integrate_scanVarying_checkBox = QtWidgets.QCheckBox(
            self.xia2options_integrate
        )
        self.Integrate_scanVarying_checkBox.setGeometry(QtCore.QRect(10, 40, 141, 20))
        self.Integrate_scanVarying_checkBox.setObjectName(
            "Integrate_scanVarying_checkBox"
        )
        self.Integrate_minSpotProfile_checkBox = QtWidgets.QCheckBox(
            self.xia2options_integrate
        )
        self.Integrate_minSpotProfile_checkBox.setGeometry(
            QtCore.QRect(10, 70, 141, 20)
        )
        self.Integrate_minSpotProfile_checkBox.setObjectName(
            "Integrate_minSpotProfile_checkBox"
        )
        self.Integrate_minCellOverall_lineEdit = QtWidgets.QLineEdit(
            self.xia2options_integrate
        )
        self.Integrate_minCellOverall_lineEdit.setGeometry(
            QtCore.QRect(150, 70, 91, 22)
        )
        self.Integrate_minCellOverall_lineEdit.setObjectName(
            "Integrate_minCellOverall_lineEdit"
        )
        self.Integrate_minCellDegree_lineEdit = QtWidgets.QLineEdit(
            self.xia2options_integrate
        )
        self.Integrate_minCellDegree_lineEdit.setGeometry(QtCore.QRect(250, 70, 91, 22))
        self.Integrate_minCellDegree_lineEdit.setObjectName(
            "Integrate_minCellDegree_lineEdit"
        )
        self.Integrate_minCellOverall_label = QtWidgets.QLabel(
            self.xia2options_integrate
        )
        self.Integrate_minCellOverall_label.setGeometry(QtCore.QRect(170, 50, 51, 20))
        self.Integrate_minCellOverall_label.setObjectName(
            "Integrate_minCellOverall_label"
        )
        self.Integrate_minCellDegree_label = QtWidgets.QLabel(
            self.xia2options_integrate
        )
        self.Integrate_minCellDegree_label.setGeometry(QtCore.QRect(260, 50, 81, 20))
        self.Integrate_minCellDegree_label.setObjectName(
            "Integrate_minCellDegree_label"
        )

        ###############################################################################################
        # dials refine
        self.xia2options_refine_scale = QtWidgets.QWidget()
        self.xia2options_refine_scale.setObjectName("xia2options_refine_scale")
        self.xia2options.addTab(self.xia2options_refine_scale, "")

        self.Refine_method_checkBox = QtWidgets.QCheckBox(self.xia2options_refine_scale)
        self.Refine_method_checkBox.setGeometry(QtCore.QRect(10, 40, 121, 20))
        self.Refine_method_checkBox.setObjectName("Refine_method_checkBox")
        self.Refine_method_comboBox = QtWidgets.QComboBox(self.xia2options_refine_scale)
        self.Refine_method_comboBox.setGeometry(QtCore.QRect(130, 40, 171, 22))
        self.Refine_method_comboBox.setObjectName("Refine_method_comboBox")
        self.Refine_method_comboBox.addItem("")
        self.Refine_method_comboBox.addItem("")
        self.Refine_FixBeamDetector_checkBox = QtWidgets.QCheckBox(
            self.xia2options_refine_scale
        )
        self.Refine_FixBeamDetector_checkBox.setGeometry(QtCore.QRect(10, 10, 151, 20))
        self.Refine_FixBeamDetector_checkBox.setObjectName(
            "Refine_FixBeamDetector_checkBox"
        )

        ###############################################################################################
        # dials other
        self.xia2options_Other = QtWidgets.QWidget()
        self.xia2options_Other.setObjectName("xia2options_Other")
        self.xia2options.addTab(self.xia2options_Other, "")

        self.Other_failover_checkBox = QtWidgets.QCheckBox(self.xia2options_Other)
        self.Other_failover_checkBox.setGeometry(QtCore.QRect(10, 10, 151, 20))
        self.Other_failover_checkBox.setObjectName("Other_failover_checkBox")

        self.Other_manualInput1_checkBox = QtWidgets.QCheckBox(self.xia2options_Other)
        self.Other_manualInput1_checkBox.setGeometry(QtCore.QRect(10, 40, 111, 20))
        self.Other_manualInput1_checkBox.setObjectName("Other_manualInput1_checkBox")
        self.Other_manualInput1_lineEdit = QtWidgets.QLineEdit(self.xia2options_Other)
        self.Other_manualInput1_lineEdit.setGeometry(QtCore.QRect(130, 40, 400, 22))
        self.Other_manualInput1_lineEdit.setObjectName("Other_manualInput1_lineEdit")
        self.Other_manualInput2_checkBox = QtWidgets.QCheckBox(self.xia2options_Other)
        self.Other_manualInput2_checkBox.setGeometry(QtCore.QRect(10, 70, 111, 20))
        self.Other_manualInput2_checkBox.setObjectName("Other_manualInput2_checkBox")
        self.Other_manualInput2_lineEdit = QtWidgets.QLineEdit(self.xia2options_Other)
        self.Other_manualInput2_lineEdit.setGeometry(QtCore.QRect(130, 70, 400, 22))
        self.Other_manualInput2_lineEdit.setObjectName("Other_manualInput2_lineEdit")
        self.Other_manualInput3_checkBox = QtWidgets.QCheckBox(self.xia2options_Other)
        self.Other_manualInput3_checkBox.setGeometry(QtCore.QRect(10, 100, 111, 20))
        self.Other_manualInput3_checkBox.setObjectName("Other_manualInput3_checkBox")
        self.Other_manualInput3_lineEdit = QtWidgets.QLineEdit(self.xia2options_Other)
        self.Other_manualInput3_lineEdit.setGeometry(QtCore.QRect(130, 100, 400, 22))
        self.Other_manualInput3_lineEdit.setObjectName("Other_manualInput3_lineEdit")
        self.Other_manualInput4_checkBox = QtWidgets.QCheckBox(self.xia2options_Other)
        self.Other_manualInput4_checkBox.setGeometry(QtCore.QRect(10, 130, 111, 20))
        self.Other_manualInput4_checkBox.setObjectName("Other_manualInput4_checkBox")
        self.Other_manualInput4_lineEdit = QtWidgets.QLineEdit(self.xia2options_Other)
        self.Other_manualInput4_lineEdit.setGeometry(QtCore.QRect(130, 130, 400, 22))
        self.Other_manualInput4_lineEdit.setObjectName("Other_manualInput4_lineEdit")

        self.Other_clusterOrLocal_label = QtWidgets.QLabel(self.xia2options_Other)
        self.Other_clusterOrLocal_label.setGeometry(QtCore.QRect(10, 160, 200, 16))
        self.Other_clusterOrLocal_label.setObjectName("Other_clusterOrLocal_label")

        self.Other_clusterOrLocal_comboBox = QtWidgets.QComboBox(self.xia2options_Other)
        self.Other_clusterOrLocal_comboBox.setGeometry(QtCore.QRect(160, 160, 171, 22))
        self.Other_clusterOrLocal_comboBox.setObjectName(
            "Other_clusterOrLocal_comboBox"
        )
        self.Other_clusterOrLocal_comboBox.addItem("")
        self.Other_clusterOrLocal_comboBox.addItem("")

        ###############################################################################################
        # dials ALL
        self.xia2options_ALL = QtWidgets.QWidget()
        self.xia2options_ALL.setObjectName("xia2options_ALL")
        self.xia2options.addTab(self.xia2options_ALL, "")

        self.ALL_plainTextEdit = QtWidgets.QPlainTextEdit(self.xia2options_ALL)
        self.ALL_plainTextEdit.setGeometry(QtCore.QRect(150, 10, 291, 121))
        self.ALL_plainTextEdit.setObjectName("ALL_plainTextEdit")

        ###############################################################################################
        # dials HP
        self.xia2options_HP = QtWidgets.QWidget()
        self.xia2options_HP.setObjectName("xia2options_HP")
        self.xia2options.addTab(self.xia2options_HP, "")

        self.HP_correction_shaddowing_checkBox = QtWidgets.QCheckBox(
            self.xia2options_HP
        )
        self.HP_correction_shaddowing_checkBox.setGeometry(
            QtCore.QRect(10, 20, 321, 20)
        )
        self.HP_correction_shaddowing_checkBox.setObjectName(
            "HP_correction_shaddowing_checkBox"
        )

        self.HP_scanVarying_checkBox = QtWidgets.QCheckBox(self.xia2options_HP)
        self.HP_scanVarying_checkBox.setGeometry(QtCore.QRect(420, 20, 121, 20))
        self.HP_scanVarying_checkBox.setObjectName("HP_scanVarying_checkBox")

        self.HP_ReferenceGeometry_checkBox = QtWidgets.QCheckBox(self.xia2options_HP)
        self.HP_ReferenceGeometry_checkBox.setGeometry(QtCore.QRect(10, 50, 161, 20))
        self.HP_ReferenceGeometry_checkBox.setObjectName(
            "HP_ReferenceGeometry_checkBox"
        )
        self.HP_ReferenceGeometry_browse = QtWidgets.QPushButton(self.xia2options_HP)
        self.HP_ReferenceGeometry_browse.setGeometry(QtCore.QRect(160, 45, 93, 28))
        self.HP_ReferenceGeometry_browse.setObjectName("HP_ReferenceGeometry_browse")
        self.HP_ReferenceGeometry_browse.clicked.connect(self.browseForReferenceModel)
        self.HP_ReferenceGeometry_path = QtWidgets.QLabel(self.xia2options_HP)
        self.HP_ReferenceGeometry_path.setGeometry(QtCore.QRect(260, 50, 271, 16))
        self.HP_ReferenceGeometry_path.setObjectName("HP_ReferenceGeometry_path")
        self.HP_gasket_checkBox = QtWidgets.QCheckBox(self.xia2options_HP)
        self.HP_gasket_checkBox.setGeometry(QtCore.QRect(10, 80, 151, 20))
        self.HP_gasket_checkBox.setObjectName("HP_gasket_checkBox")
        self.HP_gasket_comboBox = QtWidgets.QComboBox(self.xia2options_HP)
        self.HP_gasket_comboBox.setGeometry(QtCore.QRect(90, 80, 101, 22))
        self.HP_gasket_comboBox.setObjectName("HP_gasket_comboBox")
        self.HP_gasket_comboBox.addItem("")
        self.HP_gasket_comboBox.addItem("")

        self.HP_gasketUser_checkBox = QtWidgets.QCheckBox(self.xia2options_HP)
        self.HP_gasketUser_checkBox.setGeometry(QtCore.QRect(10, 120, 151, 20))
        self.HP_gasketUser_checkBox.setObjectName("HP_gasketUser_checkBox")

        self.HP_gasketUserUC_lineEdit = QtWidgets.QLineEdit(self.xia2options_HP)
        self.HP_gasketUserUC_lineEdit.setGeometry(QtCore.QRect(170, 120, 241, 22))
        self.HP_gasketUserUC_lineEdit.setObjectName("HP_gasketUserUC_lineEdit")
        self.HP_gasketUserUC_lineEdit.setStatusTip("e.g. 2.87,2.87,2.87,90,90,90")
        self.HP_gasketUserUC_label = QtWidgets.QLabel(self.xia2options_HP)
        self.HP_gasketUserUC_label.setGeometry(QtCore.QRect(240, 100, 55, 16))
        self.HP_gasketUserUC_label.setObjectName("HP_gasketUserUC_label")
        self.HP_gasketUserSG_lineEdit = QtWidgets.QLineEdit(self.xia2options_HP)
        self.HP_gasketUserSG_lineEdit.setGeometry(QtCore.QRect(420, 120, 71, 22))
        self.HP_gasketUserSG_lineEdit.setObjectName("HP_gasketUserSG_lineEdit")
        self.HP_gasketUserSG_lineEdit.setStatusTip("e.g. Im-3m")
        self.HP_gasketUserSG_label = QtWidgets.QLabel(self.xia2options_HP)
        self.HP_gasketUserSG_label.setGeometry(QtCore.QRect(420, 100, 81, 16))
        self.HP_gasketUserSG_label.setObjectName("HP_gasketUserSG_label")
        self.HP_gasketUserW_label = QtWidgets.QLabel(self.xia2options_HP)
        self.HP_gasketUserW_label.setGeometry(QtCore.QRect(520, 100, 41, 16))
        self.HP_gasketUserW_label.setObjectName("HP_gasketUserW_label")
        self.HP_gasketUserW_lineEdit = QtWidgets.QLineEdit(self.xia2options_HP)
        self.HP_gasketUserW_lineEdit.setGeometry(QtCore.QRect(500, 120, 71, 22))
        self.HP_gasketUserW_lineEdit.setObjectName("HP_gasketUserW_lineEdit")
        self.HP_gasketUserW_lineEdit.setStatusTip("e.g. 0.02")
        # medium difficulty
        self.HP_UN_SG_checkBox = QtWidgets.QCheckBox(self.xia2options_HP)
        self.HP_UN_SG_checkBox.setGeometry(QtCore.QRect(10, 190, 181, 20))
        self.HP_UN_SG_checkBox.setObjectName("HP_UN_SG_checkBox")
        self.HP_UN_lineEdit = QtWidgets.QLineEdit(self.xia2options_HP)
        self.HP_UN_lineEdit.setGeometry(QtCore.QRect(190, 190, 211, 22))
        self.HP_UN_lineEdit.setObjectName("HP_UN_lineEdit")
        self.HP_UN_lineEdit.setStatusTip("e.g. 5.4,5.4,5.4,90,90,90")
        self.HP_UN_label = QtWidgets.QLabel(self.xia2options_HP)
        self.HP_UN_label.setGeometry(QtCore.QRect(260, 170, 51, 20))
        self.HP_UN_label.setObjectName("HP_UN_label")
        self.HP_SG_lineEdit = QtWidgets.QLineEdit(self.xia2options_HP)
        self.HP_SG_lineEdit.setGeometry(QtCore.QRect(410, 190, 91, 22))
        self.HP_SG_lineEdit.setObjectName("HP_SG_lineEdit")
        self.HP_SG_lineEdit.setStatusTip("e.g. Im-3m")
        self.HP_SG_label = QtWidgets.QLabel(self.xia2options_HP)
        self.HP_SG_label.setGeometry(QtCore.QRect(420, 170, 81, 20))
        self.HP_SG_label.setObjectName("HP_SG_label")

        self.HP_dmin_checkBox = QtWidgets.QCheckBox(self.xia2options_HP)
        self.HP_dmin_checkBox.setGeometry(QtCore.QRect(10, 220, 111, 20))
        self.HP_dmin_checkBox.setObjectName("HP_dmin_checkBox")
        self.HP_dmin_lineEdit = QtWidgets.QLineEdit(self.xia2options_HP)
        self.HP_dmin_lineEdit.setGeometry(QtCore.QRect(90, 220, 113, 22))
        self.HP_dmin_lineEdit.setObjectName("HP_dmin_lineEdit")
        self.HP_dmin_lineEdit.setStatusTip("e.g. 0.84")

        self.HP_runStartEnd_checkBox = QtWidgets.QCheckBox(self.xia2options_HP)
        self.HP_runStartEnd_checkBox.setGeometry(QtCore.QRect(10, 250, 111, 20))
        self.HP_runStartEnd_checkBox.setObjectName("HP_runStartEnd_checkBox")
        self.HP_runStartEnd_lineEdit_1 = QtWidgets.QLineEdit(self.xia2options_HP)
        self.HP_runStartEnd_lineEdit_1.setGeometry(QtCore.QRect(149, 250, 61, 22))
        self.HP_runStartEnd_lineEdit_1.setObjectName("HP_runStartEnd_lineEdit_1")
        self.HP_runStartEnd_lineEdit_1.setStatusTip("e.g. 20:600")
        self.HP_runStartEnd_label_1 = QtWidgets.QLabel(self.xia2options_HP)
        self.HP_runStartEnd_label_1.setGeometry(QtCore.QRect(130, 250, 31, 20))
        self.HP_runStartEnd_label_1.setObjectName("HP_runStartEnd_label_1")
        self.HP_runStartEnd_lineEdit_2 = QtWidgets.QLineEdit(self.xia2options_HP)
        self.HP_runStartEnd_lineEdit_2.setGeometry(QtCore.QRect(240, 250, 61, 22))
        self.HP_runStartEnd_lineEdit_2.setObjectName("HP_runStartEnd_lineEdit_2")
        self.HP_runStartEnd_lineEdit_2.setStatusTip("e.g. 20:600")
        self.HP_runStartEnd_label_2 = QtWidgets.QLabel(self.xia2options_HP)
        self.HP_runStartEnd_label_2.setGeometry(QtCore.QRect(221, 250, 31, 20))
        self.HP_runStartEnd_label_2.setObjectName("HP_runStartEnd_label_2")
        self.HP_runStartEnd_lineEdit_3 = QtWidgets.QLineEdit(self.xia2options_HP)
        self.HP_runStartEnd_lineEdit_3.setGeometry(QtCore.QRect(329, 250, 61, 22))
        self.HP_runStartEnd_lineEdit_3.setObjectName("HP_runStartEnd_lineEdit_3")
        self.HP_runStartEnd_lineEdit_3.setStatusTip("e.g. 20:600")
        self.HP_runStartEnd_label_3 = QtWidgets.QLabel(self.xia2options_HP)
        self.HP_runStartEnd_label_3.setGeometry(QtCore.QRect(401, 250, 31, 20))
        self.HP_runStartEnd_label_3.setObjectName("HP_runStartEnd_label_3")
        self.HP_runStartEnd_lineEdit_4 = QtWidgets.QLineEdit(self.xia2options_HP)
        self.HP_runStartEnd_lineEdit_4.setGeometry(QtCore.QRect(420, 250, 61, 22))
        self.HP_runStartEnd_lineEdit_4.setObjectName("HP_runStartEnd_lineEdit_4")
        self.HP_runStartEnd_lineEdit_4.setStatusTip("e.g. 20:600")
        self.HP_runStartEnd_label_4 = QtWidgets.QLabel(self.xia2options_HP)
        self.HP_runStartEnd_label_4.setGeometry(QtCore.QRect(310, 250, 31, 20))
        self.HP_runStartEnd_label_4.setObjectName("HP_runStartEnd_label_4")
        self.HP_runStartEnd_lineEdit_5 = QtWidgets.QLineEdit(self.xia2options_HP)
        self.HP_runStartEnd_lineEdit_5.setGeometry(QtCore.QRect(510, 250, 61, 22))
        self.HP_runStartEnd_lineEdit_5.setObjectName("HP_runStartEnd_lineEdit_5")
        self.HP_runStartEnd_lineEdit_5.setStatusTip("e.g. 20:600")
        self.HP_runStartEnd_label_5 = QtWidgets.QLabel(self.xia2options_HP)
        self.HP_runStartEnd_label_5.setGeometry(QtCore.QRect(491, 250, 31, 20))
        self.HP_runStartEnd_label_5.setObjectName("HP_runStartEnd_label_5")
        self.HP_runStartEnd_lineEdit_6 = QtWidgets.QLineEdit(self.xia2options_HP)
        self.HP_runStartEnd_lineEdit_6.setGeometry(QtCore.QRect(149, 280, 61, 22))
        self.HP_runStartEnd_lineEdit_6.setObjectName("HP_runStartEnd_lineEdit_6")
        self.HP_runStartEnd_lineEdit_6.setStatusTip("e.g. 20:600")
        self.HP_runStartEnd_label_7 = QtWidgets.QLabel(self.xia2options_HP)
        self.HP_runStartEnd_label_7.setGeometry(QtCore.QRect(221, 280, 31, 20))
        self.HP_runStartEnd_label_7.setObjectName("HP_runStartEnd_label_7")
        self.HP_runStartEnd_lineEdit_7 = QtWidgets.QLineEdit(self.xia2options_HP)
        self.HP_runStartEnd_lineEdit_7.setGeometry(QtCore.QRect(240, 280, 61, 22))
        self.HP_runStartEnd_lineEdit_7.setObjectName("HP_runStartEnd_lineEdit_7")
        self.HP_runStartEnd_lineEdit_7.setStatusTip("e.g. 20:600")
        self.HP_runStartEnd_lineEdit_8 = QtWidgets.QLineEdit(self.xia2options_HP)
        self.HP_runStartEnd_lineEdit_8.setGeometry(QtCore.QRect(329, 280, 61, 22))
        self.HP_runStartEnd_lineEdit_8.setObjectName("HP_runStartEnd_lineEdit_8")
        self.HP_runStartEnd_lineEdit_8.setStatusTip("e.g. 20:600")
        self.HP_runStartEnd_lineEdit_9 = QtWidgets.QLineEdit(self.xia2options_HP)
        self.HP_runStartEnd_lineEdit_9.setGeometry(QtCore.QRect(420, 280, 61, 22))
        self.HP_runStartEnd_lineEdit_9.setObjectName("HP_runStartEnd_lineEdit_9")
        self.HP_runStartEnd_lineEdit_9.setStatusTip("e.g. 20:600")
        self.HP_runStartEnd_lineEdit_10 = QtWidgets.QLineEdit(self.xia2options_HP)
        self.HP_runStartEnd_lineEdit_10.setGeometry(QtCore.QRect(510, 280, 61, 22))
        self.HP_runStartEnd_lineEdit_10.setObjectName("HP_runStartEnd_lineEdit_10")
        self.HP_runStartEnd_lineEdit_10.setStatusTip("e.g. 20:600")
        self.HP_runStartEnd_label_6 = QtWidgets.QLabel(self.xia2options_HP)
        self.HP_runStartEnd_label_6.setGeometry(QtCore.QRect(130, 280, 31, 20))
        self.HP_runStartEnd_label_6.setObjectName("HP_runStartEnd_label_6")
        self.HP_runStartEnd_label_8 = QtWidgets.QLabel(self.xia2options_HP)
        self.HP_runStartEnd_label_8.setGeometry(QtCore.QRect(310, 280, 31, 20))
        self.HP_runStartEnd_label_8.setObjectName("HP_runStartEnd_label_8")
        self.HP_runStartEnd_label_9 = QtWidgets.QLabel(self.xia2options_HP)
        self.HP_runStartEnd_label_9.setGeometry(QtCore.QRect(401, 280, 31, 20))
        self.HP_runStartEnd_label_9.setObjectName("HP_runStartEnd_label_9")
        self.HP_runStartEnd_label_10 = QtWidgets.QLabel(self.xia2options_HP)
        self.HP_runStartEnd_label_10.setGeometry(QtCore.QRect(486, 280, 31, 20))
        self.HP_runStartEnd_label_10.setObjectName("HP_runStartEnd_label_10")
        # probmatic data options
        self.HP_FixBeamDetector_checkBox = QtWidgets.QCheckBox(self.xia2options_HP)
        self.HP_FixBeamDetector_checkBox.setGeometry(QtCore.QRect(10, 320, 151, 20))
        self.HP_FixBeamDetector_checkBox.setObjectName("HP_FixBeamDetector_checkBox")

        self.HP_anvilThickness_checkBox = QtWidgets.QCheckBox(self.xia2options_HP)
        self.HP_anvilThickness_checkBox.setGeometry(QtCore.QRect(10, 350, 151, 20))
        self.HP_anvilThickness_checkBox.setObjectName("HP_anvilThickness_checkBox")
        self.HP_anvilThickness_lineEdit = QtWidgets.QLineEdit(self.xia2options_HP)
        self.HP_anvilThickness_lineEdit.setGeometry(QtCore.QRect(160, 350, 113, 22))
        self.HP_anvilThickness_lineEdit.setObjectName("HP_anvilThickness_lineEdit")
        self.HP_anvilThickness_lineEdit.setStatusTip("e.g. 2.1")

        self.HP_anvilOpeningAngle_checkBox = QtWidgets.QCheckBox(self.xia2options_HP)
        self.HP_anvilOpeningAngle_checkBox.setGeometry(QtCore.QRect(10, 380, 151, 20))
        self.HP_anvilOpeningAngle_checkBox.setObjectName(
            "HP_anvilOpeningAngle_checkBox"
        )
        self.HP_anvilOpeningAngle_lineEdit = QtWidgets.QLineEdit(self.xia2options_HP)
        self.HP_anvilOpeningAngle_lineEdit.setGeometry(QtCore.QRect(160, 380, 113, 22))
        self.HP_anvilOpeningAngle_lineEdit.setObjectName(
            "HP_anvilOpeningAngle_lineEdit"
        )
        self.HP_anvilOpeningAngle_lineEdit.setStatusTip("e.g. 80")

        self.HP_line_1 = QtWidgets.QFrame(self.xia2options_HP)
        self.HP_line_1.setGeometry(QtCore.QRect(0, 0, 581, 20))
        self.HP_line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.HP_line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.HP_line_1.setObjectName("HP_line_1")
        self.HP_line_2 = QtWidgets.QFrame(self.xia2options_HP)
        self.HP_line_2.setGeometry(QtCore.QRect(0, 150, 581, 20))
        self.HP_line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.HP_line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.HP_line_2.setObjectName("HP_line_2")
        self.HP_line_3 = QtWidgets.QFrame(self.xia2options_HP)
        self.HP_line_3.setGeometry(QtCore.QRect(0, 305, 581, 20))
        self.HP_line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.HP_line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.HP_line_3.setObjectName("HP_line_3")

        self.HP_difficulty_label_1 = QtWidgets.QLabel(self.xia2options_HP)
        self.HP_difficulty_label_1.setGeometry(QtCore.QRect(250, 1, 101, 16))
        self.HP_difficulty_label_1.setObjectName("HP_difficulty_label_1")
        self.HP_difficulty_label_1.setAutoFillBackground(True)
        self.HP_difficulty_label_2 = QtWidgets.QLabel(self.xia2options_HP)
        self.HP_difficulty_label_2.setGeometry(QtCore.QRect(230, 150, 151, 20))
        self.HP_difficulty_label_2.setObjectName("HP_difficulty_label_2")
        self.HP_difficulty_label_2.setAutoFillBackground(True)
        self.HP_difficulty_label_3 = QtWidgets.QLabel(self.xia2options_HP)
        self.HP_difficulty_label_3.setGeometry(QtCore.QRect(230, 305, 141, 20))
        self.HP_difficulty_label_3.setObjectName("HP_difficulty_label_3")
        self.HP_difficulty_label_3.setAutoFillBackground(True)
        ###############################################################################################
        Xia2Options.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Xia2Options)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 613, 26))
        self.menubar.setObjectName("menubar")
        Xia2Options.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Xia2Options)
        self.statusbar.setObjectName("statusbar")
        Xia2Options.setStatusBar(self.statusbar)

        self.retranslateUi(Xia2Options)
        self.xia2options.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Xia2Options)

        self.optionListImport = [
            self.import_TrustBeamCentre,
            self.import_ReferenceGeometry,
            self.import_DD,
            self.import_BeamCentre,
            self.import_Wavelengh,
            self.Import_FixBeamDetector_checkBox,
            self.Import_RunSelector_checkBox,
            self.Import_type_checkBox,
        ]

        self.runSelectorList = [
            self.Import_RunSelector_checkBox_1,
            self.Import_RunSelector_checkBox_2,
            self.Import_RunSelector_checkBox_3,
            self.Import_RunSelector_checkBox_4,
            self.Import_RunSelector_checkBox_5,
            self.Import_RunSelector_checkBox_6,
            self.Import_RunSelector_checkBox_7,
            self.Import_RunSelector_checkBox_8,
            self.Import_RunSelector_checkBox_9,
            self.Import_RunSelector_checkBox_10,
            self.Import_RunSelector_checkBox_11,
            self.Import_RunSelector_checkBox_12,
        ]

        self.optionListSpotFinding = [
            self.findSpots_sigmaStrong,
            self.findSpots_minSpot,
            self.findSpots_maxSpot,
            self.findSpots_dmin,
            self.findSpots_dmax,
            self.findSpots_iceRings,
            self.findSpots_powderRings,
            self.findSpots_resolutionRange,
            self.findSpots_circleMask,
            self.findSpots_recMask,
        ]

        self.optionListIndexing = [
            self.Index_method_checkBox,
            self.Index_scanVarying_checkBox,
            self.Index_UN_SG_checkBox,
            self.Index_minCell_checkBox,
            self.Index_maxCell_checkBox,
            self.Index_multiprocessing_checkBox,
            self.Index_multiSweepRefine_checkBox,
            self.Index_outliers_checkBox,
        ]

        self.optionListIntegrate = [
            self.Integrate_keepAllReflections_checkBox,
            self.Integrate_scanVarying_checkBox,
            self.Integrate_minSpotProfile_checkBox,
        ]

        self.optionListRefineScale = [
            self.Refine_FixBeamDetector_checkBox,
            self.Refine_method_checkBox,
        ]

        self.optionListOther = [
            self.Other_failover_checkBox,
            self.Other_manualInput1_checkBox,
            self.Other_manualInput2_checkBox,
            self.Other_manualInput3_checkBox,
            self.Other_manualInput4_checkBox,
        ]

        self.optionListHP = [
            self.HP_correction_shaddowing_checkBox,
            self.HP_ReferenceGeometry_checkBox,
            self.HP_gasket_checkBox,
            self.HP_gasketUser_checkBox,
            self.HP_UN_SG_checkBox,
            self.HP_dmin_checkBox,
            self.HP_runStartEnd_checkBox,
            self.HP_FixBeamDetector_checkBox,
            self.HP_scanVarying_checkBox,
            self.HP_anvilThickness_checkBox,
            self.HP_anvilOpeningAngle_checkBox,
        ]

        self.runStartEnd_lineEdits = [
            self.HP_runStartEnd_lineEdit_1.text(),
            self.HP_runStartEnd_lineEdit_2.text(),
            self.HP_runStartEnd_lineEdit_3.text(),
            self.HP_runStartEnd_lineEdit_4.text(),
            self.HP_runStartEnd_lineEdit_5.text(),
            self.HP_runStartEnd_lineEdit_6.text(),
            self.HP_runStartEnd_lineEdit_7.text(),
            self.HP_runStartEnd_lineEdit_8.text(),
            self.HP_runStartEnd_lineEdit_9.text(),
            self.HP_runStartEnd_lineEdit_10.text(),
        ]

        # load previous settings:
        self.loadOptionsAuto()

    def browseForReferenceModel(self):
        path = self.openingVisit
        os.chdir(path)
        self.refGeometryPath = QFileDialog.getOpenFileName(filter="expt(*.expt)")[0]
        # qfd = QFileDialog()
        # path = "D:\ennine\SIG HTB\BGN"
        # filter = "csv(*.csv)"
        # f = QFileDialog.getOpenFileName(qfd, title, path, filter)
        if self.refGeometryPath:
            refGeometryPathTxt = str(self.refGeometryPath)
            refGeometryFileTxt = refGeometryPathTxt.split("/")[-1]

            outputMessage = (
                "Reference Geometry Path:\n	"
                + str(refGeometryPathTxt)
                + "\nReference Geometry File:\n	"
                + str(refGeometryFileTxt)
            )
            self.mainTab_txt.appendPlainText(outputMessage)
            self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)

            self.import_ReferenceGeometry_path.setText(refGeometryFileTxt)
            self.import_ReferenceGeometry_path.setScaledContents(True)

            self.HP_ReferenceGeometry_path.setText(refGeometryFileTxt)
            self.HP_ReferenceGeometry_path.setScaledContents(True)

    def updateOptions(self):
        options = ""

        #### inport #######
        for varible in self.optionListImport:
            if varible.isChecked():
                if varible == self.import_TrustBeamCentre:
                    options = options + " trust_beam_centre=true"
                if varible == self.import_ReferenceGeometry:
                    if self.refGeometryPath == "":
                        outputMessage = "	*** Reference Geometry Error. Please select .expt file with browse button first ***"
                        self.mainTab_txt.appendPlainText(outputMessage)
                        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                        return
                    else:
                        options = (
                            options + " reference_geometry=" + str(self.refGeometryPath)
                        )
                if varible == self.import_DD:
                    if self.import_DD_lineEdit.text() == "":
                        outputMessage = "	*** Detector Distance Error. Please input detector distance e.g. 85.01"
                        self.mainTab_txt.appendPlainText(outputMessage)
                        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                        return
                    else:
                        outputMessage = "Detector distance: " + str(
                            self.import_DD_lineEdit.text()
                        )
                        self.mainTab_txt.appendPlainText(outputMessage)
                        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                        options = (
                            options
                            + " detector_distance="
                            + str(self.import_DD_lineEdit.text())
                        )

                if varible == self.import_BeamCentre:
                    if self.import_BeamCentre_X_lineEdit.text() == "":
                        outputMessage = "	*** Beam Centre Error. Please input Y"
                        self.mainTab_txt.appendPlainText(outputMessage)
                        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                        return
                    elif self.import_BeamCentre_Y_lineEdit.text() == "":
                        outputMessage = "	*** Detector Distance Error. Please input X"
                        self.mainTab_txt.appendPlainText(outputMessage)
                        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                        return
                    else:
                        outputMessage = (
                            "Detector distance: "
                            + str(self.import_BeamCentre_X_lineEdit.text())
                            + ","
                            + str(self.import_BeamCentre_Y_lineEdit.text())
                        )
                        self.mainTab_txt.appendPlainText(outputMessage)
                        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                        options = (
                            options
                            + " mosflm_beam_centre="
                            + str(self.import_BeamCentre_X_lineEdit.text())
                            + ","
                            + str(self.import_BeamCentre_Y_lineEdit.text())
                        )

                if varible == self.import_Wavelengh:
                    if self.import_wavelength_lineEdit.text() == "":
                        outputMessage = "	*** Wavelength Input Error. Please add wavelength e.g. 85.01"
                        self.mainTab_txt.appendPlainText(outputMessage)
                        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                        return
                    else:
                        outputMessage = "Wavelength: " + str(
                            self.import_wavelength_lineEdit.text()
                        )
                        self.mainTab_txt.appendPlainText(outputMessage)
                        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                        options = (
                            options
                            + " wavelength="
                            + str(self.import_wavelength_lineEdit.text())
                        )

                if varible == self.Import_FixBeamDetector_checkBox:
                    options = (
                        options
                        + " integrate.phil_file=/dls_sw/i19/scripts/HP/intergration_additional_inputs.phil"
                    )

                if varible == self.Import_RunSelector_checkBox:
                    global runSelection
                    runSelection = []
                    global runImageSelector
                    runImageSelector = True
                    for num, run in enumerate(self.runSelectorList, start=1):
                        if run.isChecked():
                            runSelection.append(num)
                    self.mainTab_txt.appendPlainText(
                        "Run selector:	" + str(runSelection)
                    )
                    self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                if varible == self.Import_type_checkBox:
                    if self.Import_type_comboBox.currentText() == "Protein":
                        pass
                    else:
                        options = options + " small_molecule=True"

        #### spot finding #######
        for varible in self.optionListSpotFinding:
            if varible.isChecked():
                if varible == self.findSpots_sigmaStrong:
                    if self.findSpots_sigmaStrong_lineEdit.text() == "":
                        outputMessage = "	*** Sigma Strong Error, please entre sigma strong e.g. 6 ***"
                        self.mainTab_txt.appendPlainText(outputMessage)
                        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                        return
                    else:
                        options = (
                            options
                            + " sigma_strong="
                            + str(self.findSpots_sigmaStrong_lineEdit.text())
                        )
                if varible == self.findSpots_minSpot:
                    if self.findSpots_minSpot_lineEdit.text() == "":
                        outputMessage = "	*** Min Spot Size Error, please entre min spots size e.g. 2 ***"
                        self.mainTab_txt.appendPlainText(outputMessage)
                        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                        return
                    else:
                        options = (
                            options
                            + " min_spot_size="
                            + str(self.findSpots_minSpot_lineEdit.text())
                        )
                if varible == self.findSpots_maxSpot:
                    if self.findSpots_maxSpot_lineEdit.text() == "":
                        outputMessage = "	*** Max Spot Size Error, please entre max spots size e.g. 2 ***"
                        self.mainTab_txt.appendPlainText(outputMessage)
                        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                        return
                    else:
                        options = (
                            options
                            + " max_spot_size="
                            + str(self.findSpots_maxSpot_lineEdit.text())
                        )
                if varible == self.findSpots_dmin:
                    if self.findSpots_dmin_lineEdit.text() == "":
                        outputMessage = (
                            "	*** D_min Error, please entre d_min e.g. 0.84 ***"
                        )
                        self.mainTab_txt.appendPlainText(outputMessage)
                        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                        return
                    else:
                        options = (
                            options
                            + " d_min="
                            + str(self.findSpots_dmin_lineEdit.text())
                        )
                if varible == self.findSpots_dmax:
                    if self.findSpots_dmax_lineEdit.text() == "":
                        outputMessage = (
                            "	*** D_max Error, please entre d_max e.g. 10 ***"
                        )
                        self.mainTab_txt.appendPlainText(outputMessage)
                        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                        return
                    else:
                        options = (
                            options
                            + " d_max="
                            + str(self.findSpots_dmax_lineEdit.text())
                        )
                if varible == self.findSpots_iceRings:
                    options = options + " ice_rings=true"

                if varible == self.findSpots_powderRings:

                    powderRing_lineEdits = [
                        self.findSpots_powderRingsUC_lineEdit.text(),
                        self.findSpots_powderRingsSG_lineEdit.text(),
                        self.findSpots_powderRingsW_lineEdit.text(),
                    ]
                    for entry in powderRing_lineEdits:
                        if entry == "":
                            outputMessage = "	*** Powder ring mask error ***"
                            self.mainTab_txt.appendPlainText(outputMessage)
                            self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                            return
                    else:
                        ice_rings_UV_command = " ice_rings.unit_cell=" + str(
                            self.findSpots_powderRingsUC_lineEdit.text()
                        )
                        ice_rings_SG_command = " ice_rings.space_group=" + str(
                            self.findSpots_powderRingsSG_lineEdit.text()
                        )
                        ice_rings_W_command = " ice_rings.width=" + str(
                            self.findSpots_powderRingsW_lineEdit.text()
                        )
                        options = (
                            options
                            + ice_rings_UV_command
                            + ice_rings_SG_command
                            + ice_rings_W_command
                        )

                if varible == self.findSpots_resolutionRange:
                    fingSpot_resRange_list = [
                        self.findSpots_resolutionRange_lineEdit_1.text(),
                        self.findSpots_resolutionRange_lineEdit_2.text(),
                        self.findSpots_resolutionRange_lineEdit_3.text(),
                        self.findSpots_resolutionRange_lineEdit_4.text(),
                        self.findSpots_resolutionRange_lineEdit_5.text(),
                        self.findSpots_resolutionRange_lineEdit_6.text(),
                        self.findSpots_resolutionRange_lineEdit_7.text(),
                        self.findSpots_resolutionRange_lineEdit_8.text(),
                        self.findSpots_resolutionRange_lineEdit_9.text(),
                        self.findSpots_resolutionRange_lineEdit_10.text(),
                    ]
                    for res in fingSpot_resRange_list:
                        if not res == "":
                            options = options + " resolution_range=" + str(res)

                if varible == self.findSpots_circleMask:
                    if self.findSpots_circleMask_lineEdit.text() == "":
                        outputMessage = "	*** Circle Mask Error, please entre is the following format: xc,yc,r ***"
                        self.mainTab_txt.appendPlainText(outputMessage)
                        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                        return
                    else:
                        options = (
                            options
                            + " circle="
                            + str(self.findSpots_circleMask_lineEdit.text())
                        )

                if varible == self.findSpots_recMask:
                    if self.findSpots_recMask_lineEdit.text() == "":
                        outputMessage = "	*** Rectangle Mask Error, please entre is the following format: x0,x1,y0,y1 ***"
                        self.mainTab_txt.appendPlainText(outputMessage)
                        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                        return
                    else:
                        options = (
                            options
                            + " rectangle="
                            + str(self.findSpots_recMask_lineEdit.text())
                        )

        #### indexing #######
        for varible in self.optionListIndexing:
            if varible.isChecked():
                if varible == self.Index_method_checkBox:
                    options = (
                        options
                        + " method="
                        + str(self.Index_method_comboBox.currentText())
                    )
                if varible == self.Index_scanVarying_checkBox:
                    options = options + " scan_varying=False"
                if varible == self.Index_UN_SG_checkBox:
                    UC_SG_lineEdits = [
                        self.Index_UN_lineEdit.text(),
                        self.Index_SG_lineEdit.text(),
                    ]
                    for entry in UC_SG_lineEdits:
                        self.mainTab_txt.appendPlainText(entry)
                        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                        if entry == "":
                            outputMessage = (
                                "	*** Error in unit cell or space group entry ***"
                            )
                            self.mainTab_txt.appendPlainText(outputMessage)
                            self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                            return
                    else:
                        UC_command = " unit_cell=" + str(self.Index_UN_lineEdit.text())
                        SG_command = " space_group=" + str(
                            self.Index_SG_lineEdit.text()
                        )
                        options = options + UC_command + SG_command
                if varible == self.Index_minCell_checkBox:
                    if self.Index_minCell_lineEdit.text() == "":
                        outputMessage = "	*** Please entre valid min cell ***"
                        self.mainTab_txt.appendPlainText(outputMessage)
                        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                        return
                    else:
                        options = (
                            options
                            + " min_cell="
                            + str(self.Index_minCell_lineEdit.text())
                        )
                if varible == self.Index_maxCell_checkBox:
                    if self.Index_maxCell_lineEdit.text() == "":
                        outputMessage = "	*** Please entre valid max cell ***"
                        self.mainTab_txt.appendPlainText(outputMessage)
                        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                        return
                    else:
                        options = (
                            options
                            + " max_cell="
                            + str(self.Index_maxCell_lineEdit.text())
                        )
                if varible == self.Index_multiprocessing_checkBox:
                    options = options + " multi_sweep_processing=True"
                if varible == self.Index_multiSweepRefine_checkBox:
                    options = options + " multi_sweep_refinement=False"
                if varible == self.Index_outliers_checkBox:
                    options = options + " outlier.algorithm=null"

        #### integrate #####
        for varible in self.optionListIntegrate:
            if varible.isChecked():
                if varible == self.Integrate_keepAllReflections_checkBox:
                    options = options + " keep_all_reflections=true"
                if varible == self.Integrate_scanVarying_checkBox:
                    options = options + " scan_varying=False"
                if varible == self.Integrate_minSpotProfile_checkBox:
                    spotProfile_lineEdits = [
                        self.Integrate_minCellOverall_lineEdit.text(),
                        self.Integrate_minCellDegree_lineEdit.text(),
                    ]
                    for entry in spotProfile_lineEdits:
                        if entry == "":
                            outputMessage = (
                                "	*** Error in overall or per degree entry ***"
                            )
                            self.mainTab_txt.appendPlainText(outputMessage)
                            self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                            return
                        if self.visit == "":
                            outputMessage = (
                                "	*** For this option a .phil need to be created, this requires a the visit to be known."
                                "	Please open a dataset and retry (File>Open). ***"
                            )
                            self.mainTab_txt.appendPlainText(outputMessage)
                            self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                            return
                    else:
                        try:
                            overallLine = (
                                "	profile.gaussian_rs.min_spots.overall="
                                + str(self.Integrate_minCellOverall_lineEdit.text())
                                + "\n"
                            )
                            degreeLine = (
                                "	profile.gaussian_rs.min_spots.per_degree="
                                + str(self.Integrate_minCellDegree_lineEdit.text())
                                + "\n"
                            )
                            xia2GUI_Path = self.visit + "processing/xia2GUI/"
                            if not os.path.exists(xia2GUI_Path):
                                os.makedirs(xia2GUI_Path)
                            philFile = (
                                xia2GUI_Path + "intergration_additional_inputs.phil"
                            )
                            with open(philFile, "a") as f:
                                f.write(
                                    "refinement_additional_inputs.phil:\n"
                                    + overallLine
                                    + degreeLine
                                )
                            options = options + " integrate.phil_file=" + philFile
                        except Exception:
                            outputMessage = (
                                "\n	*** was not able to generate .phil file *** "
                            )
                            self.mainTab_txt.appendPlainText(outputMessage)
                            self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)

        #### refine ####
        for varible in self.optionListRefineScale:
            if varible.isChecked():
                if varible == self.Refine_method_checkBox:
                    options = (
                        options
                        + " method="
                        + str(self.Refine_method_comboBox.currentText())
                    )
                if varible == self.Refine_FixBeamDetector_checkBox:
                    xia2GUI_Path = self.visit + "processing/xia2GUI/"
                    if not os.path.exists(xia2GUI_Path):
                        os.makedirs(xia2GUI_Path)
                    philFile = xia2GUI_Path + "refine_additional_inputs.phil"
                    with open(philFile, "a") as f:
                        refineLine1 = "refinement.parameterisation.beam.fix=all\n"
                        refineLine2 = "refinement.parameterisation.detector.fix=all\n"
                        refineLine3 = (
                            "refinement.parameterisation.auto_reduction.action=fix\n"
                        )
                        f.write(refineLine1 + refineLine2 + refineLine3)
                    options = options + " refine.phil_file=" + philFile

        #### other #####
        for varible in self.optionListOther:
            if varible.isChecked():
                if varible == self.Other_failover_checkBox:
                    options = options + " failover=true"
                if varible == self.Other_manualInput1_checkBox:
                    options = options + " " + self.Other_manualInput1_lineEdit.text()
                if varible == self.Other_manualInput2_checkBox:
                    options = options + " " + self.Other_manualInput2_lineEdit.text()
                if varible == self.Other_manualInput3_checkBox:
                    options = options + " " + self.Other_manualInput3_lineEdit.text()
                if varible == self.Other_manualInput4_checkBox:
                    options = options + " " + self.Other_manualInput4_lineEdit.text()

        #### HP #####
        for varible in self.optionListHP:
            if varible.isChecked():
                if varible == self.HP_correction_shaddowing_checkBox:
                    options = (
                        options
                        + " high_pressure.correction=True dynamic_shadowing=True resolution_range=999,15"
                    )
                if varible == self.HP_scanVarying_checkBox:
                    options = options + " scan_varying=False"
                if varible == self.HP_ReferenceGeometry_checkBox:
                    if self.refGeometryPath == "":
                        outputMessage = "	*** Reference Geometry Error. Please select .expt file with browse button first ***"
                        self.mainTab_txt.appendPlainText(outputMessage)
                        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                        return
                    else:
                        options = (
                            options + " reference_geometry=" + str(self.refGeometryPath)
                        )
                if varible == self.HP_gasket_checkBox:
                    gasketType = str(self.HP_gasket_comboBox.currentText())
                    if gasketType == "Tungsten":
                        options = (
                            options
                            + " ice_rings.filter=True ice_rings.unit_cell=3.1652,3.1652,3.1652,90,90,90 ice_rings.space_group=Im-3m ice_rings.width=0.02"
                        )
                    if gasketType == "Steel":
                        # steel gaskets are often either Fe or Ni. The unit cell for Fe is given below.
                        options = (
                            options
                            + " ice_rings.filter=True ice_rings.unit_cell=2.87,2.87,2.87,90,90,90 ice_rings.space_group=Im-3m ice_rings.width=0.02"
                        )

                if varible == self.HP_gasketUser_checkBox:
                    powderRing_lineEdits = [
                        self.HP_gasketUserUC_lineEdit.text(),
                        self.HP_gasketUserSG_lineEdit.text(),
                        self.HP_gasketUserW_lineEdit.text(),
                    ]
                    for entry in powderRing_lineEdits:
                        if entry == "":
                            outputMessage = "	*** Powder ring mask error ***"
                            self.mainTab_txt.appendPlainText(outputMessage)
                            self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                            return
                    else:
                        ice_rings_UV_command = " ice_rings.unit_cell=" + str(
                            self.HP_gasketUserUC_lineEdit.text()
                        )
                        ice_rings_SG_command = " ice_rings.space_group=" + str(
                            self.HP_gasketUserSG_lineEdit.text()
                        )
                        ice_rings_W_command = " ice_rings.width=" + str(
                            self.HP_gasketUserW_lineEdit.text()
                        )
                        options = (
                            options
                            + ice_rings_UV_command
                            + ice_rings_SG_command
                            + ice_rings_W_command
                        )
                # medium difficulty:
                if varible == self.HP_UN_SG_checkBox:
                    UC_SG_lineEdits = [
                        self.HP_UN_lineEdit.text(),
                        self.HP_SG_lineEdit.text(),
                    ]
                    for entry in UC_SG_lineEdits:
                        self.mainTab_txt.appendPlainText(entry)
                        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                        if entry == "":
                            outputMessage = (
                                "	*** Error in unit cell or space group entry ***"
                            )
                            self.mainTab_txt.appendPlainText(outputMessage)
                            self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                            return
                    else:
                        UC_command = " unit_cell=" + str(self.HP_UN_lineEdit.text())
                        SG_command = " space_group=" + str(self.HP_SG_lineEdit.text())
                        options = options + UC_command + SG_command

                if varible == self.HP_dmin_checkBox:
                    if self.HP_dmin_lineEdit.text() == "":
                        outputMessage = (
                            "	*** D_min HP Error, please entre d_min e.g. 0.84 ***"
                        )
                        self.mainTab_txt.appendPlainText(outputMessage)
                        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                        return
                    else:
                        options = (
                            options + " d_min=" + str(self.HP_dmin_lineEdit.text())
                        )

                if varible == self.HP_runStartEnd_checkBox:
                    runImageSelector = True
                    counter = 0
                    self.runStartEnd_lineEdits = [
                        self.HP_runStartEnd_lineEdit_1.text(),
                        self.HP_runStartEnd_lineEdit_2.text(),
                        self.HP_runStartEnd_lineEdit_3.text(),
                        self.HP_runStartEnd_lineEdit_4.text(),
                        self.HP_runStartEnd_lineEdit_5.text(),
                        self.HP_runStartEnd_lineEdit_6.text(),
                        self.HP_runStartEnd_lineEdit_7.text(),
                        self.HP_runStartEnd_lineEdit_8.text(),
                        self.HP_runStartEnd_lineEdit_9.text(),
                        self.HP_runStartEnd_lineEdit_10.text(),
                    ]

                    for entry in self.runStartEnd_lineEdits:
                        if entry == "":
                            counter += 1
                            pass
                        else:
                            global imageSelection
                            imageSelection[counter] = entry
                            counter += 1
                    outputMessage = "Image start/end option selected.\n" "	" + str(
                        imageSelection
                    )
                    self.mainTab_txt.appendPlainText(outputMessage)
                    self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)

                if varible == self.HP_FixBeamDetector_checkBox:
                    options = (
                        options
                        + " integrate.phil_file=/dls_sw/i19/scripts/HP/intergration_additional_inputs.phil"
                    )
                    # intergration_additional_inputs.phil:
                    # refinement.parameterisation.beam.fix=all
                    # refinement.parameterisation.detector.fix=all
                    # refinement.parameterisation.auto_reduction.action=fix

                if varible == self.HP_anvilThickness_checkBox:
                    if self.HP_anvilThickness_lineEdit.text() == "":
                        outputMessage = "	*** Anvil Thickness Input Error, please entre thickness e.g. 2.1 ***"
                        self.mainTab_txt.appendPlainText(outputMessage)
                        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                        return
                    else:
                        options = (
                            options
                            + " high_pressure.anvil.thickness="
                            + str(self.HP_anvilThickness_lineEdit.text())
                        )

                if varible == self.HP_anvilOpeningAngle_checkBox:
                    if self.HP_anvilOpeningAngle_lineEdit.text() == "":
                        outputMessage = "	*** Anvil Opening Angle Input Error, please entre opening angle e.g. 38 ***"
                        self.mainTab_txt.appendPlainText(outputMessage)
                        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                        return
                    else:
                        pass
                        # options = options + " high_pressure.anvil.angle=" + str(self.HP_anvilOpeningAngle_lineEdit.text())

        global xia2OptionsList
        xia2OptionsList = options
        global datasetINPUT

        if not datasetINPUT == "MULTIPLE":

            if not runImageSelector:
                datasetInput = self.datasetPath

            else:  ############################# causing issues when multiple ###########
                if self.datasetPath == "":
                    datasetInput = self.datasetPath
                    self.mainTab_txt.appendPlainText(
                        "Dataset must be selected before selecting runs or images start/end"
                    )
                    self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
                else:
                    datasetInput = ""
                    if runSelection:  # runs have been selected
                        for entry in runSelection:
                            datasetInput = (
                                datasetInput
                                + " image="
                                + self.datasetPath
                                + "/"
                                + self.prefix
                                + str("%02d_00001.cbf" % int(entry))
                            )
                            if (entry - 1) in imageSelection:
                                datasetInput = (
                                    datasetInput + ":" + imageSelection[entry - 1]
                                )
                    else:  # runs have NOT been selected
                        for run in self.runList:
                            datasetInput = (
                                datasetInput
                                + " image="
                                + self.datasetPath
                                + "/"
                                + self.prefix
                                + str("%02d_00001.cbf" % int(run))
                            )
                            if (run - 1) in imageSelection:
                                datasetInput = (
                                    datasetInput + ":" + imageSelection[run - 1]
                                )

            datasetINPUT = datasetInput

        optionsUndateText = (
            "\n\nUpdating options"
            + "\n	Xia2 command: "
            + "\n	"
            + self.xia2command
            + datasetINPUT
            + xia2OptionsList
        )
        self.mainTab_txt.appendPlainText(optionsUndateText)
        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)

        Ui_MainWindow.updateOptionsFunction(
            self.xia2command, datasetINPUT, self.command_command
        )

        try:
            self.saveOptionsAuto()
        except Exception:
            optionsUndateText = (
                "\n	Auto saving options didn't work, try selecting a dataset first."
            )
            self.mainTab_txt.appendPlainText(optionsUndateText)
            self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)

    def resetOptions(self):
        outputMessage = "\nReseting options"
        self.mainTab_txt.appendPlainText(outputMessage)
        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)

        for checkboxes in self.optionListImport:
            checkboxes.setChecked(False)
        for checkboxes in self.optionListSpotFinding:
            checkboxes.setChecked(False)
        for checkboxes in self.optionListIndexing:
            checkboxes.setChecked(False)
        for checkboxes in self.optionListIntegrate:
            checkboxes.setChecked(False)
        for checkboxes in self.optionListRefineScale:
            checkboxes.setChecked(False)
        for checkboxes in self.optionListOther:
            checkboxes.setChecked(False)
        for checkboxes in self.optionListHP:
            checkboxes.setChecked(False)
        for checkboxes in self.runSelectorList:
            checkboxes.setChecked(False)
        self.Import_type_checkBox.setChecked(True)
        global runImageSelector
        runImageSelector = False
        global runSelection
        runSelection = []
        global imageSelection
        imageSelection = {}

        if self.visit == "":
            return
        if os.path.isfile(self.visit + "processing/autoSaveOptions.txt"):
            optionFile = self.visit + "processing/autoSaveOptions.txt"
            with open(optionFile, "w"):
                pass

        global xia2OptionsList
        xia2OptionsList = ""

        global datasetINPUT
        datasetINPUT = self.datasetPath

        optionsUndateText = (
            "\n\nUpdating options"
            + "\n	Xia2 command: "
            + "\n	"
            + self.xia2command
            + datasetINPUT
            + xia2OptionsList
        )
        self.mainTab_txt.appendPlainText(optionsUndateText)
        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)

        Ui_MainWindow.updateOptionsFunction(
            self.xia2command, datasetINPUT, self.command_command
        )

    def optionFileTextFunction(self):
        optionFileText = ""
        for num, checkboxes in enumerate(self.optionListImport):
            if checkboxes.isChecked():
                if num == 1:
                    optionFileText = (
                        optionFileText
                        + "I "
                        + str(num)
                        + " "
                        + str(self.refGeometryPath)
                        + "\n"
                    )
                elif num == 2:
                    optionFileText = (
                        optionFileText
                        + "I "
                        + str(num)
                        + " "
                        + str(self.import_DD_lineEdit.text())
                        + "\n"
                    )
                elif num == 3:
                    optionFileText = (
                        optionFileText
                        + "I "
                        + str(num)
                        + " "
                        + str(self.import_BeamCentre_X_lineEdit.text())
                        + " "
                        + str(self.import_BeamCentre_Y_lineEdit.text())
                        + "\n"
                    )
                elif num == 4:
                    optionFileText = (
                        optionFileText
                        + "I "
                        + str(num)
                        + " "
                        + str(self.import_wavelength_lineEdit.text())
                        + "\n"
                    )
                elif num == 7:
                    optionFileText = (
                        optionFileText
                        + "I "
                        + str(num)
                        + " "
                        + str(self.Import_type_comboBox.currentIndex())
                        + "\n"
                    )
                else:
                    optionFileText = optionFileText + "I " + str(num) + "\n"
        for num, checkboxes in enumerate(self.runSelectorList):
            if checkboxes.isChecked():
                optionFileText = optionFileText + "RS " + str(num) + "\n"
        # spot finding
        for num, checkboxes in enumerate(self.optionListSpotFinding):
            if checkboxes.isChecked():
                if num == 0:
                    optionFileText = (
                        optionFileText
                        + "SF "
                        + str(num)
                        + " "
                        + str(self.findSpots_sigmaStrong_lineEdit.text())
                        + "\n"
                    )
                elif num == 1:
                    optionFileText = (
                        optionFileText
                        + "SF "
                        + str(num)
                        + " "
                        + str(self.findSpots_minSpot_lineEdit.text())
                        + "\n"
                    )
                elif num == 2:
                    optionFileText = (
                        optionFileText
                        + "SF "
                        + str(num)
                        + " "
                        + str(self.findSpots_maxSpot_lineEdit.text())
                        + "\n"
                    )
                elif num == 3:
                    optionFileText = (
                        optionFileText
                        + "SF "
                        + str(num)
                        + " "
                        + str(self.findSpots_dmin_lineEdit.text())
                        + "\n"
                    )
                elif num == 4:
                    optionFileText = (
                        optionFileText
                        + "SF "
                        + str(num)
                        + " "
                        + str(self.findSpots_dmax_lineEdit.text())
                        + "\n"
                    )
                elif num == 6:
                    optionFileText = (
                        optionFileText
                        + "SF "
                        + str(num)
                        + " "
                        + str(self.findSpots_powderRingsUC_lineEdit.text())
                        + " "
                        + str(self.findSpots_powderRingsSG_lineEdit.text())
                        + " "
                        + str(self.findSpots_powderRingsW_lineEdit.text())
                        + "\n"
                    )
                elif num == 7:

                    fingSpot_resRange_list = [
                        self.findSpots_resolutionRange_lineEdit_1.text(),
                        self.findSpots_resolutionRange_lineEdit_2.text(),
                        self.findSpots_resolutionRange_lineEdit_3.text(),
                        self.findSpots_resolutionRange_lineEdit_4.text(),
                        self.findSpots_resolutionRange_lineEdit_5.text(),
                        self.findSpots_resolutionRange_lineEdit_6.text(),
                        self.findSpots_resolutionRange_lineEdit_7.text(),
                        self.findSpots_resolutionRange_lineEdit_8.text(),
                        self.findSpots_resolutionRange_lineEdit_9.text(),
                        self.findSpots_resolutionRange_lineEdit_10.text(),
                    ]
                    optionFileText = optionFileText + "SF " + str(num)
                    for resRange in fingSpot_resRange_list:
                        optionFileText = optionFileText + " " + str(resRange)
                    optionFileText = optionFileText + "\n"
                elif num == 8:
                    optionFileText = (
                        optionFileText
                        + "SF "
                        + str(num)
                        + " "
                        + str(self.findSpots_circleMask_lineEdit.text())
                        + "\n"
                    )
                elif num == 9:
                    optionFileText = (
                        optionFileText
                        + "SF "
                        + str(num)
                        + " "
                        + str(self.findSpots_recMask_lineEdit.text())
                        + "\n"
                    )
                else:
                    optionFileText = optionFileText + "SF " + str(num) + "\n"
        # indexing
        for num, checkboxes in enumerate(self.optionListIndexing):
            if checkboxes.isChecked():
                if num == 0:
                    optionFileText = (
                        optionFileText
                        + "Ind "
                        + str(num)
                        + " "
                        + str(self.Index_method_comboBox.currentIndex())
                        + "\n"
                    )
                elif num == 2:
                    optionFileText = (
                        optionFileText
                        + "Ind "
                        + str(num)
                        + " "
                        + str(self.Index_UN_lineEdit.text())
                        + " "
                        + str(self.Index_SG_lineEdit.text())
                        + "\n"
                    )
                elif num == 3:
                    optionFileText = (
                        optionFileText
                        + "Ind "
                        + str(num)
                        + " "
                        + str(self.Index_minCell_lineEdit.text())
                        + "\n"
                    )
                elif num == 4:
                    optionFileText = (
                        optionFileText
                        + "Ind "
                        + str(num)
                        + " "
                        + str(self.Index_maxCell_lineEdit.text())
                        + "\n"
                    )
                else:
                    optionFileText = optionFileText + "Ind " + str(num) + "\n"
        # Integrate
        for num, checkboxes in enumerate(self.optionListIntegrate):
            if checkboxes.isChecked():
                if num == 2:
                    optionFileText = (
                        optionFileText
                        + "Int "
                        + str(num)
                        + " "
                        + str(self.Integrate_minCellOverall_lineEdit.text())
                        + " "
                        + str(self.Integrate_minCellDegree_lineEdit.text())
                        + "\n"
                    )
                else:
                    optionFileText = optionFileText + "Int " + str(num) + "\n"
        # Refine and Scale
        for num, checkboxes in enumerate(self.optionListRefineScale):
            if checkboxes.isChecked():
                if num == 1:
                    optionFileText = (
                        optionFileText
                        + "R "
                        + str(num)
                        + " "
                        + str(self.Refine_method_comboBox.currentIndex())
                        + "\n"
                    )
                else:
                    optionFileText = optionFileText + "R " + str(num) + "\n"
        # Other
        for num, checkboxes in enumerate(self.optionListOther):
            if checkboxes.isChecked():
                if num == 1:
                    optionFileText = (
                        optionFileText
                        + "O "
                        + str(num)
                        + " "
                        + str(self.Other_manualInput1_lineEdit.text())
                        + "\n"
                    )
                if num == 2:
                    optionFileText = (
                        optionFileText
                        + "O "
                        + str(num)
                        + " "
                        + str(self.Other_manualInput1_lineEdit.text())
                        + "\n"
                    )
                if num == 3:
                    optionFileText = (
                        optionFileText
                        + "O "
                        + str(num)
                        + " "
                        + str(self.Other_manualInput1_lineEdit.text())
                        + "\n"
                    )
                if num == 4:
                    optionFileText = (
                        optionFileText
                        + "O "
                        + str(num)
                        + " "
                        + str(self.Other_manualInput1_lineEdit.text())
                        + "\n"
                    )
                else:
                    optionFileText = optionFileText + "O " + str(num) + "\n"

        # HP
        for num, checkboxes in enumerate(self.optionListHP):
            if checkboxes.isChecked():
                if num == 1:
                    optionFileText = (
                        optionFileText
                        + "HP "
                        + str(num)
                        + " "
                        + str(self.refGeometryPath)
                        + "\n"
                    )
                elif num == 2:
                    optionFileText = (
                        optionFileText
                        + "HP "
                        + str(num)
                        + " "
                        + str(self.HP_gasket_comboBox.currentIndex())
                        + "\n"
                    )
                elif num == 3:
                    optionFileText = (
                        optionFileText
                        + "HP "
                        + str(num)
                        + " "
                        + str(self.HP_gasketUserUC_lineEdit.text())
                        + " "
                        + str(self.HP_gasketUserSG_lineEdit.text())
                        + " "
                        + str(self.HP_gasketUserW_lineEdit.text())
                        + "\n"
                    )
                elif num == 4:
                    optionFileText = (
                        optionFileText
                        + "HP "
                        + str(num)
                        + " "
                        + str(self.HP_UN_lineEdit.text())
                        + " "
                        + str(self.HP_SG_lineEdit.text())
                        + "\n"
                    )
                elif num == 5:
                    optionFileText = (
                        optionFileText
                        + "HP "
                        + str(num)
                        + " "
                        + str(self.HP_dmin_lineEdit.text())
                        + "\n"
                    )
                elif num == 6:
                    optionFileText = optionFileText + "HP " + str(num)
                    self.runStartEnd_lineEdits = [
                        self.HP_runStartEnd_lineEdit_1.text(),
                        self.HP_runStartEnd_lineEdit_2.text(),
                        self.HP_runStartEnd_lineEdit_3.text(),
                        self.HP_runStartEnd_lineEdit_4.text(),
                        self.HP_runStartEnd_lineEdit_5.text(),
                        self.HP_runStartEnd_lineEdit_6.text(),
                        self.HP_runStartEnd_lineEdit_7.text(),
                        self.HP_runStartEnd_lineEdit_8.text(),
                        self.HP_runStartEnd_lineEdit_9.text(),
                        self.HP_runStartEnd_lineEdit_10.text(),
                    ]
                    for entry in self.runStartEnd_lineEdits:
                        if entry == "":
                            optionFileText = optionFileText + " #"
                        else:
                            optionFileText = optionFileText + " " + str(entry)
                    optionFileText = optionFileText + "\n"
                elif num == 8:
                    optionFileText = (
                        optionFileText
                        + "HP "
                        + str(num)
                        + " "
                        + str(self.HP_anvilThickness_lineEdit.text())
                        + "\n"
                    )
                elif num == 9:
                    optionFileText = (
                        optionFileText
                        + "HP "
                        + str(num)
                        + " "
                        + str(self.HP_anvilOpeningAngle_checkBox.text())
                        + "\n"
                    )

                else:
                    optionFileText = optionFileText + "HP " + str(num) + "\n"
        return optionFileText

    def saveOptions(self):
        outputMessage = "\n	Saving options"
        self.mainTab_txt.appendPlainText(outputMessage)
        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)

        path = self.openingVisit
        optionFile = QFileDialog.getSaveFileName(None, "Save Current Options", path)[0]

        optionFileText = self.optionFileTextFunction()

        outputMessage = (
            "\n	File location: " + str(optionFile) + "\n	" + str(optionFileText)
        )
        self.mainTab_txt.appendPlainText(outputMessage)
        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)

        with open(optionFile, "w") as oF:
            pass
        with open(optionFile, "a") as oF:
            oF.write(optionFileText)
            oF.write("")
            oF.close()

    def saveOptionsAuto(self):
        outputMessage = "\n	Saving current options"
        self.mainTab_txt.appendPlainText(outputMessage)
        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)

        if self.visit == "":
            return
        else:
            optionFile = self.visit + "processing/autoSaveOptions.txt"

        optionFileText = self.optionFileTextFunction()

        outputMessage = (
            "\n	File location: " + str(optionFile) + "\n	" + str(optionFileText)
        )
        self.mainTab_txt.appendPlainText(outputMessage)
        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)

        with open(optionFile, "w") as oF:
            pass
        with open(optionFile, "a") as oF:
            oF.write(optionFileText)
            oF.write("")
            oF.close()

    def loadOptionsAuto(self):
        if self.visit == "":
            outputMessage = "	Visit/Dataset has not been selected, therefore previous settings will not be loaded"
            self.mainTab_txt.appendPlainText(outputMessage)
            self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
            return
        if os.path.isfile(self.visit + "processing/autoSaveOptions.txt"):
            savedOptionsPathTxt = self.visit + "processing/autoSaveOptions.txt"
            self.loadOptionsMain(savedOptionsPathTxt)
        else:
            return

    def loadOptions(self):
        outputMessage = "\nLoading options"
        self.mainTab_txt.appendPlainText(outputMessage)
        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)

        path = self.openingVisit
        os.chdir(path)
        self.savedOptionsPath = QFileDialog.getOpenFileName()[0]
        if self.savedOptionsPath:
            savedOptionsPathTxt = str(self.savedOptionsPath)
        self.loadOptionsMain(savedOptionsPathTxt)

    def loadOptionsMain(self, savedOptionsPathTxt):
        outputMessage = "	Loading previous settings (" + savedOptionsPathTxt + ")"
        self.mainTab_txt.appendPlainText(outputMessage)
        self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
        try:
            with open(savedOptionsPathTxt) as optionsInput:
                for line in optionsInput:
                    lineSplit = line.split(" ")
                    # print(line)
                    if lineSplit[0] == "I":
                        if int(lineSplit[1]) == 1:
                            self.refGeometryPath = lineSplit[2]
                            refGeometryPathTxt = str(self.refGeometryPath)
                            refGeometryFileTxt = refGeometryPathTxt.split("/")[-1]
                            self.import_ReferenceGeometry_path.setText(
                                refGeometryFileTxt
                            )
                            self.import_ReferenceGeometry_path.setScaledContents(True)
                            self.HP_ReferenceGeometry_path.setText(refGeometryFileTxt)
                            self.HP_ReferenceGeometry_path.setScaledContents(True)
                            self.optionListImport[int(lineSplit[1])].setChecked(True)
                        if int(lineSplit[1]) == 2:
                            self.import_DD_lineEdit.setText(lineSplit[2])
                            self.optionListImport[int(lineSplit[1])].setChecked(True)
                        if int(lineSplit[1]) == 3:
                            self.import_BeamCentre_X_lineEdit.setText(lineSplit[2])
                            self.import_BeamCentre_Y_lineEdit.setText(lineSplit[3])
                            self.optionListImport[int(lineSplit[1])].setChecked(True)
                        if int(lineSplit[1]) == 4:
                            self.import_wavelength_lineEdit.setText(lineSplit[2])
                            self.optionListImport[int(lineSplit[1])].setChecked(True)
                        if int(lineSplit[1]) == 7:
                            self.Import_type_comboBox.setCurrentIndex(int(lineSplit[2]))
                            self.optionListImport[int(lineSplit[1])].setChecked(True)
                        else:
                            self.optionListImport[int(lineSplit[1])].setChecked(True)
                    if lineSplit[0] == "SF":
                        if int(lineSplit[1]) == 0:
                            self.findSpots_sigmaStrong_lineEdit.setText(lineSplit[2])
                            self.optionListSpotFinding[int(lineSplit[1])].setChecked(
                                True
                            )
                        if int(lineSplit[1]) == 1:
                            self.findSpots_minSpot_lineEdit.setText(lineSplit[2])
                            self.optionListSpotFinding[int(lineSplit[1])].setChecked(
                                True
                            )
                        if int(lineSplit[1]) == 2:
                            self.findSpots_maxSpot_lineEdit.setText(lineSplit[2])
                            self.optionListSpotFinding[int(lineSplit[1])].setChecked(
                                True
                            )
                        if int(lineSplit[1]) == 3:
                            self.findSpots_dmin_lineEdit.setText(lineSplit[2])
                            self.optionListSpotFinding[int(lineSplit[1])].setChecked(
                                True
                            )
                        if int(lineSplit[1]) == 4:
                            self.findSpots_dmax_lineEdit.setText(lineSplit[2])
                            self.optionListSpotFinding[int(lineSplit[1])].setChecked(
                                True
                            )
                        if int(lineSplit[1]) == 6:
                            self.findSpots_powderRingsUC_lineEdit.setText(lineSplit[2])
                            self.findSpots_powderRingsSG_lineEdit.setText(lineSplit[3])
                            self.findSpots_powderRingsW_lineEdit.setText(lineSplit[4])
                            self.optionListSpotFinding[int(lineSplit[1])].setChecked(
                                True
                            )
                        if int(lineSplit[1]) == 7:
                            self.findSpots_resolutionRange_lineEdit_1.setText(
                                lineSplit[2]
                            )
                            self.findSpots_resolutionRange_lineEdit_2.setText(
                                lineSplit[3]
                            )
                            self.findSpots_resolutionRange_lineEdit_3.setText(
                                lineSplit[4]
                            )
                            self.findSpots_resolutionRange_lineEdit_4.setText(
                                lineSplit[5]
                            )
                            self.findSpots_resolutionRange_lineEdit_5.setText(
                                lineSplit[6]
                            )
                            self.findSpots_resolutionRange_lineEdit_6.setText(
                                lineSplit[7]
                            )
                            self.findSpots_resolutionRange_lineEdit_7.setText(
                                lineSplit[8]
                            )
                            self.findSpots_resolutionRange_lineEdit_8.setText(
                                lineSplit[9]
                            )
                            self.findSpots_resolutionRange_lineEdit_9.setText(
                                lineSplit[10]
                            )
                            self.findSpots_resolutionRange_lineEdit_10.setText(
                                lineSplit[11]
                            )
                            self.optionListSpotFinding[int(lineSplit[1])].setChecked(
                                True
                            )
                        if int(lineSplit[1]) == 8:
                            self.findSpots_circleMask_lineEdit.setText(lineSplit[2])
                            self.optionListSpotFinding[int(lineSplit[1])].setChecked(
                                True
                            )
                        if int(lineSplit[1]) == 9:
                            self.findSpots_recMask_lineEdit.setText(lineSplit[2])
                            self.optionListSpotFinding[int(lineSplit[1])].setChecked(
                                True
                            )
                        else:
                            self.optionListSpotFinding[int(lineSplit[1])].setChecked(
                                True
                            )
                    if lineSplit[0] == "Ind":
                        if int(lineSplit[1]) == 0:
                            self.Index_method_comboBox.setCurrentIndex(
                                int(lineSplit[2])
                            )
                            self.optionListIndexing[int(lineSplit[1])].setChecked(True)
                        if int(lineSplit[1]) == 2:
                            self.Index_UN_lineEdit.setText((lineSplit[2]))
                            self.Index_SG_lineEdit.setText((lineSplit[3]))
                            self.optionListIndexing[int(lineSplit[1])].setChecked(True)
                        if int(lineSplit[1]) == 3:
                            self.Index_minCell_lineEdit.setText((lineSplit[2]))
                            self.optionListIndexing[int(lineSplit[1])].setChecked(True)
                        if int(lineSplit[1]) == 4:
                            self.Index_maxCell_lineEdit.setText((lineSplit[2]))
                            self.optionListIndexing[int(lineSplit[1])].setChecked(True)
                        else:
                            self.optionListIndexing[int(lineSplit[1])].setChecked(True)
                    if lineSplit[0] == "Int":
                        if int(lineSplit[1]) == 2:
                            self.Integrate_minCellOverall_lineEdit.setText(
                                (lineSplit[2])
                            )
                            self.Integrate_minCellDegree_lineEdit.setText(
                                (lineSplit[3])
                            )
                            self.optionListIntegrate[int(lineSplit[1])].setChecked(True)
                        else:
                            self.optionListIntegrate[int(lineSplit[1])].setChecked(True)
                    if lineSplit[0] == "R":
                        if int(lineSplit[1]) == 1:
                            self.Refine_method_comboBox.setCurrentIndex(
                                int(lineSplit[2])
                            )
                            self.optionListRefineScale[int(lineSplit[1])].setChecked(
                                True
                            )
                        else:
                            self.optionListRefineScale[int(lineSplit[1])].setChecked(
                                True
                            )
                    if lineSplit[0] == "O":
                        if int(lineSplit[1]) == 1:
                            self.Other_manualInput1_lineEdit.setText((lineSplit[2]))
                            self.optionListOther[int(lineSplit[1])].setChecked(True)
                        if int(lineSplit[1]) == 2:
                            self.Other_manualInput2_lineEdit.setText((lineSplit[2]))
                            self.optionListOther[int(lineSplit[1])].setChecked(True)
                        if int(lineSplit[1]) == 3:
                            self.Other_manualInput3_lineEdit.setText((lineSplit[2]))
                            self.optionListOther[int(lineSplit[1])].setChecked(True)
                        if int(lineSplit[1]) == 4:
                            self.Other_manualInput4_lineEdit.setText((lineSplit[2]))
                            self.optionListOther[int(lineSplit[1])].setChecked(True)
                        else:
                            self.optionListOther[int(lineSplit[1])].setChecked(True)
                    if lineSplit[0] == "HP":
                        if int(lineSplit[1]) == 1:
                            self.refGeometryPath = lineSplit[2]
                            refGeometryPathTxt = str(self.refGeometryPath)
                            refGeometryFileTxt = refGeometryPathTxt.split("/")[-1]
                            self.import_ReferenceGeometry_path.setText(
                                refGeometryFileTxt
                            )
                            self.import_ReferenceGeometry_path.setScaledContents(True)
                            self.HP_ReferenceGeometry_path.setText(refGeometryFileTxt)
                            self.HP_ReferenceGeometry_path.setScaledContents(True)
                            self.optionListHP[int(lineSplit[1])].setChecked(True)
                        if int(lineSplit[1]) == 2:
                            self.HP_gasket_comboBox.setCurrentIndex(int(lineSplit[2]))
                            self.optionListHP[int(lineSplit[1])].setChecked(True)
                        if int(lineSplit[1]) == 3:
                            self.HP_gasketUserUC_lineEdit.setText((lineSplit[2]))
                            self.HP_gasketUserSG_lineEdit.setText((lineSplit[3]))
                            self.HP_gasketUserW_lineEdit.setText((lineSplit[4]))
                            self.optionListHP[int(lineSplit[1])].setChecked(True)
                        if int(lineSplit[1]) == 4:
                            self.HP_UN_lineEdit.setText((lineSplit[2]))
                            self.HP_SG_lineEdit.setText((lineSplit[3]))
                            self.optionListHP[int(lineSplit[1])].setChecked(True)
                        if int(lineSplit[1]) == 5:
                            self.HP_dmin_lineEdit.setText((lineSplit[2]))
                            self.optionListHP[int(lineSplit[1])].setChecked(True)
                        if int(lineSplit[1]) == 6:
                            #### if # then skip ###
                            if "#" not in lineSplit[2]:
                                self.HP_runStartEnd_lineEdit_1.setText((lineSplit[2]))
                            if "#" not in lineSplit[3]:
                                self.HP_runStartEnd_lineEdit_2.setText((lineSplit[3]))
                            if "#" not in lineSplit[4]:
                                self.HP_runStartEnd_lineEdit_3.setText((lineSplit[4]))
                            if "#" not in lineSplit[5]:
                                self.HP_runStartEnd_lineEdit_4.setText((lineSplit[5]))
                            if "#" not in lineSplit[6]:
                                self.HP_runStartEnd_lineEdit_5.setText((lineSplit[6]))
                            if "#" not in lineSplit[7]:
                                self.HP_runStartEnd_lineEdit_6.setText((lineSplit[7]))
                            if "#" not in lineSplit[8]:
                                self.HP_runStartEnd_lineEdit_7.setText((lineSplit[8]))
                            if "#" not in lineSplit[9]:
                                self.HP_runStartEnd_lineEdit_8.setText((lineSplit[9]))
                            if "#" not in lineSplit[10]:
                                self.HP_runStartEnd_lineEdit_9.setText((lineSplit[10]))
                            if "#" not in lineSplit[11]:
                                self.HP_runStartEnd_lineEdit_10.setText((lineSplit[11]))
                            self.optionListHP[int(lineSplit[1])].setChecked(True)
                        if int(lineSplit[1]) == 8:
                            self.HP_anvilThickness_lineEdit.setText((lineSplit[2]))
                            self.optionListHP[int(lineSplit[1])].setChecked(True)
                        if int(lineSplit[1]) == 9:
                            self.HP_anvilOpeningAngle_lineEdit.setText((lineSplit[2]))
                            self.optionListHP[int(lineSplit[1])].setChecked(True)
                        else:
                            self.optionListHP[int(lineSplit[1])].setChecked(True)
                    if lineSplit[0] == "RS":
                        self.runSelectorList[int(lineSplit[1])].setChecked(True)

        except Exception:
            outputMessage = (
                "	Error in loading saved options (" + savedOptionsPathTxt + ")"
            )
            self.mainTab_txt.appendPlainText(outputMessage)
            self.mainTab_txt.moveCursor(QtGui.QTextCursor.End)
            print(savedOptionsPathTxt)

    def retranslateUi(self, Xia2Options):
        _translate = QtCore.QCoreApplication.translate
        Xia2Options.setWindowTitle(
            _translate("Xia2Options", "Options - Xia2 Additional Commands")
        )

        self.updateButton.setText(_translate("Xia2Options", "Update Command"))
        self.updateButton.setStatusTip(
            _translate(
                "Xia2Options", "Update the xia2 command with the current selection"
            )
        )
        self.resetButton.setText(_translate("Xia2Options", "Reset"))
        self.resetButton.setStatusTip(
            _translate("Xia2Options", "The rest button will uncheck all check boxes")
        )
        self.saveButton.setText(_translate("Xia2Options", "Save"))
        self.saveButton.setStatusTip(
            _translate("Xia2Options", "Save the current options")
        )
        self.loadButton.setText(_translate("Xia2Options", "Load"))
        self.loadButton.setStatusTip(
            _translate("Xia2Options", "Load a pre-saved option selection")
        )

        self.import_TrustBeamCentre.setText(
            _translate("Xia2Options", "Trust beam centre")
        )
        self.import_TrustBeamCentre.setStatusTip(
            _translate(
                "Xia2Options", "Trust the beam centre in the headers, do not refine"
            )
        )
        self.import_DD.setText(_translate("Xia2Options", "Detector Distance"))
        self.import_DD.setStatusTip(
            _translate(
                "Xia2Options", "Override the detector distance from the image header"
            )
        )
        self.import_BeamCentre.setText(_translate("Xia2Options", "Beam Centre"))
        self.import_BeamCentre.setStatusTip(
            _translate("Xia2Options", "Override the beam centre from the image headers")
        )
        self.import_BeamCentre_X_label.setText(_translate("Xia2Options", "X"))
        self.import_BeamCentre_Y_label.setText(_translate("Xia2Options", "Y"))
        self.import_ReferenceGeometry.setText(
            _translate("Xia2Options", "Reference Geometry")
        )
        self.import_ReferenceGeometry.setStatusTip(
            _translate(
                "Xia2Options", "Experimental geometry from the models selected (.expt)"
            )
        )
        self.import_ReferenceGeometry_path.setText(
            _translate("Xia2Options", "Path/To/instrumentModdel.expt")
        )
        self.import_ReferenceGeometry_browse.setText(
            _translate("Xia2Options", "Browse")
        )
        self.import_Wavelengh.setText(_translate("Xia2Options", "Wavelength"))
        self.import_Wavelengh.setStatusTip(
            _translate("Xia2Options", "Override the beam wavelength")
        )
        self.Import_FixBeamDetector_checkBox.setText(
            _translate("Xia2Options", "Fix instrument model")
        )
        self.Import_RunSelector_checkBox.setText(
            _translate("Xia2Options", "Run Select")
        )
        self.Import_RunSelector_checkBox_1.setText(_translate("Xia2Options", "1"))
        self.Import_RunSelector_checkBox_2.setText(_translate("Xia2Options", "2"))
        self.Import_RunSelector_checkBox_3.setText(_translate("Xia2Options", "3"))
        self.Import_RunSelector_checkBox_4.setText(_translate("Xia2Options", "4"))
        self.Import_RunSelector_checkBox_5.setText(_translate("Xia2Options", "5"))
        self.Import_RunSelector_checkBox_6.setText(_translate("Xia2Options", "6"))
        self.Import_RunSelector_checkBox_7.setText(_translate("Xia2Options", "7"))
        self.Import_RunSelector_checkBox_8.setText(_translate("Xia2Options", "8"))
        self.Import_RunSelector_checkBox_9.setText(_translate("Xia2Options", "9"))
        self.Import_RunSelector_checkBox_10.setText(_translate("Xia2Options", "10"))
        self.Import_RunSelector_checkBox_11.setText(_translate("Xia2Options", "11"))
        self.Import_RunSelector_checkBox_12.setText(_translate("Xia2Options", "12"))

        self.Import_type_checkBox.setText(_translate("Xia2Options", "method"))
        self.Import_type_checkBox.setStatusTip(
            _translate("Xia2Options", "Different indexing algorithms for indexing.")
        )
        self.Import_type_comboBox.setItemText(0, _translate("Xia2Options", "Chemical"))
        self.Import_type_comboBox.setItemText(1, _translate("Xia2Options", "Protein"))

        self.xia2options.setTabText(
            self.xia2options.indexOf(self.xia2options_Import),
            _translate("Xia2Options", "Import"),
        )

        self.findSpots_sigmaStrong.setStatusTip(
            _translate(
                "Xia2Options",
                "Area above which the pixel will be classified as strong.",
            )
        )
        self.findSpots_sigmaStrong.setText(_translate("Xia2Options", "sigma_strong"))
        self.findSpots_minSpot.setStatusTip(
            _translate(
                "Xia2Options",
                "The minimum number of contiguous pixels for a spot to be accepted by the filtering algorithm.",
            )
        )
        self.findSpots_minSpot.setText(_translate("Xia2Options", "min spot size"))
        self.findSpots_maxSpot.setStatusTip(
            _translate(
                "Xia2Options",
                "The minimum number of contiguous pixels for a spot to be accepted by the filtering algorithm.",
            )
        )
        self.findSpots_maxSpot.setText(_translate("Xia2Options", "max spot size"))
        self.findSpots_dmin.setStatusTip(
            _translate(
                "Xia2Options",
                "The high resolution limit in Angstrom for a pixel to be accepted by the filtering algorithm.",
            )
        )
        self.findSpots_dmin.setText(_translate("Xia2Options", "d min"))
        self.findSpots_dmax.setStatusTip(
            _translate(
                "Xia2Options",
                "The low resolution limit in Angstrom for a pixel to be accepted by the filtering algorithm.",
            )
        )
        self.findSpots_dmax.setText(_translate("Xia2Options", "d max"))
        self.findSpots_iceRings.setStatusTip(
            _translate("Xia2Options", "Mask to remove spots from ice rings")
        )
        self.findSpots_iceRings.setText(_translate("Xia2Options", "ice rings"))
        self.findSpots_powderRings.setStatusTip(
            _translate(
                "Xia2Options",
                "Generates a powder mask for given unit cell and space group input, reflections under with mask will not be used",
            )
        )
        self.findSpots_powderRings.setText(_translate("Xia2Options", "powder rings"))
        self.findSpots_powderRingsUC_label.setText(
            _translate("Xia2Options", "Unit Cell")
        )
        self.findSpots_powderRingsSG_label.setText(
            _translate("Xia2Options", "Space Group")
        )
        self.findSpots_powderRingsW_label.setText(_translate("Xia2Options", "width"))
        self.findSpots_resolutionRange.setStatusTip(
            _translate(
                "Xia2Options",
                "Generates a mask between the given resolutions, reflections under with mask will not be used",
            )
        )
        self.findSpots_resolutionRange.setText(
            _translate("Xia2Options", "resolution range")
        )
        self.findSpots_circleMask.setStatusTip(
            _translate(
                "Xia2Options",
                "Generates a circular mask, reflections under with mask will not be used",
            )
        )
        self.findSpots_circleMask.setText(_translate("Xia2Options", "Circle mask"))
        self.findSpots_recMask.setStatusTip(
            _translate(
                "Xia2Options",
                "Generates a rectangle mask, reflections under with mask will not be used",
            )
        )
        self.findSpots_recMask.setText(_translate("Xia2Options", "Rectangle mask"))

        self.Index_method_checkBox.setText(_translate("Xia2Options", "method"))
        self.Index_method_checkBox.setStatusTip(
            _translate("Xia2Options", "Different indexing algorithms for indexing.")
        )
        self.Index_method_comboBox.setItemText(0, _translate("Xia2Options", "fft1d"))
        self.Index_method_comboBox.setItemText(1, _translate("Xia2Options", "fft3d"))
        self.Index_method_comboBox.setItemText(
            2, _translate("Xia2Options", "real_space_grid_search")
        )
        self.Index_method_comboBox.setItemText(
            3, _translate("Xia2Options", "low_res_spot_match")
        )
        self.Index_scanVarying_checkBox.setText(
            _translate("Xia2Options", "scan varying off")
        )
        self.Index_scanVarying_checkBox.setStatusTip(
            _translate("Xia2Options", "Does not allows models to vary during a scan.")
        )
        self.Index_UN_SG_checkBox.setText(
            _translate("Xia2Options", "Unit Cell and Space Group")
        )
        self.Index_UN_SG_checkBox.setStatusTip(
            _translate(
                "Xia2Options",
                "User input of known unit cell and space group (must provide both).",
            )
        )
        self.Index_UN_label.setText(_translate("Xia2Options", "Unit Cell"))
        self.Index_SG_label.setText(_translate("Xia2Options", "Space Group"))
        self.Index_minCell_checkBox.setText(
            _translate("Xia2Options", "minimium cell length")
        )
        self.Index_minCell_checkBox.setStatusTip(
            _translate("Xia2Options", "Minimum unit cell volume (in Angstrom^3).")
        )
        self.Index_maxCell_checkBox.setText(
            _translate("Xia2Options", "maximium cell length")
        )
        self.Index_maxCell_checkBox.setStatusTip(
            _translate(
                "Xia2Options",
                "Maximum length of candidate unit cell basis vectors (in Angstrom).",
            )
        )
        self.Index_multiprocessing_checkBox.setText(
            _translate("Xia2Options", "Multi sweep indexing")
        )
        self.Index_multiprocessing_checkBox.setStatusTip(
            _translate("Xia2Options", "Index and process each run individually.")
        )
        self.Index_multiSweepRefine_checkBox.setText(
            _translate("Xia2Options", "Multi sweep refine")
        )
        self.Index_multiSweepRefine_checkBox.setStatusTip(
            _translate("Xia2Options", "Refine and process each run individually.")
        )
        self.Index_outliers_checkBox.setText(
            _translate("Xia2Options", "Include outliers")
        )
        self.Index_outliers_checkBox.setStatusTip(
            _translate(
                "Xia2Options", "Included all spots from spot finding (no rejection)."
            )
        )

        self.Integrate_keepAllReflections_checkBox.setText(
            _translate("Xia2Options", "Keep all reflections")
        )
        self.Integrate_keepAllReflections_checkBox.setStatusTip(
            _translate(
                "Xia2Options",
                "Will add a max resolution cutoff on individual runs based on cc-half.",
            )
        )
        self.Integrate_scanVarying_checkBox.setText(
            _translate("Xia2Options", "Scan Varying Off")
        )
        self.Integrate_scanVarying_checkBox.setStatusTip(
            _translate("Xia2Options", "Does not allows models to vary during a scan.")
        )

        self.Integrate_minSpotProfile_checkBox.setText(
            _translate("Xia2Options", "Min Spots profiles")
        )
        self.Integrate_minSpotProfile_checkBox.setStatusTip(
            _translate(
                "Xia2Options",
                "The minimum number of spots needed to do the profile moddeling",
            )
        )

        self.Integrate_minCellOverall_label.setText(
            _translate("Xia2Options", "Overall")
        )
        self.Integrate_minCellOverall_label.setStatusTip(
            _translate(
                "Xia2Options",
                "The minimum number of spots needed to do the profile moddel per overall.",
            )
        )
        self.Integrate_minCellDegree_label.setText(
            _translate("Xia2Options", "Per degree")
        )
        self.Integrate_minCellDegree_label.setStatusTip(
            _translate(
                "Xia2Options",
                "The minimum number of spots needed to do the profile moddel per degree.",
            )
        )

        self.Refine_FixBeamDetector_checkBox.setText(
            _translate("Xia2Options", "Fix instrument model")
        )
        self.Refine_FixBeamDetector_checkBox.setStatusTip(
            _translate(
                "Xia2Options",
                "Will fix beam, detector and goniometer parameters during refinment.",
            )
        )

        self.Refine_method_checkBox.setText(_translate("Xia2Options", "scaling method"))
        self.Refine_method_checkBox.setStatusTip(
            _translate("Xia2Options", "Algorithm used during scaling.")
        )
        self.Refine_method_comboBox.setItemText(0, _translate("Xia2Options", "dials"))
        self.Refine_method_comboBox.setItemText(
            1, _translate("Xia2Options", "dials-aimless")
        )

        self.Other_failover_checkBox.setText(_translate("Xia2Options", "Failover"))
        self.Other_failover_checkBox.setStatusTip(
            _translate(
                "Xia2Options",
                "Will proceed with processing even if a single scan fails.",
            )
        )

        self.Other_manualInput1_checkBox.setText(
            _translate("Xia2Options", "Manual Input 1")
        )
        self.Other_manualInput1_checkBox.setStatusTip(
            _translate("Xia2Options", "Manual input of xia command.")
        )
        self.Other_manualInput2_checkBox.setText(
            _translate("Xia2Options", "Manual Input 2")
        )
        self.Other_manualInput2_checkBox.setStatusTip(
            _translate("Xia2Options", "Manual input of xia command.")
        )
        self.Other_manualInput3_checkBox.setText(
            _translate("Xia2Options", "Manual Input 3")
        )
        self.Other_manualInput3_checkBox.setStatusTip(
            _translate("Xia2Options", "Manual input of xia command.")
        )
        self.Other_manualInput4_checkBox.setText(
            _translate("Xia2Options", "Manual Input 4")
        )
        self.Other_manualInput4_checkBox.setStatusTip(
            _translate("Xia2Options", "Manual input of xia command.")
        )

        self.Other_clusterOrLocal_label.setText(
            _translate("Xia2Options", "Processing computer")
        )
        self.Other_clusterOrLocal_label.setStatusTip(
            _translate(
                "Xia2Options", "Pick if the processing is local or on a cluster node."
            )
        )
        self.Other_clusterOrLocal_comboBox.setItemText(
            0, _translate("Xia2Options", "Cluster")
        )
        self.Other_clusterOrLocal_comboBox.setItemText(
            1, _translate("Xia2Options", "Local")
        )

        self.ALL_plainTextEdit.setPlainText(
            _translate(
                "Xia2Options",
                "Plan to automatically generate a list of all options from the xia2-working.phil file. ",
            )
        )

        self.HP_correction_shaddowing_checkBox.setText(
            _translate("Xia2Options", "High pressure correction and dynamic shadowing")
        )
        self.HP_correction_shaddowing_checkBox.setStatusTip(
            _translate(
                "Xia2Options",
                "Select this option to mask part of the image shaddowed by the cell and apply correction for beam going through diamonds",
            )
        )
        self.HP_scanVarying_checkBox.setText(
            _translate("Xia2Options", "Scan varying off")
        )
        self.HP_scanVarying_checkBox.setStatusTip(
            _translate("Xia2Options", "Does not allows models to vary during a scan.")
        )
        self.HP_ReferenceGeometry_checkBox.setText(
            _translate("Xia2Options", "Reference Geometry")
        )
        self.HP_ReferenceGeometry_checkBox.setStatusTip(
            _translate(
                "Xia2Options",
                "Add starting instrument model from test crystal (/dls/i19-2/data/2020/visit/dataset/DataFiles/*.expt",
            )
        )

        self.HP_ReferenceGeometry_path.setText(
            _translate("Xia2Options", "Path/To/instrumentModdel.expt")
        )
        self.HP_ReferenceGeometry_browse.setText(_translate("Xia2Options", "Browse"))
        self.HP_gasket_checkBox.setText(_translate("Xia2Options", "Gasket"))
        self.HP_gasket_checkBox.setStatusTip(
            _translate(
                "Xia2Options", "Generate masks for powder rings from gasket material"
            )
        )
        self.HP_gasket_comboBox.setItemText(0, _translate("Xia2Options", "Tungsten"))
        self.HP_gasket_comboBox.setItemText(1, _translate("Xia2Options", "Steel"))
        self.HP_gasket_comboBox.setStatusTip(
            _translate("Xia2Options", "Select gasket material")
        )
        self.HP_gasketUser_checkBox.setText(
            _translate("Xia2Options", "Gasket (user defined)")
        )
        self.HP_gasketUser_checkBox.setStatusTip(
            _translate(
                "Xia2Options",
                "Generate masks for powder rings from gasket, user defined material",
            )
        )
        self.HP_gasketUserW_label.setText(_translate("Xia2Options", "Width"))
        self.HP_gasketUserSG_label.setText(_translate("Xia2Options", "Space Group"))
        self.HP_gasketUserUC_label.setText(_translate("Xia2Options", "Unit Cell"))
        self.HP_FixBeamDetector_checkBox.setText(
            _translate("Xia2Options", "Fix instrument model")
        )
        self.HP_FixBeamDetector_checkBox.setStatusTip(
            _translate(
                "Xia2Options",
                "Will fix the beam and diffractometer varibles during intergration",
            )
        )
        self.HP_dmin_checkBox.setStatusTip(
            _translate(
                "Xia2Options",
                "Area above which the pixel will be classified as strong. The number of standard deviations above the mean in the local, float",
            )
        )
        self.HP_dmin_checkBox.setText(_translate("Xia2Options", "d min"))
        self.HP_UN_label.setText(_translate("Xia2Options", "Unit Cell"))
        self.HP_UN_SG_checkBox.setText(
            _translate("Xia2Options", "Unit Cell and Space Group")
        )
        self.HP_UN_SG_checkBox.setStatusTip(
            _translate(
                "Xia2Options",
                "User input of known unit cell and space group (must provide both).",
            )
        )
        self.HP_SG_label.setText(_translate("Xia2Options", "Space Group"))
        self.HP_difficulty_label_2.setText(
            _translate("Xia2Options", "medium difficulty options")
        )
        self.HP_difficulty_label_3.setText(
            _translate("Xia2Options", "probmatic data options")
        )
        self.HP_difficulty_label_1.setText(
            _translate("Xia2Options", "startard options")
        )
        self.HP_runStartEnd_checkBox.setStatusTip(
            _translate(
                "Xia2Options",
                "Set the start/end images that each run will processed (remove images with additional cell body powder rings)",
            )
        )
        self.HP_runStartEnd_checkBox.setText(_translate("Xia2Options", "Run start/end"))
        self.HP_runStartEnd_label_1.setText(_translate("Xia2Options", "r1"))
        self.HP_runStartEnd_label_2.setText(_translate("Xia2Options", "r2"))
        self.HP_runStartEnd_label_3.setText(_translate("Xia2Options", "r4"))
        self.HP_runStartEnd_label_4.setText(_translate("Xia2Options", "r3"))
        self.HP_runStartEnd_label_5.setText(_translate("Xia2Options", "r5"))
        self.HP_runStartEnd_label_7.setText(_translate("Xia2Options", "r7"))
        self.HP_runStartEnd_label_6.setText(_translate("Xia2Options", "r6"))
        self.HP_runStartEnd_label_8.setText(_translate("Xia2Options", "r8"))
        self.HP_runStartEnd_label_9.setText(_translate("Xia2Options", "r9"))
        self.HP_runStartEnd_label_10.setText(_translate("Xia2Options", "r10"))

        self.HP_anvilThickness_checkBox.setText(
            _translate("Xia2Options", "Anvil Thickness")
        )
        self.HP_anvilThickness_checkBox.setStatusTip(
            _translate("Xia2Options", "Set DAC anvil thickness. Default: 1.5925 mm")
        )
        self.HP_anvilOpeningAngle_checkBox.setText(
            _translate("Xia2Options", "Anvil Opening Angle")
        )
        self.HP_anvilOpeningAngle_checkBox.setStatusTip(
            _translate("Xia2Options", "Set DAC anvil thickness. Default: 40 deg")
        )

        self.xia2options.setTabText(
            self.xia2options.indexOf(self.xia2options_SpotFinding),
            _translate("Xia2Options", "Spot Finding"),
        )
        self.xia2options.setTabText(
            self.xia2options.indexOf(self.xia2options_Indexing),
            _translate("Xia2Options", "Indexing"),
        )
        self.xia2options.setTabText(
            self.xia2options.indexOf(self.xia2options_integrate),
            _translate("Xia2Options", "Integrate"),
        )
        self.xia2options.setTabText(
            self.xia2options.indexOf(self.xia2options_refine_scale),
            _translate("Xia2Options", "Refine/Scale"),
        )
        self.xia2options.setTabText(
            self.xia2options.indexOf(self.xia2options_Other),
            _translate("Xia2Options", "Other"),
        )
        self.xia2options.setTabText(
            self.xia2options.indexOf(self.xia2options_ALL),
            _translate("Xia2Options", "ALL"),
        )
        self.xia2options.setTabText(
            self.xia2options.indexOf(self.xia2options_HP),
            _translate("Xia2Options", "HP"),
        )


###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # QApplication.setOverrideCursor(Qt.WaitCursor)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
