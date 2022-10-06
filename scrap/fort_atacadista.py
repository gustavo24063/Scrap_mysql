
from selenium import webdriver
import arrow
from time import sleep
import os
import re
from unidecode import unidecode
from _comandos_banco import CRUD
def marketFortAtacadista():
    banco = CRUD('find_market.db', 'produtos')
    banco.createTable()
    logo = ''
    ar = arrow.now().format('DD/MM/YYYY')
    #ceps 89052-381 (itoupava norte), 89066-003 (Itoupavazinha), 
    key_words = ['TEMPERO','CALDINHO','CONSERVA','TABLETE', 'CONGELADO', 'COZIDO', 'INSTANTANEO', 'LATA', 'PAPINHA', 'PRONTO', 'INSTANTANEA', 'REFRIGERANTE', 'BISCOITO', 'MANTEIGA']
    produtos = ['arroz', 'feijao', 'açucar', 'sal', 'molho de tomate', 'farinha', 'macarrao', 'cafe', 'detergente', 'papel higienico']

    for p in produtos:
        product_category = p
        pagina = 2
        proceed = True
        navegador = webdriver.Chrome()
        navegador.get(f'https://www.deliveryfort.com.br/buscar?q={p}')
        navegador.fullscreen_window()
        while True:
            try:
                navegador.find_element('xpath','//*[@id="shelf-zipcode"]').send_keys('89052-381')
                break
            except:
                pass
        while True:
            try:
                navegador.find_element('xpath','/html/body/div[3]/div/div[3]/div[2]/a[2]').click()
                break
            except:
                pass
        while True:
            try:
                navegador.find_element('xpath','/html/body/div[5]/div/div[2]/div[4]').click()
                break
            except:
                pass
        while True:
            try:
                navegador.find_element('xpath','/html/body/div[5]/div/div[2]/a').click()
                break
            except:
                pass
        while True:
            try:
                navegador.find_element('xpath','/html/body/div[7]/div/div[3]/a[1]').click()
                break
            except:
                pass
        navegador.fullscreen_window()
        while proceed:
            while True:
                try:
                    navegador.find_element('xpath', '//*[contains(concat( " ", @class, " " ), concat( " ", "pagination-link", " " ))]')
                    break
                except:
                    pass

            xpath_link = '//*[contains(concat( " ", @class, " " ), concat( " ", "shelf-item__title-link", " " ))]'
            xpath_image = '//*[contains(concat( " ", @class, " " ), concat( " ", "shelf-item__image", " " ))]'
            xpath_price = '//*[contains(concat( " ", @class, " " ), concat( " ", "shelf-item__best-price", " " ))]//strong'
            xpath_name = '//*[contains(concat( " ", @class, " " ), concat( " ", "shelf-item__title-link", " " ))]'

            links = []
            names = []
            prices = []
            imgs = []
            weight = []

            # ---------------------------------------- LINKS -------------------------------------------- # 

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
                split_price = price.split('\n')
                split_price[0] = split_price[0].replace('R$', '').replace(' ', '').replace(',','.')
                prices.append(split_price[0])

            # ---------------------------------------- IMAGENS PRODUTOS -------------------------------------- #

            image_elements = navegador.find_elements('tag name', 'img')
            for e in image_elements:
                if 'ids' in e.get_attribute('src'):
                    imgs.append(e.get_attribute('src'))


            # --------------------------------------- INSERÇÃO NO BANCO --------------------------------------- #

            for i in range(len(links)):
                verify_product = True
                for k in key_words:
                    if k.upper() in str(names[i]).upper():
                        verify_product = False
                if verify_product:
                    banco.insert('Fort Atacadista', product_category, names[i], weight[i], float(prices[i]), imgs[i], links[i], logo, ar)

            navegador.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            sleep(4)
            pagina += 1
            while True:
                try:
                    sleep(1)
                    navegador.find_element('xpath', f'/html/body/main/div[4]/div/div[2]/ul/li[{pagina}]/a').click()
                    sleep(1)
                    navegador.find_element('xpath', f'/html/body/main/div[4]/div/div[2]/ul/li[{pagina}]/a').click()
                    sleep(1)
                    break
                except:
                    proceed = False
                    break
