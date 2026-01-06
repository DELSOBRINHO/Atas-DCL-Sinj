# -*- coding: utf-8 -*-
"""
EXTRATOR DE LINKS DO SINJ-DF - ANO 2007
========================================

Este script extrai os links dos DCLs de 2007 usando Selenium
(para lidar com JavaScript dinâmico do SINJ-DF)

Uso:
    python extrair_links_sinj_2007.py

Autor: Sistema de Automação CLDF
Data: 2025
"""

import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime
import json

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
        logging.FileHandler(f'extrator_links_2007.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ======================================================================
# FUNÇÕES PRINCIPAIS
# ======================================================================

def extrair_links_com_selenium():
    """Extrai links usando Selenium para lidar com JavaScript"""
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import Select
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
    except ImportError:
        logger.error("❌ Selenium não instalado. Execute: pip install selenium")
        return []

    logger.info("🔍 Iniciando extração com Selenium...")

    # Configurar driver (usar Chrome)
    try:
        driver = webdriver.Chrome()
    except:
        logger.error("❌ ChromeDriver não encontrado. Instale com: pip install webdriver-manager")
        return []

    dcls = []

    try:
        url = "https://www.sinj.df.gov.br/sinj/PesquisarDiretorioDiario.aspx"
        driver.get(url)

        # Aguardar página carregar
        time.sleep(3)

        # Selecionar tipo de diário (DCL = "4")
        tipo_select = Select(driver.find_element(By.ID, "select_tipo_fonte"))
        tipo_select.select_by_value("4")

        time.sleep(1)

        # Processar cada mês
        for mes in range(1, 13):
            logger.info(f"  📅 Processando mês {mes:02d}/{ANO_PROCESSAMENTO}...")

            # Selecionar ano
            ano_select = Select(driver.find_element(By.ID, "select_ano"))
            ano_select.select_by_value(str(ANO_PROCESSAMENTO))

            time.sleep(0.5)

            # Selecionar mês
            mes_select = Select(driver.find_element(By.ID, "select_mes"))
            mes_select.select_by_value(str(mes))

            # Aguardar resultados carregarem
            time.sleep(3)

            # Extrair links da tabela de resultados
            try:
                # Procurar por links na tabela tbody_resultado
                tbody = driver.find_element(By.ID, "tbody_resultado")
                links = tbody.find_elements(By.TAG_NAME, "a")

                logger.info(f"    📄 Encontrados {len(links)} links")

                for link in links:
                    href = link.get_attribute('href')
                    texto = link.text.strip()

                    if href and '.pdf' in href.lower():
                        dcls.append({
                            'url': href,
                            'texto': texto,
                            'mes': mes,
                            'ano': ANO_PROCESSAMENTO
                        })
                        logger.info(f"    ✅ {texto[:60]}")
            except Exception as e:
                logger.warning(f"    ⚠️  Erro ao extrair links: {e}")

            time.sleep(1)

        logger.info(f"\n✅ {len(dcls)} DCLs encontrados")

    except Exception as e:
        logger.error(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()

    return dcls

def salvar_links(dcls):
    """Salva os links em um arquivo JSON"""
    DIR_LINKS.mkdir(parents=True, exist_ok=True)
    
    arquivo = DIR_LINKS / "dcls_2007.json"
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dcls, f, ensure_ascii=False, indent=2)
    
    logger.info(f"✅ Links salvos em: {arquivo}")
    return arquivo

def main():
    """Função principal"""
    logger.info(f"\n{'='*70}")
    logger.info(f"EXTRATOR DE LINKS - ANO {ANO_PROCESSAMENTO}")
    logger.info(f"{'='*70}\n")
    
    # Extrair links
    dcls = extrair_links_com_selenium()
    
    if dcls:
        # Salvar links
        salvar_links(dcls)
        
        logger.info(f"\n{'='*70}")
        logger.info(f"PRÓXIMOS PASSOS:")
        logger.info(f"{'='*70}")
        logger.info(f"1. Executar: python baixar_dcls_2007.py")
        logger.info(f"2. Depois: python separar_atas_2007.py")
    else:
        logger.warning(f"⚠️  Nenhum DCL encontrado")

if __name__ == "__main__":
    main()

