#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEBUG - Verificar ata 024 duplicada
====================================

Objetivo: Entender se a ata 024 é realmente duplicada

Uso:
    python debug_ata_024_duplicada.py

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
    print("DEBUG - Verificar ata 024 duplicada")
    print("="*70)
    
    # Instalar dependências
    instalar_dependencias()
    
    try:
        import pdfplumber
        
        # Verificar ata 024 em DCL_2007-01-231.pdf (página 35)
        print(f"\n📄 DCL_2007-01-231.pdf (página 35):")
        print("="*70)
        
        caminho = DIR_DOWNLOADS / "DCL_2007-01-231.pdf"
        with pdfplumber.open(caminho) as pdf:
            pagina = pdf.pages[34]  # Índice 34 = página 35
            texto_raw = (pagina.extract_text() or "").upper()
            texto = " ".join(texto_raw.split())
            
            # Procurar por ATACIRCUNSTANCIADA
            for match in re.finditer(r'ATACIRCUNSTANCIADA', texto):
                idx = match.start()
                contexto_depois = texto[idx:min(len(texto), idx+500)]
                
                # Procurar número
                match_num = re.search(r'ATACIRCUNSTANCIADA\s*DA\s*(\d+)[ªa°º]?', contexto_depois)
                if match_num and match_num.group(1) == "024":
                    print(f"✅ Encontrada ata 024")
                    print(f"Contexto: ...{contexto_depois[:300]}...")
        
        # Verificar ata 024 em DCL_2007-01-232.pdf (página 13)
        print(f"\n📄 DCL_2007-01-232.pdf (página 13):")
        print("="*70)
        
        caminho = DIR_DOWNLOADS / "DCL_2007-01-232.pdf"
        with pdfplumber.open(caminho) as pdf:
            pagina = pdf.pages[12]  # Índice 12 = página 13
            texto_raw = (pagina.extract_text() or "").upper()
            texto = " ".join(texto_raw.split())
            
            # Procurar por ATACIRCUNSTANCIADA
            for match in re.finditer(r'ATACIRCUNSTANCIADA', texto):
                idx = match.start()
                contexto_depois = texto[idx:min(len(texto), idx+500)]
                
                # Procurar número
                match_num = re.search(r'ATACIRCUNSTANCIADA\s*DA\s*(\d+)[ªa°º]?', contexto_depois)
                if match_num and match_num.group(1) == "024":
                    print(f"✅ Encontrada ata 024")
                    print(f"Contexto: ...{contexto_depois[:300]}...")
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

