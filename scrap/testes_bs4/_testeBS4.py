import requests
from bs4 import BeautifulSoup

produtos = []
valores = []
geral = []
prices = []



alvo = f'https://www.bistek.com.br/catalogsearch/result/index/?q=acucar&product_list_limit=all'

response = requests.get(alvo)
doc = BeautifulSoup(response.text, 'html.parser')
tag = doc.find_all(["span"], class_="price-wrapper")
spans = str(tag).split('</span>')
spans2 = []

# --------------- Prices ----------------------
for i in spans:
    x = i
    lista = x.split(' ')
    for k in lista:
        if k == r'data-price-type="finalPrice"':
            spans2.append(i)
 
for i in spans2:
    print(i)
    valor = str(i).split('R$')
    prices.append(valor[1])


    
#print(tag)