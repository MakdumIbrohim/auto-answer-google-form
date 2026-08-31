# Auto-Answer Google Form Bot 🇮🇩

Project ini adalah script otomatisasi berbasis Python dan Selenium untuk mengisi kuesioner Google Form (Pre-test, Post-test, SUS) secara otomatis membaca data dari file CSV.

## Persyaratan Sistem
Sebelum menggunakan project ini, pastikan komputer Anda memiliki:
1. **Python 3.x** sudah terinstal.
2. Browser **Google Chrome** versi terbaru.

## Struktur File Utama
- `main.py`: Script utama otomatisasi pengisian form.
- `data_responden.csv`: Contoh file data responden.
- `.env.example`: Contoh format konfigurasi tautan (link).
- `requirements.txt`: Daftar library Python yang dibutuhkan.

---

## TUTORIAL PENGGUNAAN TAHAP DEMI TAHAP

Ikuti panduan berikut dari awal hingga program berhasil dijalankan.

### Langkah 1: Persiapan Lingkungan Virtual (Virtual Environment)
Sangat disarankan menjalankan script ini di dalam lingkungan virtual agar library tidak bentrok.
- Buka terminal (atau Command Prompt di Windows).
- Masuk ke folder project ini.
- Buat environment baru:
  ```bash
  python3 -m venv env
  ```
- Aktifkan environment:
  - **Linux / MacOS**: `source env/bin/activate`
  - **Windows**: `env\Scripts\activate`

### Langkah 2: Instalasi Library
Setelah *env* aktif, instal semua pustaka pendukung (Selenium & Dotenv) melalui file `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Langkah 3: Konfigurasi Tautan Form (.env)
Script ini mengambil link kuesioner dari file environment untuk alasan keamanan dan kerapian.
1. Buat file baru bernama persis `.env` di folder project ini (atau duplikat dari `.env.example`).
2. Masukkan URL Google Form Anda di dalam file `.env` tanpa spasi:
   ```env
   FORM_LINK=https://forms.gle/LinkAndaDisini
   ```

### Langkah 4: Jalankan Program
Pastikan Google Chrome sedang tidak membuka sesuatu yang mengunci profilnya (meski biasanya script ini membuka instance baru).
Eksekusi script utama:
```bash
python3 main.py
```

## PANDUAN MODIFIKASI KODE (CARA MENGUBAH INPUT)

Jika form Anda memiliki pertanyaan yang baru atau tata letaknya berubah, berikut adalah referensi kode ("cheat sheet") untuk melakukan modifikasi di dalam script.

### 1. Mengubah File CSV
Di bagian atas script `main.py`, terdapat variabel pengaturan file CSV.
```python
CSV_FILE_NAME = 'data_responden.csv'
```

### 2. Input Teks (Jawaban Singkat / Paragraf)
Jika form meminta input teks seperti Nama, NIM, atau Alamat.
```python
# Mencari semua kotak input teks di halaman aktif
name_input = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@type='text']")))

# Mengisi kotak teks pertama (indeks 0)
if name_input:
    name_input[0].send_keys("Isi Teks Jawaban")
```

### 3. Input Pilihan Ganda (Radio Button)
Untuk pertanyaan di mana Anda hanya bisa memilih satu dari beberapa opsi (misal: Laki-laki / Perempuan). 
Gunakan fungsi bawaan `click_radio()` atau `click_random_radio()`.
```python
# Klik otomatis berdasarkan urutan (misal opsi pertama = index 0)
click_radio(driver, "//div[@role='radiogroup']", 0)

# Klik otomatis opsi secara acak
click_random_radio(driver, "//div[@role='radiogroup']")
```

### 4. Input Kotak Centang (Checkbox)
Untuk pertanyaan yang bisa dipilih lebih dari satu.
```python
# Cari semua kotak centang di halaman aktif
checkboxes = driver.find_elements(By.XPATH, "//div[@role='checkbox']")

if checkboxes:
    # Contoh: Klik kotak centang secara acak (1-3 pilihan)
    import random
    choices = random.sample(checkboxes, min(3, len(checkboxes)))
    for box in choices:
        driver.execute_script("arguments[0].click();", box)
```

### 5. Input Skala Linear (Contoh: Skala 1-5 / Skala SUS)
Bentuknya biasanya baris radiogroup berurutan.
```python
# Ambil semua baris soal skala di halaman aktif
scale_rows = driver.find_elements(By.XPATH, "//div[@role='radiogroup']")

