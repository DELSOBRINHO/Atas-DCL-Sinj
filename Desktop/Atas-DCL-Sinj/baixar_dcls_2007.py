# -*- coding: utf-8 -*-
"""
BAIXADOR DE DCLs - ANO 2007
===========================

Este script baixa todos os DCLs de 2007 usando os links extraídos

Uso:
    python baixar_dcls_2007.py

Autor: Sistema de Automação CLDF
Data: 2025
"""

import os
import sys
import json
import requests
import time
import logging
from pathlib import Path
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ======================================================================
# CONFIGURAÇÕES
# ======================================================================

ANO_PROCESSAMENTO = 2007
USUARIO = "omega"

# Diretórios
DIR_LINKS = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/links_2007")
DIR_DOWNLOADS = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/downloads_2007")

# Headers
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
        logging.FileHandler(f'baixador_dcls_2007.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ======================================================================
# FUNÇÕES PRINCIPAIS
# ======================================================================

def carregar_links():
    """Carrega os links do arquivo JSON"""
    arquivo = DIR_LINKS / "dcls_2007.json"
    
    if not arquivo.exists():
        logger.error(f"❌ Arquivo não encontrado: {arquivo}")
        logger.info("Execute primeiro: python extrair_links_sinj_2007.py")
        return []
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        dcls = json.load(f)
    
    logger.info(f"✅ {len(dcls)} links carregados")
    return dcls

def baixar_dcl(url, nome_arquivo, tentativa=1):
    """Baixa um DCL"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=30, verify=False)
        response.raise_for_status()
        
        caminho = DIR_DOWNLOADS / nome_arquivo
        with open(caminho, 'wb') as f:
            f.write(response.content)
        
        tamanho_mb = os.path.getsize(caminho) / (1024 * 1024)
        return True, tamanho_mb
    except Exception as e:
        if tentativa < 3:
            time.sleep(2)
            return baixar_dcl(url, nome_arquivo, tentativa + 1)
        return False, str(e)

def main():
    """Função principal"""
    logger.info(f"\n{'='*70}")
    logger.info(f"BAIXADOR DE DCLs - ANO {ANO_PROCESSAMENTO}")
    logger.info(f"{'='*70}\n")
    
    # Criar diretório
    DIR_DOWNLOADS.mkdir(parents=True, exist_ok=True)
    
    # Carregar links
    dcls = carregar_links()
    if not dcls:
        return
    
    # Baixar DCLs
    logger.info(f"⬇️  Iniciando download de {len(dcls)} DCLs...\n")
    
    sucesso = 0
    erro = 0
    tamanho_total = 0
    
    for i, dcl in enumerate(dcls, 1):
        url = dcl['url']
        texto = dcl['texto']

        # Extrair número do DCL da URL
        # URL contém: "DCL%20n%C2%BA%20021%20de%2031%20de%20janeiro%20de%202007.pdf"
        import re
        import urllib.parse

        # Decodificar URL
        url_decoded = urllib.parse.unquote(url)

        # Procurar por "DCL nº XXX"
        match = re.search(r'DCL\s*n[º°]?\s*(\d+)', url_decoded)
        numero_dcl = match.group(1) if match else f"{dcl['mes']:02d}_{i:03d}"

        # Gerar nome do arquivo com número único do DCL
        nome_arquivo = f"DCL_{dcl['ano']}-{dcl['mes']:02d}-{numero_dcl}.pdf"

        # Verificar se já existe
        caminho = DIR_DOWNLOADS / nome_arquivo
        if caminho.exists():
            tamanho_mb = os.path.getsize(caminho) / (1024 * 1024)
            logger.info(f"[{i}/{len(dcls)}] ⏭️  Já existe: {nome_arquivo} ({tamanho_mb:.2f} MB)")
            sucesso += 1
            tamanho_total += tamanho_mb
            continue

        # Baixar
        resultado, tamanho = baixar_dcl(url, nome_arquivo)

        if resultado:
            logger.info(f"[{i}/{len(dcls)}] ✅ {nome_arquivo} ({tamanho:.2f} MB)")
            sucesso += 1
            tamanho_total += tamanho
        else:
            logger.error(f"[{i}/{len(dcls)}] ❌ Erro ao baixar {nome_arquivo}: {tamanho}")
            erro += 1

        time.sleep(0.5)  # Respeitar servidor
    
    # Resumo
    logger.info(f"\n{'='*70}")
    logger.info(f"RESUMO DO DOWNLOAD")
    logger.info(f"{'='*70}")
    logger.info(f"✅ Sucesso: {sucesso}/{len(dcls)}")
    logger.info(f"❌ Erros: {erro}/{len(dcls)}")
    logger.info(f"📊 Tamanho total: {tamanho_total:.2f} MB")
    logger.info(f"📁 Salvos em: {DIR_DOWNLOADS}")
    logger.info(f"\n{'='*70}")
    logger.info(f"PRÓXIMOS PASSOS:")
    logger.info(f"{'='*70}")
    logger.info(f"1. Executar: python separar_atas_2007.py")
    logger.info(f"2. Isso irá extrair apenas as ATAS CIRCUNSTANCIADAS")

if __name__ == "__main__":
    main()

