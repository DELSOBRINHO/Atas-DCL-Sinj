# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import urllib3
import re

urllib3.disable_warnings()

url = 'https://www.sinj.df.gov.br/sinj/PesquisarDiretorioDiario.aspx'
params = {'tipodiario': 'DCL', 'ano': 2007, 'mes': 1}

print(f"Testando URL: {url}")
print(f"Parâmetros: {params}\n")

try:
    response = requests.get(url, params=params, timeout=30, verify=False)
    print(f"Status: {response.status_code}")
    print(f"Content length: {len(response.content)} bytes\n")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Procurar por links PDF
    links_pdf = soup.find_all('a', href=re.compile(r'\.pdf$', re.IGNORECASE))
    print(f"Links PDF encontrados: {len(links_pdf)}\n")
    
    for i, link in enumerate(links_pdf[:5]):
        href = link.get('href')
        texto = link.get_text(strip=True)
        print(f"{i+1}. Texto: {texto}")
        print(f"   Href: {href}\n")
    
    # Procurar por todos os links
    todos_links = soup.find_all('a', href=True)
    print(f"\nTotal de links: {len(todos_links)}")
    
    # Mostrar alguns links
    print("\nPrimeiros 10 links:")
    for i, link in enumerate(todos_links[:10]):
        href = link.get('href')
        texto = link.get_text(strip=True)[:40]
        print(f"{i+1}. {texto} -> {href[:60]}")
    
except Exception as e:
    print(f"Erro: {e}")
    import traceback
    traceback.print_exc()

