import time
import requests
import pandas as pd 
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.safari.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import utils.conn_db as conn_db

# URL utilizada
url = "https://judobase.ijf.org/#/search"

# Abre o safari 
option = Options()
option.headless = True
driver = webdriver.Safari(options=option)

# Abre a URL indicada
driver.get(url)
# Aguarda URL Carregar
time.sleep(5)

# div class=form-control name=country
# Seleciona no drop box a opcao indicada
select_element = driver.find_element(By.NAME, "what")
select = Select(select_element)  
select.select_by_value("competitor") ##  competitor or competition

time.sleep(5)

# element = driver.find_element(By.NAME, "country")
# html_content = element.get_attribute('outerHTML')

# Carrega lista de paises possivei de selecionar
select_country_list = driver.find_element(By.XPATH, "//html/body/div[1]/div[2]/div/div[2]/div/div/div[1]/div[4]/select")
select = Select(select_country_list)  
option_list = select.options

conn = conn_db.connect_open()
cur = conn.cursor()

#TODO: Inserir try catch
#TODO: Criar script separado para captura de paises
# Imprimi lista de paises
for x in option_list:
  command = 'INSERT INTO public.tb_paises(cd_pais, nm_pais, ds_pais) VALUES '
  text = x.text.replace(" ", "")
  text = x.text.replace("'", "''")
  #imprimi valores que não tem delimitador
  if "/" not in text:
    print(text)
    continue

  command = command + "('" + text.split("/")[0]
  command = command + "', '" + text.split("/")[1]
  command = command + "', '" + text + "');"
  cur.execute(command)
  print(command)

conn.commit()
cur.close()

conn_db.connect_close(conn)
#TODO: Loop de leitura dos perfis de competidores

# Encerra safari
driver.quit()



