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
TEST_PATH = "//..\\renderResults\\TestPrint\\Test_"
FPS = 1

def render(fps, frame_step, frame_start, frame_end, filepath, camera):
    global test_print_cnt
    bpy.context.scene.render.fps = fps
    bpy.context.scene.frame_step = frame_step
    bpy.context.scene.frame_start = frame_start
    if TEST_MODE:
        bpy.context.scene.frame_end = frame_start
        test_print_cnt += 1
        bpy.data.scenes[CURRENT_SCENE].render.filepath = TEST_PATH + \
            str(test_print_cnt).zfill(4) + "_camera_" + camera + "_" + \
            str(frame_start).zfill(5) + "_" +str(frame_end).zfill(5)
    else:
        bpy.context.scene.frame_end = frame_end
        bpy.data.scenes[CURRENT_SCENE].render.filepath = filepath

    bpy.context.scene.camera = bpy.data.objects[camera]
    print("#### Render Start  #### camera:" + camera + " frame:" + str(frame_start) + \
        "-" +str(frame_end))
    bpy.ops.render.render(animation=True)

    if TEST_MODE:
        middle_frame = math.floor((frame_start + frame_end) / 2)
        bpy.context.scene.frame_start = middle_frame
        bpy.context.scene.frame_end = middle_frame
        test_print_cnt += 1
        bpy.data.scenes[CURRENT_SCENE].render.filepath = TEST_PATH + \
            str(test_print_cnt).zfill(4) + "_camera_" + camera + "_" + \
            str(frame_start).zfill(5) + "_" +str(frame_end).zfill(5)
        bpy.ops.render.render(animation=True)


    print("#### Render End    #### camera:" + camera + " frame:" + str(frame_start) + \
        "-" + str(frame_end))

# main

print("######## START ########")

#bpy.context.window.screen = bpy.data.screens['Render']

render(24, FPS, 1000, 1084, "//..\\renderResults\\Main\\", "Camera.Main")
render(24, FPS, 1085, 1182, "//..\\renderResults\\Main\\", "Camera.Main")
render(24, FPS, 1183, 1272, "//..\\renderResults\\Main\\", "Camera.Main")
render(24, FPS, 1426, 1498, "//..\\renderResults\\Main\\", "Camera.Main")
render(24, FPS, 1499, 1553, "//..\\renderResults\\Main\\", "Camera.Main")
render(24, FPS, 1554, 1578, "//..\\renderResults\\Main\\", "Camera.Main")
render(24, FPS, 1579, 1676, "//..\\renderResults\\Main\\", "Camera.Main")
render(24, FPS, 1677, 1797, "//..\\renderResults\\Main\\", "Camera.Main")
render(24, FPS, 1798, 1870, "//..\\renderResults\\Main\\", "Camera.Main")

render(24, FPS, 3000, 3024, "//..\\renderResults\\Main\\", "Camera.Main")
render(24, FPS, 3025, 3128, "//..\\renderResults\\Main\\", "Camera.Main")
render(24, FPS, 3129, 3256, "//..\\renderResults\\Main\\", "Camera.Main")
render(24, FPS, 3256, 4000, "//..\\renderResults\\Main\\", "Camera.Main")
render(24, FPS, 3500, 4000, "//..\\renderResults\\Middle\\", "Camera.Middle")
render(24, FPS, 3100, 3500, "//..\\renderResults\\Dolly\\", "Camera.Dolly")


render(24, FPS, 4800, 5000, "//..\\renderResults\\Long\\", "Camera.Long")

print("######## END   ########")


