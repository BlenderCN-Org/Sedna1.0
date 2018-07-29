#!BPY
# -*- coding: UTF-8 -*-
# Utilities of F-Cureve
#
# 2018.07.08 Natukikazemizo

import bpy
import mathutils

###################
# SUB FUNCTIONS
###################

def get_location_bone_name(fcurve):
    '''get bone name from data_path'''

    data_path = fcurve.data_path
    if "].location" in data_path:
        index = data_path.find('"')
        str = data_path[index + 1:]
        index = str.find('"')
        str = str[:index]
        return str
    else:
        return ""

def add_keyframe_point(keyframe_points, type, frame, value):
    keyframe_points.add(1)
    index = len(keyframe_points) - 1
    keyframe_points[index].type =  type
    keyframe_points[index].co =  frame, value
    keyframe_points[index].handle_left = frame - 0.5, 0
    keyframe_points[index].handle_right = frame + 0.5, 0


###################
# MAIN FUNCTIONS
###################

def get_pose(action_name, frame, bone_name_list):
	'''Get Pose(Bone Name & Location(Vector)'s Dictionary)'''
	ret = {}

	# Check Parameters & Get Objects
	if bpy.data.actions.find(action_name) < 0:
		return ret
	action = bpy.data.actions[action_name]

	# Create Vector Dictionary
	coordinate = []
	for fcurve in action.fcurves:
		bone_name = get_location_bone_name(fcurve)
		if bone_name in bone_name_list:
			coordinate.append(fcurve.evaluate(frame))
			if len(coordinate) == 3:
				v = Vector(coordinate)
				ret[bone_name] = v
				coordinate = []
		else:
			coordinate = []

	return ret

def get_pose_dic(action_name, bone_name_list):
	'''Get Pose Dictionary'''
	ret = {}

	# Check Parameters & Get Objects
	if bpy.data.actions.find(action_name) < 0:
		return ret
	fcurves = bpy.data.actions[action_name].fcurves

	# Create {frame:{bone_name:Vector}} Dictionary
	for i in range(len(fcurves)):
		bone_name = get_location_bone_name(fcurves[i])
		if bone_name in bone_name_list:
			for keyframe_point in fcurves[i].keyframe_points:
				frame = int(keyframe_point.co[0])
				ret[frame] = Vector([keyframe_point.co[1],
					fcurves[i + 1].evalulate(frame),
					fcurves[i + 2].evalulate(frame)])
			i += 3
		else:
			i += 1

	return ret

def set_pose(action_name, frame, pose):
	'''Set Pose'''
	if bpy.data.actions.find(action_name) < 0:
		return

	fcurves = bpy.data.actions[action_name].fcurves

	# remove old keyframe_points
	for fcurve in fcurves:
		for keyframe_point in fcurve.keyframe_points:
			if int(keyframe_point.co[0]) == frame:
				fcurve.keyframe_points.remove(keyframe_point)
				break
		fcurve.update

	# Register pose
	for i in range(len(fcurves)):
		bone_name = get_location_bone_name(fcurves[i])
		if bone_name in bone_name_list:
			add_keyframe_point(fcurves[i].keyframe_points, \
				"KEYFRAME", frame, pose[bone_name][0])
			fcurves[i].update()
			add_keyframe_point(fcurves[i + 1].keyframe_points, \
				"KEYFRAME", frame, pose[bone_name][1])
			fcurves[i + 1].update()
			add_keyframe_point(fcurves[i + 2].keyframe_points, \
				"KEYFRAME", frame, pose[bone_name][2])
			fcurves[i + 2].update()

			i += 3
		else:
			i += 1

	return
