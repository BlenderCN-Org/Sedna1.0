import bpy

from . import common
from . import utils_io_csv

class StringValGroup(bpy.types.PropertyGroup):
    string_val = bpy.props.StringProperty()

bpy.utils.register_class(StringValGroup)

# def INDEXS
BONE_NAME = 0
CONSTRAINT_NAME = 1
MUTE = 2
TARGET = 3
SUBTARGET_BONE_NAME = 4
EXTRAPOLATE = 5
FROM_MIN_X = 6
FROM_MAX_X = 7
FROM_MIN_Y = 8
FROM_MAX_Y = 9
FROM_MIN_Z = 10
FROM_MAX_Z = 11
MAP_TO_X_FROM = 12
MAP_TO_Y_FROM = 13
MAP_TO_Z_FROM = 14
MAP_TO = 15
TO_MIN_X = 16
TO_MAX_X = 17
TO_MIN_Y = 18
TO_MAX_Y = 19
TO_MIN_Z = 20
TO_MAX_Z = 21
TARGET_SPACE = 22
OWNER_SPACE = 23
INFLUENCE = 24
TYPE = 25
HEAD_TAIL = 26
USE_OFFSET = 27


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

    # リストで選択されているオブジェクトの名前
    #sel_armaturej= bpy.props.StringProperty()

    # 選択されている値が格納されるプロパティ
    sel_armature = bpy.props.StringProperty()
    sel_string_val = bpy.props.StringProperty()

    # Drop Downリストに表示される値のリスト
    string_val_list = bpy.props.CollectionProperty(type=bpy.types.StringValGroup)

    def init_val_list(self):
        self.string_val_list.clear()
        for obj in bpy.data.objects:
            if obj.type == 'ARMATURE':
                v = self.string_val_list.add()
                v.string_val = obj.name
                v.name = obj.name

#    def update_val(self, nm):
#        for sv in self.string_val_list:
#            if sv.name == nm:
#                self.sel_string_val = sv.string_val

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
        props = context.window_manager.sync_bone_constraints_props
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

#class NullOperationMenu(bpy.types.Menu):
#
#    bl_idname = "object.null_operation_menu"
#    bl_label = "NOP Menu"
#    bl_description = "Menu with multiple processes that do nothing"

#    def draw(self, context):
#        layout = self.layout
#        # メニュー項目の追加
#        for i in range(3):
#            layout.operator(NullOperation.bl_idname, text=("項目 %d" % (i)))

class SyncBonesIK(bpy.types.Operator):

    bl_idname = "object.sync_bones_ik"
    bl_label = "SyncBonesIK"
    bl_description = "Sync bones Invese Kinematics Settings."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.window_manager.sync_bone_constraints_props

        fromArmature = bpy.context.object.name
        for x in bpy.data.objects[props.sel_armature].pose.bones:
            if x.name in bpy.data.objects[fromArmature].pose.bones:
                fromBone = bpy.data.objects[fromArmature].pose.bones[x.name]
                x.ik_min_x = fromBone.ik_min_x
                x.ik_min_y = fromBone.ik_min_y
                x.ik_min_z = fromBone.ik_min_z
                x.ik_max_x = fromBone.ik_max_x
                x.ik_max_y = fromBone.ik_max_y
                x.ik_max_z = fromBone.ik_max_z
                x.use_ik_limit_x = fromBone.use_ik_limit_x
                x.use_ik_limit_y = fromBone.use_ik_limit_y
                x.use_ik_limit_z = fromBone.use_ik_limit_z
                x.ik_stretch = fromBone.ik_stretch
                x.lock_ik_x = fromBone.lock_ik_x
                x.lock_ik_y = fromBone.lock_ik_y
                x.lock_ik_z = fromBone.lock_ik_z

        return {'FINISHED'}



class SyncBoneConstraints(bpy.types.Operator):

    bl_idname = "object.sync_bone_constraints"
    bl_label = "Sync"
    bl_description = "Sync bones constraints of Armatures."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ExportBoneConstraints.execute(ExportBoneConstraints, context)
        ImportBoneConstraints.execute(ImportBoneConstraints, context)
        return {'FINISHED'}

