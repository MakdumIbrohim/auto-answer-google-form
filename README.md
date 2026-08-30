# Dokumentasi Bot Auto-Answer Google Form

Project ini adalah script otomatisasi berbasis Python dan Selenium untuk mengisi kuesioner Google Form (Pre-test, Post-test, SUS) secara otomatis membaca data dari file CSV.

## 🚀 Persyaratan Sistem
1. Python 3.x terinstal.
2. Install library yang dibutuhkan: `pip install -r requirements.txt` (menginstal `selenium` dan `python-dotenv`).
3. Google Chrome dan ChromeDriver terbaru.

## 📂 Struktur File Utama
- `main.py`: Script utama untuk menjalankan otomatisasi pengisian Google Form.
- `data_responden.csv`: Contoh file data responden sebagai sumber input (sesuaikan nama file di dalam script).
- `.env.example`: Contoh file konfigurasi environment.

---

## 🛠️ PENGATURAN AWAL (SETUP)

Sebelum menjalankan script, Anda wajib mengatur tautan (link) Google Form di dalam file environment.
1. Buat file baru bernama `.env` di folder yang sama (atau copy dari `.env.example`).
2. Isi file `.env` dengan format berikut:
   ```env
   LINK_FORM=https://forms.gle/LinkAndaDisini
   ```

## 🛠️ PANDUAN MODIFIKASI KODE (CARA MENGUBAH INPUT)

Jika form Anda memiliki pertanyaan yang baru atau tata letaknya berubah, berikut adalah referensi kode ("cheat sheet") untuk melakukan modifikasi di dalam script.

### 1. Mengubah File CSV
Di bagian atas script `main.py`, terdapat variabel pengaturan file CSV.
```python
NAMA_FILE_CSV = 'data_responden.csv'
```

### 2. Input Teks (Jawaban Singkat / Paragraf)
Jika form meminta input teks seperti Nama, NIM, atau Alamat.
```python
# Mencari semua kotak input teks di halaman aktif
input_teks = driver.find_elements(By.XPATH, "//input[@type='text']")

# Mengisi kotak teks pertama (indeks 0)
if input_teks:
    input_teks[0].send_keys("Isi Teks Jawaban")

# Jika bentuknya paragraf (textarea)
input_paragraf = driver.find_elements(By.XPATH, "//textarea")
if input_paragraf:
    input_paragraf[0].send_keys("Isi jawaban paragraf panjang.")
```

### 3. Input Pilihan Ganda (Radio Button)
Untuk pertanyaan di mana Anda hanya bisa memilih satu dari beberapa opsi (misal: Laki-laki / Perempuan). 
Gunakan fungsi bawaan `klik_opsi_teks()` yang sudah dibuat di script.
```python
# Klik otomatis berdasarkan teks apa yang terlihat di layar
klik_opsi_teks(driver, "Laki-Laki")
klik_opsi_teks(driver, "Siswa/i")
```

### 4. Input Kotak Centang (Checkbox)
Untuk pertanyaan yang bisa dipilih lebih dari satu.
```python
# Cari semua kotak centang di halaman aktif
kotak_centang = driver.find_elements(By.XPATH, "//div[@role='checkbox']")

if kotak_centang:
    # Contoh 1: Klik kotak centang pertama
    driver.execute_script("arguments[0].click();", kotak_centang[0])

    # Contoh 2: Klik kotak centang secara acak (misal 2 pilihan)
    import random
    pilihan = random.sample(kotak_centang, 2)
    for kotak in pilihan:
        driver.execute_script("arguments[0].click();", kotak)
```

### 5. Input Skala Linear (Contoh: Skala 1-5 / Skala SUS)
Bentuknya biasanya baris radiogroup berurutan.
```python
# Ambil semua baris soal skala di halaman aktif
baris_skala = driver.find_elements(By.XPATH, "//div[@role='radiogroup']")

for baris in baris_skala:
    # Ambil semua pilihan (titik bulat) dalam 1 soal
    opsi = baris.find_elements(By.XPATH, ".//div[@role='radio']")
    
    if len(opsi) >= 5:
        # Pilihan dihitung dari Indeks 0 (skor 1) sampai Indeks 4 (skor 5)
        # Contoh: Jika ingin memilih angka 4, gunakan indeks 3.
        idx_pilihan = 3 
        driver.execute_script("arguments[0].click();", opsi[idx_pilihan])
```

### 6. Navigasi Halaman (Klik Tombol Berikutnya / Kembali / Kirim)
Gunakan fungsi bawaan `klik_tombol()` dengan menyebutkan persis nama tombolnya.
```python
# Pindah ke halaman selanjutnya
klik_tombol(driver, "Berikutnya")

# Kembali ke halaman sebelumnya
klik_tombol(driver, "Kembali")

# Mengirim form di halaman terakhir
klik_tombol(driver, "Kirim")
```


