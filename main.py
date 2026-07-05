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
LINK_FORM = 'https://docs.google.com/forms/d/e/1FAIpQLSc_2z6L6Wmc47NSBPBtf5WObBzE9MXobGTu4rNsc6MCgj4ytg/viewform'

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


def klik_radio(driver, xpath_grup, index):
    """Mengklik opsi radio button berdasarkan index."""
    grup = driver.find_elements(By.XPATH, xpath_grup)
    if grup:
        opsi = grup[0].find_elements(By.XPATH, ".//div[@role='radio']")
        if index < len(opsi):
            driver.execute_script("arguments[0].click();", opsi[index])


def klik_radio_acak(driver, xpath_grup, indeks_opsi=None):
    """Mengklik radio button secara acak."""
    grup = driver.find_elements(By.XPATH, xpath_grup)
    if grup:
        opsi = grup[0].find_elements(By.XPATH, ".//div[@role='radio']")
        daftar_opsi = opsi if indeks_opsi is None else [opsi[i] for i in indeks_opsi if i < len(opsi)]
        if daftar_opsi:
            driver.execute_script("arguments[0].click();", random.choice(daftar_opsi))


def klik_tombol(driver, teks_tombol):
    """Mengklik tombol berdasarkan teks yang ada di tombol."""
    xpath = f"//div[@role='button']//span[text()='{teks_tombol}']"
    tombol = driver.find_element(By.XPATH, xpath)
    driver.execute_script("arguments[0].click();", tombol)


# ==========================================
# ISI KUESIONER
# ==========================================

def isi_kuesioner(url, data_user):
    nama = data_user['nama']
    kelamin = data_user['kelamin']

    driver = buat_driver()
    tunggu = WebDriverWait(driver, BATAS_WAKTU)

    try:
        # Buka form
        driver.get(url)
        time.sleep(3)

        # ===== HALAMAN 1: IDENTITAS =====
        print(f"[{nama}] Mengisi Halaman 1 (Data Diri)...")

        # Input nama
        input_nama = tunggu.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@type='text']")))
        input_nama[0].send_keys(nama)

        # Pilih jenis kelamin (L = index 0, P = index 1)
        index_kelamin = 0 if kelamin == 'L' else 1
        klik_radio(driver, "//div[@role='radiogroup']", index_kelamin)

        # Pilih usia secara acak
        klik_radio_acak(driver, "//div[@role='radiogroup']")

        # Pilih pernah akses (selalu Ya / index 0)
        klik_radio(driver, "//div[@role='radiogroup']", 0)

        # Klik tombol Berikutnya
        klik_tombol(driver, "Berikutnya")
        time.sleep(2)
        tunggu.until(EC.presence_of_element_located((By.XPATH, "//div[@role='radiogroup']")))

        # ===== HALAMAN 2: PERAN DAN INTERES =====
        print(f"[{nama}] Mengisi Halaman 2...")

        # Pilih peran (Masyarakat Umum = index 2)
        klik_radio(driver, "//div[@role='radiogroup']", 2)

        # Pilih checkbox secara acak (1 sampai 3 pilihan)
        kotak_centang = driver.find_elements(By.XPATH, "//div[@role='checkbox']")
        pilihan = random.sample(kotak_centang, min(random.randint(1, 3), len(kotak_centang)))
        for kotak in pilihan:
            driver.execute_script("arguments[0].click();", kotak)

        # Klik tombol Berikutnya
        klik_tombol(driver, "Berikutnya")
        time.sleep(2)
        tunggu.until(EC.presence_of_element_located((By.XPATH, "//div[@role='radiogroup']")))

        # ===== HALAMAN 3: SKALA UEQ =====
        print(f"[{nama}] Mengisi Halaman 3 (Skala UEQ)...")

        baris_skala = driver.find_elements(By.XPATH, "//div[@role='radiogroup']")
        for baris in baris_skala:
            opsi = baris.find_elements(By.XPATH, ".//div[@role='radio']")
            if opsi:
                driver.execute_script("arguments[0].click();", random.choice(opsi))

        # Klik tombol Kirim
        klik_tombol(driver, "Kirim")

        print(f"[SUKSES] Form atas nama '{nama}' BERHASIL dikirim!\n")
        time.sleep(3)

    except Exception as e:
        print(f"[GAGAL] Error saat mengisi form untuk '{nama}'.")
        print(f"Pesan Error: {e}")
        print("Browser dibuka selama 30 detik untuk pengecekan...\n")
        time.sleep(30)

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
