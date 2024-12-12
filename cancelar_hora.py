from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import pytz
import time
import random

driver = webdriver.Firefox()

#medseradmin / MuchoExito
#miamigopet / unipets2021
#citroen / Belladonna
#sanasalud / MuchoExito

try:
    driver.get("https://www.test.admin.ticketmed.cl")
    time.sleep(1)

    field_usuario = driver.find_element(By.ID, "login")
    field_usuario.clear()
    field_usuario.send_keys("citroen")

    field_password = driver.find_element(By.ID, "pass")
    field_password.clear()
    field_password.send_keys("Belladonna")

    button_ingresar = driver.find_element(By.ID, "buttonId")
    button_ingresar.click()

    horas_tomadas = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@id, 'check_bookableUnit')]"))
    )

    lista_horas = [hora.get_attribute('id') for hora in horas_tomadas]
    print("Lista de horas por cancelar:\n" + "\n".join(lista_horas))

    hora_por_cancelar = random.choice(lista_horas)
    print("Hora seleccionada:", hora_por_cancelar)

    boton = driver.find_element(By.ID, hora_por_cancelar)
    driver.execute_script("arguments[0].click();", boton)

    time.sleep(2)

    cancelar = driver.find_element(By.ID, "cancelar")
    driver.execute_script("arguments[0].click();", cancelar)
    time.sleep(1)

    checkbox = driver.find_element(By.ID,"notify_on_cancel_reservation")
    driver.execute_script("arguments[0].click();", checkbox)
    time.sleep(1)

    si_cancelar = driver.find_element(By.ID, "msgDialog_okButton")
    driver.execute_script("arguments[0].click();", si_cancelar)    

    time.sleep(1)


finally:
    # Cierra el navegador
    driver.quit()
