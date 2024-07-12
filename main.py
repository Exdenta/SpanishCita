from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Initialize the Chrome driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Open the web page
    driver.get("https://icp.administracionelectronica.gob.es/icpplus/index.html")
    
    # Wait for the dropdown menu to be present and select "Barcelona"
    wait = WebDriverWait(driver, 10)
    select_element = wait.until(EC.presence_of_element_located((By.ID, "form")))
    select = Select(select_element)
    select.select_by_visible_text("Barcelona")
    
    # Click on the "Aceptar" button
    accept_button = wait.until(EC.presence_of_element_located((By.ID, "btnAceptar")))
    accept_button.click()
    
    # Wait for the next page to load
    wait.until(EC.url_contains("icpplustieb/citar?p=8&locale=es"))
    
    # Wait for the second dropdown menu to be present
    select_sede_element = wait.until(EC.presence_of_element_located((By.ID, "sede")))
    
    # Print all available options to verify the text
    select_sede = Select(select_sede_element)
    options = [option.text for option in select_sede.options]
    print("Available options:", options)
    
    # Select the desired option
    select_sede.select_by_visible_text("CNP MALLORCA GRANADOS, MALLORCA")
    
    # Optionally, perform any further actions if needed
    # For example, you might want to submit the form
    # submit_button = driver.find_element(By.ID, "submit_button_id")
    # submit_button.click()

finally:
    # Close the driver after a short delay to see the result
    import time
    time.sleep(5)
    driver.quit()
