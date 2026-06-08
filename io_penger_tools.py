bl_info = {
    "name": "Penger Tools",
    "blender": (4, 0, 0),
    "category": "Import-Export",
}

import bpy
from bpy.types import Operator


class MESH_OT_penger_generate_faces(Operator):
    bl_idname = "mesh.penger_generate_faces"
    bl_label = "Generate Faces from Edges"
    bl_description = "Generate mesh faces from selected edges"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != "MESH":
            self.report({"ERROR"}, "Select a mesh object")
            return {"CANCELLED"}

        mesh = obj.data
        if len(mesh.polygons) > 0:
            self.report({"INFO"}, "Mesh already has faces")
            return {"CANCELLED"}

        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.edge_face_add()
        bpy.ops.object.mode_set(mode="OBJECT")

        self.report({"INFO"}, f"Generated {len(mesh.polygons)} faces")
        return {"FINISHED"}


class VIEW3D_MT_penger_tools(bpy.types.Menu):
    bl_label = "Penger"
    bl_idname = "VIEW3D_MT_penger_tools"

    def draw(self, context):
        layout = self.layout
        layout.operator(MESH_OT_penger_generate_faces.bl_idname)


def menu_func(self, context):
    self.layout.menu("VIEW3D_MT_penger_tools")


def register():
    bpy.utils.register_class(MESH_OT_penger_generate_faces)
    bpy.utils.register_class(VIEW3D_MT_penger_tools)
    bpy.types.VIEW3D_MT_edit_mesh.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_edit_mesh.remove(menu_func)
    bpy.utils.unregister_class(VIEW3D_MT_penger_tools)
    bpy.utils.unregister_class(MESH_OT_penger_generate_faces)


if __name__ == "__main__":
    register()
