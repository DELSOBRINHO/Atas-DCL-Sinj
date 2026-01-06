# -*- coding: utf-8 -*-
"""
EXTRATOR DE ATAS CIRCUNSTANCIADAS DO SINJ-DF - ANO 2007
========================================================

Este script:
1. Baixa todos os DCLs de 2007 do SINJ-DF
2. Faz OCR da primeira página para identificar atas no sumário
3. Separa PDFs individuais por ata (Sucinta/Circunstanciada, Ordinária/Extraordinária)
4. Integra com a estrutura de pastas local do OneDrive

Uso:
    python 01_extrair_atas_sinj_2007.py

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

# ======================================================================
# CONFIGURAÇÕES
# ======================================================================

ANO_PROCESSAMENTO = 2007
USUARIO = "omega"
ONEDRIVE_NAME = "OneDrive - Câmara Legislativa do Distrito Federal - CLDF"
BASE_PATH = Path(f"C:/Users/{USUARIO}/{ONEDRIVE_NAME}")
PASTA_BASE = 'Cadernos_Anais_CLDF'

# Diretórios de trabalho
DIR_DOWNLOADS = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/downloads_2007")
DIR_PROCESSADOS = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/processados_2007")

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
# FUNÇÕES PRINCIPAIS
# ======================================================================

def criar_diretorios():
    """Cria diretórios de trabalho necessários"""
    DIR_DOWNLOADS.mkdir(parents=True, exist_ok=True)
    DIR_PROCESSADOS.mkdir(parents=True, exist_ok=True)
    logger.info(f"✅ Diretórios criados/verificados")

def obter_dcls_sinj(ano):
    """
    Obtém lista de DCLs disponíveis no SINJ-DF para um ano específico

    Args:
        ano: Ano a processar (ex: 2007)

    Returns:
        Lista de dicionários com informações dos DCLs
    """
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

            # Fazer requisição
            response = requests.get(SINJ_PESQUISA_URL, params=params, headers=HEADERS, timeout=30)
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
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        
        caminho = DIR_DOWNLOADS / nome_arquivo
        with open(caminho, 'wb') as f:
            f.write(response.content)
        
        logger.info(f"✅ Salvo: {caminho}")
        return caminho
    except Exception as e:
        logger.error(f"❌ Erro ao baixar {nome_arquivo}: {e}")
        return None

def extrair_atas_do_sumario(caminho_pdf):
    """
    Extrai informações de atas do sumário (primeira página) do PDF

    Args:
        caminho_pdf: Caminho do arquivo PDF

    Returns:
        Lista de dicionários com informações das atas encontradas
    """
    logger.info(f"📖 Analisando sumário: {caminho_pdf.name}")

    try:
        import pdfplumber
    except ImportError:
        logger.error("❌ pdfplumber não instalado. Execute: pip install pdfplumber")
        return []

    atas = []

    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            # Extrair texto da primeira página (sumário)
            primeira_pagina = pdf.pages[0]
            texto = primeira_pagina.extract_text()

            if not texto:
                logger.warning(f"  ⚠️  Não foi possível extrair texto da primeira página")
                return []

            logger.info(f"  📄 Texto extraído ({len(texto)} caracteres)")

            # Padrões para identificar atas
            padroes = [
                (r'ATA\s+(?:SUCINTA|CIRCUNSTANCIADA|CIRC)\s+(?:DA\s+)?(\d+)ª\s+SESSÃO\s+(ORDINÁRIA|EXTRAORDINÁRIA)', 'ata'),
                (r'(\d+)ª\s+SESSÃO\s+(ORDINÁRIA|EXTRAORDINÁRIA).*?(?:SUCINTA|CIRCUNSTANCIADA|CIRC)', 'sessao'),
            ]

            for padrao, tipo in padroes:
                matches = re.finditer(padrao, texto, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    atas.append({
                        'tipo': tipo,
                        'numero': match.group(1) if len(match.groups()) > 0 else None,
                        'tipo_sessao': match.group(2) if len(match.groups()) > 1 else None,
                        'texto_encontrado': match.group(0)
                    })

            logger.info(f"  ✅ {len(atas)} atas identificadas no sumário")

    except Exception as e:
        logger.error(f"  ❌ Erro ao analisar PDF: {e}")

    return atas

def separar_pdf_por_ata(caminho_pdf, atas_info):
    """
    Separa um PDF em múltiplos PDFs, um para cada ata

    Args:
        caminho_pdf: Caminho do PDF original
        atas_info: Lista de informações das atas (páginas, tipo, etc)

    Returns:
        Lista de caminhos dos PDFs separados
    """
    logger.info(f"✂️  Separando PDF: {caminho_pdf.name}")

    if not atas_info:
        logger.warning(f"  ⚠️  Nenhuma ata identificada, copiando PDF original")
        return [caminho_pdf]

    try:
        from PyPDF2 import PdfReader, PdfWriter
    except ImportError:
        logger.error("❌ PyPDF2 não instalado. Execute: pip install PyPDF2")
        return [caminho_pdf]

    pdfs_separados = []

    try:
        with open(caminho_pdf, 'rb') as f:
            pdf_reader = PdfReader(f)
            total_paginas = len(pdf_reader.pages)

            logger.info(f"  📊 Total de páginas: {total_paginas}")

            # Se apenas uma ata, retornar o PDF original
            if len(atas_info) <= 1:
                logger.info(f"  ℹ️  Uma única ata encontrada, mantendo PDF original")
                return [caminho_pdf]

            # Separar por ata (simplificado - usar páginas sequenciais)
            paginas_por_ata = total_paginas // len(atas_info)

            for idx, ata in enumerate(atas_info):
                writer = PdfWriter()

                # Calcular páginas desta ata
                inicio = idx * paginas_por_ata
                fim = (idx + 1) * paginas_por_ata if idx < len(atas_info) - 1 else total_paginas

                # Incluir página da próxima ata (para não perder texto)
                if idx < len(atas_info) - 1 and fim < total_paginas:
                    fim += 1

                # Adicionar páginas ao novo PDF
                for page_num in range(inicio, min(fim, total_paginas)):
                    writer.add_page(pdf_reader.pages[page_num])

                # Gerar nome do arquivo
                tipo_ata = "AC" if "CIRCUNSTANCIADA" in str(ata.get('texto_encontrado', '')).upper() else "AS"
                tipo_sessao = "SE" if "EXTRAORDINÁRIA" in str(ata.get('tipo_sessao', '')).upper() else "SO"
                numero = str(ata.get('numero', idx+1)).zfill(3)

                nome_saida = f"{caminho_pdf.stem}_{numero}_{tipo_sessao}_{tipo_ata}.pdf"
                caminho_saida = DIR_PROCESSADOS / nome_saida

                with open(caminho_saida, 'wb') as output_file:
                    writer.write(output_file)

                pdfs_separados.append(caminho_saida)
                logger.info(f"  ✅ Criado: {nome_saida} (páginas {inicio+1}-{fim})")

    except Exception as e:
        logger.error(f"  ❌ Erro ao separar PDF: {e}")
        return [caminho_pdf]

    return pdfs_separados

def organizar_pdfs_na_estrutura(pdfs_separados, ano):
    """
    Organiza PDFs separados na estrutura de pastas do OneDrive

    Args:
        pdfs_separados: Lista de caminhos dos PDFs
        ano: Ano de processamento
    """
    logger.info(f"📁 Organizando PDFs na estrutura...")

    # Determinar legislatura
    legislaturas = {
        (1991, 1994): 1,
        (1995, 1998): 2,
        (1999, 2002): 3,
        (2003, 2006): 4,
        (2007, 2010): 5,
        (2011, 2014): 6,
        (2015, 2018): 7,
        (2019, 2022): 8,
        (2023, 2026): 9,
    }

    num_legislatura = None
    for (inicio, fim), num in legislaturas.items():
        if inicio <= ano <= fim:
            num_legislatura = num
            break

    if not num_legislatura:
        logger.error(f"❌ Legislatura não encontrada para ano {ano}")
        return

    # Construir caminho da pasta de destino
    leg_folder = f"{str(num_legislatura).zfill(2)}_Legislatura_{legislaturas.get((2007, 2010), 5)}"
    pasta_destino = BASE_PATH / PASTA_BASE / leg_folder / "Cadernos_PDF" / "PDFs_Individuais" / str(ano)

    pasta_destino.mkdir(parents=True, exist_ok=True)

    logger.info(f"  📂 Destino: {pasta_destino}")

    # Copiar PDFs para a estrutura
    import shutil
    for pdf_origem in pdfs_separados:
        try:
            pdf_destino = pasta_destino / pdf_origem.name
            shutil.copy2(pdf_origem, pdf_destino)
            logger.info(f"  ✅ Copiado: {pdf_origem.name}")
        except Exception as e:
            logger.error(f"  ❌ Erro ao copiar {pdf_origem.name}: {e}")

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
        time.sleep(1)  # Respeitar servidor
    
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

