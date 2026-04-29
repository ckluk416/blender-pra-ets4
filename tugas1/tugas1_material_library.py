"""
Blender Python Script - Tugas 1: Material Library
================================================

Script untuk membuat library material dengan 5 material berbeda,
masing-masing dengan minimal 5 shader nodes.

Materials yang dibuat:
1. Copper/Rusty Metal - Material logam dengan oksidasi
2. Leather - Material kain/kulit dengan roughness variation
3. Bark - Material organik dengan tekstur kayu
4. Jade/Crystal - Material transparan/translucent
5. Neon Glow - Material emisif/glowing

Objects: Sphere, Cube, Cylinder, Torus, Monkey (Suzanne)

Tested: Blender 3.x 4.x
"""

import bpy
import math


def delete_all_objects():
    """Hapus semua objek di scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    print("✓ Semua objek dihapus")


def create_copper_metal_material(name="Copper_Rusty"):
    """
    Membuat material copper dengan oxidation effect
    Nodes: Principled BSDF, Noise, ColorRamp, Bump, MixRGB (5 nodes)
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # tex Coordinate untuk variasi
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    # noise untuk variasi copper/oxidation pattern
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-600, 0)
    noise.inputs['Scale'].default_value = 20.0
    noise.inputs['Detail'].default_value = 5.0
    
    # colorRamp untuk control oxidation warna
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-400, 0)
    # copper to green oxidation
    colorramp.color_ramp.elements[0].color = (0.7, 0.35, 0.1, 1.0)   # Copper
    colorramp.color_ramp.elements[1].color = (0.2, 0.4, 0.2, 1.0)    # Green patina
    
    # mix RGB untuk blend copper base color
    base_color = nodes.new('ShaderNodeRGB')
    base_color.location = (-500, 200)
    base_color.outputs[0].default_value = (0.8, 0.45, 0.15, 1.0)  # Copper orange
    
    mix_rgb = nodes.new('ShaderNodeMixRGB')
    mix_rgb.location = (-200, 100)
    
    # Bump untuk surface roughness detail
    bump = nodes.new('ShaderNodeBump')
    bump.location = (0, -150)
    bump.inputs['Strength'].default_value = 0.4
    
    # Principled BSDF shader
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (200, 0)
    bsdf.inputs['Metallic'].default_value = 1.0      # Fully metallic
    bsdf.inputs['Roughness'].default_value = 0.3     # Slightly polished
    
    # Material Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (500, 0)
    
    # Link nodes
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], mix_rgb.inputs['Color1'])
    links.new(base_color.outputs['Color'], mix_rgb.inputs['Color2'])
    links.new(mix_rgb.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    print(f"✓ Material '{name}' created (7 nodes: Principled, Noise, ColorRamp, Bump, MixRGB, TexCoord, RGB)")
    return mat


def create_leather_material(name="Leather"):
    """
    Membuat material kulit/leather dengan texture
    Nodes: Principled BSDF, Noise, ColorRamp, Bump, MixRGB (5+ nodes)
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Texture Coordinate
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    # Noise untuk leather grain texture
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-600, 0)
    noise.inputs['Scale'].default_value = 40.0
    noise.inputs['Detail'].default_value = 8.0
    
    # ColorRamp untuk leather color variation
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-400, 0)
    colorramp.color_ramp.elements[0].color = (0.15, 0.1, 0.08, 1.0)   # Dark brown
    colorramp.color_ramp.elements[1].color = (0.35, 0.25, 0.18, 1.0)  # Light brown
    
    # Base leather color
    leather_color = nodes.new('ShaderNodeRGB')
    leather_color.location = (-500, 200)
    leather_color.outputs[0].default_value = (0.25, 0.18, 0.12, 1.0)
    
    # Mix untuk combine colors
    mix_rgb = nodes.new('ShaderNodeMixRGB')
    mix_rgb.location = (-200, 100)
    mix_rgb.blend_type = 'MULTIPLY'
    
    # Bump untuk leather surface detail
    bump = nodes.new('ShaderNodeBump')
    bump.location = (0, -150)
    bump.inputs['Strength'].default_value = 0.6
    
    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (200, 0)
    bsdf.inputs['Metallic'].default_value = 0.0
    bsdf.inputs['Roughness'].default_value = 0.5  # Leather is somewhat rough
    
    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (500, 0)
    
    # Link
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], mix_rgb.inputs['Color1'])
    links.new(leather_color.outputs['Color'], mix_rgb.inputs['Color2'])
    links.new(mix_rgb.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    print(f"✓ Material '{name}' created (8 nodes)")
    return mat


def create_bark_material(name="Bark"):
    """
    Membuat material kulit pohon/bark organik
    Nodes: Principled BSDF, Noise, Voronoi, ColorRamp, Bump (5+ nodes)
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Texture Coordinate
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-900, 0)
    
    # Mapping untuk scale control
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-700, 0)
    mapping.inputs['Scale'].default_value = (8.0, 8.0, 8.0)
    
    # Noise untuk organic variation
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-500, 100)
    noise.inputs['Scale'].default_value = 15.0
    noise.inputs['Detail'].default_value = 5.0
    
    # Voronoi untuk bark cell pattern
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-500, -200)
    voronoi.feature = 'DISTANCE_TO_EDGE'
    voronoi.inputs['Scale'].default_value = 20.0
    
    # ColorRamp untuk bark colors
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-200, 0)
    colorramp.color_ramp.elements[0].color = (0.1, 0.08, 0.05, 1.0)   # Dark bark
    colorramp.color_ramp.elements[1].color = (0.3, 0.25, 0.15, 1.0)   # Light bark
    
    # Bump untuk surface texture
    bump = nodes.new('ShaderNodeBump')
    bump.location = (100, -150)
    bump.inputs['Strength'].default_value = 0.7
    
    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (300, 0)
    bsdf.inputs['Base Color'].default_value = (0.2, 0.15, 0.08, 1.0)
    bsdf.inputs['Metallic'].default_value = 0.0
    bsdf.inputs['Roughness'].default_value = 0.8
    
    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (600, 0)
    
    # Link
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    links.new(mapping.outputs['Vector'], voronoi.inputs['Vector'])
    links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
    links.new(voronoi.outputs['Distance'], bump.inputs['Height'])
    links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    print(f"✓ Material '{name}' created (8 nodes)")
    return mat


