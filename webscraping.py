import time
import requests
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


# Funtion to initialize the webdriver
def init_driver():
    """initialize the webdriver"""
    # Abre o safari
    option = Options()
    option.headless = True
    driver = webdriver.Safari(options=option)
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
    time.sleep(5)
    return driver


# Function to select the option in the dropdown
def select_option(driver, name, value):
    """select the option in the dropdown"""
    # Seleciona no drop box a opcao indicada
    select_element = driver.find_element(By.NAME, name)
    select = Select(select_element)
    select.select_by_value(value)  # competitor or competition
    time.sleep(5)
    return driver


# Function to catch webpage contents
def get_webpage_content(driver, xpath):
    """catch webpage contents"""
    element = driver.find_element(By.XPATH, xpath)
    html_content = element.get_attribute("outerHTML")
    return html_content


def main():
    """main function"""
    # URL utilizada
    url = "https://judobase.ijf.org/#/search"

    # inicializa o driver
    driver = init_driver()

    # carrega a pagina
    driver = get_page(driver, url)

    # Catch the webpage content
    html_content = get_webpage_content(
        driver,
        "//html/",
    )

    soup = BeautifulSoup(html_content, "html.parser")

    content = soup.find(id="content")

    print(content)

    # fecha o driver
    driver = close_driver(driver)


main()
