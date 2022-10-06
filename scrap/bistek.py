from selenium import webdriver
import arrow
from time import sleep
import os
import re
import pyautogui as pi
from unidecode import unidecode
from _testeMySQL import CRUD
import requests
from bs4 import BeautifulSoup


def marketBistek():
    banco = CRUD()
    ar = arrow.now().format('DD/MM/YYYY')
    logo = ''
    key_words = ['TEMPERO','CALDINHO','CONSERVA','TABLETE', 'CONGELADO', 'COZIDO', 'INSTANTANEO', 'LATA', 'PAPINHA', 'PRONTO', 'INSTANTANEA', 'BISCOITO, ESPUMANTE', 'SALGADINHO', 'SALADA']
    produtos = ['arroz', 'molho de tomate', 'acucar', 'papel higienico', 'feijao',  'sal',  'farinha', 'macarrao', 'cafe', 'detergente' ]

    for p in produtos:
        product_category = p
        continuar = True
        navegador = webdriver.Chrome()
        navegador.get(f'https://www.bistek.com.br/catalogsearch/result/index/?q={p}&product_list_limit=all')
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
        weight = []

        # ---------------------------------------- LINKS ------------------------------------------------ # 

        link_elements = navegador.find_elements('xpath', xpath_link)
        for link_el in link_elements:
            href = link_el.get_attribute('href')
            links.append(href)

        # ------------------------------------- NOMES PRODUTOS ------------------------------------------ #

        name_elements = navegador.find_elements('xpath', xpath_name)
        for name_el in name_elements:
            name = unidecode(name_el.text)
            name = re.sub(r"[^a-zA-Z0-9- ]","",name)
            names.append(name)
            listed_name = name.split(' ')
            
            check_weight = listed_name[-1]
            check_weight = str(check_weight).upper()
            check_weight = str(check_weight).replace('KG','').replace('G','')
            print(check_weight)
            try:
                weight.append(float(check_weight))
            except:
                weight.append(0)

           

        # ---------------------------------------- IMAGENS PRODUTOS -------------------------------------- #

        image_elements = navegador.find_elements('xpath', xpath_image)
        for image_el in image_elements:
            href = image_el.get_attribute('src')
            imgs.append(href)

        # --------------------------------------------- Prices ------------------------------------------- #

        alvo = f'https://www.bistek.com.br/catalogsearch/result/index/?q={p}&product_list_limit=all'

        response = requests.get(alvo)
        doc = BeautifulSoup(response.text, 'html.parser')
        tag = doc.find_all(["span"], class_="price-wrapper")
        spans = str(tag).split('</span>')
        spans2 = []

        
        for i in spans:
            x = i
            lista = x.split(' ')
            for k in lista:
                if k == r'data-price-type="finalPrice"':
                    print(i)
                    spans2.append(i)
        
        for i in spans2:
            print(i)
            valor = str(i).split('R$')
            xa = u'\xa0'
            print(valor)
            valor = valor[1].replace(xa, '').replace(',','.')
            print(valor)
            prices.append(valor)


        # --------------------------------------- INSERÇÃO NO BANCO --------------------------------------- #
        for i in range(len(links)):
                verify_product = True
                for k in key_words:
                    if k.upper() in str(names[i]).upper():
                        verify_product = False
                if verify_product:
                    banco.insert('Bistek', product_category, names[i], weight[i], float(prices[i]), imgs[i], links[i], logo, str(ar))

        navegador.quit()
    banco.finaliza()