class ExportBoneConstraints(bpy.types.Operator):

    bl_idname = "object.export_bone_constraints"
    bl_label = "Export"
    bl_description = "Export bones constraints to CSV File."
    bl_options = {'REGISTER', 'UNDO'}

    header = [
            "bone_name",
            "constraint_name",
            "mute",
            "target",
            "subtarget_bone_name",
            "extrapolate",
            "from_min_x",
            "from_max_x",
            "from_min_y",
            "from_max_y",
            "from_min_z",
            "from_max_z",
            "map_to_x_from",
            "map_to_y_from",
            "map_to_z_from",
            "map_to",
            "to_min_x",
            "to_max_x",
            "to_min_y",
            "to_max_y",
            "to_min_z",
            "to_max_z",
            "target_space",
            "owner_space",
            "influence",
            "type",
            "head_tail",
            "use_offset"
              ]

    def execute(self, context):
        bone_data = []
        bone_data.append(self.header)

        for x in bpy.context.selected_pose_bones:
            for y in x.constraints:
                if y.type == "TRANSFORM":
                    print(x.name + ", " + y.name)
                    data_row = []
                    data_row.append(x.name)
                    data_row.append(y.name)
                    data_row.append(y.mute)
                    data_row.append(y.target.name)
                    data_row.append(y.subtarget)
                    data_row.append(y.use_motion_extrapolate)
                    data_row.append(y.from_min_x)
                    data_row.append(y.from_max_x)
                    data_row.append(y.from_min_y)
                    data_row.append(y.from_max_y)
                    data_row.append(y.from_min_z)
                    data_row.append(y.from_max_z)
                    data_row.append(y.map_to_x_from)
                    data_row.append(y.map_to_y_from)
                    data_row.append(y.map_to_z_from)
                    data_row.append(y.map_to)
                    if y.map_to == "LOCATION":
                        data_row.append(y.to_min_x)
                        data_row.append(y.to_max_x)
                        data_row.append(y.to_min_y)
                        data_row.append(y.to_max_y)
                        data_row.append(y.to_min_z)
                        data_row.append(y.to_max_z)
                    elif y.map_to == "ROTATION":
                        data_row.append(y.to_min_x_rot)
                        data_row.append(y.to_max_x_rot)
                        data_row.append(y.to_min_y_rot)
                        data_row.append(y.to_max_y_rot)
                        data_row.append(y.to_min_z_rot)
                        data_row.append(y.to_max_z_rot)
                    else:
                        # map_to:SCALE
                        data_row.append(y.to_min_x_scale)
                        data_row.append(y.to_max_x_scale)
                        data_row.append(y.to_min_y_scale)
                        data_row.append(y.to_max_y_scale)
                        data_row.append(y.to_min_z_scale)
                        data_row.append(y.to_max_z_scale)
                    data_row.append(y.target_space)
                    data_row.append(y.owner_space)
                    data_row.append(y.influence)
                    data_row.append(y.type)

                    bone_data.append(data_row)
                elif y.type == "COPY_LOCATION":
                    print(x.name + ", " + y.name)
                    data_row = []
                    data_row.append(x.name)
                    data_row.append(y.name)
                    data_row.append(y.mute)
                    data_row.append(y.target.name)
                    data_row.append(y.subtarget)
                    data_row.append("")
                    data_row.append(y.use_x)
                    data_row.append(y.invert_x)
                    data_row.append(y.use_y)
                    data_row.append(y.invert_y)
                    data_row.append(y.use_z)
                    data_row.append(y.invert_z)
                    data_row.append("")
                    data_row.append("")
                    data_row.append("")
                    data_row.append("")
                    data_row.append("")
                    data_row.append("")
                    data_row.append("")
                    data_row.append("")
                    data_row.append("")
                    data_row.append("")
                    data_row.append(y.target_space)
                    data_row.append(y.owner_space)
                    data_row.append(y.influence)
                    data_row.append(y.type)
                    data_row.append(y.head_tail)
                    data_row.append(y.use_offset)

                    bone_data.append(data_row)

        props = context.window_manager.sync_bone_constraints_props
        utils_io_csv.write(props.csv_file_directory,
                           props.csv_file_name,
                            bone_data)
        return {'FINISHED'}

