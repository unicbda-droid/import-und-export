bl_info = {
    "name": "Export Penger v3",
    "blender": (4, 0, 0),
    "category": "Import-Export",
}

import bpy
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty


class EXPORT_OT_penger_v3(Operator, ExportHelper):
    bl_idname = "export_scene.penger_v3"
    bl_label = "Export Penger v3"
    bl_description = "Export active mesh as .penger (UVs)"
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
        faces = [p.vertices for p in mesh.polygons]

        with open(self.filepath, "w") as f:
            for v in verts:
                f.write(f"{v.x:.6f} {v.y:.6f} {v.z:.6f}\n")
            f.write("---\n")
            for e in sorted(edge_set):
                f.write(f"{e[0]} {e[1]}\n")
            f.write("---\n")
            for face in faces:
                f.write(" ".join(str(i) for i in face) + "\n")
            uv_layer = mesh.uv_layers.active
            if uv_layer:
                f.write("---\n")
                for uv in uv_layer.data:
                    f.write(f"{uv.uv.x:.6f} {uv.uv.y:.6f}\n")

        eval_obj.to_mesh_clear()
        self.report({"INFO"}, f"Exported {len(verts)} verts, {len(edge_set)} edges, {len(faces)} faces")
        return {"FINISHED"}


def menu_func_export(self, context):
    self.layout.operator(EXPORT_OT_penger_v3.bl_idname, text="Penger v3 (.penger)")


def register():
    bpy.utils.register_class(EXPORT_OT_penger_v3)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.utils.unregister_class(EXPORT_OT_penger_v3)


if __name__ == "__main__":
    register()
