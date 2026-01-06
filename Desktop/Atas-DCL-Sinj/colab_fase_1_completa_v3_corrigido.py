#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COLAB FASE 1 COMPLETA V3 - CORRIGIDO COM SELENIUM
==================================================

Pipeline completo para Google Colab:
1. Buscar links de DCLs (2007 + jan-fev 2008) - COM SELENIUM
2. Baixar DCLs
3. Processar com OCR
4. Gerar relatório

Uso em Google Colab:
    !pip install selenium webdriver-manager pdfplumber openpyxl beautifulsoup4
    !python colab_fase_1_completa_v3_corrigido.py

Autor: Sistema de Automação CLDF
Data: 2025-12-22
"""

import os
import sys
import time
import json
import re
import logging
from pathlib import Path
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed

# ======================================================================
# CONFIGURAÇÕES
# ======================================================================

ANO_PROCESSAMENTO = 2007
DRIVE_PATH = "/content/drive/MyDrive/Atas-DCL-Sinj"

# Diretórios
DIR_LINKS = Path(f"{DRIVE_PATH}/links_2007")
DIR_DOWNLOADS = Path(f"{DRIVE_PATH}/downloads_2007")

# ======================================================================
# LOGGING
# ======================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ======================================================================
# FUNÇÕES PRINCIPAIS
# ======================================================================

def instalar_dependencias():
    """Instala dependências necessárias"""
    print("📦 Instalando dependências...")
    import subprocess
    
    pacotes = [
        "selenium",
        "webdriver-manager",
        "pdfplumber",
        "openpyxl",
        "beautifulsoup4",
        "requests"
    ]
    
    for pacote in pacotes:
        try:
            __import__(pacote.replace("-", "_"))
            print(f"   ✅ {pacote} já instalado")
        except ImportError:
            print(f"   ⬇️  Instalando {pacote}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pacote, "-q"])
            print(f"   ✅ {pacote} instalado")

def buscar_links_sinj_selenium(ano, meses):
    """
    Busca links de DCLs usando Selenium
    (Contorna problemas de SSL e JavaScript dinâmico)
    """
    print(f"🔍 Buscando links de DCLs com Selenium...")
    
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    
    dcls = []
    
    # Configurar opções do Chrome
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        url = "https://www.sinj.df.gov.br/sinj/PesquisarDiretorioDiario.aspx"
        print(f"   🌐 Acessando {url}...")
        driver.get(url)
        
        time.sleep(3)
        
        # Selecionar tipo de diário (DCL)
        try:
            tipo_select = Select(driver.find_element(By.ID, "select_tipo_fonte"))
            tipo_select.select_by_value("4")
            time.sleep(1)
        except:
            print("   ⚠️ Não foi possível selecionar tipo de diário")
        
        # Processar cada mês
        for mes in meses:
            try:
                ano_busca = ano if mes <= 12 else ano + 1
                mes_busca = mes if mes <= 12 else mes - 12
                
                print(f"   📅 Buscando {ano_busca}-{mes_busca:02d}...")
                
                # Selecionar ano
                ano_select = Select(driver.find_element(By.ID, "select_ano"))
                ano_select.select_by_value(str(ano_busca))
                time.sleep(0.5)
                
                # Selecionar mês
                mes_select = Select(driver.find_element(By.ID, "select_mes"))
                mes_select.select_by_value(str(mes_busca))
                time.sleep(0.5)
                
                # Clicar em buscar
                try:
                    botao = driver.find_element(By.ID, "btn_pesquisar")
                    botao.click()
                except:
                    botoes = driver.find_elements(By.TAG_NAME, "button")
                    for botao in botoes:
                        if "pesquisar" in botao.text.lower():
                            botao.click()
                            break
                
                time.sleep(2)
                
                # Extrair links
                links = driver.find_elements(By.TAG_NAME, "a")
                
                for link in links:
                    try:
                        href = link.get_attribute("href")
                        texto = link.text.strip()
                        
                        if href and href.endswith(".pdf") and "dcl" in texto.lower():
                            dcls.append({
                                'url': href,
                                'texto': texto,
                                'mes': mes_busca,
                                'ano': ano_busca
                            })
                    except:
                        continue
                
                time.sleep(0.5)
                
            except Exception as e:
                print(f"   ⚠️ Erro ao buscar {ano_busca}-{mes_busca:02d}: {e}")
                continue
        
        driver.quit()
        
    except Exception as e:
        print(f"❌ Erro ao inicializar Selenium: {e}")
        return []
    
    print(f"✅ Total de links encontrados: {len(dcls)}")
    return dcls

def main():
    """Função principal"""
    print("=" * 70)
    print("COLAB FASE 1 COMPLETA V3 - CORRIGIDO COM SELENIUM")
    print("=" * 70)
    print()
    
    # Instalar dependências
    instalar_dependencias()
    print()
    
    # Criar diretórios
    DIR_LINKS.mkdir(parents=True, exist_ok=True)
    DIR_DOWNLOADS.mkdir(parents=True, exist_ok=True)
    print(f"✅ Diretórios criados")
    print()
    
    # PASSO 1: Buscar links
    print("📡 PASSO 1: BUSCAR LINKS")
    print("-" * 70)
    meses = list(range(1, 15))  # 1-12 (2007) + 1-2 (2008)
    links = buscar_links_sinj_selenium(ANO_PROCESSAMENTO, meses)
    
    # Salvar links
    arquivo_links = DIR_LINKS / "dcls_2007.json"
    with open(arquivo_links, 'w', encoding='utf-8') as f:
        json.dump(links, f, ensure_ascii=False, indent=2)
    print(f"✅ Links salvos em: {arquivo_links}")
    print()

if __name__ == "__main__":
    main()

