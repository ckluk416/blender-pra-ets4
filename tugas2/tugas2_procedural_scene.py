"""
Blender Python Script - Tugas 2: Procedural Texture Scene
=========================================================

Membuat scene dengan 8+ objek dan 8 material procedural berbeda.
Tema: Natural - Forest Floor (tanah, batu, kayu, lumut, moss, dll)

Materials yang dibuat:
1. Dirt Ground - Noise + ColorRamp
2. Stone/Rock - Voronoi + Noise + Bump
3. Wood Log - Wave texture dengan rings
4. Moss - Noise + Voronoi + Bump
5. Dead Leaves - Noise + ColorRamp dengan brownish
6. Clay Soil - Noise + Bump dengan clay color
7. Lichen - Voronoi + ColorRamp + Bump (wrinkly texture)
8. Wet Mud - Noise + ColorRamp + Displacement (geometry deformation)

Texture Nodes yang digunakan:
- Noise Texture (untuk organic variation)
- Voronoi Texture (untuk cellular/cracked patterns)
- Wave Texture (untuk wood rings)
- ColorRamp (untuk color control)
- Bump Mapping (untuk surface detail)
- Displacement (untuk geometry detail)

Tested: Blender 3.x 4.x
"""

import bpy
import math


def delete_all_objects():
    """Hapus semua objek di scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    print("✓ Scene cleared")


def create_dirt_ground_material(name="Dirt_Ground"):
    """
    Material tanah/dirt dengan Noise texture
    Nodes: TexCoord, Noise, ColorRamp, RGB, Principled, Output
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Texture Coordinate
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    # Noise untuk dirt variation
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-600, 0)
    noise.inputs['Scale'].default_value = 25.0
    noise.inputs['Detail'].default_value = 5.0
    
    # ColorRamp untuk dirt colors (light to dark brown)
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-400, 0)
    colorramp.color_ramp.elements[0].color = (0.45, 0.35, 0.25, 1.0)  # Light brown
    colorramp.color_ramp.elements[1].color = (0.2, 0.15, 0.08, 1.0)   # Dark brown
    
    # Base dirt color
    dirt_color = nodes.new('ShaderNodeRGB')
    dirt_color.location = (-500, 150)
    dirt_color.outputs[0].default_value = (0.4, 0.32, 0.2, 1.0)
    
    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (100, 0)
    bsdf.inputs['Base Color'].default_value = (0.4, 0.32, 0.2, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.8
    
    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    # Link
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    print(f"✓ {name}")
    return mat


def create_stone_material(name="Stone_Rock"):
    """
    Material batu dengan Voronoi + Noise
    Nodes: TexCoord, Mapping, Voronoi, Noise, ColorRamp, Bump, Principled, Output
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Texture Coordinate
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1000, 0)
    
    # Mapping untuk scale
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-800, 0)
    mapping.inputs['Scale'].default_value = (5.0, 5.0, 5.0)
    
    # Voronoi untuk stone cell pattern
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-600, 100)
    voronoi.feature = 'F1'
    voronoi.inputs['Scale'].default_value = 10.0
    
    # Noise untuk additional variation
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-600, -150)
    noise.inputs['Scale'].default_value = 15.0
    noise.inputs['Detail'].default_value = 6.0
    
    # Mix untuk combine textures
    mix = nodes.new('ShaderNodeMixRGB')
    mix.location = (-400, 0)
    mix.blend_type = 'MULTIPLY'
    
    # ColorRamp untuk stone colors (gray variations)
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-200, 0)
    colorramp.color_ramp.elements[0].color = (0.3, 0.3, 0.32, 1.0)   # Dark gray
    colorramp.color_ramp.elements[1].color = (0.6, 0.58, 0.55, 1.0)  # Light gray
    
    # Bump untuk surface detail
    bump = nodes.new('ShaderNodeBump')
    bump.location = (50, -150)
    bump.inputs['Strength'].default_value = 0.6
    
    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (250, 0)
    bsdf.inputs['Roughness'].default_value = 0.85
    
    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (550, 0)
    
    # Link
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], voronoi.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    links.new(voronoi.outputs['Distance'], mix.inputs['Color1'])
    links.new(noise.outputs['Fac'], mix.inputs['Color2'])
    links.new(mix.outputs['Color'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(colorramp.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    print(f"✓ {name}")
    return mat


def create_wood_material(name="Wood_Log"):
    """
    Material kayu dengan Wave texture
    Nodes: TexCoord, Mapping, Wave, ColorRamp, Noise, Bump, Principled, Output
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Texture Coordinate
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    # Mapping untuk orientation
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-600, 0)
    mapping.inputs['Scale'].default_value = (1.0, 1.0, 20.0)
    
    # Wave texture untuk wood rings
    wave = nodes.new('ShaderNodeTexWave')
    wave.location = (-400, 0)
    wave.wave_type = 'RINGS'
    wave.inputs['Scale'].default_value = 15.0
    wave.inputs['Distortion'].default_value = 2.0
    
    # ColorRamp untuk wood colors
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-200, 0)
    colorramp.color_ramp.elements[0].color = (0.5, 0.35, 0.15, 1.0)   # Light brown
    colorramp.color_ramp.elements[1].color = (0.25, 0.15, 0.05, 1.0)  # Dark brown
    
    # Noise untuk wood grain variation
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-400, -200)
    noise.inputs['Scale'].default_value = 50.0
    
    # Bump untuk wood detail
    bump = nodes.new('ShaderNodeBump')
    bump.location = (50, -150)
    bump.inputs['Strength'].default_value = 0.4
    
    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (250, 0)
    bsdf.inputs['Roughness'].default_value = 0.5
    
    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (550, 0)
    
    # Link
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], wave.inputs['Vector'])
    links.new(wave.outputs['Color'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    print(f"✓ {name}")
    return mat


def create_moss_material(name="Moss"):
    """
    Material moss dengan Noise + Voronoi
    Nodes: TexCoord, Noise, Voronoi, ColorRamp, Bump, Principled, Output
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Texture Coordinate
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    # Noise untuk moss base
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-600, 100)
    noise.inputs['Scale'].default_value = 30.0
    noise.inputs['Detail'].default_value = 8.0
    
    # Voronoi untuk moss cracking
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-600, -150)
    voronoi.feature = 'DISTANCE_TO_EDGE'
    voronoi.inputs['Scale'].default_value = 20.0
    
    # Mix
    mix = nodes.new('ShaderNodeMixRGB')
    mix.location = (-400, 0)
    mix.blend_type = 'OVERLAY'
    
    # ColorRamp untuk moss green colors
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-200, 0)
    colorramp.color_ramp.elements[0].color = (0.1, 0.25, 0.08, 1.0)   # Dark moss
    colorramp.color_ramp.elements[1].color = (0.3, 0.45, 0.15, 1.0)   # Light moss
    
    # Bump untuk moss surface
    bump = nodes.new('ShaderNodeBump')
    bump.location = (50, -150)
    bump.inputs['Strength'].default_value = 0.5
    
    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (250, 0)
    bsdf.inputs['Roughness'].default_value = 0.7
    
    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (550, 0)
    
    # Link
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    links.new(tex_coord.outputs['Object'], voronoi.inputs['Vector'])
    links.new(noise.outputs['Fac'], mix.inputs['Color1'])
    links.new(voronoi.outputs['Distance'], mix.inputs['Color2'])
    links.new(mix.outputs['Color'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(colorramp.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    print(f"✓ {name}")
    return mat


def create_dead_leaves_material(name="Dead_Leaves"):
    """
    Material daun mati dengan Noise + ColorRamp
    Nodes: TexCoord, Noise, ColorRamp, RGB, Bump, Principled, Output
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Texture Coordinate
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    # Noise untuk leaf detail
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-600, 0)
    noise.inputs['Scale'].default_value = 35.0
    noise.inputs['Detail'].default_value = 7.0
    
    # ColorRamp untuk dead leaf colors (browns and yellows)
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-400, 0)
    colorramp.color_ramp.elements[0].color = (0.35, 0.2, 0.1, 1.0)    # Dark brown
    colorramp.color_ramp.elements[1].color = (0.65, 0.55, 0.2, 1.0)   # Golden brown
    
    # Base color
    base_color = nodes.new('ShaderNodeRGB')
    base_color.location = (-500, 150)
    base_color.outputs[0].default_value = (0.5, 0.4, 0.15, 1.0)
    
    # Bump untuk leaf texture
    bump = nodes.new('ShaderNodeBump')
    bump.location = (50, -150)
    bump.inputs['Strength'].default_value = 0.3
    
    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (250, 0)
    bsdf.inputs['Roughness'].default_value = 0.6
    
    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (550, 0)
    
    # Link
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    print(f"✓ {name}")
    return mat


