#!BPY
# -*- coding: UTF-8 -*-
# Read F-Cureves(Pose Libraly)
#
# 2018.07.08 Natukikazemizo

import bpy

def get_pose_library(armature_name):
	return bpy.data.objects["Armature.Dorothy"].pose_library

def get_pose_markers_list(armature_name):
	ret_list = []
	for x in bpy.data.objects["Armature.Dorothy"].pose_library.pose_markers:
		ret_list.append(x.name)
	return ret_list


print("test")
