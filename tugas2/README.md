# Tugas 2: Procedural Texture Scene

## Deskripsi Tugas

**Objektif:** Membuat scene dengan 8+ objek dan 8 material procedural berbeda, menggunakan minimal 3 jenis texture nodes dan 1 material dengan displacement.

**Tema:** Natural - Forest Floor Environment

## Konsep & Implementasi

Tugas 2 mendemonstrasikan **advanced procedural texture creation** untuk environment building. Scene ini mensimulasikan realistic woodland forest floor dengan:

1. **Procedural Generation** - Semua materials dari mathematical functions (0 image textures)
2. **Material Variety** - 8 berbeda materials untuk diverse surfaces
3. **Technical Sophistication** - Displacement mapping untuk actual geometry deformation
4. **Environmental Coherence** - Semua materials fit dalam tema forest floor

## 8 Materials with Procedural Textures

### 1. **Dirt_Ground** - Tanah/Ground Base
- **Texture Nodes:** Noise + ColorRamp
- **Purpose:** Base ground terrain
- **Parameters:** Noise Scale 25.0, Detail 5.0
- **Colors:** Light brown (0.45, 0.35, 0.25) → Dark brown (0.2, 0.15, 0.08)
- **Roughness:** 0.8 (earthy)

### 2. **Stone_Rock** - Batu/Rock
- **Texture Nodes:** Voronoi + Noise + Bump
- **Purpose:** Rocky surfaces, stones, boulders
- **Technique:** Cellular pattern (Voronoi) + organic variation (Noise)
- **Parameters:** Voronoi Scale 10.0, Noise Scale 15.0
- **Colors:** Gray variations (0.3 → 0.6)
- **Roughness:** 0.85

### 3. **Wood_Log** - Kayu/Wood
- **Texture Nodes:** Wave (Rings) + Noise + Bump
- **Purpose:** Fallen logs, wood details
- **Technique:** Wave texture untuk tree growth rings + Noise untuk grain variation
- **Parameters:** Wave Scale 15.0, Distortion 2.0, Noise Scale 50.0
- **Colors:** Brown tones (0.5, 0.35, 0.15) → (0.25, 0.15, 0.05)
- **Roughness:** 0.5 (polished wood)

### 4. **Moss** - Lumut
- **Texture Nodes:** Noise + Voronoi + Bump
- **Purpose:** Moss coverage on surfaces
- **Technique:** Overlay blending dari Noise + Voronoi untuk growth pattern
- **Parameters:** Noise Scale 30.0, Voronoi Scale 20.0
- **Colors:** Green shades (0.1, 0.25, 0.08) → (0.3, 0.45, 0.15)
- **Roughness:** 0.7

### 5. **Dead_Leaves** - Daun Mati
- **Texture Nodes:** Noise + ColorRamp + Bump
- **Purpose:** Fallen leaves pile
- **Technique:** Simple noise-based variation untuk organic look
- **Parameters:** Noise Scale 35.0, Detail 7.0
- **Colors:** Brown/golden (0.35, 0.2, 0.1) → (0.65, 0.55, 0.2)
- **Roughness:** 0.6

### 6. **Clay_Soil** - Tanah Liat
- **Texture Nodes:** Noise + Bump
- **Purpose:** Clay earth texture
- **Technique:** Noise dengan strong bump untuk tactile surface
- **Parameters:** Noise Scale 20.0, Detail 4.0
- **Colors:** Reddish brown (0.35, 0.25, 0.2) → (0.65, 0.45, 0.3)
- **Roughness:** 0.75

### 7. **Lichen** - Lichen/Lichens
- **Texture Nodes:** Voronoi + Bump
- **Purpose:** Crusty growth on rocks
- **Technique:** Voronoi cellular pattern untuk cracked surface
- **Parameters:** Voronoi Scale 25.0, Feature F1
- **Colors:** Grayish-green (0.35, 0.35, 0.25) → (0.4, 0.45, 0.2)
- **Roughness:** 0.8

### 8. **Wet_Mud** - Lumpur Basah **WITH DISPLACEMENT**
- **Texture Nodes:** Noise + Displacement
- **Purpose:** Muddy areas with geometry detail
- **Technique:** Noise controls displacement for actual mesh deformation
- **Parameters:** Noise Scale 30.0, Displacement Scale 0.2
- **Colors:** Dark brown (0.1, 0.08, 0.05) → (0.3, 0.2, 0.1)
- **Key Feature:**  Displacement output untuk geometry modification
- **Note:** Grid object with 20×20 subdivisions untuk displacement to work
- **Roughness:** 0.6

## Texture Nodes Used

**Inventory:**
- **Noise Texture** (6×) - Organic variation for: Dirt, Stone, Wood, Moss, Dead Leaves, Clay
- **Voronoi Texture** (3×) - Cellular patterns for: Stone, Moss, Lichen
- **Wave Texture** (1×) - Ring patterns for: Wood
- **ColorRamp** (8×) - Color control pada semua 8 materials
- **Bump Mapping** (7×) - Surface detail untuk 7 dari 8 materials
- **Displacement** (1×) -  Geometry deformation pada Wet_Mud
- **Texture Coordinate & Mapping** - Coordinate system control

**Requirements Met:**
- ✓ Minimal 3 jenis texture nodes (Noise, Voronoi, Wave, ColorRamp, Bump, Displacement = 6 types used)
- ✓ Minimal 1 material dengan Displacement (Wet_Mud)
- ✓ 8 materials dengan procedural textures

## Scene Objects & Layout

| # | Object | Material | Location | Purpose |
|---|--------|----------|----------|---------|
| 1 | Ground Plane | Dirt_Ground | (0, 0, 0) | Base terrain |
| 2 | Stone Rock 1 | Stone_Rock | (-4, -4, 0.8) | Large boulder |
| 3 | Stone Rock 2 | Stone_Rock | (4, -4, 0.5) | Small rock |
| 4 | Wood Log | Wood_Log | (-4, 4, 0.5) | Fallen log |
| 5 | Moss Rock | Moss | (-4, 0, 0.7) | Covered surface |
| 6 | Dead Leaves | Dead_Leaves | (4, 4, 0.1) | Leaf pile |
| 7 | Clay Patch | Clay_Soil | (0, 0.2, 0.05) | Clay area |
| 8 | Wet Mud | Wet_Mud | (4, 0, 0) | Muddy ground |
| 9 | Lichen Object | Lichen | (0, -4, 0.3) | Crusty surface |

**Total:** 9 objects, 8 unique procedural materials

## Lighting & Environment

- **Sun Light:** 2.5 energy, positioned (5, 5, 8) - simulates forest canopy
- **Fill Light:** Area light 0.8 energy at (-5, -5, 4) - ambient illumination
- **World Background:** Greenish dark (0.3, 0.35, 0.3) - forest mood
- **Camera:** Positioned for scenic forest floor view

## Screenshot Requirements

```
tugas2/
├── README.md
├── tugas2_procedural_scene.py
└── screenshot/
    ├── screenshot_angle1.png       ← Render dari angle pertama
    ├── screenshot_angle2.png       ← Render dari angle berbeda
    └── screenshot_shader.png       ← Node setup dari material kompleks
```

---

**Blender Version:** 3.x & 4.x compatible  
**Status:** Complete
