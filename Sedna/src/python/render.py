# !BPY
# -*- coding: UTF-8 -*-
# Render
#
# Render with Change Camera & Frame span
#
# 2019.03.23 Natukikazemizo
#

import bpy
import os
import math

# CONSTANTS
CURRENT_SCENE = "Root"
TEST_MODE = True
test_print_cnt = 0
TEST_PATH = "//..\\renderResults\\folderTree2\\Test_"

def render(fps, frame_step, frame_start, frame_end, filepath, camera):
    global test_print_cnt
    bpy.context.scene.render.fps = fps
    bpy.context.scene.frame_step = frame_step
    bpy.context.scene.frame_start = frame_start
    if TEST_MODE:
        bpy.context.scene.frame_end = frame_start
        test_print_cnt += 1
    else:
        bpy.context.scene.frame_end = frame_end

    bpy.data.scenes[CURRENT_SCENE].render.filepath = filepath
    bpy.context.scene.camera = bpy.data.objects[camera]
    print("#### Render Start #### camera:" + camera + " frame:" + str(frame_start) + \
        "-" +str(frame_end))
    bpy.ops.render.render(animation=True)
    print("#### Render End   #### camera:" + camera + " frame:" + str(frame_start) + \
        "-" + str(frame_end))

# main

print("### start ###")

#bpy.context.window.screen = bpy.data.screens['Render']

render(24, 2, 3001, 3024, "//..\\renderResults\\folderTree2\\", "Camera.Main")


print("### end ###")
