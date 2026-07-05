import time
import random
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Konfigurasi Browser
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--headless") # Aktifkan jika tidak ingin melihat browser terbuka

link_form = ''
file_csv = 'data_responden.csv'

# 1. Memeriksa keberadaan file CSV
if not os.path.exists(file_csv):
    print(f"[ERROR] File '{file_csv}' tidak ditemukan. Pastikan file berada di folder yang sama.")
    exit()

# 2. Membaca data nama dari CSV
data_responden = []
with open(file_csv, mode='r', encoding='utf-8-sig') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        if row.get('nama') and row['nama'].strip(): # Pastikan kolom nama ada dan tidak kosong
            data_responden.append(row['nama'].strip())

print(f"[INFO] Ditemukan {len(data_responden)} data responden. Memulai otomatisasi...\n")

# 3. Inisialisasi WebDriver di LUAR loop agar lebih cepat dan hemat RAM
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

def isi_kuesioner(url, nama_responden):
    try:
        driver.get(url)
        time.sleep(2) 
        
        # ==========================================
        # HALAMAN 1: IDENTITAS
        # ==========================================
        print(f"[{nama_responden}] Mengisi Halaman 1...")
        
        # 1. Input Nama Lengkap
        input_nama = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
        input_nama.send_keys(nama_responden)
        
        # Ambil semua grup radio button di Halaman 1
        radiogroups_h1 = driver.find_elements(By.XPATH, "//div[@role='radiogroup']")
        
        # 2. Pilih Usia Secara Acak (Index 0: <20, Index 1: 20-30, Index 2: >30)
        opsi_usia = radiogroups_h1[0].find_elements(By.XPATH, ".//div[@role='radio']")
        driver.execute_script("arguments[0].click();", random.choice(opsi_usia))
        
        # 3. Pilih Pekerjaan Secara Acak (Index 0 s.d 3 untuk menghindari pilihan manual 'Yang lain')
        opsi_pekerjaan = radiogroups_h1[1].find_elements(By.XPATH, ".//div[@role='radio']")
        # Memilih acak antara Pelajar, Karyawan, PNS, atau Wiraswasta
        driver.execute_script("arguments[0].click();", random.choice(opsi_pekerjaan[:4]))
        
        # Klik Tombol Berikutnya
        btn_next = driver.find_element(By.XPATH, "//div[@role='button']//span[text()='Berikutnya' or text()='Next']")
        driver.execute_script("arguments[0].click();", btn_next)
        
        # ==========================================
        # HALAMAN 2: KUESIONER UTAMA (SUS)
        # ==========================================
        print(f"[{nama_responden}] Mengisi Halaman 2 (Skala SUS)...")
        time.sleep(2) 
        
        # Tunggu sampai radio button halaman 2 termuat
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='radiogroup']")))
        
        # Ada 10 baris pertanyaan SUS di halaman ini
        pertanyaan_sus = driver.find_elements(By.XPATH, "//div[@role='radiogroup']")
        
        for index, baris in enumerate(pertanyaan_sus):
            opsi_skala = baris.find_elements(By.XPATH, ".//div[@role='radio']")
            
            # Strategi Pengisian SUS Acak yang Realistis:
            # Pertanyaan Ganjil (1,3,5,7,9) bernada positif -> cenderung skor tinggi (4 atau 5)
            # Pertanyaan Genap (2,4,6,8,10) bernada negatif -> cenderung skor rendah (1 atau 2)
            if (index + 1) % 2 != 0:
                pilihan_skala = random.choice([opsi_skala[3], opsi_skala[4]]) # Nilai 4 atau 5
            else:
                pilihan_skala = random.choice([opsi_skala[0], opsi_skala[1]]) # Nilai 1 atau 2
                
            driver.execute_script("arguments[0].click();", pilihan_skala)
            
        # Jeda acak tipis agar terlihat natural sebelum submit
        time.sleep(random.uniform(1.0, 2.5))
        
        # Klik Tombol Kirim
        btn_submit = driver.find_element(By.XPATH, "//div[@role='button']//span[text()='Kirim' or text()='Submit']")
        driver.execute_script("arguments[0].click();", btn_submit)
        
        print(f"[SUKSES] Kuesioner atas nama '{nama_responden}' BERHASIL dikirim!\n")
        time.sleep(2)
        
    except Exception as e:
        print(f"[GAGAL] Terjadi error saat mengisi atas nama '{nama_responden}'.")
        print(f"Pesan Error: {e}")
        print("Membuka ulang formulir untuk responden berikutnya...\n")
        time.sleep(5)

# 4. Eksekusi Loop Responden
for index, nama in enumerate(data_responden):
    print(f"--- Memproses Responden {index + 1}/{len(data_responden)} ---")
    isi_kuesioner(link_form, nama)

# Tutup browser setelah semua selesai
driver.quit()
print("[SELESAI] Seluruh data CSV telah diproses.")