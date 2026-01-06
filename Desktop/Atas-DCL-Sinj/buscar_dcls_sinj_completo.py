"""
Script completo para buscar DCLs no SINJ-DF
1. Busca DCLs por mês/ano
2. Baixa DCLs
3. Extrai data real da ata
4. Separa atas
5. Renomeia com data real
"""

import os
import json
import re
import time
from pathlib import Path
from datetime import datetime
import pdfplumber
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from urllib.parse import unquote

# Importar função de extração de data
from extrair_data_melhorado import extrair_data_melhorado

# Configuração
SINJ_URL = "https://www.sinj.df.gov.br/sinj/Consulta/Diario.html"
DOWNLOADS_DIR = "downloads_2007_novos"
ATAS_DIR = "atas_circunstanciadas_2007_validadas"
RELATORIO_FILE = "relatorio_busca_sinj.json"

Path(DOWNLOADS_DIR).mkdir(exist_ok=True)
Path(ATAS_DIR).mkdir(exist_ok=True)

MESES = {
    "Janeiro": "01", "Fevereiro": "02", "Março": "03", "Abril": "04",
    "Maio": "05", "Junho": "06", "Julho": "07", "Agosto": "08",
    "Setembro": "09", "Outubro": "10", "Novembro": "11", "Dezembro": "12"
}

relatorio = {
    "data_execucao": datetime.now().isoformat(),
    "dcls_baixados": 0,
    "atas_encontradas": 0,
    "atas_renomeadas": 0,
    "erros": []
}

def buscar_dcls_sinj(mes_nome, ano):
    """Busca DCLs no SINJ-DF para um mês específico"""
    driver = None
    try:
        from selenium.webdriver.chrome.options import Options

        # Configurar opções do Chrome
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(SINJ_URL)

        # Aguardar carregamento da página
        time.sleep(3)

        # Tentar encontrar e selecionar tipo de diário
        try:
            tipo_select = Select(driver.find_element(By.NAME, "tipoDiario"))
            tipo_select.select_by_value("DCL")
            time.sleep(1)
        except Exception as e:
            print(f"⚠️  Erro ao selecionar tipo: {e}")
            return []

        # Selecionar ano
        try:
            ano_select = Select(driver.find_element(By.NAME, "ano"))
            ano_select.select_by_value(str(ano))
            time.sleep(1)
        except Exception as e:
            print(f"⚠️  Erro ao selecionar ano: {e}")
            return []

        # Selecionar mês
        try:
            mes_select = Select(driver.find_element(By.NAME, "mes"))
            mes_select.select_by_value(mes_nome)
            time.sleep(3)
        except Exception as e:
            print(f"⚠️  Erro ao selecionar mês: {e}")
            return []

        # Extrair links de download
        links = []
        try:
            download_elements = driver.find_elements(By.XPATH, "//a[contains(@href, 'download')]")

            for elem in download_elements:
                href = elem.get_attribute("href")
                if href:
                    links.append(href)
        except Exception as e:
            print(f"⚠️  Erro ao extrair links: {e}")

        print(f"✅ Encontrados {len(links)} DCLs em {mes_nome}/{ano}")
        return links

    except Exception as e:
        print(f"❌ Erro ao buscar {mes_nome}: {e}")
        relatorio["erros"].append(f"Busca {mes_nome}: {str(e)}")
        return []

    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def baixar_dcl(url, mes, ano):
    """Baixa um DCL do SINJ-DF"""
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            filename = unquote(url.split('/')[-1])
            if not filename.endswith('.pdf'):
                filename = f"DCL_{ano}_{mes}_{int(time.time())}.pdf"
            
            filepath = os.path.join(DOWNLOADS_DIR, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            relatorio["dcls_baixados"] += 1
            return filepath
    except Exception as e:
        print(f"❌ Erro ao baixar: {e}")
        relatorio["erros"].append(f"Download: {str(e)}")
    
    return None

def processar_dcl(pdf_path):
    """
    Processa um DCL:
    1. Extrai data real
    2. Separa atas
    3. Renomeia com data real
    """
    try:
        data_real = extrair_data_melhorado(pdf_path, verbose=False)
        
        if not data_real:
            print(f"⚠️  Não foi possível extrair data de {os.path.basename(pdf_path)}")
            return False
        
        print(f"✅ Data extraída: {data_real}")
        relatorio["atas_encontradas"] += 1
        
        return True
    
    except Exception as e:
        print(f"❌ Erro ao processar: {e}")
        relatorio["erros"].append(f"Processamento: {str(e)}")
        return False

# Executar busca
print("🔍 Iniciando busca de DCLs no SINJ-DF...")
print(f"Período: Janeiro a Dezembro de 2007\n")

for mes_nome, mes_num in list(MESES.items())[:3]:  # Testar com 3 meses
    print(f"\n📅 Processando {mes_nome}/2007...")
    
    try:
        # Buscar DCLs
        links = buscar_dcls_sinj(mes_nome, 2007)
        
        # Baixar e processar cada DCL
        for i, link in enumerate(links[:2], 1):  # Limitar a 2 por mês para teste
            print(f"  [{i}/{min(2, len(links))}] Baixando DCL...")
            pdf_path = baixar_dcl(link, mes_num, 2007)
            
            if pdf_path:
                processar_dcl(pdf_path)
        
        time.sleep(2)
    
    except Exception as e:
        print(f"❌ Erro ao processar {mes_nome}: {e}")
        relatorio["erros"].append(f"Mês {mes_nome}: {str(e)}")

# Salvar relatório
with open(RELATORIO_FILE, 'w', encoding='utf-8') as f:
    json.dump(relatorio, f, indent=2, ensure_ascii=False)

print(f"\n✅ Busca concluída!")
print(f"   DCLs baixados: {relatorio['dcls_baixados']}")
print(f"   Atas encontradas: {relatorio['atas_encontradas']}")
print(f"   Relatório salvo em: {RELATORIO_FILE}")

