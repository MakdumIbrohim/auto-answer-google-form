import time
import random
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

load_dotenv()

FORM_LINK = os.getenv('FORM_LINK').strip() if os.getenv('FORM_LINK') else ''
CSV_FILE_NAME = 'data_responden.csv'
COL_NAME = 'nama'
COL_GENDER = 'kelamin'
WAIT_TIMEOUT = 10

CHROME_OPTIONS = Options()
CHROME_OPTIONS.add_argument("--start-maximized")
CHROME_OPTIONS.add_argument("--no-sandbox")
CHROME_OPTIONS.add_argument("--disable-dev-shm-usage")
CHROME_OPTIONS.add_argument("--disable-gpu")
CHROME_OPTIONS.add_argument("--remote-debugging-port=9222")
# CHROME_OPTIONS.add_argument("--headless")

def create_driver():
    """Create and return a new Chrome browser instance."""
    return webdriver.Chrome(options=CHROME_OPTIONS)

def check_csv_file(file_path):
    """Check if the CSV file exists before running the program."""
    if not os.path.exists(file_path):
        print(f"[ERROR] CSV file '{file_path}' not found!")
        exit()

def read_csv_data(file_path, col_name, col_gender):
    """Read and return respondent data from the CSV file as a list of dictionaries."""
    data = []
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row[col_name].strip():
                data.append({
                    'name': row[col_name].strip(),
                    'gender': row[col_gender].strip().upper()
                })
    return data

def click_radio(driver, group_xpath, index):
    """Click a specific radio button option in a group based on index."""
    group = driver.find_elements(By.XPATH, group_xpath)
    if group:
        options = group[0].find_elements(By.XPATH, ".//div[@role='radio']")
        if index < len(options):
            driver.execute_script("arguments[0].click();", options[index])

def click_random_radio(driver, group_xpath, index_options=None):
    """Click a random radio button option in a group."""
    group = driver.find_elements(By.XPATH, group_xpath)
    if group:
        options = group[0].find_elements(By.XPATH, ".//div[@role='radio']")
        option_list = options if index_options is None else [options[i] for i in index_options if i < len(options)]
        if option_list:
            driver.execute_script("arguments[0].click();", random.choice(option_list))

def click_button(driver, button_text):
    """Click a button based on its displayed text (e.g., 'Berikutnya', 'Kirim')."""
    xpath = f"//div[@role='button']//span[text()='{button_text}']"
    button = driver.find_element(By.XPATH, xpath)
    driver.execute_script("arguments[0].click();", button)

def fill_questionnaire(url, user_data):
    """Main function to navigate and fill out data on the Google Form."""
    name = user_data['name']
    gender = user_data['gender']

    driver = create_driver()
    wait = WebDriverWait(driver, WAIT_TIMEOUT)

    try:
        driver.get(url)
        time.sleep(3)

        print(f"[{name}] Filling Page 1 (Personal Data)...")
        name_input = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@type='text']")))
        name_input[0].send_keys(name)

        gender_index = 0 if gender == 'L' else 1
        click_radio(driver, "//div[@role='radiogroup']", gender_index)
        click_random_radio(driver, "//div[@role='radiogroup']")
        click_radio(driver, "//div[@role='radiogroup']", 0)

        click_button(driver, "Berikutnya")
        time.sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='radiogroup']")))

        print(f"[{name}] Filling Page 2...")
        click_radio(driver, "//div[@role='radiogroup']", 2)

        checkboxes = driver.find_elements(By.XPATH, "//div[@role='checkbox']")
        choices = random.sample(checkboxes, min(random.randint(1, 3), len(checkboxes)))
        for box in choices:
            driver.execute_script("arguments[0].click();", box)

        click_button(driver, "Berikutnya")
        time.sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='radiogroup']")))

        print(f"[{name}] Filling Page 3 (UEQ Scale)...")
        scale_rows = driver.find_elements(By.XPATH, "//div[@role='radiogroup']")
        for row in scale_rows:
            options = row.find_elements(By.XPATH, ".//div[@role='radio']")
            if options:
                driver.execute_script("arguments[0].click();", random.choice(options))

        click_button(driver, "Kirim")
        print(f"[SUCCESS] Form for '{name}' submitted SUCCESSFULLY!\n")
        time.sleep(3)

    except Exception as e:
        print(f"[FAILED] Error while filling form for '{name}'.")
        print(f"Error Message: {e}\n")
        time.sleep(5)

    finally:
        driver.quit()

if __name__ == "__main__":
    check_csv_file(CSV_FILE_NAME)
    respondent_data = read_csv_data(CSV_FILE_NAME, COL_NAME, COL_GENDER)

    print(f"[INFO] Found {len(respondent_data)} respondents. Starting automation...\n")

    for number, data in enumerate(respondent_data, 1):
        print(f"--- Respondent {number}/{len(respondent_data)} ---")
        fill_questionnaire(FORM_LINK, data)
        time.sleep(2)

    print("[COMPLETED] All data has been processed.")
