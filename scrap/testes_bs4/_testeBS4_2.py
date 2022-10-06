import requests
from bs4 import BeautifulSoup

produtos = []
valores = []
geral = []
prices = []



alvo = f'https://www.bistek.com.br/catalogsearch/result/index/?q=acucar&product_list_limit=all'

response = requests.get(alvo)
doc = BeautifulSoup(response.text, 'html.parser')
tag = doc.find_all('a', class_='')

print(tag)