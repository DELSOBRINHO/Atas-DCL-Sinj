#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEBUG - Verificar conteúdo de um PDF
====================================

Mostra o conteúdo das primeiras páginas de um PDF para análise

Uso:
    python debug_pdf_content.py

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
    print("DEBUG - VERIFICAR CONTEÚDO DE UM PDF")
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
            
            # Mostrar primeiras 5 páginas
            for num_p in range(min(5, total_paginas)):
                pagina = pdf.pages[num_p]
                texto = pagina.extract_text() or ""
                
                print(f"\n{'='*70}")
                print(f"PÁGINA {num_p + 1}")
                print(f"{'='*70}")
                print(texto[:1000])  # Primeiros 1000 caracteres
                
                # Procurar por padrões
                texto_upper = texto.upper()
                
                if "ATACIR" in texto_upper:
                    print("\n✅ ENCONTRADO: ATACIR")
                
                if "CIRCUNSTANCIADA" in texto_upper:
                    print("✅ ENCONTRADO: CIRCUNSTANCIADA")
                
                if "SESSÃO" in texto_upper or "SESSAO" in texto_upper:
                    print("✅ ENCONTRADO: SESSÃO")
                
                # Procurar por datas
                datas = re.findall(r'\d{1,2}\s+de\s+\w+\s+de\s+\d{4}', texto, re.IGNORECASE)
                if datas:
                    print(f"✅ ENCONTRADO: Datas = {datas}")
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

