from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
from  PySide2 import QtUiTools
import os 
import sys
import turntable_icons #icons ไฟล์
import turntable_utility_v2 as uti
from importlib import reload
import maya.OpenMaya as om
reload (uti)

moduleDir = os.path.dirname(sys.modules[__name__].__file__)
maya_ptr = omui.MQtUtil.mainWindow()
ptr = wrapInstance(int(maya_ptr), QWidget)
myUiFile = "%s\\turntable.ui" %moduleDir
widgetUiFile = "%s\\Help!.ui" %moduleDir
OopUiFile = "%s\\Oop!.ui" %moduleDir

def setup_ui_maya(uiFile, parent): #Qt Module to load .ui file
    # read .ui directly
    moduleDir = os.path.dirname(uiFile)
    loader = QtUiTools.QUiLoader()
    loader.setWorkingDirectory(moduleDir)

    f = QFile(uiFile)
    f.open(QFile.ReadOnly)

    myWidget = loader.load(f, parent)
    f.close()

    return myWidget

mainUi = setup_ui_maya(myUiFile, ptr)
oopUi = setup_ui_maya(OopUiFile, ptr)
    # Directory of your .ui file

def run():
    global mainUi
    try:
        mainUi.close()
    except:
        pass

    mainUi.show()

def isCheck_func():
    rotation_selected = ""
    camera_selected = ""
    try:
        if mainUi.modelChoose_button.isChecked():
            rotation_selected = uti.selected_model()
            camera_selected = uti.create_cam()

        elif mainUi.camChoose_button.isChecked():
            camera_selected = uti.create_cam()

        else :
            print("error: plsss select the button")

        return rotation_selected, camera_selected
    
    except: 
        print("error: isCheck_func is error")

def user_file_named():
    named_file = ""
    if mainUi.typeName_box.text():
        named_file = mainUi.typeName_box.text()
    else :
        named_file = "playblast"
    return named_file

def rotations_per_cycle():
    rotate_value = mainUi.sNum_button.value()
    return rotate_value

def rotations_axis():
    axis_value = ""
    if mainUi.clockwise_button.isChecked():
        axis_value = 360

    elif mainUi.antiClockwise_button.isChecked():
        axis_value = -360

    return axis_value

def check_file_format():
    data_list = []
    set_format = ""
    set_compression = ""
    if mainUi.formatChoose_button.currentIndex() == 0:
        set_format = "avi"
        set_compression = "none"

    else:
        set_format = "image"
        set_compression = mainUi.formatChoose_button.currentText()

    data_list.append(set_format)
    data_list.append(set_compression)
    print(data_list)
    return data_list

def check_displayMode():
    display_check = 0
    checked_mode = []
    
    if mainUi.Cwireframe_button.isChecked():
        display_check += 1
        checked_mode.append('wireframe')

    if mainUi.CShaded_button.isChecked():
        display_check += 1
        checked_mode.append('smoothShade')

    if mainUi.CwireShade_button.isChecked():
        display_check += 1
        checked_mode.append('wireframeOnShade')

    file_named = []
    if display_check > 0:
        for item in checked_mode:
            named_file = ""
            if mainUi.typeName_box.text():
                named_file = "{}_{}".format(mainUi.typeName_box.text(), item)
            else :
                named_file = "playblast_{}".format(item)

            file_named.append(named_file)
    else:
        print("error: plss select Display Mode")
    print(file_named)
    return file_named

def overwrite():
    file_dialog = FileExistsDialog()
    show_dialog()
    resource = file_dialog.file_existsDialog()
    print("resource", resource)
    return resource

class FileExistsDialog(QDialog):
    def __init__(self, parent = ptr):
        super(FileExistsDialog, self).__init__()
        self.setFixedSize(QSize(400, 106))
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.setWindowTitle("file already exists")

        self.main_label = QLabel("Ohhh Nooo!!! file already exists, plss choose one :)")
        self.button_layout = QHBoxLayout()
        self.increment_button = QPushButton("save increment")
        self.overwritten_button = QPushButton("overwritten")
        self.cancle_button = QPushButton("cancle")

        self.increment_button.clicked.connect(self.file_existsDialog)
        self.overwritten_button.clicked.connect(self.file_existsDialog)
        self.cancle_button.clicked.connect(self.file_existsDialog)

        self.button_layout.addWidget(self.increment_button)
        self.button_layout.addWidget(self.overwritten_button)
        self.button_layout.addWidget(self.cancle_button)

        self.main_layout.addWidget(self.main_label)
        self.main_layout.addLayout(self.button_layout)
        self.data = ""

    """def self_show(self):
        global ui_miniwindow
        try:
            ui_miniwindow.close()
        except:
            pass

        ui_miniwindow = FileExistsDialog(parent=ptr)
        ui_miniwindow.show()"""

    def file_existsDialog(self):
        clicked_button = self.sender()

        if clicked_button == self.increment_button:
            self.data = "increment"
            self.close()

        elif clicked_button == self.overwritten_button:
            self.data = "overwritten"
            self.close()

        elif clicked_button == self.cancle_button:
            self.data = "cancle"
            self.close()
            
def show_dialog():
    global ui_miniwindow
    try:
        ui_miniwindow.close()
    except:
        pass

    ui_miniwindow = FileExistsDialog(parent=ptr)
    result = ui_miniwindow.exec_()
    ui_miniwindow.show()

def close_oop():
    oopUi.close()

#if user selects button A, deselect button B
def check_select_and_deselect(A_Button, B_button):
    if A_Button.isChecked():
        B_button.setChecked(False)

def file_location():
    filePath = uti.get_filePath()
    mainUi.filePath_box.setText(filePath)

widgetUi = setup_ui_maya(widgetUiFile, ptr)
mainUi.camChoose_button.clicked.connect(lambda: check_select_and_deselect(mainUi.camChoose_button, mainUi.modelChoose_button))
mainUi.modelChoose_button.clicked.connect(lambda: check_select_and_deselect(mainUi.modelChoose_button, mainUi.camChoose_button))
mainUi.clockwise_button.clicked.connect(lambda: check_select_and_deselect(mainUi.clockwise_button, mainUi.antiClockwise_button))
mainUi.antiClockwise_button.clicked.connect(lambda: check_select_and_deselect(mainUi.antiClockwise_button, mainUi.clockwise_button))
mainUi.browse_button.clicked.connect(lambda: file_location())
mainUi.ok_button.clicked.connect(lambda: uti.main_utility(isCheck_func(), rotations_per_cycle(), rotations_axis(), check_file_format()[0], check_file_format()[1], check_displayMode(), mainUi.filePath_box.text()))
mainUi.Q_button.clicked.connect(lambda: widgetUi.show())