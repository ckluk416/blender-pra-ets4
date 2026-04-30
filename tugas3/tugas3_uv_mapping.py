"""
Blender Python Script - Tugas 3: UV Mapping Project
==================================================

Script untuk praktik UV unwrapping dan texture painting preparation.
Objek yang digunakan: Chair (kursi) - furniture dengan multiple parts.

Proses UV Mapping:
1. Mark seams pada edge yang sesuai (antara seat, back, legs)
2. Smart UV unwrap dengan minimal distortion
3. Pack UV islands secara optimal
4. Export UV layout sebagai image
5. Apply checker texture untuk verifikasi

Requirements:
- Objek kompleks dengan multiple parts
- UV unwrapping dengan seams
- Minimal distortion
- Exported UV layout image
- Checker texture verification

Tested: Blender 3.x 4.x
"""

import bpy
import math


def delete_all_objects():
    """Hapus semua objek di scene menggunakan direct data manipulation"""
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    print("Scene cleared")


def create_chair_object():
    """
    Membuat objek chair (kursi) dengan multiple parts untuk UV mapping practice.
    Parts: Seat, Back, 4 Legs
    """
    # Clear scene first
    delete_all_objects()

    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # seat (cube scaled)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.5))
    seat = bpy.context.active_object
    seat.name = "Chair_Seat"
    seat.scale = (1.2, 1.2, 0.1)  # Wide seat

    # back (cube rotated and scaled)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -1.0, 1.0))
    back = bpy.context.active_object
    back.name = "Chair_Back"
    back.scale = (1.2, 0.1, 1.0)  # Tall back
    back.rotation_euler = (math.radians(10), 0, 0)  # Slight tilt

    # 4 legs 
    leg_positions = [
        (-0.8, -0.8, 0),   # Front left
        (0.8, -0.8, 0),    # Front right
        (-0.8, 0.8, 0),    # Back left
        (0.8, 0.8, 0)      # Back right
    ]

    legs = []
    for i, pos in enumerate(leg_positions):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=1.0, location=pos)
        leg = bpy.context.active_object
        leg.name = f"Chair_Leg_{i+1}"
        legs.append(leg)

    for obj in bpy.context.scene.objects:
        obj.select_set(False)
    
    seat.select_set(True)
    back.select_set(True)
    for leg in legs:
        leg.select_set(True)

    bpy.context.view_layer.objects.active = seat
    bpy.ops.object.join()
    chair = bpy.context.active_object
    chair.name = "Chair_Complete"
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')

    return chair


def mark_seams_by_angle(obj, angle_threshold=30):
    """
    Mark seams otomatis berdasarkan angle threshold.
    Seams akan dibuat pada edge dengan angle > threshold (sharp edges).
    """
    # Set context and enter Edit Mode
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')

    # Select mode to edge
    bpy.ops.mesh.select_mode(type='EDGE')

    # Deselect all first
    bpy.ops.mesh.select_all(action='DESELECT')
        
    # Select sharp edges based on angle threshold
    bpy.ops.mesh.edges_select_sharp(sharpness=math.radians(angle_threshold))

    # Mark selected edges as seams
    bpy.ops.mesh.mark_seam()

    # Back to Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')

    print(f"✓ Seams marked on sharp edges (angle > {angle_threshold}°)")


def perform_uv_unwrap(obj):
    """
    Lakukan UV unwrapping dengan Smart UV Project.
    """
    # Set context and enter Edit Mode
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')

    # Switch to face select mode and select all
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action='SELECT')

    # Smart UV Unwrap
    bpy.ops.uv.smart_project(angle_limit=66, island_margin=0.02, user_area_weight=0.0, use_aspect=True, stretch_to_bounds=True)

    # Pack UV islands
    bpy.ops.uv.pack_islands(rotate=True, margin=0.02)

    # Back to Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')

    print("UV unwrapping completed with Smart UV Project")


def create_checker_material(name="UV_Checker"):
    """
    Membuat material checker untuk verifikasi UV mapping.
    Menggunakan Checker Texture node untuk lihat distortion.
    Shader: TexCoord → Mapping → Checker → Principled BSDF
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Texture Coordinate - gunakan UV dari unwrapped mesh
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)

    # Mapping untuk scale checker pattern agar terlihat
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-400, 0)
    mapping.inputs['Scale'].default_value = (8.0, 8.0, 8.0)

    # Checker Texture - kotak hitam putih untuk verifikasi UV
    checker = nodes.new('ShaderNodeTexChecker')
    checker.location = (-100, 0)
    checker.inputs['Color1'].default_value = (0.0, 0.0, 0.0, 1.0)  # Black
    checker.inputs['Color2'].default_value = (1.0, 1.0, 1.0, 1.0)  # White
    checker.inputs['Scale'].default_value = 5.0

    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (200, 0)
    bsdf.inputs['Roughness'].default_value = 0.4  # rada matte sikit agar texture jelas

    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (500, 0)

    # Connect nodes: TexCoord → Mapping → Checker → BSDF → Output
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], checker.inputs['Vector'])
    links.new(checker.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    return mat


def export_uv_layout(obj, filepath="uv_layout.png"):
    """
    Export UV layout sebagai image PNG.
    """
    bpy.context.view_layer.objects.active = obj
        
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    if hasattr(bpy.ops.uv, 'export_layout'):
        bpy.ops.uv.export_layout(filepath=filepath, size=(1024, 1024), opacity=1.0)
        print(f"UV layout exported to {filepath}")
    else:
        print("UV export operator not available, skipping export")


def setup_scene_lighting():
    """Setup basic lighting untuk scene"""
    # dlete existing light
    for obj in list(bpy.data.objects):
        if obj.type == 'LIGHT':
            bpy.data.objects.remove(obj, do_unlink=True)

    # Add sun light
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 5))
    sun = bpy.context.active_object
    sun.name = "Sun_Light"
    sun.data.energy = 3.0

    # Add camera
    bpy.ops.object.camera_add(location=(3, -3, 2), rotation=(math.radians(60), 0, math.radians(45)))
    camera = bpy.context.active_object
    camera.name = "Scene_Camera"

    # Set camera as active
    bpy.context.scene.camera = camera

    print("Scene lighting and camera setup")


def main():
    """
    Main function untuk menjalankan semua proses UV mapping.
    """
    print("Tugas 3: UV Mapping Project")
    print("=" * 50)

    # 1. ceate chair object
    chair = create_chair_object()

    # 2. mark seams
    mark_seams_by_angle(chair, angle_threshold=30)

    # 3. perform UV unwrap
    perform_uv_unwrap(chair)

    # 4. create checker material
    checker_mat = create_checker_material()

    # 5. apply checker material to all faces of chair
    chair.data.materials.clear()
    chair.data.materials.append(checker_mat)
    
    bpy.context.view_layer.objects.active = chair
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.object.material_slot_assign()
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # 6. Export UV layout
    export_uv_layout(chair, filepath="../tugas3/screenshot/uv_layout.png")

    # 7. Setup scene
    setup_scene_lighting()


if __name__ == "__main__":
    main()