# import-und-export

Blender addon for importing/exporting `.penger` files.

## Format

`.penger` files are plain text with sections separated by `---`:

- **Section 0**: Vertex coordinates (`x y z` per line)
- **Section 1**: Edges (`i j`) or faces (`i j k ...`)
- **Section 2 (v2 only)**: Faces (`i j k ...`)

## Files

| File | Description |
|------|-------------|
| `io_import_penger.py` | Import v1 (verts + edges) |
| `io_export_penger.py` | Export v1 (verts + edges) |
| `io_import_penger_v2.py` | Import v2 (verts + edges + faces) |
| `io_export_penger_v2.py` | Export v2 (verts + edges + faces) |

## License

Penger Public License – No copyright.
https://www.youtube.com/watch?v=qjWkNZ0SXfo&t=163s
Rotation Matrix:    • Rotation matrix derivation (step-by-step p...  
Penger Model: https://github.com/Max-Kawula/penger-obj
Source Code: https://github.com/tsoding/formula
