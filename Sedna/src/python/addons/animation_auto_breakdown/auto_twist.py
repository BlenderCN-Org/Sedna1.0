#!BPY
# -*- coding: UTF-8 -*-
# Automatically Twist Pose
#
# 2018.07.08 Natukikazemizo

if "bpy" in locals():
    import imp
    imp.reload(common)
    imp.reload(utils_armature)
    imp.reload(utils_fcurve)
else:
    from . import common
    from . import utils_armature
    from . import utils_fcurve

import bpy
import mathutils

# CONSTANTS
# Twisted Objects trailer
TWISTED_TRAILER = "_Twist"

# Action Target Bone Name
ACT_TARGET = "Act_Target"

# Source Pose Armature Layers
SRC_POSE_LAYERS = [
False,  False,  False,  False,  False,  False,  False,  False,
False,  False,  False,  False,  False,  False,  False,  False,
False,  False,  False,  False,  False,  False,  True,   True,
False,  False,  False,  False,  False,  False,  False,  False
]

# Twist target Armature Layers
TWIST_LAYERS = [
False,  False,  False,  False,  False,  False,  False,  True,
False,  False,  False,  False,  False,  False,  False,  False,
False,  False,  False,  False,  False,  False,  True,   True,
False,  False,  False,  False,  False,  False,  False,  False
]


class MySettings(bpy.types.PropertyGroup):

    source_track_name = bpy.props.StringProperty(
        name = "source_track_name",
        description = "Source Track name."
    )

    source_strip_name = bpy.props.StringProperty(
        name = "source_strip_name",
        description = "Source Strip name."
    )

    source_action_name = bpy.props.StringProperty(
        name = "source_action_name",
        description = "Source Action name."
    )

    destination_track_name = bpy.props.StringProperty(
        name = "destination_track_name",
        description = "Destination Track name."
    )

    destination_strip_name = bpy.props.StringProperty(
        name = "destination_strip_name",
        description = "Destination Strip name."
    )

    destination_action_name = bpy.props.StringProperty(
        name = "destination_action_name",
        description = "Destination Action name."
    )

    character = bpy.props.EnumProperty(
        name = "Character",
        description = "Select Character.",
        items = common.characters
    )

    overwrite_data = bpy.props.BoolProperty(
        name = "Overwrite Strip",
        description = "Enable or disable overwriting of Strip.",
        default = True
    )

    msg_chk = bpy.props.StringProperty()
    msg_icon = bpy.props.StringProperty(
        default = "NONE"
    )

    res_msg = bpy.props.StringProperty()
    res_icon = bpy.props.StringProperty(
        default = "NONE"
    )

    def check(self):
        if self.source_strip_name == "":
            self.msg_chk = bpy.app.translations.pgettext("Select Strip.")
            self.msg_icon = "ERROR"
        else:
            self.msg_chk = "OK"
            self.msg_icon = "INFO"

    def result(self, msg, icon):
        self.res_msg = bpy.app.translations.pgettext(msg)
        self.res_icon = icon

