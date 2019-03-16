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
# DEF FOR TEST
#ROOT_FOLDER = "C:/tmp/folder_tree_test/"
#ROOT_FOLDER_ORG_NAME = "root"
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
FILE_Y_MARGIN = 0.2
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

# Global dic
file_parent_dic = {}
folder_pos_dic = {ROOT_FOLDER_SHORT_NAME:("", 0, 0, 0)}
FOLDER_POS_PARENT_FOLDER_NAME = 0
FOLDER_POS_INDEX = 1
FOLDER_POS_LEVEL = 2
FOLDER_POS_ABSOLUTE_INDEX = 3

folder_num_name_dic = {"":"", ROOT_FOLDER_SHORT_NAME:ROOT_FOLDER_SHORT_NAME}
file_cnt_dic = {}
folder_end_frame_dic = {ROOT_FOLDER_SHORT_NAME:0}

# Global params
folder_absolute_index = 0

# File I/O
FOLDER_LIST_FILE_NAME="FolderList.txt" 
root_path = bpy.path.abspath("//") + "data/"
text_file = open(root_path + FOLDER_LIST_FILE_NAME, mode = 'w')
    

def get_file_num_name(folder_name):
    folder_num_name = folder_num_name_dic[folder_name]
    file_num_name = NEW_FILE_NAME + folder_num_name[-FOLDER_ZFILL:]
    return file_num_name
    
    

def convert_folder_id(folder):    
    
    ret = folder.replace(ROOT_FOLDER_ORG_NAME, ROOT_FOLDER_SHORT_NAME)
    ret = ret.replace(os.sep, FOLDER_SPLITTER)

    return ret

def clear_old_breakpoints(fcurve):
    old_keyframe_index_list = []

    for i, point in enumerate(fcurve.keyframe_points):
        if point.co[0] != START_FRAME:
            old_keyframe_index_list.append(i)

    if len(old_keyframe_index_list) > 0:
        old_keyframe_index_list.reverse()
        for i in old_keyframe_index_list:
            fcurve.keyframe_points.remove(fcurve.keyframe_points[i])
        fcurve.update()

def clear_all_old_breakpoints(fcurves):

    clear_old_breakpoints(fcurves[F_CURVE_X_LOC])
    clear_old_breakpoints(fcurves[F_CURVE_Y_LOC])
    clear_old_breakpoints(fcurves[F_CURVE_Z_LOC])
    clear_old_breakpoints(fcurves[F_CURVE_X_ROT])
    clear_old_breakpoints(fcurves[F_CURVE_Y_ROT])
    clear_old_breakpoints(fcurves[F_CURVE_Z_ROT])
    clear_old_breakpoints(fcurves[F_CURVE_X_SCA])
    clear_old_breakpoints(fcurves[F_CURVE_Y_SCA])
    clear_old_breakpoints(fcurves[F_CURVE_Z_SCA])

def add_location_key_frame(fcurves, frame, x, y, z):
    add_keyframe_point(fcurves[F_CURVE_X_LOC], frame, x)
    add_keyframe_point(fcurves[F_CURVE_Y_LOC], frame, y)
    add_keyframe_point(fcurves[F_CURVE_Z_LOC], frame, z)

def add_rotation_key_rrame(fcurves, frame, x, y, z):
    add_keyframe_point(fcurves[F_CURVE_X_ROT], frame, x)
    add_keyframe_point(fcurves[F_CURVE_Y_ROT], frame, y)
    add_keyframe_point(fcurves[F_CURVE_Z_ROT], frame, z)

