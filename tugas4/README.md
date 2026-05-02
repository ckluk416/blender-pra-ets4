# Tugas 4: Advanced Shader Challenge

## Deskripsi Tugas

**Objektif:** Membuat sebuah **Reusable Node Group** yang kompleks dengan param input yang fleksibel dan mengimplementasikan teknik shader tingkat lanjut

## Implementasi Node Group

Saya membuat node group bernama **"Advanced_Procedural_Shader"** yg dirancang untuk menghasilkan tekstur prosedural berbasis pola Voronoi dengan kontrol penuh atas aspek visualnya.

### Input Parameters:
1. **Base Color:** Warna dasar material.
2. **Scale:** Mengontrol kerapatan pola tekstur (Voronoi).
3. **Metallic:** Menentukan sifat konduktifitas material (0.0 - 1.0).
4. **Roughness:** Mengontrol tingkat kehalusan permukaan.

### Advanced Techniques:
1. **Fresnel Effect (Layer Weight):** Menambahkan kilau dinamis pada pov miring (edges).
2. **Bump Mapping:** Mengonversi data prosedural Voronoi menjadi informasi ketinggian (height map) untuk memberikan tekstur fisik semu pada permukaan objek.

## 3 Material Variations

Menggunakan satu Node Group yang sama, saya menghasilkan 3 material unik melalui variasi parame:

1. **Ceramic_Pattern (Sphere):**
   - Material non-metalik berwarna putih.
   - Pola halus dengan roughness rendah (mengkilap).

2. **Metallic_Tech (Cube):**
   - Material fully metallic (1.0) berwarna biru.
   - Skala pola sangat tinggi (kecil-kecil).
   - menunjukan penggunaan Bump Mapping pada permukaan logam.

3. **Matte_Organic (Icosphere):**
   - Material organic berwarna hijau.
   - Skala pola rendah (besar) dengan roughness tinggi (0.8).

---

**Blender Version:** 3.x & 4.x compatible  
**Status:** Complete
