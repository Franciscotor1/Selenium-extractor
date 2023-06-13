from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd

website = 'https://www.adamchoi.co.uk/teamgoals/detailed'
path = 'C:/Users/franc/Downloads/chromedriver/chromedriver.exe'

# Configurar opciones del navegador
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# Crear un objeto Service con la ubicación del controlador de Chrome
service = Service(path)

# Crear una instancia del navegador Chrome
driver = webdriver.Chrome(service=service, options=options)

# Abrir el sitio web
driver.get(website)

# Encontrar el botón "All Matches" y hacer clic en él
all_matches_button = driver.find_element(By.XPATH, '//label[@analytics-event="All matches"]')
all_matches_button.click()

# Encontrar el elemento del menú desplegable de países y seleccionar "Spain"
country_dropdown = Select(driver.find_element(By.ID, 'country'))
country_dropdown.select_by_visible_text('Spain')

partidos = []
matches = driver.find_elements(By.TAG_NAME, 'tr')

# Omitir la primera fila que contiene los encabezados de la tabla
for match in matches[1:]:
    celdas = match.find_elements(By.TAG_NAME, 'td')
    fecha = celdas[0].text
    equipo_local = celdas[1].text
    resultado = celdas[2].text
    equipo_visitante = celdas[3].text
    
    informacion = f"Fecha: {fecha}\tEquipo local: {equipo_local}, resultado: {resultado}\tEquipo visitante: {equipo_visitante}"
    partidos.append(informacion)

df = pd.DataFrame(partidos, columns=['Información'])
df.to_csv('partidos-españa.csv', index=False)

# Cerrar el navegador
driver.quit()
