#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INVESTIGAR DCLs PROBLEMÁTICOS
=============================

Objetivo: Investigar DCLs específicos para encontrar atas faltantes

Uso:
    python investigar_dcls_problematicos.py

Autor: Sistema de Automação CLDF
Data: 2025-12-24
"""

import pdfplumber
from pathlib import Path
import re

USUARIO = "omega"
PASTA_DCLS = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/downloads_2007")

# DCLs problemáticos
DCLS_INVESTIGAR = [
    "DCL_2007-01-231.pdf",      # Falta 22ª na página 33
    "DCL_2007-12-1766369304.pdf" # Falta 97ª na página 1
]

def extrair_atas_dcl(caminho_pdf):
    """Extrai todas as atas de um DCL"""
    atas = []

    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            print(f"\n📄 Processando: {caminho_pdf.name}")
            print(f"   Total de páginas: {len(pdf.pages)}")

            for num_pag, page in enumerate(pdf.pages, 1):
                text = page.extract_text()

                # Procurar por "ATA CIRCUNSTANCIADA"
                if "ATACIRCUNSTANCIADA" in text.replace(" ", ""):
                    # Extrair contexto maior
                    linhas = text.split('\n')
                    for i, linha in enumerate(linhas):
                        if "ATACIRCUNSTANCIADA" in linha.replace(" ", ""):
                            contexto = '\n'.join(linhas[max(0, i-3):min(len(linhas), i+8)])

                            # Procurar número da sessão (pode estar em várias posições)
                            # Procurar padrão: número + ª/a/º/°
                            matches = re.findall(r'(\d+)[ªa°º]', contexto)

                            if matches:
                                # Pegar o primeiro número encontrado
                                num_sessao = int(matches[0])

                                # Verificar se é um número válido (1-118)
                                if 1 <= num_sessao <= 118:
                                    atas.append({
                                        'pagina': num_pag,
                                        'sessao': num_sessao,
                                        'contexto': contexto[:300]
                                    })
                                    print(f"   ✅ Página {num_pag}: {num_sessao}ª")
                            break
    except Exception as e:
        print(f"   ❌ Erro: {e}")

    return atas

def main():
    print("\n" + "="*70)
    print("INVESTIGAR DCLs PROBLEMÁTICOS")
    print("="*70)
    
    for dcl_nome in DCLS_INVESTIGAR:
        caminho = PASTA_DCLS / dcl_nome
        
        if not caminho.exists():
            print(f"\n❌ Arquivo não encontrado: {caminho}")
            continue
        
        atas = extrair_atas_dcl(caminho)
        
        if atas:
            print(f"\n   Atas encontradas: {len(atas)}")
            for ata in atas:
                print(f"   - {ata['sessao']}ª (página {ata['pagina']})")

if __name__ == "__main__":
    main()