def add_scale_key_frame(fcurves, frame, x, y, z):
    add_keyframe_point(fcurves[F_CURVE_X_SCA], frame, x)
    add_keyframe_point(fcurves[F_CURVE_Y_SCA], frame, y)
    add_keyframe_point(fcurves[F_CURVE_Z_SCA], frame, z)


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
    text_file.write(t + file_name + '\n')

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
        folder_num_name_dic[folder_name] = NEW_FOLDER_NAME \
            + str(len(folder_num_name_dic) + 1).zfill(FOLDER_ZFILL)
        
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
    
    
    create_folder_num_name(folder_name)
    
    # duplicate object
    num_name = folder_num_name_dic[folder_name]

    # delete org
    # Enable hire when you want to delete objects 
    #if bpy.data.objects.find(num_name) > 0:    
    #    bpy.ops.object.select_all(action='DESELECT')
    #    bpy.data.objects[num_name].select = True
    #    bpy.ops.object.delete()

    dupObject(SEED_FOLDER_NAME , num_name)
    
    # Enable Render
    bpy.data.objects[num_name].hide_render = False
    
    # Create new Action on new Object
    create_action(num_name)
    
    act = bpy.data.objects[num_name].animation_data.action

    # remove old keyframes
    clear_all_old_breakpoints(act.fcurves)

    # set start location
    add_location_key_frame(act.fcurves, 1000, 0, 0, 0)
    
    # set start scale
    add_scale_key_frame(act.fcurves, 1000, SCALE_STORAGE, SCALE_STORAGE, SCALE_STORAGE)

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

    # Create new Action on new Object
    create_action(file_name)
        
    act = bpy.data.objects[file_name].animation_data.action

    # remove old keyframes
    clear_all_old_breakpoints(act.fcurves)

    # set start location
    add_location_key_frame(act.fcurves, 1000, 0, 0, 0)

    # set start rotation
    add_rotation_key_rrame(act.fcurves, 1000, 0, 0, 0)
    
    # set start scale
    add_scale_key_frame(act.fcurves, 1000, SCALE_STORAGE, SCALE_STORAGE, SCALE_STORAGE)
    

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
    global folder_absolute_index
    root, folders, files, parent_folder = arg

    folder_len = len(folders)
    file_len = len(files)

    # Output subfolder

    for i, folder_name in enumerate(folders):
        nounder = (i == folder_len - 1 and file_len == 0)
        
        
        folder_id = folder_name
        # Replace root folder name to short name
        if folder_id == ROOT_FOLDER_ORG_NAME:
            folder_id = ROOT_FOLDER_SHORT_NAME
            
        if parent_folder != "":
            folder_id = parent_folder + FOLDER_SPLITTER + folder_id

        create_folder_mesh(parent_folder, folder_id)
        print_file('<' + folder_id + '>', level_list, nounder)
        
        folder_pos_dic[folder_id] = (parent_folder, i, len(level_list),  \
            folder_absolute_index)
        folder_absolute_index += 1

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

def add_keyframe_point(fcurve, frame, value):
    
    # find same frame keyframe_point
    index = 0
    find_frame = False
    for i, point in enumerate(fcurve.keyframe_points):
        if point.co[0] == frame:
            index = i
            find_frame = True
            break
    
    if find_frame == False:
        # add keyframe_point when same frame not found
        fcurve.keyframe_points.add(1)
        index = len(fcurve.keyframe_points) - 1

    # setup keyframe        
    fcurve.keyframe_points[index].type =  "BREAKDOWN"
    fcurve.keyframe_points[index].co =  frame, value
    fcurve.keyframe_points[index].handle_left = frame - 0.5, value
    fcurve.keyframe_points[index].handle_right = frame + 0.5, value
        
    

    
    

