#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BUSCAR LINKS DCL 2007 + JAN-FEV 2008 COM SELENIUM
==================================================

Busca links de DCLs no SINJ-DF para:
- 2007: janeiro a dezembro (12 meses)
- 2008: janeiro a fevereiro (2 meses)

Total: 14 meses de busca

Uso:
    python buscar_links_2007_2008_selenium.py

Autor: Sistema de Automação CLDF
Data: 2025-12-22
"""

import os
import sys
import time
import json
import logging
from pathlib import Path
from datetime import datetime

# ======================================================================
# CONFIGURAÇÕES
# ======================================================================

ANO_PROCESSAMENTO = 2007
USUARIO = "omega"

# Diretórios
DIR_LINKS = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/links_2007")

# ======================================================================
# LOGGING
# ======================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'buscar_links_2007_2008.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ======================================================================
# FUNÇÕES PRINCIPAIS
# ======================================================================

def instalar_dependencias():
    """Instala dependências necessárias"""
    print("📦 Verificando dependências...")
    
    import subprocess
    
    pacotes = {
        "selenium": "selenium",
        "webdriver_manager": "webdriver-manager",
        "bs4": "beautifulsoup4"
    }
    
    for modulo, pacote in pacotes.items():
        try:
            __import__(modulo)
            print(f"   ✅ {pacote} já instalado")
        except ImportError:
            print(f"   ⬇️  Instalando {pacote}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pacote, "-q"])
            print(f"   ✅ {pacote} instalado")

def buscar_links_selenium():
    """
    Busca links de DCLs usando Selenium
    Busca: 2007 (jan-dez) + 2008 (jan-fev)
    """
    print("\n" + "="*70)
    print("🔍 BUSCANDO LINKS DE DCLs COM SELENIUM")
    print("="*70)

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
        print("\n📥 Inicializando Selenium...")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        url = "https://www.sinj.df.gov.br/sinj/PesquisarDiretorioDiario.aspx"
        print(f"🌐 Acessando {url}...")
        driver.get(url)

        # Aguardar página carregar
        time.sleep(4)

        # Selecionar tipo de diário (DCL = "4")
        print("⚙️  Configurando filtros...")
        try:
            tipo_select = Select(driver.find_element(By.ID, "select_tipo_fonte"))
            tipo_select.select_by_value("4")
            time.sleep(1)
            print("   ✅ Tipo de diário selecionado (DCL)")
        except Exception as e:
            print(f"   ⚠️  Erro ao selecionar tipo: {e}")

        # Meses a buscar: 1-12 (2007) + 1-2 (2008)
        meses_busca = [
            (2007, 1), (2007, 2), (2007, 3), (2007, 4), (2007, 5), (2007, 6),
            (2007, 7), (2007, 8), (2007, 9), (2007, 10), (2007, 11), (2007, 12),
            (2008, 1), (2008, 2)
        ]

        print(f"\n📅 Buscando {len(meses_busca)} meses...")
        print("-" * 70)

        for ano, mes in meses_busca:
            try:
                print(f"\n   🔍 Buscando {ano}-{mes:02d}...")

                # Selecionar ano
                ano_select = Select(driver.find_element(By.ID, "select_ano"))
                ano_select.select_by_value(str(ano))
                time.sleep(0.5)

                # Selecionar mês
                mes_select = Select(driver.find_element(By.ID, "select_mes"))
                mes_select.select_by_value(str(mes))

                # Aguardar resultados carregarem (sem clicar em botão)
                time.sleep(3)

                # Extrair links da tabela de resultados
                try:
                    # Procurar por links na tabela tbody_resultado
                    tbody = driver.find_element(By.ID, "tbody_resultado")
                    links = tbody.find_elements(By.TAG_NAME, "a")

                    links_encontrados = 0
                    for link in links:
                        href = link.get_attribute('href')
                        texto = link.text.strip()

                        if href and '.pdf' in href.lower():
                            dcls.append({
                                'url': href,
                                'texto': texto,
                                'mes': mes,
                                'ano': ano
                            })
                            links_encontrados += 1

                    print(f"      ✅ {links_encontrados} link(s) encontrado(s)")

                except Exception as e:
                    print(f"      ⚠️  Erro ao extrair links: {e}")

                time.sleep(1)  # Respeitar servidor

            except Exception as e:
                print(f"      ⚠️  Erro ao buscar {ano}-{mes:02d}: {e}")
                continue

        driver.quit()
        print("\n" + "-" * 70)

    except Exception as e:
        print(f"❌ Erro ao inicializar Selenium: {e}")
        print("   💡 Certifique-se de que o Chrome está instalado")
        return []

    return dcls

def salvar_links(dcls):
    """Salva links em arquivo JSON"""
    print(f"\n💾 SALVANDO LINKS")
    print("-" * 70)
    
    # Criar diretório se não existir
    DIR_LINKS.mkdir(parents=True, exist_ok=True)
    
    # Arquivo de saída
    arquivo_links = DIR_LINKS / "dcls_2007.json"
    
    # Salvar JSON
    with open(arquivo_links, 'w', encoding='utf-8') as f:
        json.dump(dcls, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Links salvos em: {arquivo_links}")
    print(f"   Total de links: {len(dcls)}")
    
    # Estatísticas por ano
    links_2007 = sum(1 for d in dcls if d['ano'] == 2007)
    links_2008 = sum(1 for d in dcls if d['ano'] == 2008)
    
    print(f"\n📊 ESTATÍSTICAS")
    print("-" * 70)
    print(f"   2007: {links_2007} links")
    print(f"   2008: {links_2008} links")
    print(f"   Total: {len(dcls)} links")
    
    # Mostrar primeiros 5 links
    print(f"\n📋 PRIMEIROS 5 LINKS")
    print("-" * 70)
    for i, dcl in enumerate(dcls[:5], 1):
        print(f"   {i}. {dcl['texto']}")
        print(f"      URL: {dcl['url']}")

def main():
    """Função principal"""
    print("\n" + "="*70)
    print("BUSCAR LINKS DCL 2007 + JAN-FEV 2008 COM SELENIUM")
    print("="*70)
    
    # Instalar dependências
    instalar_dependencias()
    
    # Buscar links
    dcls = buscar_links_selenium()
    
    if dcls:
        # Salvar links
        salvar_links(dcls)
        print("\n✅ SUCESSO! Links buscados e salvos com sucesso!")
    else:
        print("\n❌ ERRO! Nenhum link foi encontrado.")
        print("   💡 Verifique sua conexão com a internet")
        print("   💡 Verifique se o SINJ-DF está acessível")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()