def create_jade_material(name="Jade_Crystal"):
    """
    Membuat material jade/crystal transparent
    Nodes: Principled BSDF, Mix Shader, Transparent BSDF, LayerWeight, RGB, Output (6+ nodes)
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Jade base color
    jade_color = nodes.new('ShaderNodeRGB')
    jade_color.location = (-600, 200)
    jade_color.outputs[0].default_value = (0.2, 0.6, 0.4, 1.0)  # Green jade
    
    # Principled BSDF untuk reflections
    bsdf_principal = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf_principal.location = (-200, 100)
    bsdf_principal.inputs['Base Color'].default_value = (0.2, 0.6, 0.4, 1.0)
    
    # Handle Transmission parameter yang berbeda di Blender 3.x vs 4.x
    if 'Transmission Weight' in bsdf_principal.inputs:
        # Blender 4.x
        bsdf_principal.inputs['Transmission Weight'].default_value = 1.0
    elif 'Transmission' in bsdf_principal.inputs:
        # Blender 3.x
        bsdf_principal.inputs['Transmission'].default_value = 1.0
    
    bsdf_principal.inputs['IOR'].default_value = 1.66  # Jade IOR
    bsdf_principal.inputs['Roughness'].default_value = 0.05
    
    # Transparent BSDF untuk translucency
    bsdf_transparent = nodes.new('ShaderNodeBsdfTransparent')
    bsdf_transparent.location = (-200, -100)
    bsdf_transparent.inputs['Color'].default_value = (0.2, 0.6, 0.4, 0.7)
    
    # Layer Weight untuk fresnel effect
    layer_weight = nodes.new('ShaderNodeLayerWeight')
    layer_weight.location = (-500, 0)
    layer_weight.inputs['Blend'].default_value = 0.5
    
    # Mix shader untuk combine reflective and transparent
    mix_shader = nodes.new('ShaderNodeMixShader')
    mix_shader.location = (100, 0)
    mix_shader.inputs['Fac'].default_value = 0.7  # More reflective
    
    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    # Link
    links.new(layer_weight.outputs['Facing'], mix_shader.inputs['Fac'])
    links.new(bsdf_principal.outputs['BSDF'], mix_shader.inputs[1]) 
    links.new(bsdf_transparent.outputs['BSDF'], mix_shader.inputs[2])  
    links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])
    
    print(f"✓ Material '{name}' created (6 nodes: LayerWeight, MixShader, Principled, Transparent, RGB, Output)")
    return mat


def create_neon_material(name="Neon_Glow"):
    """
    Membuat material neon glowing/emissive
    Nodes: Principled BSDF, Emission, MixShader, ColorRamp, RGB, Output (6+ nodes)
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Neon color RGB
    neon_color = nodes.new('ShaderNodeRGB')
    neon_color.location = (-600, 200)
    neon_color.outputs[0].default_value = (0.0, 1.0, 0.7, 1.0)  # Cyan neon
    
    # Principled BSDF untuk base
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (-200, 100)
    bsdf.inputs['Base Color'].default_value = (0.0, 0.3, 0.2, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.1
    
    # Emission shader untuk glow
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (-200, -100)
    emission.inputs['Color'].default_value = (0.0, 1.0, 0.7, 1.0)
    emission.inputs['Strength'].default_value = 3.0  # Strong glow
    
    # ColorRamp untuk control emission intensity
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-400, -200)
    colorramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)  # Dark
    colorramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)  # Bright
    
    # Mix shader untuk combine emission and BSDF
    mix_shader = nodes.new('ShaderNodeMixShader')
    mix_shader.location = (100, 0)
    mix_shader.inputs['Fac'].default_value = 0.8  # More emission
    
    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    # Link
    links.new(neon_color.outputs['Color'], emission.inputs['Color'])
    links.new(neon_color.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(emission.outputs['Emission'], mix_shader.inputs[1])
    links.new(bsdf.outputs['BSDF'], mix_shader.inputs[2])
    links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])
    
    print(f"✓ Material '{name}' created (6 nodes: RGB, Principled, Emission, ColorRamp, MixShader, Output)")
    return mat


