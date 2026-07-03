import time
import random
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--headless") 

link_form = 'https://docs.google.com/forms/d/e/1FAIpQLSc_2z6L6Wmc47NSBPBtf5WObBzE9MXobGTu4rNsc6MCgj4ytg/viewform'

file_csv = 'data_responden.csv'

# Memeriksa keberadaan file CSV
if not os.path.exists(file_csv):
    print(f"[ERROR] File '{file_csv}' tidak ditemukan. Pastikan file berada di folder yang sama.")
    exit()

# Membaca data dari CSV
data_responden = []
with open(file_csv, mode='r', encoding='utf-8-sig') as file:
    # utf-8-sig digunakan agar BOM (Byte Order Mark) dari Excel tidak ikut terbaca
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        if row['nama'].strip(): # Pastikan baris tidak kosong
            data_responden.append({
                'nama': row['nama'].strip(),
                'kelamin': row['kelamin'].strip().upper() # Jadikan huruf besar (L/P)
            })

print(f"[INFO] Ditemukan {len(data_responden)} data responden. Memulai otomatisasi...\n")

def isi_kuesioner(url, data_user):
    nama_responden = data_user['nama']
    kelamin_responden = data_user['kelamin']
    
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
    
    try:
        driver.get(url)
        time.sleep(3) 
        
        # ==========================================
        # HALAMAN 1
        # ==========================================
        print(f"[{nama_responden}] Sedang mengisi Halaman 1... (Kelamin: {kelamin_responden})")
        
        # 1. Input Nama
        input_nama = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@type='text']")))
        input_nama[0].send_keys(nama_responden)
        
        # 2. Radio Buttons Halaman 1
        radiogroups_h1 = driver.find_elements(By.XPATH, "//div[@role='radiogroup']")
        
        # --- LOGIKA JENIS KELAMIN DARI CSV ---
        opsi_kelamin = radiogroups_h1[0].find_elements(By.XPATH, ".//div[@role='radio']")
        # Di Google Form Anda: Index 0 = Laki-Laki, Index 1 = Perempuan
        index_kelamin = 0 if kelamin_responden == 'L' else 1
        driver.execute_script("arguments[0].click();", opsi_kelamin[index_kelamin])
        
        # --- USIA (Acak) ---
        opsi_usia = radiogroups_h1[1].find_elements(By.XPATH, ".//div[@role='radio']")
        driver.execute_script("arguments[0].click();", random.choice(opsi_usia))
        
        # --- PERNAH AKSES (Selalu 'Ya' / Index 0) ---
        opsi_akses = radiogroups_h1[2].find_elements(By.XPATH, ".//div[@role='radio']")
        driver.execute_script("arguments[0].click();", opsi_akses[0])
        
        btn_next_1 = driver.find_element(By.XPATH, "//div[@role='button']//span[text()='Next' or text()='Berikutnya']")
        driver.execute_script("arguments[0].click();", btn_next_1)
        
        # ==========================================
        # HALAMAN 2
        # ==========================================
        print(f"[{nama_responden}] Sedang mengisi Halaman 2...")
        time.sleep(2) 
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='radiogroup']")))
        
        radiogroups_h2 = driver.find_elements(By.XPATH, "//div[@role='radiogroup']")
        opsi_peran = radiogroups_h2[0].find_elements(By.XPATH, ".//div[@role='radio']")
        
        # --- PERUBAHAN DI SINI ---
        # Memilih opsi ke-3 yaitu "Masyarakat Umum" (Index 2)
        driver.execute_script("arguments[0].click();", opsi_peran[2])
        
        checkboxes = driver.find_elements(By.XPATH, "//div[@role='checkbox']")
        pilihan_terpilih = random.sample(checkboxes, random.randint(1, 3))
        for box in pilihan_terpilih:
            driver.execute_script("arguments[0].click();", box)
            
        btn_next_2 = driver.find_element(By.XPATH, "//div[@role='button']//span[text()='Next' or text()='Berikutnya']")
        driver.execute_script("arguments[0].click();", btn_next_2)
        
        # ==========================================
        # HALAMAN 3
        # ==========================================
        print(f"[{nama_responden}] Sedang mengisi Halaman 3 (Skala UEQ)...")
        time.sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='radiogroup']")))
        
        baris_grid_ueq = driver.find_elements(By.XPATH, "//div[@role='radiogroup']")
        for baris in baris_grid_ueq:
            opsi_skala = baris.find_elements(By.XPATH, ".//div[@role='radio']")
            driver.execute_script("arguments[0].click();", random.choice(opsi_skala))
            
        btn_submit = driver.find_element(By.XPATH, "//div[@role='button']//span[text()='Submit' or text()='Kirim']")
        driver.execute_script("arguments[0].click();", btn_submit)
        
        print(f"[SUKSES] Kuesioner atas nama '{nama_responden}' BERHASIL dikirim!\n")
        time.sleep(3) 
        driver.quit() 
        
    except Exception as e:
        print(f"[GAGAL] Terjadi error saat mengisi atas nama '{nama_responden}'.")
        print(f"Pesan Error: {e}")
        print("Browser dibiarkan terbuka selama 30 detik agar Anda bisa mengecek masalahnya...\n")
        time.sleep(30) 
        driver.quit()

# Eksekusi Loop
for index, data in enumerate(data_responden):
    print(f"--- Memproses Responden {index + 1}/{len(data_responden)} ---")
    isi_kuesioner(link_form, data)
    time.sleep(2)

print("[SELESAI] Seluruh data CSV telah diproses.")