import bpy

from . import common


class MySettings(bpy.types.PropertyGroup):

    emotion = bpy.props.EnumProperty(
        name = "Emotion",
        description = "Select emotion of registration destination.",
        items = common.emotions
    )

    overwrite_data = bpy.props.BoolProperty(
        name = "Overwrite Data",
        description = "Enable or disable overwriting of data.",
        default = True
        )


class NullOperation(bpy.types.Operator):

    bl_idname = "object.null_operation"
    bl_label = "NOP"
    bl_description = "何もしない"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return {'FINISHED'}

class NullOperationMenu(bpy.types.Menu):

    bl_idname = "object.null_operation_menu"
    bl_label = "NOP メニュー"
    bl_description = "何もしない処理を複数持つメニュー"

    def draw(self, context):
        layout = self.layout
        # メニュー項目の追加
        for i in range(3):
            layout.operator(NullOperation.bl_idname, text=("項目 %d" % (i)))

# Add "Auto Breakdown" tab on Tool Shelf
class VIEW3D_PT_AutoBreakdown(bpy.types.Panel):

    bl_label = bpy.app.translations.pgettext("Export Pose")
              # String on TAB
    bl_space_type = 'VIEW_3D'           # Area which show menu
    bl_region_type = 'TOOLS'            # Region which show menu
    bl_category = bpy.app.translations.pgettext("Auto Breakdown")
            # String displayed in the header of the menu that opened the tab
    bl_context = "posemode"            # Context which show panel

    # 本クラスの処理が実行可能かを判定する
    @classmethod
    def poll(cls, context):
        # オブジェクトが選択されている時のみメニューを表示させる
        for o in bpy.data.objects:
            if o.select:
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
        props = scene.export_pose_props

        # CharacterName
        layout.label(text = bpy.app.translations.pgettext("Character Name:"))
        layout.label(text = bpy.context.active_object.name.replace(\
            "Armature.", ""))
        layout.label(text = bpy.path.abspath("//"))
        # display the properties
        layout.prop(props, "emotion", \
            text=bpy.app.translations.pgettext("Emotion"))

        layout.separator()

        layout.prop(props, "overwrite_data", \
            text=bpy.app.translations.pgettext("Overwrite Data"))

        layout.separator()

        layout.operator(NullOperation.bl_idname, \
            text=bpy.app.translations.pgettext("Export Pose"))


#def menu_fn_1(self, context):
#    self.layout.separator()
#    self.layout.operator(NullOperation.bl_idname, text="項目 1", icon='PLUGIN')


#def menu_fn_2(self, context):
#    self.layout.operator(NullOperation.bl_idname, text="項目 2", icon='PLUGIN')
#    self.layout.separator()
