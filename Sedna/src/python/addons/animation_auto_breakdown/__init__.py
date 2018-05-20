
bl_info = {
    "name": "Auto Breakdown",
    "author": "N(Natukikazemizo)",
    "version": (0, 0),
    "blender": (2, 79, 0),
    "location": "Dope Sheet > Key / NLA Editor > Edit",
    "description": "Automatic Breakdown and related functions",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Animation"
}

# Translation dictionary
translation_dict = {
    "en_US": {
        ("*", "Auto Breakdown: Enabled add-on 'Auto Breakdown'"):
            "Auto Breakdown: Enabled add-on 'Auto Breakdown'",
        ("*", "Auto Breakdown: Disabled add-on 'Auto Breakdown'"):
            "Auto Breakdown: Disabled add-on 'Auto Breakdown'",
        ("*", "Auto Breakdown"):
            "Auto Breakdown",
        ("*", "Overwrite Data"):
            "Overwrite Data",
        ("*", "Export Pose"):
            "Export Pose",
        ("*", "Emotion"):
            "Emotion",
        ("*", "Character Name:"):
            "Character Name:"
    },
    "ja_JP": {
        ("*", "Auto Breakdown: Enabled add-on 'Auto Breakdown'"):
            "自動中割り: アドオン「自動中割り」が有効化されました。",
        ("*", "Auto Breakdown: Disabled add-on 'testee'"):
            "自動中割り: アドオン「自動中割り」が無効化されました。",
        ("*", "Auto Breakdown"):
            "自動中割り",
        ("*", "Overwrite Data"):
            "データ上書き",
        ("*", "Export Pose"):
            "ポーズ抽出",
        ("*", "Emotion"):
            "感情",
        ("*", "Character Name:"):
            "キャラクター名："
    }
}

if "bpy" in locals():
    import imp
    imp.reload(auto_twist)
    imp.reload(auto_breakdown)
    imp.reload(export_pose)
else:
    from . import auto_twist
    from . import auto_breakdown
    from . import export_pose

import bpy

class TestOps1(bpy.types.Operator):

    bl_idname = "object.test_ops_1d"
    bl_label = "Test1"
    bl_description = "Test target Operation1"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return {'FINISHED'}


class TestOps2(bpy.types.Operator):

    bl_idname = "object.test_ops_2d"
    bl_label = "Test2"
    bl_description = "Test target Operation2"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # オブジェクト名が「Cube」であるオブジェクトが存在しない場合
        if bpy.data.objects.find('Cube') == -1:
            return {'CANCELLED'}
        return {'FINISHED'}


def register():
    bpy.utils.register_module(__name__)
    # Register Translation dictionary
    bpy.app.translations.register(__name__, translation_dict)
    bpy.types.Scene.export_pose_props = bpy.props.PointerProperty(type=export_pose.MySettings)

#    # 項目をメニューの先頭に追加
#    bpy.types.VIEW3D_MT_pose.append(export_pose.menu_fn_1)
#    # 項目をメニューの末尾に追加
#    bpy.types.VIEW3D_MT_pose.prepend(export_pose.menu_fn_2)

    print(
        bpy.app.translations.pgettext(
            "Auto Breakdown: Enabled add-on 'Auto Breakdown'"
        )
    )

def unregister():
#    bpy.types.VIEW3D_MT_pose.remove(export_pose.menu_fn_2)
#    bpy.types.VIEW3D_MT_pose.remove(export_pose.menu_fn_1)

    # UnRegister Translation dictionary
    bpy.app.translations.unregister(__name__)
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.export_pose_props
    print(
        bpy.app.translations.pgettext(
            "Auto Breakdown: Disabled add-on 'Auto Breakdown'"
        )
    )



if __name__ == "__main__":
    register()