class ImportBoneConstraints(bpy.types.Operator):

    bl_idname = "object.import_bone_constraints"
    bl_label = "Import"
    bl_description = "Import bones constraints from CSV file."
    bl_options = {'REGISTER', 'UNDO'}




    def imp(self, target, context):
        props = context.window_manager.sync_bone_constraints_props
        header, data = utils_io_csv.read(props.csv_file_directory, \
                           props.csv_file_name)

        for row in data:
            if bpy.data.objects.find(target) == -1:
                print("Object not found. Object name is " + target)
                break
            if bpy.data.objects[target].pose.bones.find(row[BONE_NAME]) == -1:
                print("Bone not found. Bone name is " + row[BONE_NAME])
                break
            bone = bpy.data.objects[target].pose.bones[row[BONE_NAME]]

            if bone.constraints.find(row[CONSTRAINT_NAME]) == -1:
                constraint = bone.constraints.new(type=row[TYPE])
                constraint.name = row[CONSTRAINT_NAME]

            constraint = bone.constraints[row[CONSTRAINT_NAME]]

            print(bone.name + constraint.name)

            constraint.mute = row[MUTE] == "True"
            constraint.target = bpy.data.objects[target]
            constraint.subtarget = row[SUBTARGET_BONE_NAME]

            if row[TYPE] == "TRANSFORM":
                constraint.use_motion_extrapolate = row[EXTRAPOLATE] == "True"

                constraint.from_min_x = float(row[FROM_MIN_X])
                constraint.from_max_x = float(row[FROM_MAX_X])
                constraint.from_min_y = float(row[FROM_MIN_Y])
                constraint.from_max_y = float(row[FROM_MAX_Y])
                constraint.from_min_z = float(row[FROM_MIN_Z])
                constraint.from_max_z = float(row[FROM_MAX_Z])

                constraint.map_to_x_from = row[MAP_TO_X_FROM]
                constraint.map_to_y_from = row[MAP_TO_Y_FROM]
                constraint.map_to_z_from = row[MAP_TO_Z_FROM]
                constraint.map_to = row[MAP_TO]
                if constraint.map_to == "LOCATION":
                    constraint.to_min_x = float(row[TO_MIN_X])
                    constraint.to_max_x = float(row[TO_MAX_X])
                    constraint.to_min_y = float(row[TO_MIN_Y])
                    constraint.to_max_y = float(row[TO_MAX_Y])
                    constraint.to_min_z = float(row[TO_MIN_Z])
                    constraint.to_max_z = float(row[TO_MAX_Z])
                elif constraint.map_to == "ROTATION":
                    constraint.to_min_x_rot = float(row[TO_MIN_X])
                    constraint.to_max_x_rot = float(row[TO_MAX_X])
                    constraint.to_min_y_rot = float(row[TO_MIN_Y])
                    constraint.to_max_y_rot = float(row[TO_MAX_Y])
                    constraint.to_min_z_rot = float(row[TO_MIN_Z])
                    constraint.to_max_z_rot = float(row[TO_MAX_Z])
                else:
                    # map_to:SCALE
                    constraint.to_min_x_scale = float(row[TO_MIN_X])
                    constraint.to_max_x_scale = float(row[TO_MAX_X])
                    constraint.to_min_y_scale = float(row[TO_MIN_Y])
                    constraint.to_max_y_scale = float(row[TO_MAX_Y])
                    constraint.to_min_z_scale = float(row[TO_MIN_Z])
                    constraint.to_max_z_scale = float(row[TO_MAX_Z])
            elif row[TYPE] == "COPY_LOCATION":
                constraint.use_x = row[FROM_MIN_X] == "True"
                constraint.invert_x = row[FROM_MAX_X] == "True"
                constraint.use_y = row[FROM_MIN_Y] == "True"
                constraint.invert_y = row[FROM_MAX_Y] == "True"
                constraint.use_z = row[FROM_MIN_Z] == "True"
                constraint.invert_z = row[FROM_MAX_Z] == "True"
                constraint.head_tail = float(row[HEAD_TAIL])
                constraint.use_offset = row[USE_OFFSET] == "True"

            constraint.target_space = row[TARGET_SPACE]
            constraint.owner_space = row[OWNER_SPACE]
            constraint.influence = float(row[INFLUENCE])



    def execute(self, context):
        props = context.window_manager.sync_bone_constraints_props
        self.imp(self, props.sel_armature, context)
        return {'FINISHED'}


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
        props = context.window_manager.sync_bone_constraints_props


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


#        layout.prop_search(props, "sel_obj", context.scene, \
#            "objects", text="Objects")
#        row = layout.row()
#        row.prop_search(props, "sel_obj", context.scene, "objects", text="Objects")
#        row = layout.row()
#        row.prop(props, "sel_obj")

        row = layout.row()

        props.init_val_list()

        row.prop_search(props, "sel_armature", props,
                        "string_val_list",
                        text = bpy.app.translations.pgettext("Target"))

#        row = layout.row()
#        row.prop(props, "sel_armature")

 #       props.update_val(props.sel_armature)
#        row.prop(props, "sel_string_val")

        layout.separator()

        layout.operator(SyncBoneConstraints.bl_idname, \
            text = bpy.app.translations.pgettext("Sync"))

        layout.separator()

        layout.operator(ExportBoneConstraints.bl_idname, \
            text = bpy.app.translations.pgettext("Write CSV"))

        layout.separator()

        layout.operator(ImportBoneConstraints.bl_idname, \
            text = bpy.app.translations.pgettext("Read CSV"))

        layout.separator()

        layout.operator(SyncBonesIK.bl_idname, \
            text = bpy.app.translations.pgettext("Sync IK"))

