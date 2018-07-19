#!BPY
# -*- coding: UTF-8 -*-
# Automatically Twist Pose
#
# 2018.07.08 Natukikazemizo

if "bpy" in locals():
    import imp
    imp.reload(common)
else:
    from . import common

import bpy
import mathutils

# CONSTANTS
# Twisted Objects trailer
TWISTED_TRAILER = "_Twist"

# Action Target Bone Name
ACT_TARGET = "Act_Target"

class MySettings(bpy.types.PropertyGroup):

    source_strip_name = bpy.props.StringProperty(
        name = "source_strip_name",
        description = "Source Strip name."
    )

    destination_track_name = bpy.props.StringProperty(
        name = "destination_track_name",
        description = "Destination Track name."
    )

    destination_strip_name = bpy.props.StringProperty(
        name = "destination_strip_name",
        description = "Destination Strip name."
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
    msg_icon = bpy.props.StringProperty()

    def check(self):
        if self.source_strip_name == "":
            self.msg_chk = bpy.app.translations.pgettext("Select Strip.")
            self.msg_icon = "ERROR"
        else:
            self.msg_chk = "OK"
            self.msg_icon = "INFO"

# Create Auto twisted Strip
class CreateAutoTwistedStrip(bpy.types.Operator):

    bl_idname = "object.create_auto_twisted_strip"
    bl_label = "Create"
    bl_description = "Create auto twisted strip."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        #ExportBoneConstraints.execute(ExportBoneConstraints, context)
        #ImportBoneConstraints.execute(ImportBoneConstraints, context)
        #SyncBonesIK.execute(SyncBonesIK, context)
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

    # 本クラスの処理が実行可能かを判定する
    @classmethod
    def poll(cls, context):
        # Stripが1個選択されている時のみメニューを表示させる
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
            props.source_strip_name = \
                selected_strips[0].name
            props.destination_track_name = \
                bpy.context.object.animation_data.nla_tracks.active.name + \
                TWISTED_TRAILER
            props.destination_strip_name = \
                props.source_strip_name + TWISTED_TRAILER
            return True
        return False

    # ヘッダーのカスタマイズ
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='PLUGIN')

    # メニューの描画処理
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = context.window_manager.auto_twist_props

        layout.prop(props, "source_strip_name", \
            text = bpy.app.translations.pgettext("Source Strip"))
        layout.prop(props, "destination_track_name", \
            text = bpy.app.translations.pgettext("Destination Track"))
        layout.prop(props, "destination_strip_name", \
            text = bpy.app.translations.pgettext("Destination Strip"))

        row = layout.row()

        layout.prop(props, "character", \
            text=bpy.app.translations.pgettext("Character Name"))

        layout.prop(props, "overwrite_data", \
            text=bpy.app.translations.pgettext("Overwrite Strip"))

        row = layout.row()

        layout.separator()

        row = layout.row()
        box = row.box()
        box_row = box.row()

        # Check Selected Value & Show result with icon and label
        props.check()

        box_row.label(text = props.msg_chk, icon=props.msg_icon)

        layout.operator(CreateAutoTwistedStrip.bl_idname, \
            text = bpy.app.translations.pgettext("Auto Twist"))
