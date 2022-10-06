
from selenium import webdriver
import arrow
from time import sleep
import re
import pyautogui as pi
from unidecode import unidecode
from _testeMySQL import CRUD
def marketAtacadao():
    banco = CRUD()
    logo = ''
    ar = arrow.now().format('DD/MM/YYYY')
    key_words = ['TEMPERO','CALDINHO','CONSERVA','TABLETE', 'CONGELADO', 'COZIDO', 'INSTANTANEO', 'LATA', 'PAPINHA', 'PRONTO', 'INSTANTANEA']
    produtos = ['papel higienico', 'molho de tomate', 'acucar', 'arroz', 'feijao',  'sal',  'farinha', 'macarrao', 'cafe', 'detergente' ]

    for p in produtos:
        product_category = p
        navegador = webdriver.Chrome()
        navegador.get(f'https://www.atacadao.com.br/catalogo/?q={p}')
        navegador.fullscreen_window()

        while True:
            try:
                navegador.find_element('xpath','/html/body/div[3]/div/div/div/div/div/div[2]/div')
                print('foi')
                break
            except:
                pass
                print('n foi')

        for i in range(10):
            pi.hotkey('ctrl','-')
            sleep(0.2)
        sleep(8)
        xpath_price = '//*[contains(concat( " ", @class, " " ), concat( " ", "product-box__price--number", " " ))]'
        xpath_name = '//*[contains(concat( " ", @class, " " ), concat( " ", "product-box__name", " " ))]'

        links = []
        names = []
        prices = []
        imgs = []
        weight = []
        if f == 'molho de tomate':
            f = 'molho'

        elif f == 'papel higiênico':
            f = 'papel'

        # ---------------------------------------- LINKS -------------------------------------------- # 

        link_elements = navegador.find_elements('tag name', 'a')
        for link_el in link_elements:
            try:
                href = link_el.get_attribute('href')
                if f in href and '#' not in href:
                    print(href, 'Passou')
                    links.append(href)  
            except:
                pass     

        # ------------------------------------- NOMES PRODUTOS ------------------------------------------ #

        name_elements = navegador.find_elements('xpath', xpath_name)
        for name_el in name_elements:
            name = unidecode(name_el.text)
            name = re.sub(r"[^a-zA-Z0-9- ]","",name)
            names.append(name)
            listed_name = name.split(' ')
            check_weight = str(listed_name[-1])

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

        image_elements = navegador.find_elements('tag name', 'img')
        for e in image_elements:
            try:
                img = e.get_attribute('src')
                if 'sku' in img and 'bing' not in img:
                    imgs.append(img)
                    print(img)
            except:
                pass
        

        # --------------------------------------- INSERÇÃO NO BANCO --------------------------------------- #

        print(f'{len(names)} {len(prices)} {len(links)} {len(imgs)}')
        for i in range(len(names)):
            verify_product = True
            for k in key_words:
                if k.upper() in str(names[i]).upper():
                    verify_product = False
            if verify_product:
                banco.insert('Bistek', product_category, names[i], weight[i], float(prices[i]), imgs[i], links[i], logo, str(ar))
        
        navegador.quit()
    banco.finaliza()
