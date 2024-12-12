from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

driver = webdriver.Firefox()


def seleccionar_opcion(driver, combobox_id):
    combobox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, combobox_id))
    )
    
    opciones = combobox.find_elements(By.TAG_NAME, "option")
    valores_opciones = [opcion.get_attribute("value") for opcion in opciones]
    
    if "-1" not in valores_opciones:
        raise Exception(f"No se encontró el valor '-1' en el combobox con ID {combobox_id}")

    indice_inicio = valores_opciones.index("-1")

    if "-2" in valores_opciones:
        indice_fin = valores_opciones.index("-2")
    else:
        indice_fin = len(valores_opciones)

    opciones_validas = [opcion for opcion in opciones[indice_inicio + 1:indice_fin] 
    if opcion.get_attribute("value") not in ["-1", "-2"]]

    if not opciones_validas:
        raise Exception(f"No hay opciones válidas para el combobox con ID {combobox_id}")

    print([opcion.text for opcion in opciones_validas])
    opcion_seleccionada = random.choice(opciones_validas)
    opcion_value = opcion_seleccionada.get_attribute("value")
    print(f"Seleccionando la opción: {opcion_seleccionada.text} del combobox con ID: {combobox_id}")

    driver.execute_script(f"document.getElementById('{combobox_id}').value = '{opcion_value}';")
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", combobox)
    time.sleep(1)

#medseradmin / MuchoExito
#miamigopet / unipets2021
#citroen / Belladonna
#sanasalud / MuchoExito

try:
    #Inicio de sesión

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

    time.sleep(2)

    #Seleccion de persona

    comboboxes = driver.find_elements(By.CSS_SELECTOR, "select[id^='combobox_dimension_']")

    combobox_ids = [combobox.get_attribute("id") for combobox in comboboxes]

    print("IDs de comboboxes encontrados:", combobox_ids)

    for combobox_id in combobox_ids:
        print(f"Procesando combobox con ID: {combobox_id}")
        seleccionar_opcion(driver, combobox_id)

    time.sleep(1)
    #Seleccion de hora
    horas_disponibles = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@id, 'bookableUnit_')]"))
    )

    lista_horas = [hora.get_attribute('id') for hora in horas_disponibles]
    print("Lista de horas disponibles:\n" + "\n".join(lista_horas))

    while lista_horas:
        hora_seleccionada_id = random.choice(lista_horas)
        hora_seleccionada = driver.find_element(By.ID, hora_seleccionada_id)
        style_attribute = hora_seleccionada.get_attribute("style")

        if "background-color: rgb(209, 238, 252);" not in style_attribute:
            print(f"Hora seleccionada no está reservada: {hora_seleccionada_id}")
            break
        
        else:
            print(f"Hora reservada: {hora_seleccionada_id}")
            lista_horas.remove(hora_seleccionada_id)  # Eliminar la hora reservada de la lista

        if not lista_horas:  # Verificar si la lista está vacía
            print("No hay horas disponibles que no estén reservadas.")
            break

    tomar_hora = driver.find_element(By.ID, hora_seleccionada_id)
    tomar_hora.click()
    time.sleep(1)

    driver.find_element(By.ID, "btn_searchContact").click()
    time.sleep(1)

    input_field = driver.find_element(By.ID, "hint")
    input_field.clear()
    input_field.send_keys("204968233")

    driver.find_element(By.ID, "btn_search").click()

    driver.find_element(By.XPATH, "//div[text()='Agendar']").click()
    time.sleep(1)

    driver.find_element(By.XPATH, "//div[text()='Reservar']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[text()='Confirmar Reserva']").click()

finally:
    # Cierra el navegador
    driver.quit()
