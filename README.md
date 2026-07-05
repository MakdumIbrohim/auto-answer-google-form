# Auto Answer Google Form

Script otomatis untuk mengisi kuesioner Google Form menggunakan data dari CSV.

## Cara Penggunaan

### Langkah Terakhir - Jalankan Script
```
python main.py
```
Script akan membaca data dari `data_responden.csv` dan mengisi form secara otomatis untuk setiap responden.

### Persiapan - Edit Data Responden
Buka file `data_responden.csv` dan isi data responden sesuai format:

| nama | kelamin |
|------|---------|
| Ananda Lestari | P |
| Arif Kusuma | L |

Kolom `nama` dan `kelamin` wajib diisi. Gunakan **L** untuk Laki-laki dan **P** untuk Perempuan.

### Persiapan - Ubah Link Form (Opsional)
Jika ingin menggunakan form lain, edit variabel `link_form` di `main.py` atau `money-mind.py`.

### Persiapan - Install Dependencies
```
pip install -r requirements.txt
```

Pastikan Google Chrome terinstal di komputer. ChromeDriver otomatis terpasang jika menggunakan Selenium versi terbaru.

## Catatan
- Script akan membuka browser secara otomatis
- Jangan tutup browser saat proses berjalan
- Setelah satu responden selesai, browser akan reload untuk responden berikutnya
