bl_info = {
    "name": "Export Penger",
    "blender": (4, 0, 0),
    "category": "Import-Export",
}

import bpy
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty


class EXPORT_OT_penger(Operator, ExportHelper):
    bl_idname = "export_scene.penger"
    bl_label = "Export Penger"
    bl_description = "Export active mesh as .penger"
    filename_ext = ".penger"

    filter_glob: StringProperty(default="*.penger", options={"HIDDEN"})

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != "MESH":
            self.report({"ERROR"}, "Select a mesh object")
            return {"CANCELLED"}

        depsgraph = context.evaluated_depsgraph_get()
        eval_obj = obj.evaluated_get(depsgraph)
        mesh = eval_obj.to_mesh()
        if not mesh:
            self.report({"ERROR"}, "Could not get mesh data")
            return {"CANCELLED"}

        mesh.transform(obj.matrix_world)

        verts = [v.co for v in mesh.vertices]
        edge_set = set()
        for e in mesh.edges:
            edge_set.add(tuple(sorted((e.vertices[0], e.vertices[1]))))

        with open(self.filepath, "w") as f:
            for v in verts:
                f.write(f"{v.x:.6f} {v.y:.6f} {v.z:.6f}\n")
            f.write("---\n")
            for e in sorted(edge_set):
                f.write(f"{e[0]} {e[1]}\n")

        eval_obj.to_mesh_clear()
        self.report({"INFO"}, f"Exported {len(verts)} verts, {len(edge_set)} edges")
        return {"FINISHED"}


def menu_func_export(self, context):
    self.layout.operator(EXPORT_OT_penger.bl_idname, text="Penger (.penger)")


def register():
    bpy.utils.register_class(EXPORT_OT_penger)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.utils.unregister_class(EXPORT_OT_penger)


if __name__ == "__main__":
    register()
