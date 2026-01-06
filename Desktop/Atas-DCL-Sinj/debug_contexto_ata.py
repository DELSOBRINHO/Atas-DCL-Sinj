#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEBUG - Mostrar contexto das atas encontradas
==============================================

Objetivo: Ver o contexto exato onde as atas são encontradas

Uso:
    python debug_contexto_ata.py

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
    print("DEBUG - Mostrar contexto das atas encontradas")
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
            # Analisar página 15 (onde encontrou a primeira ata)
            pagina = pdf.pages[14]  # Índice 14 = página 15
            texto_raw = (pagina.extract_text() or "").upper()
            texto = " ".join(texto_raw.split())
            
            print(f"\n📄 PÁGINA 15 - CONTEÚDO COMPLETO:")
            print("="*70)
            print(texto)
            
            print(f"\n\n🔍 PROCURANDO POR ATACIRCUNSTANCIADA:")
            print("="*70)
            
            # Encontrar todas as ocorrências de ATACIRCUNSTANCIADA
            for match in re.finditer(r'ATACIRCUNSTANCIADA', texto):
                idx = match.start()
                # Mostrar contexto de 300 caracteres antes e depois
                inicio = max(0, idx - 300)
                fim = min(len(texto), idx + 300)
                contexto = texto[inicio:fim]
                
                print(f"\n✅ Encontrado em posição {idx}:")
                print(f"   Contexto: ...{contexto}...")
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