def create_demo_objects():
    """Membuat 5 objek untuk demo material"""
    
    objects = {}
    
    # Sphere - Copper Metal
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(-4, 0, 0))
    objects['sphere'] = bpy.context.active_object
    objects['sphere'].name = "Material_Sphere"
    
    # Cube - Leather
    bpy.ops.mesh.primitive_cube_add(size=2.0, location=(-2, 0, 0))
    objects['cube'] = bpy.context.active_object
    objects['cube'].name = "Material_Cube"
    
    # Cylinder - Bark
    bpy.ops.mesh.primitive_cylinder_add(radius=0.8, depth=2.0, location=(0, 0, 0))
    objects['cylinder'] = bpy.context.active_object
    objects['cylinder'].name = "Material_Cylinder"
    
    # Torus - Jade
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.4, location=(2, 0, 0))
    objects['torus'] = bpy.context.active_object
    objects['torus'].name = "Material_Torus"
    
    # Monkey (Suzanne) - Neon
    bpy.ops.mesh.primitive_monkey_add(location=(4, 0, 0))
    objects['monkey'] = bpy.context.active_object
    objects['monkey'].name = "Material_Monkey"
    
    print("✓ 5 Objects created")
    return objects


def assign_material_to_object(obj, material):
    """Assign material ke object"""
    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)


