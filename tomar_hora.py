from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import mysql.connector

driver = webdriver.Firefox()

db_config = {
    'user': 'root',
    'password': 'Belladonna',
    'host': 'localhost',
    'database': 'qa_testing'
}

def save_db(result, log_message=""):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        query = """
        INSERT INTO test_results (run_id, result, log)
        VALUES (1, %s, %s)
        """
        cursor.execute(query, (result, log_message))
        conn.commit()
        print("Resultado registrado en la base de datos.")

    except mysql.connector.Error as err:
        print(f"Error al registrar resultado en la base de datos: {err}")

    finally:
        cursor.close()
        conn.close()

def selector(driver, xpath):
    try:
        elementos = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
        lista_elementos = [elemento.text for elemento in elementos]
        print(f"Lista de elementos encontrados:\n" + "\n".join(lista_elementos))

        elemento_seleccionado = random.choice(elementos)
        print(f"Elemento seleccionado:\n", elemento_seleccionado.text)

        elemento_seleccionado.click()
        time.sleep(2)
    except Exception as e:
        print(f"Error en selector con xpath '{xpath}': {str(e)}")
        raise

try:
    try:
        # Primera vista: "Identificación"
        driver.get("https://www.test.medicosdelservet.ticketmed.cl/")

        field_rut = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@id, '_rut')]"))
        )
        field_rut.clear()
        field_rut.send_keys("204968233")

        button_siguiente_1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[text()='Siguiente >']"))
        )
        button_siguiente_1.click()

        field_nombre = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@id, '_name')]"))
        )
        field_nombre.clear()
        field_nombre.send_keys("Guillermo Ignacio")

        field_apellido = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@id, '_apellidos')]"))
        )
        field_apellido.clear()
        field_apellido.send_keys("Martínez González")

        time.sleep(1)

        button_siguiente_2 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[text()='Siguiente >']"))
        )
        button_siguiente_2.click()

        time.sleep(2)
        print("Vista de Identificación completada con éxito.")
    except Exception as e:
        print("Error en la vista de Identificación: ", str(e))
        save_db(0, f"Error en la vista de Identificación: {str(e)}")
        driver.quit()
        exit()

    try:
        # Segunda vista: "Especialidad"
        selector(driver, "//div[contains(@id, '_dimId_')]")
        print("Vista de Especialidades completada con éxito.")
    except Exception as e:
        print("Error en la vista de Especialidades: ", str(e))
        raise

    try:
        # Tercera vista: "Doctores"
        selector(driver, "//div[contains(@id, '_dimId_')]")
    except Exception as e:
        print("Error en la vista de Doctores: ", str(e))
        raise

    try:
        # Cuarta vista: "Horas"
        time.sleep(2)
        horas_disponibles = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@id, 'bookableUnit_')]"))
        )

        lista_horas = [hora.get_attribute('id') for hora in horas_disponibles]
        print("Lista de horas disponibles:\n" + "\n".join(lista_horas))

        while lista_horas:
            hora_seleccionada_id = random.choice(lista_horas)
            hora_seleccionada = driver.find_element(By.ID, hora_seleccionada_id)
            style_attribute = hora_seleccionada.get_attribute("style")

            if "background:#D1EEFC" not in style_attribute:
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
        time.sleep(2)
        field_mail = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@id, '_email')]"))
        )
        field_mail.clear()
        field_mail.send_keys("guillermomg2013@gmail.com")

        field_numero = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@id, '_fono')]"))
        )
        field_numero.clear()
        field_numero.send_keys("998364247")

        time.sleep(1)
        button_siguiente_3 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[text()='Confirmar datos y tomar la hora']"))
        )
        button_siguiente_3.click()

        time.sleep(3)
        print("Vista de Tomar Horas completada con éxito: ", hora_seleccionada_id)
    except Exception as e:
        print("Error en la vista de Tomar Horas: ", str(e))
        raise
    save_db(1, "El script se ejecutó correctamente.")
except Exception as e:
    print("El script encontró un error y se detuvo:", str(e))
finally:
    driver.quit()
    print("Navegador cerrado.")
