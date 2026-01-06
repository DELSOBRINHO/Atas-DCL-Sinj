# -*- coding: utf-8 -*-
"""
INSPETOR DO SINJ-DF
===================

Inspeciona a página do SINJ-DF para encontrar os elementos corretos
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

print("Abrindo SINJ-DF...")
driver = webdriver.Chrome()

try:
    url = "https://www.sinj.df.gov.br/sinj/PesquisarDiretorioDiario.aspx"
    driver.get(url)
    
    print(f"Página carregada: {driver.title}")
    print(f"URL: {driver.current_url}\n")
    
    # Aguardar um pouco para a página carregar
    time.sleep(3)
    
    # Procurar por elementos comuns
    print("Procurando por elementos...\n")
    
    # Procurar por selects
    selects = driver.find_elements(By.TAG_NAME, "select")
    print(f"Encontrados {len(selects)} elementos SELECT:")
    for i, select in enumerate(selects):
        print(f"  {i+1}. ID: {select.get_attribute('id')}")
        print(f"     Name: {select.get_attribute('name')}")
        print(f"     Class: {select.get_attribute('class')}\n")
    
    # Procurar por inputs
    inputs = driver.find_elements(By.TAG_NAME, "input")
    print(f"\nEncontrados {len(inputs)} elementos INPUT:")
    for i, inp in enumerate(inputs[:10]):  # Mostrar apenas os 10 primeiros
        print(f"  {i+1}. ID: {inp.get_attribute('id')}")
        print(f"     Type: {inp.get_attribute('type')}")
        print(f"     Name: {inp.get_attribute('name')}\n")
    
    # Procurar por botões
    buttons = driver.find_elements(By.TAG_NAME, "button")
    print(f"\nEncontrados {len(buttons)} elementos BUTTON:")
    for i, btn in enumerate(buttons[:5]):
        print(f"  {i+1}. ID: {btn.get_attribute('id')}")
        print(f"     Text: {btn.text}")
        print(f"     Class: {btn.get_attribute('class')}\n")
    
    # Procurar por links
    links = driver.find_elements(By.TAG_NAME, "a")
    print(f"\nEncontrados {len(links)} elementos LINK")
    
    # Procurar por PDFs
    pdf_links = [l for l in links if '.pdf' in l.get_attribute('href').lower()]
    print(f"Links PDF encontrados: {len(pdf_links)}")
    
    # Salvar HTML para análise
    with open('sinj_page.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print("\nHTML salvo em: sinj_page.html")
    
finally:
    driver.quit()
    print("\nNavegador fechado.")

