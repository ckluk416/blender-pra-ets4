# Tugas 3: UV Mapping Project

## Deskripsi Tugas

**Objektif:** Praktik UV unwrapping dan texture painting preparation pada objek kompleks dengan multiple parts.

## Konsep & Implementasi

Tugas 3 mendemonstrasikan **fundamental UV mapping techniques** untuk persiapan texturing. Fokus pada:

1. **Seam Placement** - Strategic edge marking untuk minimal distortion
2. **Unwrapping Methods** - Smart UV project dengan optimal island packing
3. **Texture Verification** - Checker pattern untuk distortion checking
4. **Layout Export** - UV layout sebagai reference untuk texturing

## Objek yang Digunakan

### **Chair (Kursi)** - Furniture dengan Multiple Parts
- **Parts:** 6 komponen (seat, back, 4 legs)
- **Kompleksitas:** Organic shapes dengan sharp angles
- **UV Challenge:** Multiple disconnected parts yang perlu di-pack optimal

## Proses UV Mapping

### 1. **Seam Marking**
- **Metode:** Mark seams by angle (threshold: 30°)
- **Lokasi Seams:** Antara seat-back, seat-legs, back-legs
- **Tujuan:** Minimal visible seams pada surface yang terlihat

### 2. **UV Unwrapping**
- **Metode:** Smart UV Project
- **Parameter:**
  - Angle limit: 66°
  - Island margin: 0.02
  - Stretch to bounds: True
- **Hasil:** 6 UV islands terpisah untuk setiap part

### 3. **Island Packing**
- **Teknik:** Automatic packing dengan rotation optimization
- **Margin:** 0.02 untuk texel spacing
- **Coverage:** Optimal use of UV space (0-1 range)

### 4. **Verification**
- **Material:** Checker texture dengan 10x10 scale
- **Purpose:** Visual check untuk distortion dan stretching
- **Export:** UV layout sebagai PNG (1024x1024)



## Struktur Folder `tugas3`

```
tugas3/
├── tugas3_uv_mapping.py
├── README.md
└── screenshot/
    ├── screenshot_uv_editor.png
    ├── screenshot_viewport_checker.png
    └── uv_layout.png
```

---

*Tested on Blender 3.x & 4.x*