def setupFolders():

    # reset root folder size
    act = bpy.data.objects[ROOT_FOLDER_SHORT_NAME].animation_data.action
    # set start scale
    add_scale_key_frame(act.fcurves, 1000, SCALE_NORMAL, SCALE_NORMAL, SCALE_NORMAL)

    for folder_name, pos in folder_pos_dic.items():
        
        # Skip root folder
        if folder_name == ROOT_FOLDER_SHORT_NAME:
            continue
        
        parent_folder_name, index, level, absolute_index = pos
        
        # Calclate folder relative index
        folder_num_name  = folder_num_name_dic[folder_name]
        parent_absolute_index = 0
        
        if parent_folder_name != "":
            parent_absolute_index = \
                folder_pos_dic[parent_folder_name][FOLDER_POS_ABSOLUTE_INDEX]
                
        relative_index = absolute_index - parent_absolute_index
        
        # set parent object
        set_obj_parent(folder_num_name_dic[parent_folder_name], \
            folder_num_name)
        
        
        
        # calc start frame
        frame = START_FRAME + level * (FOLDER_FRAME_START_MARGIN + \
            FOLDER_FRAME_Z_EXPAND \
            + FOLDER_FRAME_X_EXPAND_WAIT + FOLDER_FRAME_X_EXPAND)
        
        # get fcurves
        fcurves = bpy.data.objects[folder_num_name].animation_data.action.fcurves
        
        # add move start key_frame
        frame +=  FOLDER_FRAME_START_MARGIN
        add_location_key_frame(fcurves, frame, 0, 0, 0)
        add_scale_key_frame(fcurves, frame, SCALE_STORAGE, SCALE_STORAGE, \
            SCALE_STORAGE)
            
        # add Z expand end key_frame
        frame += FOLDER_FRAME_Z_EXPAND
        add_location_key_frame(fcurves, frame, 0, FOLDER_Y_MARGIN, FOLDER_Z_MARGIN)
        add_scale_key_frame(fcurves, frame, SCALE_NORMAL, SCALE_NORMAL, \
            SCALE_NORMAL)
        
        # add X expand wait key_frame
        frame += FOLDER_FRAME_X_EXPAND_WAIT
        add_location_key_frame(fcurves, frame, 0, FOLDER_Y_MARGIN, FOLDER_Z_MARGIN)        

        # add X expand end key_frame
        frame += FOLDER_FRAME_X_EXPAND
        add_location_key_frame(fcurves, frame, FOLDER_X_MARGIN * relative_index, \
            FOLDER_Y_MARGIN, FOLDER_Z_MARGIN)        
        
        # write log
        text_file.write(folder_num_name + ":" + str(relative_index).zfill(4) + ":" +  parent_folder_name + ":" + folder_name + '\n')
        
        
        # update fcurve
        fcurves.update()
        
        # add folder motion end frame to dic
        folder_end_frame_dic[folder_name] = frame


def setupFiles():
    for parent_folder, val in file_cnt_dic.items():
        
        file_num_name, file_cnt = val

        set_obj_parent(folder_num_name_dic[parent_folder], file_num_name)

        # get fcurves
        fcurves = bpy.data.objects[file_num_name].animation_data.action.fcurves

        # get start frame
        frame = folder_end_frame_dic[parent_folder]
        
        # add move start key frame
        frame += FILE_FRAME_START_MARGIN
        add_location_key_frame(fcurves, frame, 0, 0, 0)
        add_rotation_key_rrame(fcurves, frame, 0, 0, 0)
        add_scale_key_frame(fcurves, frame, SCALE_STORAGE, SCALE_STORAGE, \
            SCALE_STORAGE)
        
        # add x rot end key frame
        frame += FILE_FRAME_X_ROT
        add_location_key_frame(fcurves, frame, FILE_X_MARGIN, FILE_Y_MARGIN, \
             FILE_Z_MARGIN)
        add_rotation_key_rrame(fcurves, frame, math.pi / 2, 0, 0)
        add_scale_key_frame(fcurves, frame, SCALE_NORMAL, SCALE_NORMAL, \
            SCALE_NORMAL)

        # add y expand start key frame
        frame += FILE_FRAME_Y_EXPAND_WAIT
        add_scale_key_frame(fcurves, frame, SCALE_NORMAL, SCALE_NORMAL, \
            SCALE_NORMAL)
        
        # add y expand end key frame
        frame += FILE_FRAME_Y_EXPAND
        add_scale_key_frame(fcurves, frame, SCALE_NORMAL, \
            SCALE_NORMAL * file_cnt, SCALE_NORMAL)

        # update fcurve
        fcurves.update()

# START
print("### start ###")
create_folder_mesh("", ROOT_FOLDER_SHORT_NAME)
func_main(file_list.pop(0), [])
setupFolders()
setupFiles()
text_file.close()
print("### end ###")