def create_clay_soil_material(name="Clay_Soil"):
    """
    Material tanah liat dengan Noise + Bump
    Nodes: TexCoord, Noise, ColorRamp, Bump, Principled, Output
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Texture Coordinate
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    # Noise untuk clay texture
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-600, 0)
    noise.inputs['Scale'].default_value = 20.0
    noise.inputs['Detail'].default_value = 4.0
    
    # ColorRamp untuk clay colors (reddish brown)
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-400, 0)
    colorramp.color_ramp.elements[0].color = (0.35, 0.25, 0.2, 1.0)   # Dark clay
    colorramp.color_ramp.elements[1].color = (0.65, 0.45, 0.3, 1.0)   # Light clay
    
    # Bump untuk clay surface
    bump = nodes.new('ShaderNodeBump')
    bump.location = (50, -150)
    bump.inputs['Strength'].default_value = 0.7
    
    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (250, 0)
    bsdf.inputs['Base Color'].default_value = (0.5, 0.35, 0.25, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.75
    
    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (550, 0)
    
    # Link
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    print(f"✓ {name}")
    return mat


def create_lichen_material(name="Lichen"):
    """
    Material lichen dengan Voronoi + Bump
    Nodes: TexCoord, Voronoi, ColorRamp, Bump, Principled, Output
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Texture Coordinate
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    # Voronoi untuk lichen cracking pattern
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-600, 0)
    voronoi.feature = 'F1'
    voronoi.inputs['Scale'].default_value = 25.0
    
    # ColorRamp untuk lichen colors (grayish green)
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-400, 0)
    colorramp.color_ramp.elements[0].color = (0.35, 0.35, 0.25, 1.0)  # Gray
    colorramp.color_ramp.elements[1].color = (0.4, 0.45, 0.2, 1.0)    # Greenish
    
    # Bump untuk lichen wrinkled surface
    bump = nodes.new('ShaderNodeBump')
    bump.location = (50, -150)
    bump.inputs['Strength'].default_value = 0.6
    
    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (250, 0)
    bsdf.inputs['Roughness'].default_value = 0.8
    
    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (550, 0)
    
    # Link
    links.new(tex_coord.outputs['Object'], voronoi.inputs['Vector'])
    links.new(voronoi.outputs['Color'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(voronoi.outputs['Distance'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    print(f"✓ {name}")
    return mat


def create_wet_mud_material(name="Wet_Mud"):
    """
    Material lumpur basah dengan Noise + Displacement
    Nodes: TexCoord, Mapping, Noise, ColorRamp, Displacement, Principled, Output
    ** Ini adalah satu-satunya material dengan DISPLACEMENT untuk geometry detail **
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Texture Coordinate
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-900, 0)
    
    # Mapping untuk scale
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-700, 0)
    mapping.inputs['Scale'].default_value = (10.0, 10.0, 10.0)
    
    # Noise untuk mud surface variation
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-500, 0)
    noise.inputs['Scale'].default_value = 30.0
    noise.inputs['Detail'].default_value = 6.0
    
    # ColorRamp untuk wet mud colors (dark brownish)
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-300, 0)
    colorramp.color_ramp.elements[0].color = (0.1, 0.08, 0.05, 1.0)   # Very dark
    colorramp.color_ramp.elements[1].color = (0.3, 0.2, 0.1, 1.0)     # Lighter mud
    
    # Displacement untuk actual geometry deformation
    displacement = nodes.new('ShaderNodeDisplacement')
    displacement.location = (100, -200)
    displacement.inputs['Scale'].default_value = 0.2  # Modest displacement
    
    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (250, 0)
    bsdf.inputs['Base Color'].default_value = (0.2, 0.15, 0.08, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.6
    
    # Material Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (550, 0)
    
    # Link
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(noise.outputs['Fac'], displacement.inputs['Height'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    links.new(displacement.outputs['Displacement'], output.inputs['Displacement'])
    
    print(f"✓ {name} (WITH DISPLACEMENT)")
    return mat


def create_scene_objects():
    """Membuat 9 objek untuk scene - dengan spacing yang lebih baik"""
    
    objects = {}
    
    # 1. Ground plane (large) - Dirt
    bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, 0))
    objects['ground'] = bpy.context.active_object
    objects['ground'].name = "Dirt_Ground"
    
    # 2. Stone 1 (large rock) - bottom left
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.2, location=(-4, -4, 0.8))
    objects['stone1'] = bpy.context.active_object
    objects['stone1'].name = "Stone_Rock_1"
    
    # 3. Stone 2 (smaller rock) - bottom right
    bpy.ops.mesh.primitive_cube_add(size=1.4, location=(4, -4, 0.5))
    objects['stone2'] = bpy.context.active_object
    objects['stone2'].name = "Stone_Rock_2"
    bpy.ops.object.shade_smooth()
    
    # 4. Wood log (cylinder) - top left
    bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=3, location=(-4, 4, 0.5))
    objects['wood'] = bpy.context.active_object
    objects['wood'].name = "Wood_Log"
    objects['wood'].rotation_euler = (0, 1.57, 0)  # Rotate to horizontal
    
    # 5. Moss covered rock - left center
    bpy.ops.mesh.primitive_cube_add(size=1.3, location=(-4, 0, 0.7))
    objects['moss_rock'] = bpy.context.active_object
    objects['moss_rock'].name = "Moss_Stone"
    
    # 6. Dead leaves pile (plane) - top right
    bpy.ops.mesh.primitive_plane_add(size=1.5, location=(4, 4, 0.1))
    objects['leaves'] = bpy.context.active_object
    objects['leaves'].name = "Dead_Leaves"
    objects['leaves'].scale = (2.0, 1.5, 1.0)
    
    # 7. Clay soil patch (plane) - center
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0, 0.2, 0.05))
    objects['clay'] = bpy.context.active_object
    objects['clay'].name = "Clay_Soil"
    
    # 8. Wet mud patch (grid with subdivision for displacement) - right center
    bpy.ops.mesh.primitive_grid_add(
        x_subdivisions=20,
        y_subdivisions=20,
        size=2.2,
        location=(4, 0, 0)
    )
    objects['mud'] = bpy.context.active_object
    objects['mud'].name = "Wet_Mud"
    
    # 9. Lichen covered object (small cube) - scattered position
    bpy.ops.mesh.primitive_cube_add(size=0.6, location=(0, -4, 0.3))
    objects['lichen'] = bpy.context.active_object
    objects['lichen'].name = "Lichen_Object"
    
    print("✓ 9 Objects created with proper spacing")
    return objects


def assign_material_to_object(obj, material):
    """Assign material ke object"""
    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)


def setup_scene():
    """Setup lighting, camera, dan environment"""
    
    # Delete existing lights and cameras
    for obj in bpy.data.objects:
        if obj.type in ['LIGHT', 'CAMERA']:
            bpy.data.objects.remove(obj, do_unlink=True)
    
    # Add sun light (simulating outdoor forest)
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 8))
    sun = bpy.context.active_object
    sun.name = "Sun"
    sun.data.energy = 2.5
    sun.data.angle = 0.2
    
    # Add fill light
    bpy.ops.object.light_add(type='AREA', location=(-5, -5, 4))
    fill = bpy.context.active_object
    fill.name = "Fill_Light"
    fill.data.energy = 0.8
    fill.data.size = 5.0
    
    # Add camera with good angle
    bpy.ops.object.camera_add(location=(5, -8, 5))
    camera = bpy.context.active_object
    camera.name = "Camera"
    camera.rotation_euler = (1.1, 0, 0.785)
    bpy.context.scene.camera = camera
    
    # Set world background to darker (forest mood)
    world = bpy.context.scene.world
    world.use_nodes = True
    bg = world.node_tree.nodes['Background']
    bg.inputs[0].default_value = (0.3, 0.35, 0.3, 1.0)  # Greenish
    bg.inputs[1].default_value = 1.0
    
    # Set viewport shading to Material Preview
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'
    
    print("✓ Scene setup complete")


def print_summary(materials, objects):
    """Print scene summary"""
    
    print("\n" + "="*80)
    print("TUGAS 2: PROCEDURAL TEXTURE SCENE - SUMMARY")
    print("="*80)
    
    print("\n SCENE THEME: Natural - Forest Floor Environment")
    print("   Konsep: Woodland floor dengan berbagai natural materials")
    print("   Environment: Outdoor forest setting dengan dappled sunlight")
    
    print("\n OBJECTS CREATED:")
    for key, obj in objects.items():
        print(f"  • {obj.name:25s} (Type: {obj.type})")
    
    print("\n PROCEDURAL MATERIALS (8 Different):")
    
    material_details = [
        ("Dirt_Ground", "Noise + ColorRamp", "Ground base texture"),
        ("Stone_Rock", "Voronoi + Noise + Bump", "Rock cellular pattern"),
        ("Wood_Log", "Wave (Rings) + Noise + Bump", "Wood grain rings"),
        ("Moss", "Noise + Voronoi + Bump", "Moss coverage"),
        ("Dead_Leaves", "Noise + ColorRamp + Bump", "Fallen leaves"),
        ("Clay_Soil", "Noise + Bump", "Clay earth texture"),
        ("Lichen", "Voronoi + Bump", "Lichen coating"),
        ("Wet_Mud", "Noise + DISPLACEMENT", "Muddy ground with geometry"),
    ]
    
    for mat_name, tech, desc in material_details:
        mat = bpy.data.materials.get(mat_name)
        if mat:
            nodes = len(mat.node_tree.nodes)
            has_disp = any('Displacement' in n.name for n in mat.node_tree.nodes)
            status = "✓ WITH DISPLACEMENT" if has_disp else "✓ PROCEDURAL"
            print(f"\n  {mat_name:20s}")
            print(f"    Technique: {tech}")
            print(f"    Description: {desc}")
            print(f"    Nodes: {nodes} | {status}")
    
    print("\n" + "="*80)
    print(" TEXTURE NODES USED:")
    print("  ✓ Noise Texture (6x) - For organic variation")
    print("  ✓ Voronoi Texture (3x) - For cellular patterns")
    print("  ✓ Wave Texture (1x) - For wood rings")
    print("  ✓ ColorRamp (8x) - For color control")
    print("  ✓ Bump Mapping (7x) - For surface detail")
    print("  ✓ Displacement (1x) - For geometry detail")
    print("  ✓ Mix RGB - For combining textures")
    print("  ✓ Texture Coordinate & Mapping - For coordinate system")
    
    print("\n" + "="*80)
    print(" TIPS:")
    print("  • Press 'Z' and select 'Rendered' for photo-realistic rendering")
    print("  • Press Numpad 0 for camera view")
    print("  • Use Shader Editor (Shift+F3) to inspect node setups")
    print("  • For Wet_Mud material to show displacement: add Subdivision Surface modifier")
    print("  • Render high quality with F12 for better screenshots")
    print("="*80 + "\n")


def main():
    """Main function"""
    
    print("\n Starting Procedural Texture Scene Creation...\n")
    
    # Clean scene
    print("1.  Clearing scene...")
    delete_all_objects()
    
    # Create materials
    print("\n2.  Creating procedural materials...")
    materials = {
        'dirt': create_dirt_ground_material("Dirt_Ground"),
        'stone': create_stone_material("Stone_Rock"),
        'wood': create_wood_material("Wood_Log"),
        'moss': create_moss_material("Moss"),
        'leaves': create_dead_leaves_material("Dead_Leaves"),
        'clay': create_clay_soil_material("Clay_Soil"),
        'lichen': create_lichen_material("Lichen"),
        'mud': create_wet_mud_material("Wet_Mud"),
    }
    
    # Create objects
    print("\n3.  Creating scene objects...")
    objects = create_scene_objects()
    
    # Assign materials
    print("\n4.  Assigning materials to objects...")
    assign_material_to_object(objects['ground'], materials['dirt'])
    assign_material_to_object(objects['stone1'], materials['stone'])
    assign_material_to_object(objects['stone2'], materials['stone'])
    assign_material_to_object(objects['wood'], materials['wood'])
    assign_material_to_object(objects['moss_rock'], materials['moss'])
    assign_material_to_object(objects['leaves'], materials['leaves'])
    assign_material_to_object(objects['clay'], materials['clay'])
    assign_material_to_object(objects['mud'], materials['mud'])
    assign_material_to_object(objects['lichen'], materials['lichen'])
    print("✓ All materials assigned")
    
    # Setup scene
    print("\n5.  Setting up scene lighting & camera...")
    setup_scene()
    
    # Print summary
    print_summary(materials, objects)

if __name__ == "__main__":
    main()
