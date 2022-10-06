from selenium import webdriver
import arrow
from time import sleep
import os
import re
import pyautogui as pi
from unidecode import unidecode
from _comandos_banco import CRUD

ar = arrow.now().format('DD/MM/YYYY')
key_words = ['TEMPERO','CALDINHO','CONSERVA','TABLETE', 'CONGELADO', 'COZIDO', 'INSTANTANEO', 'LATA', 'PAPINHA', 'PRONTO', 'INSTANTANEA']
produtos = ['papel higienico', 'molho de tomate', 'acucar', 'arroz', 'feijao',  'sal',  'farinha', 'macarrao', 'cafe', 'detergente' ]

for f in produtos:
    continuar = True
    navegador = webdriver.Chrome()
    navegador.get(f'https://www.bistek.com.br/catalogsearch/result/index/?q={f}&product_list_limit=all')
    navegador.fullscreen_window()
    sleep(2)

    xpath_link = '//*[contains(concat( " ", @class, " " ), concat( " ", "product-item-link", " " ))]'
    xpath_image = '//*[contains(concat( " ", @class, " " ), concat( " ", "product-image-photo", " " ))]'
    xpath_price = '//*[@id="maincontent"]/div[3]/div[1]/div[3]/div[2]/ol/li[8]/div/div[2]/div[1]/span[2]/span[1]'
    xpath_name = '//*[contains(concat( " ", @class, " " ), concat( " ", "product-item-link", " " ))]'

    links = []
    names = []
    prices = []
    imgs = []

    # ---------------------------------------- LINKS -------------------------------------------- # 

    # link_elements = navegador.find_elements('xpath', xpath_link)
    # for link_el in link_elements:
    #     href = link_el.get_attribute('href')
    #     links.append(href)

    # # ------------------------------------- NOMES PRODUTOS ------------------------------------------ #

    # name_elements = navegador.find_elements('xpath', xpath_name)
    # for name_el in name_elements:
    #     name = unidecode(name_el.text)
    #     name = re.sub(r"[^a-zA-Z0-9- ]","",name)
    #     names.append(name)

    # ---------------------------------------- PREÇOS PRODUTOS --------------------------------------- #

    price_elements = navegador.find_elements('xpath', '//*[contains(concat( " ", @class, " " ), concat( " ", "weee", " " ))]')
    for price_el in price_elements:
        price_el = price_el.find_element('xpath','//*[contains(concat( " ", @class, " " ), concat( " ", "price", " " ))]')
        price = price_el.text
        bkprice = price.split('\n')
        bkprice[0] = bkprice[0].replace('R$', '').replace(' ', '').replace(',','.')
        prices.append(bkprice[0])

    # ---------------------------------------- IMAGENS PRODUTOS -------------------------------------- #

    image_elements = navegador.find_elements('xpath', xpath_image)
    for image_el in image_elements:
        href = image_el.get_attribute('src')
        imgs.append(href)

    # --------------------------------------- INSERÇÃO NO BANCO --------------------------------------- #

    for i in prices:
        print(i)

    for i in  imgs:
        print(i)

    navegador.quit()