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

    time.sleep(1)
    button_menu = driver.find_element(By.ID, "mostrarMenu")
    button_menu.click()

    button_reservas = driver.find_element(By.ID, "menuOption_search_reservations")
    button_reservas.click()
    time.sleep(2)

    input_fecha = driver.find_element(By.ID, "date_to")

    fecha_actual_str = input_fecha.get_attribute("value")

    fecha_actual = datetime.strptime(fecha_actual_str, "%Y-%m-%d")

    nueva_fecha = fecha_actual + timedelta(days=3)

    nueva_fecha_formateada = nueva_fecha.strftime("%Y-%m-%d")

    driver.execute_script(f"arguments[0].value = '{nueva_fecha_formateada}';", input_fecha)

    time.sleep(1)
    button_buscar = driver.find_element(By.ID, "btn_search")
    button_buscar.click()

    time.sleep(2)
    tabla_resultados = driver.find_element(By.ID, "searchResults")

    filas = tabla_resultados.find_elements(By.TAG_NAME, "tr")

    celdas_no_confirmadas = []
    for fila in filas:
        celdas = fila.find_elements(By.TAG_NAME, "td")
        for celda in celdas:
            if celda.text.strip() == "No confirmada":
                celdas_no_confirmadas.append(celda)

    for celda in celdas_no_confirmadas:
        print("ID de la celda:", celda.get_attribute("id"))

    celda_seleccionada = random.choice(celdas_no_confirmadas)
    print("ID de la celda seleccionada al azar:", celda_seleccionada.get_attribute("id"))

    button_celda = driver.find_element(By.ID, celda_seleccionada.get_attribute("id"))
    button_celda.click()

    time.sleep(2)

    horas_tomadas = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@id, 'check_bookableUnit')]"))
    )

    lista_horas = [hora.get_attribute('id') for hora in horas_tomadas]
    print("Lista de horas disponibles:\n" + "\n".join(lista_horas))

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
