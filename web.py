import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def check_citas(nie_code: str, nombre_apellidos: str, office: str, tramite: str, do_not_quit=False, sleep_time=5) -> bool:
    no_appointments_text = "En este momento no hay citas disponibles"

    # Initialize the Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

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

        # Click on the "Aceptar" button
        enviar_button = wait.until(EC.presence_of_element_located((By.ID, "btnEnviar")))
        enviar_button.click()

        retry_attempts = 3  # Number of retries
        for attempt in range(retry_attempts):
            try:
                # Wait for the next page to load
                wait.until(EC.url_contains("icpplustieb/acValidarEntrada"))

                # Click on the 'Solicitar Cita' button
                enviar_button = wait.until(EC.presence_of_element_located((By.ID, "btnEnviar")))
                enviar_button.click()
                break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if no_appointments_text in driver.page_source:
                    return False
                if attempt < retry_attempts - 1:
                    time.sleep(5)  # Wait before retrying

        for attempt in range(retry_attempts):
            try:
                wait.until(EC.url_contains("icpplustieb/acCitar"))
                return no_appointments_text not in driver.page_source
            except Exception as e:
                if EC.url_contains("icpplustieb/acValidarEntrada"):
                    return no_appointments_text in driver.page_source
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if no_appointments_text in driver.page_source:
                    return False
                if attempt < retry_attempts - 1:
                    time.sleep(5)  # Wait before retrying

        return no_appointments_text not in driver.page_source

    finally:
        # Close the driver after a short delay to see the result
        time.sleep(sleep_time)
        check = no_appointments_text not in driver.page_source
        if not do_not_quit:
            driver.quit()
        return check
