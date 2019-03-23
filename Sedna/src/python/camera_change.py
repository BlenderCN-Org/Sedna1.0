# !BPY
# -*- coding: UTF-8 -*-
# Camera Change
#
# Change Camera & Frame span
#
# 2019.03.23 Natukikazemizo
#

import bpy
import os
import math

# CONSTANTS
CURRENT_SCENE = "Root"

def render(fps, frame_step, frame_start, frame_end, filepath, camera):
    bpy.context.scene.render.fps = fps
    bpy.context.scene.frame_step = frame_step
    bpy.context.scene.frame_start = frame_start
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

render(24, 2, 3001, 3024, "//..\\renderResults\\folderTree2\\", "Camera.001")


print("### end ###")
