import bpy


bl_info = {
    "name": "Test Target Addon",
    "author": "N(Natukikazemizo)",
    "version": (2, 0),
    "blender": (2, 79, 0),
    "location": "Object",
    "description": "Test Target Addon",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}


class TestOps1(bpy.types.Operator):

    bl_idname = "object.test_ops_1"
    bl_label = "Test1"
    bl_description = "Test target Operation1"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return {'FINISHED'}


class TestOps2(bpy.types.Operator):

    bl_idname = "object.test_ops_2"
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


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
