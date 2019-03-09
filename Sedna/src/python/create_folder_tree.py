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

# CONSTANT OF PARAMETERS
DIR_SPLITTER = "_"
SEED_FOLDER_NAME = 'Folder'
SEED_FILE_NAME = 'File'
ROOT_DIR = "C:/SRC/blender"
ROOT_DIR_ORG_NAME = "blender-2.79b"
ROOT_DIR_SHORT_NAME = "bl"

NEW_FOLDER_NAME = 'Folder_'
FOLDER_ZFILL = 4
NEW_FILE_NAME = 'File_'
FILE_ZFILL = 8

START_FRAME = 1000
FPS = 12
SCALE_STORAGE = 0.5
SCALE_NORMAL = 0

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
FILE_FRAME_Z_1ST_EXPAND = 12
FILE_FRAME_Z_2ND_EXPAND_WAIT = 4
FILE_FRAME_Z_2ND_EXPAND = 18

file_pos_dic = {}
dir_pos_dic = {}
dir_num_name_dic = {"":"", ROOT_DIR_SHORT_NAME:ROOT_DIR_SHORT_NAME}


def convert_dir_id(dir):    
    
    ret = dir.replace(ROOT_DIR_ORG_NAME, ROOT_DIR_SHORT_NAME)
    ret = ret.replace(os.sep, DIR_SPLITTER)

    return ret



# get file list
file_list = []
for root, dirs, files in os.walk(ROOT_DIR):
    root = os.path.relpath(root, ROOT_DIR)
    if root == '.': root = ''
    parent_dir = convert_dir_id(root)
    file_list.append([root, sorted(dirs), sorted(files), parent_dir])


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
        for ob in bpy.context.scene.objects:
            ob.select = False
        src_obj.select = True
        
        bpy.ops.object.duplicate(linked=True)
        new_obj = bpy.data.objects[src_name + '.001']
        new_obj.name = dup_name

def create_folder_num_name(folder_name):
    if folder_name not in dir_num_name_dic:
        dir_num_name_dic[folder_name] = NEW_FOLDER_NAME + str(len(dir_num_name_dic) + 1).zfill(FOLDER_ZFILL)

def create_folder_mesh(parent_dir_name, folder_name):
    """
    create folder mesh
    """
    print("folder:" + folder_name)
    print("parent:" + parent_dir_name)
    
    create_folder_num_name(folder_name)
    
    # duplicate object
    dupObject(SEED_FOLDER_NAME , dir_num_name_dic[folder_name])
        
    # set location
    
    # set scale

def create_file_mesh(parent_dir_name, file_name):
    """
    create file mesh
    """
    
    return
    
    print("file:" + file_name)
    print("parent:" + parent_dir_name)
    
    # duplicate object
    dupObject(SEED_FOLDER_NAME , file_name)
    
        
    # set location
    
    # set scale
    

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
    root, dirs, files, parent_dir = arg

    dir_len = len(dirs)
    file_len = len(files)

    # Output subdir

    for i, dir_name in enumerate(dirs):
        nounder = (i == dir_len - 1 and file_len == 0)
        
        dir_id = parent_dir + DIR_SPLITTER + dir_name

        create_folder_mesh(parent_dir, dir_id)
        
        print_file('<' + dir_id + '>', level_list, nounder)
        
        dir_pos_dic[dir_id] = (parent_dir, i, len(level_list))

        # Output subdir's subdir

        under_root = os.path.join(root, dir_name)
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
        file_id = parent_dir + DIR_SPLITTER + file_name
        create_file_mesh(parent_dir, file_id)
        print_file(file_id, level_list, (i == file_len - 1))
        
        file_pos_dic[file_id] = (parent_dir, i)

def setDirFCurve():
    for dir_name, pos in dir_pos_dic.items():
        set_obj_parent(dir_num_name_dic[pos[0]], dir_num_name_dic[dir_name])


def setFileFCurve():
    for file_name, pos in file_pos_dic.items():
        print(file_name)
        

# START
create_folder_mesh("", ROOT_DIR_SHORT_NAME)
func_main(file_list.pop(0), [])
setDirFCurve()
#setFileFCurve()
