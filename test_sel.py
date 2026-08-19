from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--remote-debugging-port=9222")

print("Membuka browser...")
driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(10)
print("Navigasi ke Google...")
try:
    driver.get("https://google.com")
    print("Sukses buka Google! Judul:", driver.title)
except Exception as e:
    print("Gagal:", e)
finally:
    driver.quit()
