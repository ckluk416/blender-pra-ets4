# Tugas 1: Material Library

## Deskripsi Tugas

**Objektif:** Membuat library 5 material berbeda dengan karakteristik unik, masing-masing menggunakan minimal 5 shader nodes.

## Konsep & Implementasi

Tugas 1 mendemonstrasikan **fundamental material creation** menggunakan Blender's Principled BSDF shader. Setiap material dirancang untuk menampilkan:

1. **Material Diversity** - Berbagai tipe material (metal, fabric, organik, transparent, emissive)
2. **Node Complexity** - Setiap material minimal 5 nodes yang bekerja sinergis
3. **Physical Accuracy** - Properti yang realistis (metallic, roughness, IOR, transmission)
4. **Visual Distinctiveness** - Setiap material terlihat jelas berbeda dari yang lain

## 5 Materials Created

### 1. **Copper_Rusty** (Sphere) - Logam dengan Oxidation
- **Nodes:** 7 (TexCoord, Noise, ColorRamp, RGB, MixRGB, Bump, Principled, Output)
- **Karakteristik:**
  - Material logam (Metallic = 1.0)
  - Noise texture untuk variasi oxidation
  - Warna berubah dari copper orange ke green patina
  - Bump mapping untuk surface roughness detail
  - Roughness = 0.3 (polished metal)
- **Teknik:** Procedural color mixing dengan noise-based control

### 2. **Leather** (Cube) - Kain/Kulit
- **Nodes:** 8 (TexCoord, Noise, ColorRamp, RGB, MixRGB, Bump, Principled, Output)
- **Karakteristik:**
  - Non-metallic (Metallic = 0.0)
  - Noise untuk leather grain texture
  - Brown color variations dari dark ke light
  - MixRGB dengan MULTIPLY blend mode untuk realistic darkening
  - Roughness = 0.5 (semi-rough fabric)
- **Teknik:** Blended texture mixing untuk authentic material appearance

### 3. **Bark** (Cylinder) - Kulit Pohon Organik
- **Nodes:** 8 (TexCoord, Mapping, Noise, Voronoi, ColorRamp, Bump, Principled, Output)
- **Karakteristik:**
  - Organic texture dari 2 jenis noise
  - Voronoi untuk bark cell pattern
  - Dark brown color untuk tree bark
  - Roughness = 0.8 (very rough natural material)
  - Mapping node untuk precise scale control
- **Teknik:** Layered procedural textures (Noise + Voronoi) untuk complexity

### 4. **Jade_Crystal** (Torus) - Transparent Crystal
- **Nodes:** 6 (RGB, Principled, Transparent BSDF, LayerWeight, MixShader, Output)
- **Karakteristik:**
  - Transparent material dengan Transmission Weight = 1.0
  - IOR = 1.66 (jade refractive index)
  - Green color (0.2, 0.6, 0.4)
  - LayerWeight untuk fresnel effect (reflection angle control)
  - MixShader untuk combine reflective dan transparent aspects
- **Teknik:** Advanced shader mixing - demonstrasi transparent material workflow

### 5. **Neon_Glow** (Monkey/Suzanne) - Emissive Material
- **Nodes:** 6 (RGB, Principled, Emission, ColorRamp, MixShader, Output)
- **Karakteristik:**
  - Emissive shader dengan Strength = 3.0
  - Cyan neon color (0.0, 1.0, 0.7)
  - MixShader untuk blend emission dengan BSDF
  - Glow effect untuk glowing appearance
  - ColorRamp untuk intensity control
- **Teknik:** Shader mixing - menggabungkan diffuse dan emissive properties

## Objects & Composition

| Object | Material | Position | Purpose |
|--------|----------|----------|---------|
| Sphere | Copper_Rusty | (-4, 0, 0) | Metal demonstration |
| Cube | Leather | (-2, 0, 0) | Fabric/fabric-like |
| Cylinder | Bark | (0, 0, 0) | Organic material |
| Torus | Jade_Crystal | (2, 0, 0) | Transparent material |
| Monkey | Neon_Glow | (4, 0, 0) | Emissive material |

**Total:** 5 objects, 5 materials, 35 shader nodes

## Screenshot Requirements

```
tugas1/
├── README.md
├── tugas1_material_library.py
└── screenshot/
    ├── screenshot_viewport.png     ← Full viewport dengan 5 objek
    └── screenshot_shader.png       ← Salah satu material node setup
```

---

**Blender Version:** 3.x & 4.x compatible  
**Status:** Complete
