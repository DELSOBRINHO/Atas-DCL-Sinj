#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEBUG - Verificar página 35 do DCL_2007-01-231.pdf
====================================================

Objetivo: Ver o conteúdo da página 35

Uso:
    python debug_pagina_35_231.py

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
    import subprocess
    
    try:
        __import__("pdfplumber")
    except ImportError:
        subprocess.check_call([__import__('sys').executable, "-m", "pip", "install", "pdfplumber", "-q"])

def main():
    """Função principal"""
    print("\n" + "="*70)
    print("DEBUG - Verificar página 35 do DCL_2007-01-231.pdf")
    print("="*70)
    
    # Instalar dependências
    instalar_dependencias()
    
    try:
        import pdfplumber
        
        caminho = DIR_DOWNLOADS / "DCL_2007-01-231.pdf"
        
        with pdfplumber.open(caminho) as pdf:
            print(f"\nTotal de páginas: {len(pdf.pages)}")
            
            # Verificar página 35
            if len(pdf.pages) >= 35:
                pagina = pdf.pages[34]  # Índice 34 = página 35
                texto_raw = (pagina.extract_text() or "").upper()
                texto = " ".join(texto_raw.split())
                
                print(f"\n📄 Página 35 (primeiros 500 caracteres):")
                print("="*70)
                print(texto[:500])
                
                # Procurar por ATACIRCUNSTANCIADA
                if "ATACIRCUNSTANCIADA" in texto:
                    print(f"\n✅ Encontrada ATACIRCUNSTANCIADA na página 35")
                else:
                    print(f"\n❌ ATACIRCUNSTANCIADA NÃO encontrada na página 35")
            else:
                print(f"\n❌ Arquivo tem apenas {len(pdf.pages)} páginas")
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

