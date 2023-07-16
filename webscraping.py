import time
import requests
import pandas as pd 
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.safari.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

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


#TODO: Inserir paises em banco de dados
# Imprimi lista de paises
for x in option_list:
  print(x.text)
  print(x.id)

#TODO: Loop de leitura dos perfis de competidores

# Encerra safari
driver.quit()



