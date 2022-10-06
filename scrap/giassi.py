#Giassi Supermercados - 

from selenium import webdriver
import arrow
from time import sleep
import os
import re
import pyautogui as pi
from unidecode import unidecode
from _comandos_banco import CRUD
def marketGiassi():
    banco = CRUD('find_market.db', 'produtos')
    banco.createTable()
    logo = ''
    ar = arrow.now().format('DD/MM/YYYY')
    key_words = ['TEMPERO','CALDINHO','CONSERVA','TABLETE', 'CONGELADO', 'COZIDO', 'INSTANTANEO', 'LATA', 'PAPINHA', 'PRONTO', 'INSTANTANEA']
    produtos = ['arroz', 'feijao', 'açucar', 'sal', 'Molho de Tomate', 'Farinha', 'Macarrão', 'Café', 'Detergente', 'Papel Higiênico']

    # ---------------------------------------------------- ABRIR O SITE ------------------------------------------------- #
    for p in produtos:
        product_category = p
        navegador = webdriver.Chrome()
        navegador.get(f'https://www.giassi.com.br/{p}?_q={p}&fuzzy=0&initialMap=ft&initialQuery={p}&map=ft&operator=and&order=&priceRange=1%20TO%2028&searchState')
        navegador.fullscreen_window()
        sleep(2)

        while True:
            try:
                navegador.find_element('xpath','/html/body/div[2]/div/div[1]/div/div[2]/div/div/section/div[2]/div/div[4]/div/div[2]/div/div[4]/div/div/div/div/div/a').click()
            except:
                break
            
    # ---------------------------------------------------- CAMINHO DOS ITENS ------------------------------------------------- #

        xpath_link = '#gallery-layout-container .t-body'
        xpath_image = '//*[contains(concat( " ", @class, " " ), concat( " ", "product-variation__image", " " ))]'
        xpath_price = '//*[contains(concat( " ", @class, " " ), concat( " ", "product-variation__price", " " ))]'
        xpath_name = '#gallery-layout-container .t-body'

        links = []
        names = []
        prices = []
        imgs = []
        weight = []

        # ---------------------------------------- LINKS -------------------------------------------- # 

        link_elements = navegador.find_elements('xpath', xpath_link)
        for link_el in link_elements:
            href = link_el.get_attribute('href')
            print(href)
            if p in href:
                links.append(href)

        # ------------------------------------- NOMES PRODUTOS ------------------------------------------ #

        name_elements = navegador.find_elements('xpath', xpath_name)
        for name_el in name_elements:
            name = unidecode(name_el.text)
            name = re.sub(r"[^a-zA-Z0-9- ]","",name)
            names.append(name)
            listed_name = name.split(' ')
            check_weight = listed_name[-1]
            if 'KG' in check_weight.upper:
                weight.append(float(check_weight)*1000)
            elif 'G' in check_weight.upper:
                weight.append(float(check_weight))
            else:
                weight.append('')

        # ---------------------------------------- PREÇOS PRODUTOS --------------------------------------- #

        price_elements = navegador.find_elements('xpath', xpath_price)
        for price_el in price_elements:
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

        for i in range(len(links)):
            verify_product = True
            for k in key_words:
                if k.upper() in str(names[i]).upper():
                    verify_product = False
            if verify_product:
                banco.insert('Giassi', product_category, names[i], weight[i], float(prices[i]), imgs[i], links[i], logo, ar)
