import time
from selenium import webdriver
from selenium.webdriver.safari.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import utils.conn_db as conn_db


# Inicializa o driver
def init_driver():
    """initialize the webdriver"""
    # Abre o safari
    option = Options()
    option.headless = True
    driver = webdriver.Safari(options=option)
    return driver


# Encerra o driver
def close_driver(driver):
    """close the webdriver"""
    # fecha o driver
    driver.close()
    return driver


# Abre a pagina
def get_page(driver, url):
    """get the page"""
    # Abre a URL indicada
    driver.get(url)
    # Aguarda URL Carregar
    time.sleep(5)
    return driver


# Seleciona a opcao no dropbox
def select_option(driver, name, value):
    """select the option in the dropdown"""
    # Seleciona no drop box a opcao indicada
    select_element = driver.find_element(By.NAME, name)
    select = Select(select_element)
    select.select_by_value(value)  # competitor or competition
    time.sleep(5)
    return driver


def extracao_list(xPathAno, xPathMes, campos):
    # URL utilizada
    url = "https://judobase.ijf.org/#/search"

    driver = init_driver()

    # Abre a URL indicada
    driver.get(url)

    select_option(driver, "what", "competition")

    # Carrega lista anos do dropbox
    select_list = driver.find_element(
        By.XPATH,
        xPathAno,
    )
    select = Select(select_list)
    option_list_ano = select.options

    # Carrega lista meses do dropbox
    select_list = driver.find_element(
        By.XPATH,
        xPathMes,
    )
    select = Select(select_list)
    option_list_mes = select.options

    conn = conn_db.connect_open()

    # Imprimi lista de paises
    for x in option_list_ano:
        # Trata espacos
        textAno = x.text.replace(" ", "")
        # validate if textAno is a integer
        try:
            int(textAno)
        except ValueError:
            continue

        for y in option_list_mes:
            textMes = y.text
            # imprimi valores que não tem delimitador
            if "-" not in textMes:
                print(textMes)
                continue
            # Monta string com inserts
            valores = [
                textAno.strip(),
                textMes.split("-")[0].strip(),
                textMes.split("-")[1].strip(),
                textMes.strip(),
            ]
            print(valores)
            conn_db.insert_table(conn, "tb_data_competicao", campos, valores)

    conn.commit()
    # Encerra conexao
    conn_db.connect_close(conn)

    # Encerra safari
    driver.quit()


campos = ["cd_ano", "cd_mes", "ds_mes", "ds_mes_completo"]

# /html/body/div[1]/div[2]/div/div[2]/div/div/div[1]/div[5]/select  --ano
# /html/body/div[1]/div[2]/div/div[2]/div/div/div[1]/div[6]/select  --mes


extracao_list(
    "/html/body/div[1]/div[2]/div/div[2]/div/div/div[1]/div[5]/select",
    "/html/body/div[1]/div[2]/div/div[2]/div/div/div[1]/div[6]/select",
    campos,
)
