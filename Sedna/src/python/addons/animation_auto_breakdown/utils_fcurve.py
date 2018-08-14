﻿#!BPY
# -*- coding: UTF-8 -*-
# Utilities of F-Cureve
#
# 2018.07.08 Natukikazemizo

import bpy
import mathutils

###################
# SUB FUNCTIONS
###################

def get_location_bone(fcurve):
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

def get_pose(action, frame, bone_list):
    '''Get Pose(Bone Name & Location(Vector)'s Dictionary)'''
    ret = {}

    # Check Parameters & Get Objects

    # Create Vector Dictionary
    coordinate = []
    for fcurve in action.fcurves:
        bone = get_location_bone(fcurve)
        if bone in bone_list:
            coordinate.append(fcurve.evaluate(frame))
            if len(coordinate) == 3:
                v = mathutils.Vector(coordinate)
                ret[bone] = v
                coordinate = []
        else:
            coordinate = []

    return ret

def get_pose_dic(action, bone_list):
    '''Get Pose Dictionary'''
    ret = {}

    # Check Parameters & Get Objects
    fcurves = action.fcurves

    # Create {frame:{bone:Vector}} Dictionary
    i = 0
    while i < len(fcurves):
        bone = get_location_bone(fcurves[i])
        if bone in bone_list:
            for keyframe_point in fcurves[i].keyframe_points:
                frame = int(keyframe_point.co[0])
                pos = [ keyframe_point.co[1], \
                    fcurves[i + 1].evaluate(frame), \
                    fcurves[i + 2].evaluate(frame) ]
                ret.setdefault(frame, {})
                ret[frame][bone] = mathutils.Vector(pos)
            i += 3
        else:
            i += 1

    return ret


def create_act_dic(action, bone_list, frame_list):
    '''Create Act Dictionary'''
    ret = {}

    for frame in frame_list:
        ret[frame] = {}
        for bone in bone_list:
            ret[frame][bone] = mathutils.Vector([0, 0, 0])

    # Check Parameters & Get Objects
    fcurves = action.fcurves

    # Create {frame:{bone:Vector}} Dictionary
    i = 0
    while i < len(fcurves):
        bone = get_location_bone(fcurves[i])
        if bone in bone_list:
            for keyframe_point in fcurves[i].keyframe_points:
                frame = int(keyframe_point.co[0])
                pos = [ keyframe_point.co[1], \
                    fcurves[i + 1].evaluate(frame), \
                    fcurves[i + 2].evaluate(frame) ]
                ret.setdefault(frame, {})
                ret[frame][bone] = mathutils.Vector(pos)
            i += 3
        else:
            i += 1

    return ret

def set_pose(action, frame, pose, bone_list):
    '''Set Pose'''

    fcurves = action.fcurves

    # remove old keyframe_points
    for fcurve in fcurves:
        for keyframe_point in fcurve.keyframe_points:
            if int(keyframe_point.co[0]) == frame:
                fcurve.keyframe_points.remove(keyframe_point)
                break
        fcurve.update

    # Register pose
    i = 0
    while i < len(fcurves):
        bone = get_location_bone(fcurves[i])
        if bone in bone_list:
            add_keyframe_point(fcurves[i].keyframe_points, \
                "KEYFRAME", frame, pose[bone][0])
            fcurves[i].update()
            add_keyframe_point(fcurves[i + 1].keyframe_points, \
                "KEYFRAME", frame, pose[bone][1])
            fcurves[i + 1].update()
            add_keyframe_point(fcurves[i + 2].keyframe_points, \
                "KEYFRAME", frame, pose[bone][2])
            fcurves[i + 2].update()

            i += 3
        else:
            i += 1

    return
