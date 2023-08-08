import time
from selenium import webdriver
from selenium.webdriver.safari.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import utils.conn_db as conn_db


def extracao_paises():
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
    select.select_by_value("competitor")  # competitor or competition

    time.sleep(5)

    # element = driver.find_element(By.NAME, "country")
    # html_content = element.get_attribute('outerHTML')

    # Carrega lista de paises possivei de selecionar
    select_country_list = driver.find_element(
        By.XPATH,
        "//html/body/div[1]/div[2]/div/div[2]/div/div/div[1]/div[4]/select",
    )
    select = Select(select_country_list)
    option_list = select.options

    conn = conn_db.connect_open()
    cur = conn.cursor()

    # Imprimi lista de paises
    for x in option_list:
        # Vetor campos
        campos = [
            "cd_atributo_pais",
            "cd_pais",
            "nm_pais",
            "ds_pais",
        ]
        # Trata espacos
        text = x.text.replace(" ", "")
        value = x.get_attribute("value")

        # Trata texto com '
        text = x.text.replace("'", "''")
        # imprimi valores que não tem delimitador
        if "/" not in text:
            print(text)
            continue
        # Vetor valores
        valores = [
            value,
            text.split("/")[0].strip(),
            text.split("/")[1].strip(),
            text.strip(),
        ]
        print(valores)
        conn_db.insert_table(conn, "tb_pais", campos, valores)

    conn.commit()
    cur.close()

    conn_db.connect_close(conn)

    # Encerra safari
    driver.quit()


extracao_paises()
