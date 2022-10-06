from selenium import webdriver
import arrow
from time import sleep
import os
import re
from unidecode import unidecode
from _testeMySQL import CRUD

def marketCooper():

    banco = CRUD()
    logo = ''
    ar = arrow.now().format('DD/MM/YYYY')
    mercados = ['a.verde', 'garcia', 'i.norte', 'mafisa', 'omino', 'v.nova']
    key_words = ['TEMPERO','CALDINHO','CONSERVA','TABLETE', 'CONGELADO', 'COZIDO', 'INSTANTANEO', 'LATA', 'PAPINHA', 'PRONTO', 'INSTANTANEA']
    for j in mercados:
        #feijao, arroz, açucar, café, >>cerveja, detergente, feijao, macarrao, molho, papel higienico, sal
        produtos_n = ['feijao', 'arroz', 'acucar', 'cafe', 'detergente', 'macarrao', 'molho', 'papel_higienico', 'sal' ]
        produtos = ['busca?q=Feijao+1kg', 'listar/12', 'listar/5',  'listar/43',   'listar/401', 
        'listar/199', 'listar/106', 'busca?q=papel%20higiênico',  'listar/97']

        for i in range(9):
            product_category = produtos_n[i]
            continuar = True
            navegador = webdriver.Chrome()
            navegador.get(f'https://www.minhacooper.com.br/loja/{j}-bnu/produto/{produtos[i]}')
            navegador.fullscreen_window()
            height = navegador.execute_script("return document.body.scrollHeight")
            while True:
                try:
                    navegador.find_element('xpath','//*[@id="variant-list"]/div/div/div/div[4]/div[3]/div[2]/div/a').click()
                    break
                except:
                    pass
            
            while continuar:
                #Scroll down the page to show all the products
                for i in range(5):
                    navegador.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                    sleep(1.5)
                try:
                    navegador.find_element('xpath', '//*[@id="variant-list"]/div/div/div/div[4]/div[3]/div[2]/div/a').click()
                except:
                    continuar = False
                    pass

            xpath_link = '//*[contains(concat( " ", @class, " " ), concat( " ", "product-variation__name", " " ))]'
            xpath_image = '//*[contains(concat( " ", @class, " " ), concat( " ", "product-variation__image", " " ))]'
            xpath_price = '//*[contains(concat( " ", @class, " " ), concat( " ", "product-variation__price", " " ))]'
            xpath_name = '//*[contains(concat( " ", @class, " " ), concat( " ", "product-variation__name", " " ))]'

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
                bkprice = price.split('\n')
                bkprice[0] = bkprice[0].replace('R$', '').replace(' ', '').replace(',', '.').replace('De', '')
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
                    banco.insert('Bistek', product_category, names[i], weight[i], float(prices[i]), imgs[i], links[i], logo, str(ar))
            
        navegador.quit()
    banco.finaliza()
        