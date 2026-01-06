#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEBUG v2 - Verificar conteúdo de um PDF com mais detalhes
===========================================================

Mostra o conteúdo das primeiras páginas de um PDF para análise

Uso:
    python debug_pdf_content_v2.py

Autor: Sistema de Automação CLDF
Data: 2025-12-22
"""

import re
from pathlib import Path

# ======================================================================
# CONFIGURAÇÕES
# ======================================================================

USUARIO = "omega"
DIR_DOWNLOADS = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/downloads_2007")

# ======================================================================
# FUNÇÕES PRINCIPAIS
# ======================================================================

def instalar_dependencias():
    """Instala dependências necessárias"""
    print("📦 Verificando dependências...")
    
    import subprocess
    
    try:
        __import__("pdfplumber")
        print(f"   ✅ pdfplumber já instalado")
    except ImportError:
        print(f"   ⬇️  Instalando pdfplumber...")
        subprocess.check_call([__import__('sys').executable, "-m", "pip", "install", "pdfplumber", "-q"])
        print(f"   ✅ pdfplumber instalado")

def main():
    """Função principal"""
    print("\n" + "="*70)
    print("DEBUG v2 - VERIFICAR CONTEÚDO DE UM PDF COM MAIS DETALHES")
    print("="*70)
    
    # Instalar dependências
    instalar_dependencias()
    
    # Usar o primeiro DCL com atas circunstanciadas
    arquivo = "DCL_2007-01-009.pdf"
    caminho = DIR_DOWNLOADS / arquivo
    
    print(f"\n📄 Analisando: {arquivo}")
    print("="*70)
    
    if not caminho.exists():
        print(f"❌ Arquivo não encontrado: {caminho}")
        return
    
    try:
        import pdfplumber
        
        with pdfplumber.open(caminho) as pdf:
            total_paginas = len(pdf.pages)
            print(f"\n📊 Total de páginas: {total_paginas}")
            
            # Mostrar primeiras 3 páginas com mais detalhes
            for num_p in range(min(3, total_paginas)):
                pagina = pdf.pages[num_p]
                texto = pagina.extract_text() or ""
                texto_upper = texto.upper()
                
                print(f"\n{'='*70}")
                print(f"PÁGINA {num_p + 1}")
                print(f"{'='*70}")
                
                # Procurar por padrões específicos
                print("\n🔍 PROCURANDO POR PADRÕES:")
                
                # Procurar por "ATACIRCUNSTANCIADA"
                if "ATACIRCUNSTANCIADA" in texto_upper:
                    print("✅ ENCONTRADO: ATACIRCUNSTANCIADA")
                    # Mostrar contexto
                    idx = texto_upper.find("ATACIRCUNSTANCIADA")
                    contexto = texto[max(0, idx-100):min(len(texto), idx+300)]
                    print(f"   Contexto: ...{contexto}...")
                
                # Procurar por "ATA CIRCUNSTANCIADA"
                if "ATA CIRCUNSTANCIADA" in texto_upper:
                    print("✅ ENCONTRADO: ATA CIRCUNSTANCIADA")
                    idx = texto_upper.find("ATA CIRCUNSTANCIADA")
                    contexto = texto[max(0, idx-100):min(len(texto), idx+300)]
                    print(f"   Contexto: ...{contexto}...")
                
                # Procurar por "CIRCUNSTANCIADA"
                if "CIRCUNSTANCIADA" in texto_upper:
                    print("✅ ENCONTRADO: CIRCUNSTANCIADA")
                    idx = texto_upper.find("CIRCUNSTANCIADA")
                    contexto = texto[max(0, idx-100):min(len(texto), idx+300)]
                    print(f"   Contexto: ...{contexto}...")
                
                # Procurar por "SESSÃO"
                if "SESSÃO" in texto_upper or "SESSAO" in texto_upper:
                    print("✅ ENCONTRADO: SESSÃO")
                    # Encontrar todas as ocorrências
                    matches = re.finditer(r'(\d+)\s*[ªa°º]?\s*SESS[ÃA]O\s+(\w+)', texto_upper)
                    for match in matches:
                        print(f"   - {match.group(0)}")
                
                # Procurar por datas
                datas = re.findall(r'(\d{1,2})\s+DE\s+(\w+)\s+DE\s+(\d{4})', texto_upper)
                if datas:
                    print(f"✅ ENCONTRADO: Datas")
                    for data in datas:
                        print(f"   - {data[0]} DE {data[1]} DE {data[2]}")
                
                # Mostrar primeiros 500 caracteres
                print(f"\n📝 PRIMEIROS 500 CARACTERES:")
                print(texto[:500])
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

