# -*- coding: utf-8 -*-
"""
SEPARADOR DE ATAS CIRCUNSTANCIADAS - ANO 2007
==============================================

Este script:
1. Lê os DCLs baixados de 2007
2. Extrai o sumário (primeira página)
3. Identifica APENAS as ATAS CIRCUNSTANCIADAS
4. Separa PDFs individuais para cada ata circunstanciada
5. Organiza na estrutura de pastas

Uso:
    python separar_atas_2007.py

Autor: Sistema de Automação CLDF
Data: 2025
"""

import os
import sys
import re
import time
import logging
from pathlib import Path
from datetime import datetime

# Importar bibliotecas de PDF
try:
    import pdfplumber
    import PyPDF2
except ImportError:
    print("❌ Bibliotecas necessárias não instaladas.")
    print("Execute: pip install pdfplumber PyPDF2")
    sys.exit(1)

# ======================================================================
# CONFIGURAÇÕES
# ======================================================================

ANO_PROCESSAMENTO = 2007
USUARIO = "omega"

# Diretórios
DIR_DOWNLOADS = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/downloads_2007")
DIR_ATAS_AC = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/atas_circunstanciadas_2007")

# ======================================================================
# LOGGING
# ======================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'separador_atas_2007.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ======================================================================
# FUNÇÕES PRINCIPAIS
# ======================================================================

