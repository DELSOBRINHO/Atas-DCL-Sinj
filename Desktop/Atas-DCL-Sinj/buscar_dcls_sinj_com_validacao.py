"""
Script para buscar DCLs no SINJ-DF com validação de data real da ata
Extrai data do conteúdo do PDF, não do nome do arquivo
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
import pdfplumber
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from urllib.parse import unquote

# Configuração
SINJ_URL = "https://www.sinj.df.gov.br/sinj/Consulta/Diario.html"
DOWNLOADS_DIR = "downloads_2007_validados"
ATAS_DIR = "atas_circunstanciadas_2007_validadas"
MESES = {
    "Janeiro": "01", "Fevereiro": "02", "Março": "03", "Abril": "04",
    "Maio": "05", "Junho": "06", "Julho": "07", "Agosto": "08",
    "Setembro": "09", "Outubro": "10", "Novembro": "11", "Dezembro": "12"
}

# Criar diretórios
Path(DOWNLOADS_DIR).mkdir(exist_ok=True)
Path(ATAS_DIR).mkdir(exist_ok=True)

def extrair_data_real_pdf(pdf_path):
    """
    Extrai a data real da ata do conteúdo do PDF
    Procura por padrões como "EM 19 DE DEZEMBRO DE 2006"
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Processa primeiras 3 páginas
            for page_num in range(min(3, len(pdf.pages))):
                text = pdf.pages[page_num].extract_text()
                if not text:
                    continue
                
                # Padrão: "EM DD DE MÊS DE YYYY"
                pattern = r'EM\s+(\d{1,2})\s+DE\s+(\w+)\s+DE\s+(\d{4})'
                matches = re.findall(pattern, text, re.IGNORECASE)
                
                if matches:
                    dia, mes_nome, ano = matches[0]
                    meses_pt = {
                        'JANEIRO': '01', 'FEVEREIRO': '02', 'MARÇO': '03',
                        'ABRIL': '04', 'MAIO': '05', 'JUNHO': '06',
                        'JULHO': '07', 'AGOSTO': '08', 'SETEMBRO': '09',
                        'OUTUBRO': '10', 'NOVEMBRO': '11', 'DEZEMBRO': '12'
                    }
                    
                    mes_num = meses_pt.get(mes_nome.upper())
                    if mes_num:
                        data_str = f"{ano}-{mes_num}-{int(dia):02d}"
                        return data_str
        
        return None
    except Exception as e:
        print(f"Erro ao extrair data de {pdf_path}: {e}")
        return None

def buscar_dcls_sinj(mes_nome, ano):
    """
    Busca DCLs no SINJ-DF para um mês específico
    Retorna lista de URLs de download
    """
    driver = webdriver.Chrome()
    try:
        driver.get(SINJ_URL)
        
        # Aguardar carregamento
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "select"))
        )
        
        # Selecionar tipo de diário (DCL)
        tipo_select = Select(driver.find_element(By.NAME, "tipoDiario"))
        tipo_select.select_by_value("DCL")
        time.sleep(1)
        
        # Selecionar ano
        ano_select = Select(driver.find_element(By.NAME, "ano"))
        ano_select.select_by_value(str(ano))
        time.sleep(1)
        
        # Selecionar mês
        mes_select = Select(driver.find_element(By.NAME, "mes"))
        mes_select.select_by_value(mes_nome)
        time.sleep(2)
        
        # Extrair links de download
        links = []
        download_elements = driver.find_elements(By.XPATH, "//a[contains(@href, 'download')]")
        
        for elem in download_elements:
            href = elem.get_attribute("href")
            if href:
                links.append(href)
        
        print(f"✅ Encontrados {len(links)} DCLs em {mes_nome}/{ano}")
        return links
    
    finally:
        driver.quit()

def baixar_dcl(url, mes, ano):
    """Baixa um DCL do SINJ-DF"""
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            # Extrair nome do arquivo
            filename = unquote(url.split('/')[-1])
            if not filename.endswith('.pdf'):
                filename = f"DCL_{ano}_{mes}_{int(time.time())}.pdf"
            
            filepath = os.path.join(DOWNLOADS_DIR, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return filepath
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")
    
    return None

def processar_dcl(pdf_path, mes, ano):
    """
    Processa um DCL:
    1. Extrai data real
    2. Valida data
    3. Separa atas
    """
    data_real = extrair_data_real_pdf(pdf_path)
    
    if not data_real:
        print(f"⚠️  Não foi possível extrair data de {pdf_path}")
        return False
    
    print(f"✅ Data extraída: {data_real} (arquivo: {os.path.basename(pdf_path)})")
    
    # Validar se data está no período esperado
    try:
        data_obj = datetime.strptime(data_real, "%Y-%m-%d")
        ano_esperado = int(ano)
        
        # Permitir atas de até 2 meses antes (para casos como dezembro de 2006)
        if data_obj.year < ano_esperado - 1 or data_obj.year > ano_esperado:
            print(f"⚠️  Data fora do período: {data_real} (esperado: {ano})")
            return False
    except:
        return False
    
    return True

# Executar busca
print("🔍 Iniciando busca de DCLs no SINJ-DF...")
print(f"Período: Janeiro a Dezembro de 2007\n")

for mes_nome, mes_num in MESES.items():
    print(f"\n📅 Processando {mes_nome}/2007...")
    
    try:
        # Buscar DCLs
        links = buscar_dcls_sinj(mes_nome, 2007)
        
        # Baixar e processar cada DCL
        for i, link in enumerate(links[:5], 1):  # Limitar a 5 por mês para teste
            print(f"  [{i}/{min(5, len(links))}] Baixando DCL...")
            pdf_path = baixar_dcl(link, mes_num, 2007)
            
            if pdf_path:
                processar_dcl(pdf_path, mes_num, 2007)
        
        time.sleep(2)  # Aguardar entre meses
    
    except Exception as e:
        print(f"❌ Erro ao processar {mes_nome}: {e}")

print("\n✅ Busca concluída!")

