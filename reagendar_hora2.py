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
    field_usuario.send_keys("medseradmin")

    field_password = driver.find_element(By.ID, "pass")
    field_password.clear()
    field_password.send_keys("MuchoExito")

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

    reagendar_1 = driver.find_element(By.ID, "reagendar")
    driver.execute_script("arguments[0].click();", reagendar_1)
    time.sleep(1)

    horas_disponibles = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[starts-with(@id, 'bookableUnit_')]"))
    )

    lista_horas = [hora.get_attribute('id') for hora in horas_disponibles]
    print("Lista de horas disponibles:\n" + "\n".join(lista_horas))
    #arreglar este ciclo
    while True:
        hora_seleccionada_id = random.choice(lista_horas)
        hora_seleccionada = driver.find_element(By.ID, hora_seleccionada_id)
        style_attribute = hora_seleccionada.get_attribute("style")

    
        if "background-color: rgb(209, 238, 252);" not in style_attribute:
            break  
        else:
            print(f"Hora   reservada: {hora_seleccionada_id}")

    print("Hora final seleccionada:", hora_seleccionada_id)

    time.sleep(1)
    tomar_hora = driver.find_element(By.ID,hora_seleccionada_id)
    tomar_hora.click()

    time.sleep(2)

    field_rut = driver.find_element(By.ID, "1_contact_dni")
    field_rut.clear()
    field_rut.send_keys("204968233")

    reagendar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[starts-with(@id, 'ticketmed_continue')]"))
    )

    driver.execute_script("arguments[0].click();", reagendar)
    time.sleep(2)

    confirm = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[starts-with(@id, 'ticketmed_confirm_')]"))
    )

    print("Elemento 'ticketmed_confirm' encontrado con ID:", confirm.get_attribute('id'))
    driver.execute_script("arguments[0].click();", confirm)

    time.sleep(2)
    ok_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'msgDialog_okButton'))
    )

    driver.execute_script("arguments[0].click();", ok_button)

    time.sleep(1)

    print("Hora reagendada con éxito")
finally:
    # Cierra el navegador
    driver.quit()
