#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEBUG - Analisar DCL_2008-02-1766369371.pdf
============================================

Objetivo: Entender as datas problemáticas neste arquivo

Uso:
    python debug_dcl_2008_02.py

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
    print("DEBUG - Analisar DCL_2008-02-1766369371.pdf")
    print("="*70)
    
    # Instalar dependências
    instalar_dependencias()
    
    try:
        import pdfplumber
        
        caminho = DIR_DOWNLOADS / "DCL_2008-02-1766369371.pdf"
        
        if not caminho.exists():
            print(f"❌ Arquivo não encontrado: {caminho}")
            return
        
        with pdfplumber.open(caminho) as pdf:
            print(f"\nTotal de páginas: {len(pdf.pages)}\n")
            
            # Procurar por ATACIRCUNSTANCIADA em todas as páginas
            for num_p, pagina in enumerate(pdf.pages, 1):
                texto_raw = (pagina.extract_text() or "").upper()
                texto = " ".join(texto_raw.split())
                
                if "ATACIRCUNSTANCIADA" in texto:
                    print(f"📄 Página {num_p}:")
                    print("="*70)
                    
                    # Procurar por ATACIRCUNSTANCIADA
                    for match in re.finditer(r'ATACIRCUNSTANCIADA', texto):
                        idx = match.start()
                        contexto_depois = texto[idx:min(len(texto), idx+500)]
                        
                        # Procurar número
                        match_num = re.search(r'ATACIRCUNSTANCIADA\s*DA\s*(\d+)[ªa°º]?', contexto_depois)
                        if match_num:
                            print(f"\n✅ Ata {match_num.group(1)}")
                            print(f"Contexto: ...{contexto_depois[:300]}...")
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

