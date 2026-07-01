import requests
from bs4 import BeautifulSoup
import re
import demjson3
import json
import sqlite3

pesquisa = "nome_da_pesquisa"  # Troque pelo nome que quiser dar para sua base de dados.
termo = "termos de pesquisa"  # Troque pelos termos de busca que deseja utilizar.
filename = re.sub(r"\W+", "_", termo.lower())

url = (
    'https://periodicos.capes.gov.br/index.php/acervo/buscador.html?q=all%3Acontains%28'+ termo.replace(' ', '+') 
    + '%29&mode=advanced&source=all')

headers = {'Host': 'www.periodicos.capes.gov.br', #sempre que vamos trabalhar com Web, usamos o protocolo HTTP, composto por requisições e respostas. Cada uma tem cabeçalhos antes dos dados. Este cabeçalho é o que mandamos pro site para ele saber q é legítimo.
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:152.0) Gecko/20100101 Firefox/152.0', 
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3', 
'Accept-Encoding': 'gzip, deflate, br, zstd', 
'Connection': 'keep-alive', 
"Cookie": "COLE_AQUI_SEUS_COOKIES_ATUALIZADOS" 
'Upgrade-Insecure-Requests': '1', 
'Sec-Fetch-Dest': 
'document', 
'Sec-Fetch-Mode': 
'navigate', 
'Sec-Fetch-Site': 'none', 
'Sec-GPC': '1', 
'Priority': 'u=0, i'}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.content, 'html.parser')
script_tag = soup.find('script', string=re.compile(r'const itens'))
script_text = script_tag.string

pattern = re.search(r'const\s+itens\s*+=\s*(\[.*?\]);', script_text, re.DOTALL)

js_obj = pattern.group(1)

json_obj = demjson3.decode(js_obj)

for artigo in json_obj:
    id = artigo.get('id')
    #print(id)
    nurl = "https://www.periodicos.capes.gov.br/index.php/acervo/buscador.html?task=detalhes&source=all&id=" + id
    nresponse = requests.get(nurl, headers=headers)
    nsoup = BeautifulSoup(nresponse.content, 'html.parser')
    abs_tag = nsoup.find('meta', attrs={'name' : 'abstract'})
    abstract = abs_tag['content']
    artigo['concept'] = abstract

conn = sqlite3.connect(f'{pesquisa}.db', isolation_level=None)
conn.execute(f'CREATE TABLE IF NOT EXISTS {filename} (type TEXT, id TEXT, title TEXT, autor TEXT, resource_title TEXT, publish_year TEXT, volume TEXT, issue TEXT, first_page TEXT, last_page TEXT, doi TEXT, abstract TEXT) STRICT')

for item in json_obj:
    conn.execute(f'INSERT OR REPLACE INTO {filename} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (item.get('type'), item.get('id'),
                                                                                                item.get('title'), item.get('autor'),
                                                                                                item.get('resource_title'), item.get('publish_year'),
                                                                                                item.get('volume'), item.get('issue'),
                                                                                                item.get('first_page'), item.get('last_page'),
                                                                                                item.get('doi'), item.get('concept'))) 
