import time
import random
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# ==========================================
# PENGATURAN - EDIT SESUAI KEBUTUHAN ANDA
# ==========================================

# URL Google Form yang ingin diisi
LINK_FORM = 'https://docs.google.com/forms/d/e/1FAIpQLSc_qOMnarp0AI93Nd1WmiWRGrzgpiFsS5MIY_8pZ41Eysr6Vg/viewform?pli=1'

# Nama file CSV yang berisi data responden
NAMA_FILE_CSV = 'data_responden.csv'

# Nama kolom di dalam file CSV (harus sesuai dengan header CSV)
KOLOM_NAMA = 'nama'
KOLOM_KELAMIN = 'kelamin'

# ==========================================
# PENGATURAN LANJUTAN (BIASANYA TIDAK PERLU DIUBAH)
# ==========================================

# Konfigurasi browser Chrome
OPSI_CHROME = Options()
OPSI_CHROME.add_argument("--start-maximized")
OPSI_CHROME.add_argument("--no-sandbox")
OPSI_CHROME.add_argument("--disable-dev-shm-usage")
OPSI_CHROME.add_argument("--disable-gpu")
OPSI_CHROME.add_argument("--remote-debugging-port=9222")
# Hapus tanda # di bawah jika ingin browser tidak terbuka (background)
# OPSI_CHROME.add_argument("--headless")

# Batas waktu menunggu elemen form muncul (detik)
BATAS_WAKTU = 10


# ==========================================
# FUNGSI-FUNGSI BANTUAN
# ==========================================

def buat_driver():
    """Membuat browser Chrome baru."""
    return webdriver.Chrome(options=OPSI_CHROME)


def cek_file_csv(path_file):
    """Memeriksa apakah file CSV tersedia."""
    if not os.path.exists(path_file):
        print(f"[ERROR] File CSV '{path_file}' tidak ditemukan!")
        print("Pastikan file berada di folder yang sama dengan program ini.")
        exit()


def baca_data_csv(path_file, kolom_nama, kolom_kelamin):
    """Membaca data responden dari file CSV."""
    data = []
    with open(path_file, mode='r', encoding='utf-8-sig') as file:
        pembaca = csv.DictReader(file)
        for baris in pembaca:
            if baris[kolom_nama].strip():
                data.append({
                    'nama': baris[kolom_nama].strip(),
                    'kelamin': baris[kolom_kelamin].strip().upper()
                })
    return data


def klik_opsi_teks(driver, teks):
    """Mengklik radio button berdasarkan teks yang terkandung."""
    try:
        xpath = f"//div[@role='radio' and (contains(@data-value, '{teks}') or contains(., '{teks}'))]"
        opsi = driver.find_elements(By.XPATH, xpath)
        if opsi:
            driver.execute_script("arguments[0].click();", opsi[0])
    except:
        pass


def klik_opsi_mayoritas(driver, teks_mayoritas):
    """Mengklik opsi teks 80%, sisanya klik opsi lain di grup yang sama."""
    try:
        xpath = f"//div[@role='radio' and (contains(@data-value, '{teks_mayoritas}') or contains(., '{teks_mayoritas}'))]"
        opsi = driver.find_elements(By.XPATH, xpath)
        if opsi:
            if random.random() < 0.8:  # 80% peluang
                driver.execute_script("arguments[0].click();", opsi[0])
            else:
                grup = opsi[0].find_element(By.XPATH, "./ancestor::div[@role='radiogroup']")
                semua_opsi = grup.find_elements(By.XPATH, ".//div[@role='radio']")
                opsi_lain = [o for o in semua_opsi if o != opsi[0]]
                if opsi_lain:
                    driver.execute_script("arguments[0].click();", random.choice(opsi_lain))
                else:
                    driver.execute_script("arguments[0].click();", opsi[0])
    except:
        pass


def klik_tombol(driver, teks_tombol):
    """Mengklik tombol berdasarkan teks yang ada di tombol."""
    xpath = f"//div[@role='button']//span[text()='{teks_tombol}']"
    tombol = driver.find_element(By.XPATH, xpath)
    driver.execute_script("arguments[0].click();", tombol)


