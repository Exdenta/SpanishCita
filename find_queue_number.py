import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

def find_queue_number(office: str, tramite: str) -> int:
    queue_number = -1  # Default value if not found

    # Initialize the Chrome driver
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)

    try:
        # Open the web page
        driver.get("https://icp.administracionelectronica.gob.es/icpplus/index.html")
        
        # Wait for the dropdown menu to be present and select "Barcelona"
        wait = WebDriverWait(driver, 30)
        select_element = wait.until(EC.presence_of_element_located((By.ID, "form")))
        select = Select(select_element)
        select.select_by_visible_text("Barcelona")
        
        # Click on the "Aceptar" button
        accept_button = wait.until(EC.presence_of_element_located((By.ID, "btnAceptar")))
        accept_button.click()
        
        # Wait for the next page to load
        wait.until(EC.url_contains("icpplustieb/citar"))
        
        # Wait for the second dropdown menu to be present and select the option
        select_sede_element = wait.until(EC.presence_of_element_located((By.NAME, "sede")))
        select_sede = Select(select_sede_element)
        select_sede.select_by_visible_text(office)
        
        # Wait for the new elements to load after selecting the office
        wait.until(EC.presence_of_element_located((By.ID, "tramiteGrupo[0]")))
        
        # Locate the new dropdown and select the desired option
        select_tramite_element = wait.until(EC.presence_of_element_located((By.ID, "tramiteGrupo[0]")))
        select_tramite = Select(select_tramite_element)
        select_tramite.select_by_visible_text(tramite)
        
        # Click on the second "Aceptar" button
        second_accept_button = wait.until(EC.presence_of_element_located((By.ID, "btnAceptar")))
        second_accept_button.click()

        # Wait for the next page to load
        wait.until(EC.url_contains("icpplustieb/acInfo"))

        # Extract the queue number from the text on the acInfo page
        ac_info_text = driver.find_element(By.TAG_NAME, "h3").text
        match = re.search(r"EL ÚLTIMO LOTE RECIBIDO EN LA OFICINA SELECCIONADA ES EL \d+ / (\d+)", ac_info_text)
        if match:
            queue_number = int(match.group(1))
    except Exception as e:
        print(str(e))
    finally:
        # Close the driver after a short delay to see the result
        driver.quit()
    
    return queue_number
