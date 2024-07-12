import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Initialize the command-line argument parser
parser = argparse.ArgumentParser(description='Automate NIE submission.')
parser.add_argument('nie_code', type=str, help='NIE code to submit')
parser.add_argument('nombre_apellidos', type=str, help='Nombre y apellidos to submit')

# Parse the arguments
args = parser.parse_args()
nie_code = args.nie_code
nombre_apellidos = args.nombre_apellidos

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
    wait.until(EC.url_contains("icpplustieb/citar"))
    
    # Wait for the second dropdown menu to be present and select the option
    select_sede_element = wait.until(EC.presence_of_element_located((By.NAME, "sede")))
    select_sede = Select(select_sede_element)
    select_sede.select_by_visible_text("CNP MALLORCA GRANADOS, MALLORCA, 213")
    
    # Wait for the new elements to load after selecting the office
    wait.until(EC.presence_of_element_located((By.ID, "tramiteGrupo[0]")))
    
    # Locate the new dropdown and select the desired option
    select_tramite_element = wait.until(EC.presence_of_element_located((By.ID, "tramiteGrupo[0]")))
    select_tramite = Select(select_tramite_element)
    
    select_tramite.select_by_visible_text("POLICIA - RECOGIDA DE TARJETA DE IDENTIDAD DE EXTRANJERO (TIE)")
    
    # Click on the second "Aceptar" button
    second_accept_button = wait.until(EC.presence_of_element_located((By.ID, "btnAceptar")))
    second_accept_button.click()

    # Wait for the next page to load
    wait.until(EC.url_contains("icpplustieb/acInfo"))

    # Scroll to and click on the "Entrar" button
    entrar_button = wait.until(EC.presence_of_element_located((By.ID, "btnEntrar")))
    driver.execute_script("arguments[0].scrollIntoView();", entrar_button)
    entrar_button.click()

    # Wait for the next page to load
    wait.until(EC.url_contains("icpplustieb/acEntrada"))

    # Fill in the NIE code
    nie_input = wait.until(EC.presence_of_element_located((By.ID, "txtIdCitado")))
    nie_input.send_keys(nie_code)

    # Fill in the nombre y apellidos
    nombre_input = wait.until(EC.presence_of_element_located((By.ID, "txtDesCitado")))
    nombre_input.send_keys(nombre_apellidos)

    entrar_button = wait.until(EC.presence_of_element_located((By.ID, "btnEntrar")))
    entrar_button.click()

    # Wait for the next page to load
    wait.until(EC.url_contains("icpplustieb/acValidarEntrada"))

    # Click on the 'Solicitar Cita' button
    enviar_button = wait.until(EC.presence_of_element_located((By.ID, "btnEnviar")))
    enviar_button.click()



finally:
    # Close the driver after a short delay to see the result
    import time
    time.sleep(5)
    driver.quit()