def extrair_sumario(pdf_path):
    """Extrai texto da primeira página (sumário) do PDF"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            primeira_pagina = pdf.pages[0]
            texto = primeira_pagina.extract_text()
            return texto
    except Exception as e:
        logger.error(f"❌ Erro ao extrair sumário de {pdf_path}: {e}")
        return None

def encontrar_atas_circunstanciadas(texto_sumario):
    """
    Encontra APENAS as atas circunstanciadas no sumário
    Retorna lista com informações das atas
    Mais flexível com OCR
    """
    atas = []

    # Padrões para encontrar atas circunstanciadas (mais flexíveis)
    padroes = [
        # Padrão 1: "Ata Circunstanciada da XXXa Sessão (Ordinária|Extraordinária) YYY"
        r'Ata\s+Circunstanciada\s+da\s+(\d+)a?\s+Sessão\s+(Ordinária|Extraordinária)\s+(\d+)',
        # Padrão 2: "ATA CIRCUNSTANCIADA DA XXXa SESSÃO (ORDINÁRIA|EXTRAORDINÁRIA) YYY"
        r'ATA\s+CIRCUNSTANCIADA\s+DA\s+(\d+)a?\s+SESSÃO\s+(ORDINÁRIA|EXTRAORDINÁRIA)\s+(\d+)',
        # Padrão 3: Com caracteres OCR ruins
        r'Ata\s*Circ\.?\s*da\s+(\d+)a?\s+Sessão\s+(Ordinária|Extraordinária)\s+(\d+)',
        # Padrão 4: Sem espaços (OCR muito ruim)
        r'ATA\s*CIRCUNSTANCIADA\s*DA\s*(\d+)a?\s*(?:SESSÃO|Sessão)\s+(ORDINÁRIA|Ordinária|EXTRAORDINÁRIA|Extraordinária)\s*(\d+)',
        # Padrão 5: Sem espaços e com caracteres estranhos
        r'ATACIRCUNSTANCIADADA(\d+)a?\s*(?:SESSÃO|Sessão)?\s*(ORDINÁRIA|Ordinária|EXTRAORDINÁRIA|Extraordinária)?\s*(\d+)?',
    ]

    for padrao in padroes:
        matches = re.finditer(padrao, texto_sumario, re.IGNORECASE)

        for match in matches:
            try:
                numero_sessao = match.group(1)
                tipo_sessao = match.group(2) if len(match.groups()) >= 2 else "Ordinária"
                pagina_inicio = int(match.group(3)) if len(match.groups()) >= 3 and match.group(3) else 1

                # Normalizar tipo de sessão
                if tipo_sessao:
                    tipo_sessao = tipo_sessao.capitalize()
                    if "extraordin" in tipo_sessao.lower():
                        tipo_sessao = "Extraordinária"
                    else:
                        tipo_sessao = "Ordinária"
                else:
                    tipo_sessao = "Ordinária"

                # Verificar se já existe
                existe = any(a['numero_sessao'] == numero_sessao and
                           a['tipo_sessao'].lower() == tipo_sessao.lower()
                           for a in atas)

                if not existe and numero_sessao:
                    atas.append({
                        'numero_sessao': numero_sessao,
                        'tipo_sessao': tipo_sessao,
                        'pagina_inicio': pagina_inicio,
                        'tipo_ata': 'Circunstanciada'
                    })
            except (IndexError, ValueError, AttributeError):
                continue

    return atas

def separar_pdf_por_ata(pdf_path, atas):
    """
    Separa o PDF em PDFs individuais para cada ata circunstanciada
    """
    if not atas:
        logger.warning(f"⚠️  Nenhuma ata circunstanciada encontrada em {pdf_path}")
        return []

    pdfs_criados = []

    try:
        with open(pdf_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            total_paginas = len(pdf_reader.pages)

            # Ordenar atas por página de início
            atas_ordenadas = sorted(atas, key=lambda x: x['pagina_inicio'])

            for i, ata in enumerate(atas_ordenadas):
                pagina_inicio = ata['pagina_inicio'] - 1  # Converter para índice 0

                # Determinar página final
                if i < len(atas_ordenadas) - 1:
                    pagina_fim = atas_ordenadas[i + 1]['pagina_inicio'] - 1
                else:
                    pagina_fim = total_paginas

                # Criar novo PDF com as páginas da ata
                pdf_writer = PyPDF2.PdfWriter()

                for pagina_num in range(pagina_inicio, pagina_fim):
                    if pagina_num < total_paginas:
                        pdf_writer.add_page(pdf_reader.pages[pagina_num])

                # Gerar nome do arquivo
                data_dcl = Path(pdf_path).stem.replace('DCL_', '')
                tipo_sessao_abrev = 'SE' if 'Extraordinária' in ata['tipo_sessao'] else 'SO'
                numero_sessao = str(ata['numero_sessao']).zfill(3)

                nome_arquivo = f"{data_dcl}-{tipo_sessao_abrev}-{numero_sessao}-AC.pdf"
                caminho_saida = DIR_ATAS_AC / nome_arquivo

                # Salvar PDF
                with open(caminho_saida, 'wb') as out_f:
                    pdf_writer.write(out_f)
            
            tamanho_kb = os.path.getsize(caminho_saida) / 1024
            logger.info(f"✅ Criado: {nome_arquivo} ({tamanho_kb:.1f} KB)")
            pdfs_criados.append(caminho_saida)
        
        return pdfs_criados
    
    except Exception as e:
        logger.error(f"❌ Erro ao separar PDF {pdf_path}: {e}")
        return []

def main():
    """Função principal"""
    logger.info(f"\n{'='*70}")
    logger.info(f"SEPARADOR DE ATAS CIRCUNSTANCIADAS - ANO {ANO_PROCESSAMENTO}")
    logger.info(f"{'='*70}\n")
    
    # Criar diretório de saída
    DIR_ATAS_AC.mkdir(parents=True, exist_ok=True)
    
    # Listar DCLs baixados
    dcls = sorted(DIR_DOWNLOADS.glob("DCL_*.pdf"))
    
    if not dcls:
        logger.warning(f"⚠️  Nenhum DCL encontrado em {DIR_DOWNLOADS}")
        logger.info(f"Execute primeiro: python extrair_atas_2007.py")
        return
    
    logger.info(f"📄 Encontrados {len(dcls)} DCLs para processar\n")
    
    total_atas_ac = 0
    
    # Processar cada DCL
    for i, dcl_path in enumerate(dcls, 1):
        logger.info(f"[{i}/{len(dcls)}] Processando: {dcl_path.name}")
        
        # Extrair sumário
        sumario = extrair_sumario(dcl_path)
        if not sumario:
            continue
        
        # Encontrar atas circunstanciadas
        atas_ac = encontrar_atas_circunstanciadas(sumario)
        
        if atas_ac:
            logger.info(f"  📋 Encontradas {len(atas_ac)} atas circunstanciadas")
            
            # Separar PDFs
            pdfs = separar_pdf_por_ata(dcl_path, atas_ac)
            total_atas_ac += len(pdfs)
        else:
            logger.info(f"  ℹ️  Nenhuma ata circunstanciada encontrada")
    
    # Resumo final
    logger.info(f"\n{'='*70}")
    logger.info(f"RESUMO FINAL")
    logger.info(f"{'='*70}")
    logger.info(f"✅ Total de atas circunstanciadas extraídas: {total_atas_ac}")
    logger.info(f"📁 Salvas em: {DIR_ATAS_AC}")
    logger.info(f"{'='*70}\n")

if __name__ == "__main__":
    main()