def setup_scene():
    """Setup lighting dan camera"""
    
    # Delete existing lights
    for obj in bpy.data.objects:
        if obj.type == 'LIGHT':
            bpy.data.objects.remove(obj, do_unlink=True)
    
    # Add sun light
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 8))
    sun = bpy.context.active_object
    sun.name = "Sun"
    sun.data.energy = 2.0
    
    # Add fill light
    bpy.ops.object.light_add(type='AREA', location=(-3, -3, 5))
    fill = bpy.context.active_object
    fill.name = "Fill_Light"
    fill.data.energy = 1.0
    fill.data.size = 4.0
    
    # Delete existing cameras
    for obj in bpy.data.objects:
        if obj.type == 'CAMERA':
            bpy.data.objects.remove(obj, do_unlink=True)
    
    # Add camera
    bpy.ops.object.camera_add(location=(0, -10, 4))
    camera = bpy.context.active_object
    camera.name = "Camera"
    camera.rotation_euler = (1.1, 0, 0)
    bpy.context.scene.camera = camera
    
    # Set viewport shading
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'
    
    print("✓ Scene setup complete")


def print_material_info(materials, objects):
    """Print information tentang materials yang dibuat"""
    
    print("\n" + "="*70)
    print(" TUGAS 1: MATERIAL LIBRARY - SUMMARY")
    print("="*70 + "\n")
    
    print(" OBJECTS CREATED:")
    for key, obj in objects.items():
        print(f"  • {obj.name:20s} ({key.capitalize()})")
    
    print("\n MATERIALS CREATED:")
    
    material_info = [
        ("Copper_Rusty", "Sphere", "Metal with oxidation effect", 7),
        ("Leather", "Cube", "Fabric material with grain", 8),
        ("Bark", "Cylinder", "Organic tree bark texture", 8),
        ("Jade_Crystal", "Torus", "Transparent crystal material", 6),
        ("Neon_Glow", "Monkey", "Emissive glowing material", 6),
    ]
    
    for mat_name, obj_name, desc, node_count in material_info:
        mat = bpy.data.materials.get(mat_name)
        if mat:
            actual_nodes = len(mat.node_tree.nodes)
            print(f"\n  {mat_name:15s} → {obj_name:10s}")
            print(f"    Description: {desc}")
            print(f"    Nodes: {actual_nodes} (Required: ≥5)")
            print(f"    ✓ Status: {'PASS' if actual_nodes >= 5 else 'FAIL'}")
    
    print("\n" + "="*70)
    print(" TIPS:")
    print("  • Press 'Z' and select 'Rendered' for realistic rendering")
    print("  • Press Numpad 0 for camera view")
    print("  • Use Shader Editor (Shift+F3) to see node setup")
    print("  • Switch to Material Preview for better preview")
    print("="*70 + "\n")


def main():
    """Main function"""
    
    print("\n Starting Material Library Creation...\n")
    
    # Clean scene
    print("1. Clearing scene...")
    delete_all_objects()
    
    # Create materials
    print("\n2.  Creating materials...")
    materials = {
        'copper': create_copper_metal_material("Copper_Rusty"),
        'leather': create_leather_material("Leather"),
        'bark': create_bark_material("Bark"),
        'jade': create_jade_material("Jade_Crystal"),
        'neon': create_neon_material("Neon_Glow"),
    }
    
    # Create objects
    print("\n3. Creating objects...")
    objects = create_demo_objects()
    
    # Assign materials to objects
    print("\n4.  Assigning materials to objects...")
    assign_material_to_object(objects['sphere'], materials['copper'])
    assign_material_to_object(objects['cube'], materials['leather'])
    assign_material_to_object(objects['cylinder'], materials['bark'])
    assign_material_to_object(objects['torus'], materials['jade'])
    assign_material_to_object(objects['monkey'], materials['neon'])
    print("✓ All materials assigned")
    
    # Setup scene
    print("\n5. Setting up scene...")
    setup_scene()
    
    # Print summary
    print_material_info(materials, objects)

if __name__ == "__main__":
    main()