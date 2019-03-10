# !BPY
# -*- coding: UTF-8 -*-
# Create Folder Tree
#
# Create Objects & Expnasion Motion
#
# 2019.03.12 Natukikazemizo
#

import bpy
import os
import math

# CONSTANT OF PARAMETERS
FOLDER_SPLITTER = "_"
SEED_FOLDER_NAME = 'Folder'
SEED_FILE_NAME = 'File'
ROOT_FOLDER = "C:/SRC/blender"
ROOT_FOLDER_ORG_NAME = "blender-2.79b"
ROOT_FOLDER_SHORT_NAME = "bl"

ACTION_SUFFIX = 'Action'
SEED_ACTION = 'FolderAction'

NEW_FOLDER_NAME = 'Folder_'
FOLDER_ZFILL = 4
NEW_FILE_NAME = 'File_'
FILE_ZFILL = 8

START_FRAME = 1000
FPS = 12
SCALE_STORAGE = 0.5
SCALE_NORMAL = 1.0

FOLDER_X_MARGIN = 0.7
FOLDER_Y_MARGIN = 0.7
FOLDER_Z_MARGIN = 0.48

FOLDER_FRAME_START_MARGIN = 4
FOLDER_FRAME_Z_EXPAND = 12
FOLDER_FRAME_X_EXPAND_WAIT = 4
FOLDER_FRAME_X_EXPAND = 18

FILE_X_MARGIN = 0
FILE_Y_MARGIN = 0.5
FILE_Z_MARGIN = 0.4

FILE_FRAME_START_MARGIN = 4
FILE_FRAME_X_ROT = 8
FILE_FRAME_Y_EXPAND_WAIT = 4
FILE_FRAME_Y_EXPAND = 18

F_CURVE_X_LOC = 0
F_CURVE_Y_LOC = 1
F_CURVE_Z_LOC = 2
F_CURVE_X_ROT = 3
F_CURVE_Y_ROT = 4
F_CURVE_Z_ROT = 5
F_CURVE_X_SCA = 6
F_CURVE_Y_SCA = 7
F_CURVE_Z_SCA = 8


file_parent_dic = {}
folder_pos_dic = {}
folder_num_name_dic = {"":"", ROOT_FOLDER_SHORT_NAME:ROOT_FOLDER_SHORT_NAME}
file_cnt_dic = {}

def get_file_num_name(folder_name):
    folder_num_name = folder_num_name_dic[folder_name]
    file_num_name = NEW_FILE_NAME + folder_num_name[-FOLDER_ZFILL:]
    return file_num_name
    
    

def convert_folder_id(folder):    
    
    ret = folder.replace(ROOT_FOLDER_ORG_NAME, ROOT_FOLDER_SHORT_NAME)
    ret = ret.replace(os.sep, FOLDER_SPLITTER)

    return ret



# get file list
file_list = []
for root, folders, files in os.walk(ROOT_FOLDER):
    root = os.path.relpath(root, ROOT_FOLDER)
    if root == '.': root = ''
    parent_folder = convert_folder_id(root)
    file_list.append([root, sorted(folders), sorted(files), parent_folder])


def print_file(file_name, level_list, last):
    """
    print fileName
    """
    t = ''

    if len(level_list): t += ' '

    if len(level_list) >= 2:
        for b in level_list[1:]:
            if b:
                t += ' '
            else:
                t += '|'

    if len(level_list):
        if last:
            t += '-'
        else:
            t += '+'

    print(t + file_name)

def dupObject(src_name, dup_name):
    """
    duplidate object
    """
    
    if bpy.data.objects.find(dup_name) < 0:
        src_obj = bpy.data.objects[src_name]
        
        # Select object
        bpy.ops.object.select_all(action='DESELECT')
        src_obj.select = True
        
        bpy.ops.object.duplicate(linked=True)
        new_obj = bpy.data.objects[src_name + '.001']
        new_obj.name = dup_name

def create_folder_num_name(folder_name):
    if folder_name not in folder_num_name_dic:
        folder_num_name_dic[folder_name] = NEW_FOLDER_NAME + str(len(folder_num_name_dic) + 1).zfill(FOLDER_ZFILL)
        
def create_action(object_name):
    action_name = object_name + ACTION_SUFFIX
    if bpy.data.actions.find(action_name) < 0:
        new_action = bpy.data.actions[SEED_ACTION].copy()
        new_action.name = action_name
        bpy.data.objects[object_name].animation_data.action = new_action


def create_folder_mesh(parent_folder_name, folder_name):
    """
    create folder mesh
    """
    print("folder:" + folder_name)
    print("parent:" + parent_folder_name)
    
    create_folder_num_name(folder_name)
    
    # duplicate object
    num_name = folder_num_name_dic[folder_name]
    dupObject(SEED_FOLDER_NAME , num_name)
    
    # Enable Render
    bpy.data.objects[num_name].hide_render = False
    
    # Create new Action on new Object
    create_action(num_name)
    
    act = bpy.data.objects[num_name].animation_data.action

    # set start location
    act.fcurves[F_CURVE_X_LOC].keyframe_points[0].co = (1000.0, 0)
    act.fcurves[F_CURVE_Y_LOC].keyframe_points[0].co = (1000.0, 0)
    act.fcurves[F_CURVE_Z_LOC].keyframe_points[0].co = (1000.0, 0)
    
    # set start scale
    act.fcurves[F_CURVE_X_SCA].keyframe_points[0].co = (1000.0, SCALE_STORAGE)
    act.fcurves[F_CURVE_Y_SCA].keyframe_points[0].co = (1000.0, SCALE_STORAGE)
    act.fcurves[F_CURVE_Z_SCA].keyframe_points[0].co = (1000.0, SCALE_STORAGE)

