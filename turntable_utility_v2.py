import maya.cmds as cmds
import os
import run_v2 as runV2

def main_utility(rotation_selected, rotate_value, axis_value, data_list_0, data_list_1, fnames, output_path):
    print("nabtew")
    if not rotation_selected[0]:
        camRO_set_keyframe(rotation_selected[1], rotate_value, axis_value)
        render(fnames, data_list_0, data_list_1, output_path, rotate_value)
        clear_all_trans_camera(rotation_selected[1])

    else:
        camRO_set_keyframe(rotation_selected[0][0], rotate_value, axis_value)
        render(fnames, data_list_0, data_list_1, output_path, rotate_value)
        clear_all_trans_model((rotation_selected[0])[1], (rotation_selected[0])[0], rotation_selected[1])

def selected_model():
    try:
        if cmds.ls(sl=True):
            first_selected = cmds.ls(sl=True)
            name_Gmodel = "Nab_obj_group"
            cmds.group(first_selected, name = name_Gmodel)
            cmds.select(d=True)
            return name_Gmodel, first_selected # return the user's models        
        
        else :
            print({"error: pls select your model"})

    
    except Exception as e: # if this function has an error, return error result
        return {"error": str(e)}
    
def create_cam():
    creat_camera = cmds.duplicate ('persp', smartTransform = True)
    cmds.showHidden (creat_camera, a = True)
    name_Gcam = "Nab_cam_group"
    group_cam = cmds.group(creat_camera, name = name_Gcam)
    cmds.lookThru(group_cam)
    cmds.xform(group_cam, piv=[0, 0, 0], ws=True)
    return name_Gcam

def parent_func(parent_A, parent_B):
    cmds.parent(parent_A, parent_B)

def get_filePath():
    output_path = str(cmds.fileDialog2(fileMode=3, dialogStyle=2, okCaption="Select")[0])
    return output_path

def render(fnames, data_list_0, data_list_1, output_path, rotate_value):
    fps_get = cmds.currentTime( '1sec', edit=True ) #check fps

    for Fname in fnames:
        newpath = os.path.join(output_path, Fname)

        if os.path.exists(newpath):
            dialog = runV2.FileExistsDialog()
            dialog.exec_()

            if dialog.data == "increment":
                newpath = get_incremented_filename(output_path, Fname)
            elif dialog.data == "overwrite":
                pass
            elif dialog.data == "cancel":
                print("Operation canceled by user.")
                return
        
        else:
            if not os.path.exists(newpath):
                os.makedirs(newpath, exist_ok=True)

        cmds.playblast(filename="{}/{}".format(newpath, Fname), clearCache=True, viewer=False, format=data_list_0, compression=data_list_1, sequenceTime=True, forceOverwrite=True, fr=[0, rotate_value * fps_get], fp=0, v=False, os=True)

def get_incremented_filename(output_path, Fname):
    base, extension = os.path.splitext(Fname)
    counter = 1
    while True:
        new_filename = f"{base}_{counter}{extension}"
        newpath = os.path.join(output_path, new_filename)
        if not os.path.exists(newpath):
            return newpath
        counter += 1

