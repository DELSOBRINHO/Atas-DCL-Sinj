#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEBUG - Verificar TODAS as atas no DCL_2007-01-009.pdf
========================================================

Objetivo: Contar quantas vezes "ATACIRCUNSTANCIADA" aparece

Uso:
    python debug_todas_atas_dcl_009.py

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
    print("DEBUG - Verificar TODAS as atas no DCL_2007-01-009.pdf")
    print("="*70)
    
    # Instalar dependências
    instalar_dependencias()
    
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
            
            # Contar todas as ocorrências de ATACIRCUNSTANCIADA
            contador = 0
            
            for num_p, pagina in enumerate(pdf.pages, 1):
                texto_raw = (pagina.extract_text() or "").upper()
                texto = " ".join(texto_raw.split())
                
                # Contar ocorrências
                matches = list(re.finditer(r'ATACIRCUNSTANCIADA', texto))
                
                if matches:
                    print(f"\n📄 Página {num_p}: {len(matches)} ata(s) encontrada(s)")
                    
                    for match in matches:
                        contador += 1
                        idx = match.start()
                        
                        # Extrair número
                        contexto_depois = texto[idx:min(len(texto), idx+300)]
                        match_num = re.search(r'ATACIRCUNSTANCIADA\s*DA\s*(\d+)[ªa°º]?', contexto_depois)
                        
                        if match_num:
                            num_sessao = match_num.group(1)
                            print(f"   ✅ Ata #{contador}: Sessão {num_sessao}")
                        else:
                            print(f"   ❌ Ata #{contador}: Número não encontrado")
            
            print(f"\n📊 TOTAL DE ATAS ENCONTRADAS: {contador}")
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

