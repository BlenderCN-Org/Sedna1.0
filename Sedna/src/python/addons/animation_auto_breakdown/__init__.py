import bpy


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
            "Auto Breakdown: Disabled add-on 'Auto Breakdown'"
    },
    "ja_JP": {
        ("*", "Auto Breakdown: Enabled add-on 'Auto Breakdown'"):
            "自動中割り: アドオン「自動中割り」が有効化されました。",
        ("*", "Auto Breakdown: Disabled add-on 'testee'"):
            "自動中割り: アドオン「自動中割り」が無効化されました。"
    }
}

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
    print(
        bpy.app.translations.pgettext(
            "Auto Breakdown: Enabled add-on 'Auto Breakdown'"
        )
    )

def unregister():
    # UnRegister Translation dictionary
    bpy.app.translations.unregister(__name__)
    bpy.utils.unregister_module(__name__)
    print(
        bpy.app.translations.pgettext(
            "Auto Breakdown: Disabled add-on 'Auto Breakdown'"
        )
    )



if __name__ == "__main__":
    register()