"""for Fname in fnames: # fnames return a_wireframe
        print("fnames" ,fnames)
        print("outpute", output_path)
        sf_command = ""
        if Fname.split("_")[-1] == "wireframe":
            dp_wireframe()

        elif Fname.split("_")[-1] == "smoothShade":
            dp_smooth_shade_all()

        elif Fname.split("_")[-1] == "wireframeOnShade":
            dp_wireframe_onShade()

        dir_list = os.listdir(output_path)
        if dir_list:
            for i in dir_list:
                file_name = os.path.basename(i) #return /hh_1
                print("file_name" ,file_name)
                if file_name == Fname:
                    sf_command = runV2.overwrite()
                else:
                    sf_command = "Oop_pass"

                    if sf_command == "Oop_pass":
                        newpath = os.path.join(output_path, Fname)

                        if not os.path.exists(newpath):
                            os.makedirs(newpath, exist_ok=True)

                        cmds.playblast(filename="{}/{}".format(newpath,Fname), clearCache=True, viewer=False, format=data_list_0, compression=data_list_1, sequenceTime=True, forceOverwrite=True, fr=[0,rotate_value*fps_get], fp=0, v=False, os=True)
        
                    elif sf_command == "increment":
                        newpath = get_incremented_filename(output_path,Fname)
                        cmds.playblast(filename="{}/{}".format(newpath,Fname), clearCache=True, viewer=False, format=data_list_0, compression=data_list_1, sequenceTime=True, forceOverwrite=True, fr=[0,rotate_value*fps_get], fp=0, v=False, os=True)

                    elif sf_command == "overwritten":
                        newpath = os.path.join(output_path, Fname)

                        if not os.path.exists(newpath):
                            os.makedirs(newpath, exist_ok=True)

                        cmds.playblast(filename="{}/{}".format(newpath,Fname), clearCache=True, viewer=False, format=data_list_0, compression=data_list_1, sequenceTime=True, forceOverwrite=True, fr=[0,rotate_value*fps_get], fp=0, v=False, os=True)
        
                    else:
                        print("error: cancle")

        else:
            sf_command = "Oop_pass"

        print("sf_command", sf_command)

        if sf_command == "Oop_pass":
            newpath = os.path.join(output_path, Fname)

            if not os.path.exists(newpath):
                os.makedirs(newpath, exist_ok=True)

            cmds.playblast(filename="{}/{}".format(newpath,Fname), clearCache=True, viewer=False, format=data_list_0, compression=data_list_1, sequenceTime=True, forceOverwrite=True, fr=[0,rotate_value*fps_get], fp=0, v=False, os=True)
        
        elif sf_command == "increment":
            newpath = get_incremented_filename(output_path,Fname)
            cmds.playblast(filename="{}/{}".format(newpath,Fname), clearCache=True, viewer=False, format=data_list_0, compression=data_list_1, sequenceTime=True, forceOverwrite=True, fr=[0,rotate_value*fps_get], fp=0, v=False, os=True)

        elif sf_command == "overwritten":
            newpath = os.path.join(output_path, Fname)

            if not os.path.exists(newpath):
                os.makedirs(newpath, exist_ok=True)

            cmds.playblast(filename="{}/{}".format(newpath,Fname), clearCache=True, viewer=False, format=data_list_0, compression=data_list_1, sequenceTime=True, forceOverwrite=True, fr=[0,rotate_value*fps_get], fp=0, v=False, os=True)
        
        else:
            print("error: cancle")

    dir_list = os.listdir(output_path)
          fps_get = cmds.currentTime( '1sec', edit=True ) #check fps

    for Fname in fnames:
        if Fname.split("_")[-1] == "wireframe":
            dp_wireframe()

        elif Fname.split("_")[-1] == "smoothShade":
            dp_smooth_shade_all()

        elif Fname.split("_")[-1] == "wireframeOnShade":
            dp_wireframe_onShade()

        if dir_list:
            for i in dir_list:
                print("alresdy_fileNamed")
                file_name = os.path.basename(i)
                if file_name.split("_")[0] == Fname.split("_")[0]:
                    user_fileManage = runV2.overwrite()
                    if user_fileManage == "increment":
                        newpath = get_incremented_filename(i)
                        cmds.playblast(filename="{}/{}".format(newpath,Fname), clearCache=True, viewer=False, format=data_list_0, compression=data_list_1, sequenceTime=True, forceOverwrite=True, fr=[0,rotate_value*fps_get], fp=0, v=False, os=True)

                    elif user_fileManage == "overwritten":
                        newpath = os.path.join(i, Fname)
                        if not os.path.exists(newpath):
                            os.makedirs(newpath, exist_ok=True)
                        cmds.playblast(filename="{}/{}".format(newpath,Fname), clearCache=True, viewer=False, format=data_list_0, compression=data_list_1, sequenceTime=True, forceOverwrite=True, fr=[0,rotate_value*fps_get], fp=0, v=False, os=True)

                    elif user_fileManage == "cancle":
                        print("cancle")

                else:
                    newpath = os.path.join(output_path, Fname)
                    if not os.path.exists(newpath):
                        os.makedirs(newpath, exist_ok=True)
                    cmds.playblast(filename="{}/{}".format(newpath,Fname), clearCache=True, viewer=False, format=data_list_0, compression=data_list_1, sequenceTime=True, forceOverwrite=True, fr=[0,rotate_value*fps_get], fp=0, v=False, os=True)
        else:
            print("nahhAlresdy_fileNamed")
            newpath = os.path.join(output_path, Fname)
            if not os.path.exists(newpath):
                os.makedirs(newpath, exist_ok=True)
            cmds.playblast(filename="{}/{}".format(newpath,Fname), clearCache=True, viewer=False, format=data_list_0, compression=data_list_1, sequenceTime=True, forceOverwrite=True, fr=[0,rotate_value*fps_get], fp=0, v=False, os=True)"""

