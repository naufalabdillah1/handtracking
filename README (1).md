# Hand Tracking Filter

Program webcam yang mengubah filter warna secara realtime berdasarkan
gestur tangan, menggunakan **OpenCV** + **MediaPipe**.

## Struktur File

```
hand-tracking-project/
├── main.py           # Program utama (jalankan ini)
├── hand.py           # Deteksi tangan & pengenalan gestur
├── selfie.py         # Filter warna & tampilan HUD
├── requirements.txt  # Daftar library yang dibutuhkan
├── .gitignore
└── README.md
```

## Instalasi

1. Pastikan Python 3.9–3.11 terpasang (MediaPipe belum selalu stabil di versi Python terbaru).
2. (Opsional tapi disarankan) buat virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```
3. Install dependency:
   ```bash
   pip install -r requirements.txt
   ```

## Menjalankan

```bash
python main.py
```

Jendela kamera akan terbuka. Tekan **q** untuk keluar.

## Gestur yang Dikenali

| Gestur              | Filter          |
|---------------------|-----------------|
| ✊ Kepal (0 jari)    | Invert          |
| ☝️ 1 jari terbuka    | Sepia           |
| ✌️ 2 jari terbuka    | Grayscale       |
| 🤟 3 jari terbuka    | Blur            |
| 🖐️ 5 jari terbuka    | Normal          |
| 🤏 Pinch (jempol+telunjuk dekat) | Rainbow Wave |

## Kustomisasi

- Tambah filter baru: buat fungsi `apply_xxx(frame)` di `selfie.py`, lalu
  daftarkan di dict `FILTERS`.
- Ubah sensitivitas deteksi: atur `detection_conf` / `tracking_conf` saat
  membuat `HandTracker(...)` di `main.py`.