# ==========================================
# ISI KUESIONER
# ==========================================

def isi_halaman_skala(driver):
    """Mengisi semua radiogroup (skala 1-5) di halaman yang aktif."""
    baris_skala = driver.find_elements(By.XPATH, "//div[@role='radiogroup']")
    for baris in baris_skala:
        opsi = baris.find_elements(By.XPATH, ".//div[@role='radio']")
        if len(opsi) >= 5:
            # Pilihan skor 1, 2, 3 untuk pre-test (indeks 0, 1, 2)
            idx_pilihan = random.choice([0, 1, 2]) 
            driver.execute_script("arguments[0].click();", opsi[idx_pilihan])

def isi_kuesioner(url, data_user):
    nama = data_user['nama']

    driver = buat_driver()
    tunggu = WebDriverWait(driver, BATAS_WAKTU)

    try:
        # Buka form
        driver.get(url)
        time.sleep(3)

        # ===== HALAMAN 1: IDENTITAS =====
        print(f"[{nama}] Mengisi Halaman 1 (Data Diri)...")
        input_nama = tunggu.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@type='text']")))
        if input_nama:
            input_nama[0].send_keys(nama)

        # Pilih Status (Guru)
        klik_opsi_teks(driver, "Guru")

        klik_tombol(driver, "Berikutnya")
        time.sleep(2)
        
        # ===== HALAMAN 2: EVALUASI KEGIATAN MENGAJAR =====
        tunggu.until(EC.presence_of_element_located((By.XPATH, "//div[@role='radiogroup']")))
        print(f"[{nama}] Mengisi Halaman 2 (Evaluasi Kegiatan Mengajar)...")
        isi_halaman_skala(driver)
        klik_tombol(driver, "Berikutnya")
        time.sleep(2)

        # ===== HALAMAN 3: EVALUASI GREENHOUSE DAN HIDROPONIK =====
        tunggu.until(EC.presence_of_element_located((By.XPATH, "//div[@role='radiogroup']")))
        print(f"[{nama}] Mengisi Halaman 3 (Evaluasi Greenhouse & Hidroponik)...")
        isi_halaman_skala(driver)
        klik_tombol(driver, "Berikutnya")
        time.sleep(2)

        # ===== HALAMAN 4: EVALUASI IOT DAN AI CHATBOT =====
        tunggu.until(EC.presence_of_element_located((By.XPATH, "//div[@role='radiogroup']")))
        print(f"[{nama}] Mengisi Halaman 4 (Evaluasi IoT & AI Chatbot)...")
        isi_halaman_skala(driver)
        klik_tombol(driver, "Berikutnya")
        time.sleep(2)

        # ===== HALAMAN 5: EVALUASI PEMANFAATAN PROGRAM =====
        tunggu.until(EC.presence_of_element_located((By.XPATH, "//div[@role='radiogroup']")))
        print(f"[{nama}] Mengisi Halaman 5 (Evaluasi Pemanfaatan Program)...")
        isi_halaman_skala(driver)
        klik_tombol(driver, "Kirim")

        print(f"[SUKSES] Form atas nama '{nama}' BERHASIL dikirim!\n")
        time.sleep(3)

    except Exception as e:
        print(f"[GAGAL] Error saat mengisi form untuk '{nama}'.")
        print(f"Pesan Error: {e}")
        time.sleep(5)

    finally:
        driver.quit()


# ==========================================
# JALANKAN PROGRAM
# ==========================================

if __name__ == "__main__":
    # Cek file CSV ada atau tidak
    cek_file_csv(NAMA_FILE_CSV)

    # Baca data responden
    data_responden = baca_data_csv(NAMA_FILE_CSV, KOLOM_NAMA, KOLOM_KELAMIN)

    print(f"[INFO] Ditemukan {len(data_responden)} responden. Memulai otomatisasi...\n")

    # Isi form untuk setiap responden
    for nomor, data in enumerate(data_responden, 1):
        print(f"--- Responden {nomor}/{len(data_responden)} ---")
        isi_kuesioner(LINK_FORM, data)
        time.sleep(2)

    print("[SELESAI] Semua data telah diproses.")
    input("Tekan Enter untuk keluar...")
