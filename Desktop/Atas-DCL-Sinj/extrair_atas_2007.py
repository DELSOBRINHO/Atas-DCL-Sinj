# -*- coding: utf-8 -*-
"""
EXTRATOR DE ATAS CIRCUNSTANCIADAS DO SINJ-DF - ANO 2007
========================================================

Este script:
1. Extrai links dos DCLs de 2007 do SINJ-DF
2. Baixa todos os DCLs
3. Faz OCR da primeira página para identificar atas no sumário
4. Separa PDFs individuais apenas das ATAS CIRCUNSTANCIADAS
5. Organiza na estrutura de pastas local

Uso:
    python extrair_atas_2007.py

Autor: Sistema de Automação CLDF
Data: 2025
"""

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
import urllib3

# Desabilita avisos de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ======================================================================
# CONFIGURAÇÕES
# ======================================================================

ANO_PROCESSAMENTO = 2007
USUARIO = "omega"

# Diretórios de trabalho
DIR_DOWNLOADS = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/downloads_2007")
DIR_PROCESSADOS = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/processados_2007")
DIR_ATAS_AC = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/atas_circunstanciadas_2007")

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
        logging.FileHandler(f'extrator_atas_2007.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ======================================================================
# FUNÇÕES PRINCIPAIS
# ======================================================================

def criar_diretorios():
    """Cria diretórios de trabalho necessários"""
    DIR_DOWNLOADS.mkdir(parents=True, exist_ok=True)
    DIR_PROCESSADOS.mkdir(parents=True, exist_ok=True)
    DIR_ATAS_AC.mkdir(parents=True, exist_ok=True)
    logger.info(f"✅ Diretórios criados/verificados")

def obter_dcls_sinj(ano):
    """Obtém lista de DCLs disponíveis no SINJ-DF para um ano específico"""
    logger.info(f"🔍 Buscando DCLs de {ano} no SINJ-DF...")

    try:
        from bs4 import BeautifulSoup
    except ImportError:
        logger.error("❌ BeautifulSoup4 não instalado. Execute: pip install beautifulsoup4")
        return []

    dcls = []
    meses = list(range(1, 13))  # 1 a 12

    for mes in meses:
        try:
            # Construir URL de pesquisa
            params = {
                'tipodiario': 'DCL',
                'ano': ano,
                'mes': mes
            }

            logger.info(f"  📅 Buscando mês {mes:02d}/{ano}...")

            # Fazer requisição (desabilita verificação SSL)
            response = requests.get(SINJ_PESQUISA_URL, params=params, headers=HEADERS, timeout=30, verify=False)
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')

            # Encontrar links de download (padrão do SINJ)
            links = soup.find_all('a', href=re.compile(r'\.pdf$', re.IGNORECASE))

            for link in links:
                href = link.get('href')
                texto = link.get_text(strip=True)

                if href and 'dcl' in texto.lower():
                    url_completa = urljoin(SINJ_BASE_URL, href)

                    # Extrair data do texto
                    match_data = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', texto)
                    if match_data:
                        dia, mes_txt, ano_txt = match_data.groups()
                        data_str = f"{ano_txt}-{mes_txt.zfill(2)}-{dia.zfill(2)}"
                    else:
                        data_str = f"{ano}-{mes:02d}-01"

                    dcls.append({
                        'url': url_completa,
                        'nome': f"DCL_{data_str}.pdf",
                        'data': data_str,
                        'texto': texto
                    })

            time.sleep(0.5)  # Respeitar servidor

        except Exception as e:
            logger.warning(f"  ⚠️  Erro ao processar mês {mes}: {e}")
            continue

    logger.info(f"✅ {len(dcls)} DCLs encontrados para {ano}")
    return dcls

def baixar_dcl(url, nome_arquivo):
    """Baixa um DCL do SINJ-DF"""
    try:
        logger.info(f"⬇️  Baixando: {nome_arquivo}")
        # Desabilita verificação SSL para evitar problemas de certificado
        response = requests.get(url, headers=HEADERS, timeout=30, verify=False)
        response.raise_for_status()

        caminho = DIR_DOWNLOADS / nome_arquivo
        with open(caminho, 'wb') as f:
            f.write(response.content)

        tamanho_mb = os.path.getsize(caminho) / (1024 * 1024)
        logger.info(f"✅ Salvo: {caminho} ({tamanho_mb:.2f} MB)")
        return caminho
    except Exception as e:
        logger.error(f"❌ Erro ao baixar {nome_arquivo}: {e}")
        return None

def main():
    """Função principal"""
    logger.info(f"\n{'='*70}")
    logger.info(f"EXTRATOR DE ATAS CIRCUNSTANCIADAS - ANO {ANO_PROCESSAMENTO}")
    logger.info(f"{'='*70}\n")
    
    criar_diretorios()
    
    # 1. Obter lista de DCLs
    dcls = obter_dcls_sinj(ANO_PROCESSAMENTO)
    if not dcls:
        logger.warning(f"⚠️  Nenhum DCL encontrado para {ANO_PROCESSAMENTO}")
        return
    
    # 2. Baixar DCLs
    logger.info(f"\n{'='*70}")
    logger.info(f"BAIXANDO {len(dcls)} DCLs")
    logger.info(f"{'='*70}\n")
    
    dcls_baixados = []
    for i, dcl_info in enumerate(dcls, 1):
        logger.info(f"[{i}/{len(dcls)}] Processando: {dcl_info['nome']}")
        caminho = baixar_dcl(dcl_info['url'], dcl_info['nome'])
        if caminho:
            dcls_baixados.append(caminho)
        time.sleep(1)  # Respeitar servidor
    
    logger.info(f"\n✅ {len(dcls_baixados)} DCLs baixados com sucesso")
    logger.info(f"\n{'='*70}")
    logger.info(f"PRÓXIMOS PASSOS:")
    logger.info(f"{'='*70}")
    logger.info(f"1. Executar: python separar_atas_2007.py")
    logger.info(f"2. Isso irá extrair e separar apenas as ATAS CIRCUNSTANCIADAS")
    logger.info(f"3. Os PDFs serão salvos em: {DIR_ATAS_AC}")

if __name__ == "__main__":
    main()

