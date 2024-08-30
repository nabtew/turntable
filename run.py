from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
from PySide2 import QtUiTools
import os
import sys
import turntable_icons #icons ไฟล์
import turntable_utility as uti 
from importlib import reload #****
import maya.OpenMaya as om
reload (uti)

moduleDir = os.path.dirname(sys.modules[__name__].__file__)
maya_ptr = omui.MQtUtil.mainWindow()
ptr = wrapInstance(int(maya_ptr), QWidget)
myUiFile = '%s\\turntable.ui' %moduleDir
widgetUiFile = '%s\\Help!.ui' %moduleDir
OopUiFile = '%s\\Oop!.ui' %moduleDir #****

def setup_ui_maya(uiFile, parent):
    """Qt Module to load .ui file"""
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
    # Directory of your .ui file

def run():
    global mainUi
    try:
        mainUi.close()
    except:
        pass

    mainUi.show()

def check_selected_rotate_with(a):
    rotation_selected = ""
    if mainUi.modelChoose_button.isChecked():
        rotation_selected = uti.get_selected_model()

    elif mainUi.camChoose_button.isChecked():
        rotation_selected = uti.select_active_camera(a)

    else :
        print("plsss select the rotation with button")

    return rotation_selected

def check_file_format():
    data_list = []
    set_format = ""
    set_compression = ""
    if mainUi.formatChoose_button.currentIndex() == 0 or 3:
        set_format = "movie"
        if mainUi.formatChoose_button.currentIndex() == 0:
            set_compression = "mov"
        
        elif mainUi.formatChoose_button.currentIndex() == 3:
            set_compression = "qt"

        elif mainUi.formatChoose_button.currentIndex() == 1 or 2:
            set_format = "image"

    data_list.append(set_format)
    data_list.append(set_compression)

    return data_list

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

### display mode
def wireframe_checkle():
    if mainUi.Cwireframe_button.isChecked():
        uti.dp_wireframe()

    else :
        pass

def shaded_checkle():
    if mainUi.CShaded_button.isChecked():
        uti.dp_smooth_shade_all()

    else :
        pass

def wireShaded_checkle():
    if mainUi.CwireShade_button.isChecked():
        uti.dp_wireframe_onShade()

    else :
        pass

########
def user_file_named():
    named_file = ""
    if mainUi.typeName_box.text():
        named_file = mainUi.typeName_box.text()
    else :
        named_file = "playblast"
    return named_file

def user_file_path(a):
    path_file = uti.get_filePath(a)
    return path_file

def clockwise_button():
    if mainUi.clockwise_button.isChecked():
        mainUi.antiClockwise_button.setChecked(False)

def antiClockwise_button():
    if mainUi.antiClockwise_button.isChecked():
        mainUi.clockwise_button.setChecked(False)

def camera_retation_button():
    if mainUi.camChoose_button.isChecked():
        mainUi.modelChoose_button.setChecked(False)

def model_selectCam_button():
    if mainUi.modelChoose_button.isChecked():
        mainUi.camChoose_button.setChecked(False)

widgetUi = setup_ui_maya(widgetUiFile, ptr)
mainUi.browse_button.clicked.connect(lambda: user_file_path(user_file_named))
mainUi.clockwise_button.clicked.connect(clockwise_button)
mainUi.antiClockwise_button.clicked.connect(antiClockwise_button)
mainUi.camChoose_button.clicked.connect(camera_retation_button)
mainUi.modelChoose_button.clicked.connect(model_selectCam_button)
mainUi.Cwireframe_button.clicked.connect(wireframe_checkle)
mainUi.CShaded_button.clicked.connect(shaded_checkle)
mainUi.CwireShade_button.clicked.connect(wireShaded_checkle)
mainUi.ok_button.clicked.connect(lambda: uti.main_util(check_selected_rotate_with(uti.select_model), check_file_format, rotations_per_cycle, rotations_axis,  user_file_named))
mainUi.Q_button.clicked.connect(lambda: widgetUi.show())