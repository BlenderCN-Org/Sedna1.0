import bpy

from . import common


class MySettings(bpy.types.PropertyGroup):

#    emotion = bpy.props.EnumProperty(
#        name = "Emotion",
#        description = "Select emotion of registration destination.",
#        items = common.emotions
#    )

#    overwrite_data = bpy.props.BoolProperty(
#        name = "Overwrite Data",
#        description = "Enable or disable overwriting of data.",
#        default = True
#        )

    csv_file_name = bpy.props.StringProperty(
        name = "csv_file_name",
        description = "CSV file name."
    )
    csv_file_directory = bpy.props.StringProperty(subtype="FILE_PATH")
    target_armature_name = bpy.props.StringProperty(
        name = "target_armature_name",
        description = "Object name of the targeted of the constraints sync."
    )

class StringValGroup(bpy.types.PropertyGroup):
    string_val = bpy.props.StringProperty()


class SelectCSVFile(bpy.types.Operator):

    bl_idname = "object.select_csv_file"
    bl_label = bpy.app.translations.pgettext("Select CSV File")
    bl_description = bpy.app.translations.pgettext("Select CSV File")
    bl_options = {'REGISTER', 'UNDO'}

    filepath = bpy.props.StringProperty(subtype="FILE_PATH")
    filename = bpy.props.StringProperty(name="filename")
    directory = bpy.props.StringProperty(subtype="FILE_PATH")
    # Search Filter
    filter_glob = bpy.props.StringProperty(
        default="*.csv",
        options={'HIDDEN'}
    )

    def execute(self, context):
        self.report(
            {'INFO'},
            " [FilePath] %s, [FileName] %s, [Directory] %s"
            % (self.filepath, self.filename, self.directory)
        )
        props = context.scene.sync_bone_constraints_props
        props.csv_file_directory = self.directory
        props.csv_file_name = self.filename
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        # Show File Browser
        wm.fileselect_add(self)

        return {'RUNNING_MODAL'}

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

class TestPropSearchProps(bpy.types.PropertyGroup):

    # リストで選択されているオブジェクトの名前
    sel_obj = bpy.props.StringProperty()

    # Drop Downリストに表示される値のリスト
    string_val_list = bpy.props.CollectionProperty(type=StringValGroup)

    # 選択されている値が格納されるプロパティ
    sel_string = bpy.props.StringProperty()
    sel_string_val = bpy.props.StringProperty()

    def init_val_list(self):
        self.string_val_list.clear()
        for i in range(100):
            v = self.string_val_list.add()
            v.string_val = "val" + str( i )
            v.name = "name" + str(i)

    def update_val(self, nm):
        for sv in self.string_val_list:
            if sv.name == nm:
                self.sel_string_val = sv.string_val


class ArmatureMenu(bpy.types.Menu):

    bl_idname = "object.armature_menu"
    bl_label = bpy.app.translations.pgettext("Armature Menu")
    bl_description = bpy.app.translations.pgettext("Select Objects which has Armature.")

    def draw(self, context):
        layout = self.layout
        # メニュー項目の追加
        for i in range(3):
            layout.operator(NullOperation.bl_idname, text=("項目 %d" % (i)))


# Add "Auto Breakdown" tab on Tool Shelf
class VIEW3D_PT_AutoBreakdown(bpy.types.Panel):

    bl_label = bpy.app.translations.pgettext("Sync Bone Constraints")
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
        props = scene.sync_bone_constraints_props

        tps = context.window_manager.test_prop_search

        # ファイルブラウザを表示する
        layout.label(text = props.csv_file_directory)
        layout.label(text = props.csv_file_name)
        layout.operator(SelectCSVFile.bl_idname)

#        # CharacterName
#        layout.label(text = bpy.app.translations.pgettext("Character Name:"))
#        layout.label(text = bpy.path.abspath("//"))

#        # display the properties
#        layout.prop(props, "emotion", \
#            text=bpy.app.translations.pgettext("Emotion"))

#        layout.separator()

#        layout.prop(props, "overwrite_data", \
#            text=bpy.app.translations.pgettext("Overwrite Data"))

#        layout.prop_search(tps, "sel_obj", context.scene, "objects", text="Objects")
        layout.prop_search(tps, "sel_obj", context.scene, \
            "objects", text="Objects")
        row = layout.row()
        row.prop_search(tps, "sel_obj", context.scene, "objects", text="Objects")
        row = layout.row()
        row.prop(tps, "sel_obj")

        tps.init_val_list()
        row = layout.row()
        row.prop_search(tps, "sel_string", tps, "string_val_list", text="Test")
        row = layout.row()
        row.prop(tps, "sel_string")

        tps.update_val(tps.sel_string)
        row.prop(tps, "sel_string_val")


        layout.separator()

        layout.operator(NullOperation.bl_idname, \
            text = bpy.app.translations.pgettext("Sync"))

        layout.separator()

        layout.operator(NullOperation.bl_idname, \
            text = bpy.app.translations.pgettext("Write CSV"))

        layout.separator()

        layout.operator(NullOperation.bl_idname, \
            text = bpy.app.translations.pgettext("Read CSV"))