"""def get_incremented_filename(output_path, Fname):
    print(output_path)
    newpath = os.path.join(output_path, Fname)
    base, extension = os.path.splitext(newpath)
    counter = 1
    if '_' in base and base.split('_')[-1].isdigit():
        base, counter = base.rsplit('_', 1)
        counter = int(counter) + 1
    else:
        base = base
        counter = 1

    new_filepath = f"{base}_{counter}{extension}"
    
    while os.path.exists(new_filepath):
        counter += 1
        new_filepath = f"{base}_{counter}{extension}"

    if not os.path.exists(new_filepath):
        os.makedirs(new_filepath, exist_ok=True)
    
    return new_filepath"""



def camRO_set_keyframe(rotation_selected_A, rotate_value, axis_value):
    cmds.select(rotation_selected_A, r=True)
    cmds.currentTime(0)
    cmds.setKeyframe(attribute='rotateY')
    cmds.currentTime(rotate_value)
    cmds.setAttr('{}.rotateY'.format(rotation_selected_A), axis_value)
    cmds.setKeyframe(attribute='rotateY', t=["{}.sec".format(rotate_value)])
    cmds.currentTime(0)

def dp_wireframe():
    cmds.modelEditor("modelPanel4", e=True, da="smoothShaded", displayTextures=False, wos=False)
    cmds.modelEditor("modelPanel4", e=True, da="wireframe")

def dp_smooth_shade_all():
    cmds.modelEditor("modelPanel4", e=True, da="smoothShaded", displayTextures=False, wos=False)
    cmds.modelEditor("modelPanel4", e=True, displayTextures=True)

def dp_wireframe_onShade():
    cmds.modelEditor("modelPanel4", e=True, da="smoothShaded", displayTextures=False, wos=False)
    cmds.modelEditor("modelPanel4", e=True, wos=True)

def clear_all_trans_camera(firstSelected_B):
    #cmds.modelEditor(name_Gcam, e=True, wos=True)
    cmds.lookThru("perspView", "modelPanel4", q=True)
    cmds.delete(firstSelected_B)
    print("cleared")

def clear_all_trans_model(firstSelected_A, firstSelected_B, name_Gcam):
    #cmds.modelEditor(name_Gcam, e=True, wos=True)
    cmds.parent(firstSelected_A, w=True)
    cmds.lookThru("perspView", "modelPanel4", q=True)
    cmds.delete(firstSelected_B, name_Gcam)
    print("cleared")

"""def pb_render(data_list_0, file_named, data_list_1):
    cmds.playblast(filename="{}".format(file_named), clearCache=True, viewer=False, format=data_list_0, compression=data_list_1, sequenceTime=True, forceOverwrite=True)"""
