bl_info = {
    "name": "Import Penger",
    "blender": (4, 0, 0),
    "category": "Import-Export",
}

import bpy
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty


class IMPORT_OT_penger(Operator, ImportHelper):
    bl_idname = "import_scene.penger"
    bl_label = "Import Penger"
    bl_description = "Import Penger model (.penger)"
    filename_ext = ".penger"

    filter_glob: StringProperty(default="*.penger", options={"HIDDEN"})

    def execute(self, context):
        vs, edges = [], []
        section = 0
        with open(self.filepath) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line == "---":
                    section += 1
                    continue
                parts = line.split()
                if section == 0:
                    vs.append((float(parts[0]), float(parts[1]), float(parts[2])))
                elif section == 1:
                    if len(parts) == 2:
                        edges.append([int(parts[0]), int(parts[1])])
                    else:
                        face = [int(p) for p in parts]
                        for i in range(len(face)):
                            a, b = face[i], face[(i + 1) % len(face)]
                            edges.append([a, b])
        mesh = bpy.data.meshes.new("penger")
        mesh.from_pydata(vs, edges, [])
        mesh.update()
        obj = bpy.data.objects.new("penger", mesh)
        context.collection.objects.link(obj)
        return {"FINISHED"}


def menu_func_import(self, context):
    self.layout.operator(IMPORT_OT_penger.bl_idname, text="Penger (.penger)")


def register():
    bpy.utils.register_class(IMPORT_OT_penger)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.utils.unregister_class(IMPORT_OT_penger)


if __name__ == "__main__":
    register()
