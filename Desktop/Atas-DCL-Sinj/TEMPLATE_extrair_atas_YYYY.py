# -*- coding: utf-8 -*-
"""
EXTRATOR DE ATAS CIRCUNSTANCIADAS DO SINJ-DF - ANO YYYY
========================================================

INSTRUÇÕES DE USO:
1. Copie este arquivo e renomeie para: 02_extrair_atas_sinj_2006.py (para 2006)
2. Altere a variável ANO_PROCESSAMENTO para o ano desejado
3. Execute: python 02_extrair_atas_sinj_2006.py

Este script:
1. Baixa todos os DCLs do ano especificado do SINJ-DF
2. Faz OCR da primeira página para identificar atas no sumário
3. Separa PDFs individuais por ata (Sucinta/Circunstanciada, Ordinária/Extraordinária)
4. Integra com a estrutura de pastas local do OneDrive

Autor: Sistema de Automação CLDF
Data: 2025
"""

# ======================================================================
# ⚠️  CONFIGURAÇÃO NECESSÁRIA
# ======================================================================
# Altere o ano abaixo para o ano que deseja processar
ANO_PROCESSAMENTO = 2006  # ← ALTERE AQUI PARA O ANO DESEJADO (2006, 2005, etc)
# ======================================================================

import os
import sys
import requests
import json
import re
import time
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin, urlparse
import logging
import shutil

# ======================================================================
# CONFIGURAÇÕES
# ======================================================================

USUARIO = "omega"
ONEDRIVE_NAME = "OneDrive - Câmara Legislativa do Distrito Federal - CLDF"
BASE_PATH = Path(f"C:/Users/{USUARIO}/{ONEDRIVE_NAME}")
PASTA_BASE = 'Cadernos_Anais_CLDF'

# Diretórios de trabalho
DIR_DOWNLOADS = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/downloads_{ANO_PROCESSAMENTO}")
DIR_PROCESSADOS = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/processados_{ANO_PROCESSAMENTO}")

# URL base do SINJ-DF
SINJ_BASE_URL = "https://www.sinj.df.gov.br/sinj"
SINJ_PESQUISA_URL = f"{SINJ_BASE_URL}/PesquisarDiretorioDiario.aspx"

# Headers para requisições
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# ======================================================================
# LOGGING
# ======================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'extrator_atas_{ANO_PROCESSAMENTO}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ======================================================================
# FUNÇÕES (Copie do arquivo 01_extrair_atas_sinj_2007.py)
# ======================================================================

def criar_diretorios():
    """Cria diretórios de trabalho necessários"""
    DIR_DOWNLOADS.mkdir(parents=True, exist_ok=True)
    DIR_PROCESSADOS.mkdir(parents=True, exist_ok=True)
    logger.info(f"✅ Diretórios criados/verificados")

def obter_dcls_sinj(ano):
    """Obtém lista de DCLs disponíveis no SINJ-DF para um ano específico"""
    # [COPIE A FUNÇÃO DO ARQUIVO 01_extrair_atas_sinj_2007.py]
    pass

def baixar_dcl(url, nome_arquivo):
    """Baixa um DCL do SINJ-DF"""
    # [COPIE A FUNÇÃO DO ARQUIVO 01_extrair_atas_sinj_2007.py]
    pass

def extrair_atas_do_sumario(caminho_pdf):
    """Extrai informações de atas do sumário (primeira página) do PDF"""
    # [COPIE A FUNÇÃO DO ARQUIVO 01_extrair_atas_sinj_2007.py]
    pass

def separar_pdf_por_ata(caminho_pdf, atas_info):
    """Separa um PDF em múltiplos PDFs, um para cada ata"""
    # [COPIE A FUNÇÃO DO ARQUIVO 01_extrair_atas_sinj_2007.py]
    pass

def organizar_pdfs_na_estrutura(pdfs_separados, ano):
    """Organiza PDFs separados na estrutura de pastas do OneDrive"""
    # [COPIE A FUNÇÃO DO ARQUIVO 01_extrair_atas_sinj_2007.py]
    pass

def processar_ano(ano):
    """Processa todos os DCLs de um ano"""
    logger.info(f"\n{'='*70}")
    logger.info(f"PROCESSANDO ANO {ano}")
    logger.info(f"{'='*70}\n")
    
    criar_diretorios()
    
    # 1. Obter lista de DCLs
    dcls = obter_dcls_sinj(ano)
    if not dcls:
        logger.warning(f"⚠️  Nenhum DCL encontrado para {ano}")
        return
    
    # 2. Baixar DCLs
    dcls_baixados = []
    for dcl_info in dcls:
        caminho = baixar_dcl(dcl_info['url'], dcl_info['nome'])
        if caminho:
            dcls_baixados.append(caminho)
        time.sleep(1)
    
    logger.info(f"✅ {len(dcls_baixados)} DCLs baixados")
    
    # 3. Processar cada DCL
    for caminho_dcl in dcls_baixados:
        atas = extrair_atas_do_sumario(caminho_dcl)
        if atas:
            pdfs_separados = separar_pdf_por_ata(caminho_dcl, atas)
            organizar_pdfs_na_estrutura(pdfs_separados, ano)

if __name__ == "__main__":
    try:
        processar_ano(ANO_PROCESSAMENTO)
        logger.info(f"\n✅ PROCESSAMENTO CONCLUÍDO!")
    except Exception as e:
        logger.error(f"❌ ERRO: {e}", exc_info=True)
        sys.exit(1)

