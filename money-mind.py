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

# URL Google Form yang ingin diisi (GANTI dengan link form Anda)
LINK_FORM = os.getenv('MONEY_MIND_GOOGLE_FORM_URL', '')

# Nama file CSV yang berisi data responden
NAMA_FILE_CSV = 'data_responden.csv'

# Nama kolom di dalam file CSV
KOLOM_NAMA = 'nama'

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


def baca_data_csv(path_file, kolom_nama):
    """Membaca data responden dari file CSV."""
    data = []
    with open(path_file, mode='r', encoding='utf-8-sig') as file:
        pembaca = csv.DictReader(file)
        for baris in pembaca:
            if baris.get(kolom_nama) and baris[kolom_nama].strip():
                data.append(baris[kolom_nama].strip())
    return data


def klik_tombol(driver, teks_tombol):
    """Mengklik tombol berdasarkan teks yang ada di tombol."""
    xpath = f"//div[@role='button']//span[text()='{teks_tombol}']"
    tombol = driver.find_element(By.XPATH, xpath)
    driver.execute_script("arguments[0].click();", tombol)


# ==========================================
# ISI KUESIONER
# ==========================================

def isi_kuesioner(url, nama_responden):
    driver = buat_driver()
    tunggu = WebDriverWait(driver, BATAS_WAKTU)

    try:
        # Buka form
        driver.get(url)
        time.sleep(2)

        # ===== HALAMAN 1: IDENTITAS =====
        print(f"[{nama_responden}] Mengisi Halaman 1...")

        # Input nama lengkap
        input_nama = tunggu.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
        input_nama.send_keys(nama_responden)

        # Ambil grup radio button di Halaman 1
        grup_radio = driver.find_elements(By.XPATH, "//div[@role='radiogroup']")

        # Pilih usia secara acak
        opsi_usia = grup_radio[0].find_elements(By.XPATH, ".//div[@role='radio']")
        driver.execute_script("arguments[0].click();", random.choice(opsi_usia))

        # Pilih pekerjaan secara acak (hindari pilihan 'Yang lain')
        opsi_pekerjaan = grup_radio[1].find_elements(By.XPATH, ".//div[@role='radio']")
        driver.execute_script("arguments[0].click();", random.choice(opsi_pekerjaan[:4]))

        # Klik tombol Berikutnya
        klik_tombol(driver, "Berikutnya")

        # ===== HALAMAN 2: KUESIONER SUS =====
        print(f"[{nama_responden}] Mengisi Halaman 2 (Skala SUS)...")
        time.sleep(2)

        # Tunggu radio button halaman 2 termuat
        tunggu.until(EC.presence_of_element_located((By.XPATH, "//div[@role='radiogroup']")))

        # 10 baris pertanyaan SUS
        pertanyaan = driver.find_elements(By.XPATH, "//div[@role='radiogroup']")

        for index, baris in enumerate(pertanyaan):
            opsi = baris.find_elements(By.XPATH, ".//div[@role='radio']")

            # Strategi pengisian SUS yang realistis:
            # Pertanyaan Ganjil (positif) -> skor tinggi (4 atau 5)
            # Pertanyaan Genap (negatif) -> skor rendah (1 atau 2)
            if (index + 1) % 2 != 0:
                pilihan = random.choice([opsi[3], opsi[4]])  # Nilai 4 atau 5
            else:
                pilihan = random.choice([opsi[0], opsi[1]])  # Nilai 1 atau 2

            driver.execute_script("arguments[0].click();", pilihan)

        # Jeda acak agar terlihat natural
        time.sleep(random.uniform(1.0, 2.5))

        # Klik tombol Kirim
        klik_tombol(driver, "Kirim")

        print(f"[SUKSES] Form atas nama '{nama_responden}' BERHASIL dikirim!\n")
        time.sleep(2)

    except Exception as e:
        print(f"[GAGAL] Error saat mengisi form untuk '{nama_responden}'.")
        print(f"Pesan Error: {e}")
        print("Membuka ulang form untuk responden berikutnya...\n")
        time.sleep(5)

    finally:
        driver.quit()


# ==========================================
# JALANKAN PROGRAM
# ==========================================

if __name__ == "__main__":
    # Cek dan baca data
    cek_file_csv(NAMA_FILE_CSV)
    data_responden = baca_data_csv(NAMA_FILE_CSV, KOLOM_NAMA)

    print(f"[INFO] Ditemukan {len(data_responden)} responden. Memulai otomatisasi...\n")

    # Isi form untuk setiap responden
    for nomor, nama in enumerate(data_responden, 1):
        print(f"--- Responden {nomor}/{len(data_responden)} ---")
        isi_kuesioner(LINK_FORM, nama)

    print("[SELESAI] Semua data telah diproses.")
    input("Tekan Enter untuk keluar...")
