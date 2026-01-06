#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEBUG - Encontrar padrão exato das atas
========================================

Objetivo: Entender o padrão exato de onde estão os dados

Uso:
    python debug_padrao_exato.py

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
    print("DEBUG - Encontrar padrão exato das atas")
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
            # Analisar página 15
            pagina = pdf.pages[14]  # Índice 14 = página 15
            texto_raw = (pagina.extract_text() or "").upper()
            texto = " ".join(texto_raw.split())
            
            print(f"\n🔍 PROCURANDO POR ATACIRCUNSTANCIADA:")
            print("="*70)
            
            # Encontrar todas as ocorrências
            for match in re.finditer(r'ATACIRCUNSTANCIADA', texto):
                idx = match.start()
                
                # Mostrar 200 caracteres antes e 300 depois
                inicio = max(0, idx - 200)
                fim = min(len(texto), idx + 300)
                contexto = texto[inicio:fim]
                
                print(f"\n✅ Encontrado em posição {idx}:")
                print(f"   Contexto: ...{contexto}...")
                
                # Procurar por padrões específicos
                contexto_depois = texto[idx:min(len(texto), idx+300)]
                
                # Procurar número DEPOIS de ATACIRCUNSTANCIADA
                # Padrão: "ATACIRCUNSTANCIADADA108A" (sem espaço)
                match_num = re.search(r'ATACIRCUNSTANCIADA\s*DA\s*(\d+)[ªa°º]?', contexto_depois)
                if match_num:
                    print(f"   ✅ Número encontrado: {match_num.group(1)}")
                else:
                    print(f"   ❌ Número NÃO encontrado")
                
                # Procurar tipo de sessão
                match_tipo = re.search(r'SESS[ÃA]O\s*(ORDIN[ÁA]RIA|EXTRAORDIN[ÁA]RIA)', contexto_depois)
                if match_tipo:
                    print(f"   ✅ Tipo de sessão encontrado: {match_tipo.group(1)}")
                
                # Procurar data
                match_data = re.search(r'EM\s*(\d{1,2})\s*DE\s*(\w+)\s*DE\s*(200\d)', contexto_depois)
                if match_data:
                    print(f"   ✅ Data encontrada: {match_data.group(1)}/{match_data.group(2)}/{match_data.group(3)}")
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

