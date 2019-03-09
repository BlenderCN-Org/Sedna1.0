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


dic_file_pos = {}
dic_dir_pos = {}
dic_dir_level = {}

# get file list
file_list = []
for root, dirs, files in os.walk(ROOT_DIR):
    root = os.path.relpath(root, ROOT_DIR)
    if root == '.': root = ''
    parent_dir = root.replace(ROOT_DIR_ORG_NAME, ROOT_DIR_SHORT_NAME)
    parent_dir = parent_dir.replace(os.sep, DIR_SPLITTER)
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

def create_folder_mesh(file_name, parent_dir_name):
    """
    create folder mesh
    """
    # check objects
    
    # check parent setting
    
    # set scale

def create_file_mesh(file_name, parent_dir_name):
    """
    create folder mesh
    """
    # check objects
    
    # check parent setting

    # set scale
    

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

        print_file('<' + dir_id + '>', level_list, nounder)
        
        dic_dir_pos[dir_id] = (len(level_list), i)

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
        print_file(file_id, level_list, (i == file_len - 1))
        
        dic_file_pos[file_id] = i
    

# START
func_main(file_list.pop(0), [])

print(dic_dir_pos)

