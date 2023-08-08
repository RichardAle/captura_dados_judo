import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.safari.options import (
    Options,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import (
    Select,
)
import utils.conn_db as conn_db
from selenium.webdriver import ActionChains
from concurrent.futures import ThreadPoolExecutor


# Funtion to initialize the webdriver
def init_driver():
    """initialize the webdriver"""
    # Abre o safari
    option = Options()
    option.headless = True
    # Selenium options
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    # /Applications/Google Chrome.app/Contents/MacOS/Google Chrome

    return driver


# function to close the webdriver
def close_driver(driver):
    """close the webdriver"""
    # fecha o driver
    driver.close()
    return driver


# Function to get the page
def get_page(driver, url):
    """get the page"""
    # Abre a URL indicada
    driver.get(url)
    # Aguarda URL Carregar
    time.sleep(1)
    return driver


# Function to select the option in the dropdown
def select_option(driver, name, value):
    """select the option in the dropdown"""
    # Seleciona no drop box a opcao indicada
    select_element = driver.find_element(By.NAME, name)
    select = Select(select_element)
    select.select_by_value(value)  # competitor or competition
    time.sleep(0)
    return driver


# Function to catch webpage contents
def get_webpage_content(driver, xpath):
    """catch webpage contents"""
    element = driver.find_element(By.XPATH, xpath)
    html_content = element.get_attribute("outerHTML")
    return html_content


# function to click on the button
def click_button(driver, xpath):
    """click on the button"""
    element = driver.find_element(By.XPATH, xpath)
    ActionChains(driver).click(element).perform()
    time.sleep(1)
    return driver


def main(id_pais, id_peso, cd_atributo_pais, cd_categoria):
    try:
        """main function"""
        # URL utilizada
        url = "https://judobase.ijf.org/#/search"

        # inicializa o driver
        driver = init_driver()

        conn = conn_db.connect_open()

        # carrega a pagina
        driver = get_page(driver, url)

        select_option(driver, "what", "competitor")

        select_option(driver, "country", str(cd_atributo_pais))

        select_option(driver, "weight", str(cd_categoria))

        click_button(
            driver,
            "/html/body/div[1]/div[2]/div/div[2]/div/div/div[1]/button",
        )

        id_pais = id_pais
        id_peso = id_peso

        # Catch the webpage content
        html_content = get_webpage_content(
            driver,
            "/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/table",
        )

        page = driver.find_element(By.XPATH, "//*")

        # Get the page source
        html_content = page.get_attribute("innerHTML")

        soup = BeautifulSoup(html_content, "html.parser")

        content = soup.find(
            "table", class_="js-tbl_results table-tr_middle table table-hover"
        )

        for row in content.tbody.find_all("tr"):
            columns = row.find_all("td")

            if columns != []:
                link_foto = columns[0].find("img")["src"]
                nome = columns[1].text.strip()
                data_nascimento = columns[2].text.strip()

                button_td = columns[3].find_all("a")

                link_perfil = (
                    "https://judobase.ijf.org/" + button_td[0]["href"]
                )
                link_resultados = (
                    "https://judobase.ijf.org/" + button_td[1]["href"]
                )
                link_disputas = (
                    "https://judobase.ijf.org/" + button_td[2]["href"]
                )
                link_estatisticas = (
                    "https://judobase.ijf.org/" + button_td[3]["href"]
                )

                id_judoca = link_perfil.split("/")[6]

                campos = [
                    "id_judoca",
                    "nm_judoca",
                    "ds_link_foto",
                    "ds_link_perfil",
                    "ds_link_resultado",
                    "ds_link_disputa",
                    "ds_link_estatistica",
                    "id_peso",
                    "id_pais",
                ]

                valores = [
                    id_judoca,
                    nome.replace("'", "''"),
                    link_foto,
                    link_perfil,
                    link_resultados,
                    link_disputas,
                    link_estatisticas,
                    id_peso,
                    id_pais,
                ]
                # print(valores)
                conn_db.insert_table(conn, "tb_judoca_lista", campos, valores)

        conn.commit()

        conn_db.connect_close(conn)

    except Exception as e:
        print(e)

    # on error print

    # Encerra safari
    # driver.quit()


def get_filtros():
    conn = conn_db.connect_open()

    # Opcoes de filtro
    query = conn_db.execute_query(
        conn,
        " SELECT "
        "    cd_atributo_pais, "
        "    id_pais, "
        "    cd_categoria, "
        "    id_peso "
        "  FROM tb_pais, tb_categoria "
        "  ;",
    )

    df = pd.DataFrame(
        query,
        columns=["cd_atributo_pais", "id_pais", "cd_categoria", "id_peso"],
    )

    conn_db.connect_close(conn)

    return df


def set_up_threads():
    filtros = get_filtros()

    with ThreadPoolExecutor(max_workers=5) as executor:
        return executor.map(
            main,
            filtros["id_pais"],
            filtros["id_peso"],
            filtros["cd_atributo_pais"],
            filtros["cd_categoria"],
            timeout=60,
        )


if __name__ == "__main__":
    print("Iniciando a captura de dados")
    print("Aguarde...")  # noqa: T001
    print(time.strftime("%d/%m/%Y %H:%M:%S"))  # noqa: T001
    start_time = time.perf_counter()

    conn = conn_db.connect_open()
    execute = "DELETE FROM tb_judoca_lista"
    conn_db.execute_query(conn, execute)
    conn.commit()
    conn_db.connect_close(conn)

    set_up_threads()

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print("Elapsed time: ", elapsed_time)
    print(time.strftime("%d/%m/%Y %H:%M:%S"))  # noqa: T001
    print("Dados capturados com sucesso!")  # noqa: T001
