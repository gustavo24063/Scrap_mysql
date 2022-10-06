from email.mime import image
from selenium import webdriver, common
import arrow
from time import sleep
import re
from unidecode import unidecode
import pyautogui as pi 
from _comandos_banco import CRUD



def marketSam():
    banco = CRUD('find_market.db', 'produtos')
    banco.createTable()
    logo = 'https://samsclubqa.vtexassets.com/arquivos/sams-club-logo.png'
    key_words = ['TEMPERO','CALDINHO','CONSERVA','TABLETE', 'CONGELADO', 'COZIDO', 'INSTANTANEO', 'LATA', 'PAPINHA', 'PRONTO', 'INSTANTANEA']
    produtos = ['arroz', 'feijao', 'acucar', 'sal', 'molho de tomate', 'farinha', 'macarrao', 'cafe', 'detergente', 'papel higienico']
    ar = arrow.now().format('DD/MM/YYYY')

    for p in produtos:
        product_category = p

        # ---------------------------------------------------- ABRIR O SITE ------------------------------------------------- #

        navegador = webdriver.Chrome()
        navegador.get(f'https://www.samsclub.com.br/{p}?_q={p}&map=ft')
        sleep(2)
        while True:
            try:
                navegador.find_element('xpath','//*[contains(concat( " ", @class, " " ), concat( " ", "vtex-cep", " " ))]')
                break
            except:
                pass
        
        # ------------------------------------------------------- COLOCAR CEP ------------------------------------------------ #

        sleep(3)
        navegador.find_element('xpath','//*[contains(concat( " ", @class, " " ), concat( " ", "vtex-cep", " " ))]').send_keys('89052-381')
        sleep(1)
        navegador.find_element('xpath','//*[@id="button"]').click()
        sleep(3)
        navegador.fullscreen_window()
        sleep(3)
        navegador.fullscreen_window()
        for i in range(10):
            pi.hotkey('ctrl','-')
            sleep(0.2)
        sleep(2)
        try:
            navegador.find_element('xpath','//*[contains(concat( " ", @class, " " ), concat( " ", "h-100", " " )) and contains(concat( " ", @class, " " ), concat( " ", "ph5", " " ))]').click()
        except:
            pass

        #  ----------------------------------------------- LINK DAS INFORMAÇÕES ---------------------------------------- #

        sleep(2)
        xpath_link = '//*[contains(concat( " ", @class, " " ), concat( " ", "pa4", " " ))]'
        xpath_image = '//*[contains(concat( " ", @class, " " ), concat( " ", "vtex-product-summary-2-x-image", " " ))]'
        xpath_price = '//*[contains(concat( " ", @class, " " ), concat( " ", "vtex-productShowCasePrice", " " ))]'
        xpath_name = '//*[contains(concat( " ", @class, " " ), concat( " ", "vtex-product-summary-2-x-brandName", " " ))]'

        links = []
        links2 = []
        names = []
        prices = []
        imgs = []
        weight = []

        cont = 0

        # ---------------------------------------- LINKS -------------------------------------------- # 

        while True:
            link_elements = navegador.find_elements('tag name', 'a')
            for link_el in link_elements:
                try:
                    href = link_el.get_attribute('href')
                    if 'p' in href[-1] and '/' in href[-2] and href not in links:
                        links.append(href)
                            
                except:
                    pass
            navegador.execute_script("window.scrollTo(0,(document.body.scrollHeight/2))")
            link_elements2 = navegador.find_elements('tag name', 'a')
            for link_el in link_elements2:
                try:
                    href = link_el.get_attribute('href')
                    print(href)
                    if 'p' in href[-1] and '/' in href[-2] and href not in links:
                        links2.append(href)
                        
                except:
                    pass
            for i in links2:
                if i not in links:
                    links.append(i)
            for i in links:
                print(i)
            try:
                navegador.find_element('xpath','//*[contains(concat( " ", @class, " " ), concat( " ", "h-100", " " )) and contains(concat( " ", @class, " " ), concat( " ", "ph5", " " ))]').click()
                pass
            except:
                break
        
        # ------------------------------------- NOMES PRODUTOS ------------------------------------------ #

        name_elements = navegador.find_elements('xpath', xpath_name)
        price_elements = navegador.find_elements('xpath', xpath_price)
        image_elements = navegador.find_elements('xpath', xpath_image)
        for name_el in name_elements:
            name = unidecode(name_el.text)
            name = re.sub(r"[^a-zA-Z0-9- ]","",name)
            names.append(name)
            print(name)
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
            bkprice[0] = bkprice[0].replace('R$', '').replace(' ', '').replace(',', '.')
            prices.append(bkprice[0])
        
        # ---------------------------------------- IMAGENS PRODUTOS -------------------------------------- #

        image_elements = navegador.find_elements('xpath', xpath_image)
        for image_el in image_elements:
            href = image_el.get_attribute('src')
            imgs.append(href)
        
        navegador.quit()

        # --------------------------------------- INSERÇÃO NO BANCO --------------------------------------- #

        print(f'{len(names)} {len(prices)} {len(links)} {len(imgs)}')
        for i in range(len(links)):
            verify_product = True
            for k in key_words:
                if k.upper() in str(names[i]).upper():
                    verify_product = False
            if verify_product:
                banco.insert('Sams', product_category, names[i], weight[i], float(prices[i]), imgs[i], links[i], logo, ar)