# Create Auto twisted Strip
class CreateAutoTwistedStrip(bpy.types.Operator):

    bl_idname = "object.create_auto_twisted_strip"
    bl_label = "Create"
    bl_description = "Create auto twisted strip."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        props = context.window_manager.auto_twist_props

        props.result('Start', 'INFO')

        # GetSourceTruck
        src_track = bpy.context.object.animation_data.nla_tracks[\
            props.source_track_name]

        # GetSourceStrip
        src_strip = src_track.strips[props.source_strip_name]

        frame_start = src_strip.frame_start

        # Crete NLA track
        if props.destination_track_name in \
            bpy.context.object.animation_data.nla_tracks:
            if props.overwrite_data:
                track = bpy.context.object.animation_data.nla_tracks[\
                    props.destination_track_name]
            else:
                props.result('Duplicate Object.', 'ERROR')
                return {'FINISHED'}
        else:
            track = bpy.context.object.animation_data.nla_tracks.new()
            track.name = props.destination_track_name

        # Create Action
        if props.destination_action_name in bpy.data.actions:
            if props.overwrite_data:
                act = bpy.data.actions[props.destination_action_name]
            else:
                props.result('Duplicate Object.', 'ERROR')
                return {'FINISHED'}
        else:
            act = bpy.data.actions.new(props.destination_action_name)

        # Create Strip
        if props.destination_strip_name in track.strips:
            if props.overwrite_data:
                strip = track.strips[props.destination_strip_name]
            else:
                props.result('Duplicate Object.', 'ERROR')
                return {'FINISHED'}
        else:
            # Seek Same frame Strip
            find = False
            for x in track.strips:
                if x.frame_start == frame_start:
                    find = True
                    strip = x
                    break
            if not find:
                strip = track.strips.new(name = props.destination_strip_name,\
                    start = frame_start, action = act)

        # Get Emotion on Character
        armature_name = bpy.context.selected_objects[0].name
        char_action_name = common.char_action[props.character]
        char_emotion = {}

        emotion_bone_name_list = utils_armature.get_bone_name_list(\
            armature_name, SRC_POSE_LAYERS)

        for i, x in enumerate(common.emotions, start=1):
            emotion = utils_fcurve.get_pose(char_action_name, i, \
                emotion_bone_name_list)
            char_emotion.update({x[0]: emotion})

        # Get Source Action's Pose Dictionary
        twist_bone_name_list = utils_armature.get_bone_name_list(\
            armature_name, TWIST_LAYERS)

        src_pose_dic = utils_fcurve.get_pose_dic(props.source_action_name, \
            twist_bone_name_list)

        # Create Twisted Pose
        frames = src_pose_dic.keys()

        for frame in frames:
            pose = src_pose_dic[frame]
            # Modify pose here

            # Set Pose
            utils_fcurve.set_pose(props.destination_action_name, frame, pose)


        return {'FINISHED'}

# Add "Auto Breakdown" tab on Tool Shelf
class VIEW3D_PT_AutoBreakdown(bpy.types.Panel):

    bl_label = bpy.app.translations.pgettext("Auto Twist")
              # String on TAB
    bl_space_type = 'NLA_EDITOR'        # Area which show menu
    bl_region_type = 'UI'               # Region which show menu
    bl_category = bpy.app.translations.pgettext("Auto Breakdown")
            # String displayed in the header of the menu that opened the tab
    #bl_context = "auto_twist"            # Context which show panel

    # Determine whether this class of processing can be executed
    @classmethod
    def poll(cls, context):
        # Display menu only when 1 Strip is selected
        selected_strips = []
        try:
            selected_strips = [strip for strip in
            bpy.context.object.animation_data.nla_tracks.active.strips
            if strip.select]
        except AttributeError:
            pass
        if len(selected_strips) == 1:
            # Create Initial Names
            props = context.window_manager.auto_twist_props
            props.source_track_name = \
                bpy.context.object.animation_data.nla_tracks.active.name
            props.source_strip_name = \
                selected_strips[0].name
            props.source_action_name = \
                selected_strips[0].action.name
            props.destination_track_name = \
                props.source_track_name + TWISTED_TRAILER
            props.destination_strip_name = \
                props.source_strip_name + TWISTED_TRAILER
            props.destination_action_name = \
                props.source_action_name + TWISTED_TRAILER
            return True
        return False

    # Customize header
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='PLUGIN')

    # Draw Menu
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = context.window_manager.auto_twist_props

        layout.prop(props, "source_strip_name", \
            text = bpy.app.translations.pgettext("Source Strip"))
        layout.prop(props, "source_action_name", \
            text = bpy.app.translations.pgettext("Source Action"))
        layout.prop(props, "destination_track_name", \
            text = bpy.app.translations.pgettext("Destination Track"))
        layout.prop(props, "destination_strip_name", \
            text = bpy.app.translations.pgettext("Destination Strip"))
        layout.prop(props, "destination_action_name", \
            text = bpy.app.translations.pgettext("Destination Action"))

        row = layout.row()

        layout.prop(props, "character", \
            text=bpy.app.translations.pgettext("Character Name"))

        layout.prop(props, "overwrite_data", \
            text=bpy.app.translations.pgettext("Overwrite Strip&Action"))

        row = layout.row()

        layout.separator()

        row = layout.row()
        box = row.box()
        box_row = box.row()

        # Check Selected Value & Show result with icon and label
        props.check()

        box_row.label(text = props.msg_chk, icon=props.msg_icon)

        row = layout.row()
        box = row.box()
        box_row = box.row()
        box_row.label(text = props.res_msg, icon=props.res_icon)

        layout.operator(CreateAutoTwistedStrip.bl_idname, \
            text = bpy.app.translations.pgettext("Auto Twist"))
