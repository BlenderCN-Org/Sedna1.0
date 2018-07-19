#!BPY
# -*- coding: UTF-8 -*-
# Utility of F-Cureve
#
# 2018.07.08 Natukikazemizo

import bpy
import mathutils

# Is Both True
def is_agreement_layer(src_list, tgt_list):
	for i, val in enumerate(src_lict):
		if val and tgt_list[i]:
			return True
	return False

# Get Pose(Bone Name & Location(Vector)'s Dictionary)
def get_pose(action_name, frame, armature_name, layers_list):
	ret = {}

	# Check Parameters & Get Objects
	if bpy.data.actions.find(action_name) < 0:
		return ret
	action = bpy.data.actions[action_name]

	if bpy.data.objects.find(armature_name) < 0:
		return ret
	armature = bpy.data.objects[armature_name]

	if armature.type != 'ARMATURE':
		return ret

    armature_data_name = bpy.data.objects["Armature.Dorothy"].data.name
	armature_data = bpy.data.armatures[armature_data_name]



    # set current frame
    bpy.context.scene.frame_set(frame)




	return ret

# Get Pose list
def get_pose_list(action, frame, layers_list):
	ret = []

	return ret

# Set Pose
def set_pose(action, frame, pose):
