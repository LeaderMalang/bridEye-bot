from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
options.add_extension("./Phantom.crx")
# options.add_argument('--headless')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
options.add_argument("window-size=1400,600")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument("--test-third-party-cookie-phaseout")
    # Use ChromeDriverManager to automatically manage the ChromeDriver version
s = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=options)
url="https://birdeye.so/token/4neSyzJmcSWQF58DKHdo7FNzJDDKSgaaQqrzuSXS5U6g?chain=solana"

# user_email="ibrahimberro3@gmail.com"
# user_password="Shades#2023$$2022#"
# driver.get(url)
driver.set_window_size(1920, 1080)
time.sleep(2)
#switch windows
if driver.title!="Phantom Wallet":
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)
# driver.switch_to.window(driver.window_handles[0])
# Locate the button with data-testid="import-wallet-button"
button = driver.find_element(By.CSS_SELECTOR, '[data-testid="import-wallet-button"]')

# Click the button
button.click()

time.sleep(2)
def read_secret():
# Open the file in read mode
    file1 = open("phantom_recovery.txt", "r",encoding="utf-8-sig")

    # Read the lines from the file
    lines = file1.readlines()

    # Initialize an empty list to hold the arrays
    wallet_secret = []

    # Loop through each line
    for line in lines:
        # Strip the newline character at the end and split the line by space
        word = line.strip().split()
        # Add the array to the list
        wallet_secret.append(word[0])

    # Close the file
    file1.close()


    return wallet_secret

wallet_secret_list=read_secret()


# Locate all input elements on the page
input_elements = driver.find_elements(By.TAG_NAME, "input")


# Ensure there are enough values to map to input elements
if len(wallet_secret_list) < len(input_elements):

    print("Warning: Not enough values to map to input elements.")
    # Handle this case if necessary

# Map the values to the input elements
for i, input_element in enumerate(input_elements):
    # Set the value of the input element to the corresponding value from the list
    input_element.clear()  # Clear any existing text in the input field
    input_element.send_keys(wallet_secret_list[i])


button_import_wallet = driver.find_element(By.CSS_SELECTOR, '[data-testid="onboarding-form-submit-button"]')
button_import_wallet.click()
print("Wallet import is completed!")




