"""
Blender Python Script - Tugas 4: Advanced Shader Challenge
==========================================================

Objektif: Membuat reusable Node Group dengan 3+ parameter input dan 
mengimplementasikan teknik advanced (Fresnel & Bump Mapping).

Fitur:
- Reusable Node Group: "Advanced_Procedural_Shader"
- 3 Input Parameters: Base Color, Pattern Scale, Roughness
- Advanced Techniques: Fresnel (Layer Weight) & Bump Mapping
- 3 Materials: Ceramic_Pattern, Metallic_Tech, Matte_Organic

Tested: Blender 3.x & 4.x
"""

import bpy

def delete_all_objects():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def create_advanced_node_group():
    """Membuat Reusable Node Group"""
    group_name = "Advanced_Procedural_Shader"
    
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    
    # Buat group baru
    group = bpy.data.node_groups.new(group_name, 'ShaderNodeTree')
    
    # 1. Setup Input & Output Socket
    nodes = group.nodes
    links = group.links
    
    # Inputs
    if hasattr(group, "interface"): # lender 4
        group.interface.new_socket(name="Base Color", in_out='INPUT', socket_type='NodeSocketColor')
        group.interface.new_socket(name="Scale", in_out='INPUT', socket_type='NodeSocketFloat')
        group.interface.new_socket(name="Metallic", in_out='INPUT', socket_type='NodeSocketFloat')
        group.interface.new_socket(name="Roughness", in_out='INPUT', socket_type='NodeSocketFloat')
        group.interface.new_socket(name="Shader Output", in_out='OUTPUT', socket_type='NodeSocketShader')
    else: # Blender 3
        group.inputs.new('NodeSocketColor', 'Base Color')
        group.inputs.new('NodeSocketFloat', 'Scale')
        group.inputs.new('NodeSocketFloat', 'Metallic')
        group.inputs.new('NodeSocketFloat', 'Roughness')
        group.outputs.new('NodeSocketShader', 'Shader Output')

    input_node = nodes.new('NodeGroupInput')
    input_node.location = (-600, 0)
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (600, 0)

    # 2.Fresnel Effect (Layer Weight)
    layer_weight = nodes.new('ShaderNodeLayerWeight')
    layer_weight.location = (-200, 200)
    layer_weight.inputs['Blend'].default_value = 0.5

    # 3. Procedural Pattern Generation
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-400, -100)
    
    # 4. Bump Mapping
    bump = nodes.new('ShaderNodeBump')
    bump.location = (0, -200)
    bump.inputs['Strength'].default_value = 0.5

    # 5. Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (200, 0)

    # 6. Linking Nodes
    links.new(input_node.outputs['Base Color'], bsdf.inputs['Base Color'])
    links.new(input_node.outputs['Scale'], voronoi.inputs['Scale'])
    links.new(input_node.outputs['Metallic'], bsdf.inputs['Metallic'])
    links.new(input_node.outputs['Roughness'], bsdf.inputs['Roughness'])
    
    # Link Voronoi to Bump
    links.new(voronoi.outputs['Distance'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    
    # Mix Fresnel with Base Color (Optional highlight)
    mix_rgb = nodes.new('ShaderNodeMixRGB')
    mix_rgb.location = (0, 100)
    mix_rgb.blend_type = 'ADD'
    links.new(input_node.outputs['Base Color'], mix_rgb.inputs['Color1'])
    links.new(layer_weight.outputs['Fresnel'], mix_rgb.inputs['Color2'])
    links.new(mix_rgb.outputs['Color'], bsdf.inputs['Base Color'])

    # Final Output
    links.new(bsdf.outputs['BSDF'], output_node.inputs[0])
    
    return group

def create_material(name, group, params):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    group_node = nodes.new('ShaderNodeGroup')
    group_node.node_tree = group
    group_node.location = (0, 0)
    
    # Set Parameters
    group_node.inputs['Base Color'].default_value = params['color']
    group_node.inputs['Scale'].default_value = params['scale']
    group_node.inputs['Metallic'].default_value = params['metallic']
    group_node.inputs['Roughness'].default_value = params['roughness']
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    links.new(group_node.outputs[0], output.inputs['Surface'])
    return mat

def setup_scene():
    delete_all_objects()
    group = create_advanced_node_group()
    
    # 3 Material conf
    materials_config = [
        {
            "name": "Ceramic_Pattern",
            "type": "SPHERE",
            "pos": (-4, 0, 0),
            "params": {"color": (1.0, 1.0, 1.0, 1.0), "scale": 15.0, "metallic": 0.0, "roughness": 0.1}
        },
        {
            "name": "Metallic_Tech",
            "type": "CUBE",
            "pos": (0, 0, 0),
            "params": {"color": (0.1, 0.4, 0.8, 1.0), "scale": 50.0, "metallic": 1.0, "roughness": 0.2}
        },
        {
            "name": "Matte_Organic",
            "type": "ICOSPHERE",
            "pos": (4, 0, 0),
            "params": {"color": (0.3, 0.6, 0.2, 1.0), "scale": 5.0, "metallic": 0.0, "roughness": 0.8}
        }
    ]
    
    for cfg in materials_config:
        # Create Object
        if cfg["type"] == "SPHERE":
            bpy.ops.mesh.primitive_uv_sphere_add(location=cfg["pos"])
        elif cfg["type"] == "CUBE":
            bpy.ops.mesh.primitive_cube_add(location=cfg["pos"])
        elif cfg["type"] == "ICOSPHERE":
            bpy.ops.mesh.primitive_ico_sphere_add(location=cfg["pos"])
        
        obj = bpy.context.active_object
        obj.name = cfg["name"]
        
        # Create and Assign Material
        mat = create_material(cfg["name"], group, cfg["params"])
        obj.data.materials.append(mat)
        
        # Smooth shading
        bpy.ops.object.shade_smooth()

    # Setup Lighting
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    bpy.ops.object.camera_add(location=(0, -12, 5))
    cam = bpy.context.active_object
    cam.rotation_euler = (1.2, 0, 0)
    bpy.context.scene.camera = cam

if __name__ == "__main__":
    setup_scene()