def create_file_mesh(file_name):
    """
    create file mesh
    """

    # delete org
    # Enable hire when you want to delete objects 
    #if bpy.data.objects.find(file_name) > 0:    
    #    bpy.ops.object.select_all(action='DESELECT')
    #    bpy.data.objects[file_name].select = True
    #    bpy.ops.object.delete()
        
    # duplicate object
    dupObject(SEED_FILE_NAME , file_name)
    
    # Enable Render
    bpy.data.objects[file_name].hide_render = False
    
        
    act = bpy.data.objects[file_name].animation_data.action

    # set start location
    act.fcurves[F_CURVE_X_LOC].keyframe_points[0].co = (1000.0, 0)
    act.fcurves[F_CURVE_Y_LOC].keyframe_points[0].co = (1000.0, 0)
    act.fcurves[F_CURVE_Z_LOC].keyframe_points[0].co = (1000.0, 0)

    # set start rotation
    act.fcurves[F_CURVE_X_ROT].keyframe_points[0].co = (1000.0, 0)
    act.fcurves[F_CURVE_Y_ROT].keyframe_points[0].co = (1000.0, 0)
    act.fcurves[F_CURVE_Z_ROT].keyframe_points[0].co = (1000.0, 0)
    
    # set start scale
    act.fcurves[F_CURVE_X_SCA].keyframe_points[0].co = (1000.0, SCALE_STORAGE)
    act.fcurves[F_CURVE_Y_SCA].keyframe_points[0].co = (1000.0, SCALE_STORAGE)
    act.fcurves[F_CURVE_Z_SCA].keyframe_points[0].co = (1000.0, SCALE_STORAGE)
    

def set_obj_parent(parent_name, obj_name):
    """
    set parent on object
    """
    # set parent
    if parent_name != "":
        obj = bpy.data.objects[obj_name]
        
        # set parent
        obj.parent = bpy.data.objects[parent_name]
    

def func_main(arg, level_list):
    """
    MAIN
    """
    root, folders, files, parent_folder = arg

    folder_len = len(folders)
    file_len = len(files)

    # Output subfolder

    for i, folder_name in enumerate(folders):
        nounder = (i == folder_len - 1 and file_len == 0)
        
        folder_id = parent_folder + FOLDER_SPLITTER + folder_name

        create_folder_mesh(parent_folder, folder_id)
        
        print_file('<' + folder_id + '>', level_list, nounder)
        
        folder_pos_dic[folder_id] = (parent_folder, i, len(level_list))

        # Output subfolder's subfolder

        under_root = os.path.join(root, folder_name)
        under_list = []

        for t in file_list:
            if t[0] == under_root:
                under_list.append(t)

        for j, t in enumerate(under_list):
            if nounder and j == len(under_list) - 1:
                add = [True]
            else:
                add = [False]

            func_main(t, level_list + add)
            
    # Output files

    for i, file_name in enumerate(files):
        file_id = parent_folder + FOLDER_SPLITTER + file_name
        print_file(file_id, level_list, (i == file_len - 1))
    
    file_cnt = len(files)    
    if file_cnt > 0:
        file_num_name = get_file_num_name(parent_folder)
        create_file_mesh(file_num_name)
        file_cnt_dic[parent_folder] = (file_num_name, file_cnt)

def setupFolders():

    # reset root folder size
    act = bpy.data.objects[ROOT_FOLDER_SHORT_NAME].animation_data.action
    # set start scale
    act.fcurves[F_CURVE_X_SCA].keyframe_points[0].co = (1000.0, SCALE_NORMAL)
    act.fcurves[F_CURVE_Y_SCA].keyframe_points[0].co = (1000.0, SCALE_NORMAL)
    act.fcurves[F_CURVE_Z_SCA].keyframe_points[0].co = (1000.0, SCALE_NORMAL)


    for folder_name, pos in folder_pos_dic.items():
        
        # Skip root folder
        if folder_name == ROOT_FOLDER_SHORT_NAME:
            continue
        
        parent_folder_name, index, level = pos
        
        # set parent object
        set_obj_parent(folder_num_name_dic[parent_folder_name], folder_num_name_dic[folder_name])
        


def setupFiles():
    for parent_folder, val in file_cnt_dic.items():
        set_obj_parent(folder_num_name_dic[parent_folder], val[0])
        

# START
print("### start ###")
create_folder_mesh("", ROOT_FOLDER_SHORT_NAME)
func_main(file_list.pop(0), [])
setupFolders()
setupFiles()
print("### end ###")