for row in scale_rows:
    # Ambil semua pilihan (titik bulat) dalam 1 soal
    options = row.find_elements(By.XPATH, ".//div[@role='radio']")
    
    if options:
        # Memilih secara acak
        driver.execute_script("arguments[0].click();", random.choice(options))
```

### 6. Navigasi Halaman (Klik Tombol Berikutnya / Kembali / Kirim)
Gunakan fungsi bawaan `click_button()` dengan menyebutkan persis nama tombolnya.
```python
# Pindah ke halaman selanjutnya
click_button(driver, "Berikutnya")

# Mengirim form di halaman terakhir
click_button(driver, "Kirim")
```

---
---

# Auto-Answer Google Form Bot 🇬🇧

This project is a Python and Selenium-based automation script for automatically filling out Google Form questionnaires (Pre-test, Post-test, SUS) by reading data from a CSV file.

## System Requirements
Before using this project, ensure your computer has:
1. **Python 3.x** installed.
2. The latest version of the **Google Chrome** browser.

## Main File Structure
- `main.py`: The core script for form filling automation.
- `data_responden.csv`: Sample respondent data file.
- `.env.example`: Example format for link configuration.
- `requirements.txt`: List of required Python libraries.

---

## STEP-BY-STEP USAGE TUTORIAL

Follow this guide from scratch until the program runs successfully.

### Step 1: Virtual Environment Setup
It is highly recommended to run this script inside a virtual environment to prevent library conflicts.
- Open your terminal (or Command Prompt on Windows).
- Navigate to this project folder.
- Create a new environment:
  ```bash
  python3 -m venv env
  ```
- Activate the environment:
  - **Linux / MacOS**: `source env/bin/activate`
  - **Windows**: `env\Scripts\activate`

### Step 2: Install Libraries
Once the *env* is active, install all required dependencies (Selenium & Dotenv) via the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### Step 3: Form Link Configuration (.env)
This script fetches the questionnaire link from an environment file for security and neatness.
1. Create a new file named exactly `.env` in this project folder (or duplicate from `.env.example`).
2. Insert your Google Form URL inside the `.env` file without any spaces:
   ```env
   FORM_LINK=https://forms.gle/YourLinkHere
   ```

### Step 4: Run the Program
Ensure Google Chrome is not locking its profile with another active session (though this script usually spawns a new instance).
Execute the main script:
```bash
python3 main.py
```

## CODE MODIFICATION GUIDE (HOW TO CHANGE INPUTS)

If your form has new questions or the layout changes, here is a code reference ("cheat sheet") for making modifications in the script.

### 1. Changing the CSV File
At the top of the `main.py` script, there is a configuration variable for the CSV file.
```python
CSV_FILE_NAME = 'data_responden.csv'
```

### 2. Text Input (Short Answer / Paragraph)
If the form asks for text inputs like Name, Student ID, or Address.
```python
# Find all text input boxes on the active page
name_input = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@type='text']")))

# Fill the first text box (index 0)
if name_input:
    name_input[0].send_keys("Text Answer Here")
```

### 3. Multiple Choice (Radio Button)
For questions where you can only select one out of several options (e.g., Male / Female).
Use the built-in `click_radio()` or `click_random_radio()` functions.
```python
# Automatically click based on order (e.g., first option = index 0)
click_radio(driver, "//div[@role='radiogroup']", 0)

# Automatically click a random option
click_random_radio(driver, "//div[@role='radiogroup']")
```

### 4. Checkboxes
For questions where multiple choices can be selected.
```python
# Find all checkboxes on the active page
checkboxes = driver.find_elements(By.XPATH, "//div[@role='checkbox']")

if checkboxes:
    # Example: Click random checkboxes (1-3 choices)
    import random
    choices = random.sample(checkboxes, min(3, len(checkboxes)))
    for box in choices:
        driver.execute_script("arguments[0].click();", box)
```

### 5. Linear Scale (Example: 1-5 Scale / SUS Scale)
Usually structured as sequential radiogroup rows.
```python
# Get all scale question rows on the active page
scale_rows = driver.find_elements(By.XPATH, "//div[@role='radiogroup']")

for row in scale_rows:
    # Get all options (radio circles) within 1 question
    options = row.find_elements(By.XPATH, ".//div[@role='radio']")
    
    if options:
        # Select randomly
        driver.execute_script("arguments[0].click();", random.choice(options))
```

### 6. Page Navigation (Click Next / Back / Submit Buttons)
Use the built-in `click_button()` function by mentioning the exact button text.
```python
# Move to the next page
click_button(driver, "Berikutnya")

# Submit the form on the last page
click_button(driver, "Kirim")
```
