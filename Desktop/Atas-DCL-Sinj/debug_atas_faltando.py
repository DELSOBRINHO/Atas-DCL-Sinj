#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEBUG - Verificar por que atas estão faltando
==============================================

Objetivo: Entender por que atas 36, 108, 110 não foram extraídas

Uso:
    python debug_atas_faltando.py

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
    print("DEBUG - Verificar por que atas estão faltando")
    print("="*70)
    
    # Instalar dependências
    instalar_dependencias()
    
    arquivo = "DCL_2007-01-009.pdf"
    caminho = DIR_DOWNLOADS / arquivo
    
    if not caminho.exists():
        print(f"❌ Arquivo não encontrado: {caminho}")
        return
    
    try:
        import pdfplumber
        
        with pdfplumber.open(caminho) as pdf:
            # Analisar página 13 (ata 36)
            print(f"\n📄 PÁGINA 13 (ATA 36):")
            print("="*70)
            
            pagina = pdf.pages[12]  # Índice 12 = página 13
            texto_raw = (pagina.extract_text() or "").upper()
            texto = " ".join(texto_raw.split())
            
            # Procurar por ATACIRCUNSTANCIADA
            for match in re.finditer(r'ATACIRCUNSTANCIADA', texto):
                idx = match.start()
                contexto_depois = texto[idx:min(len(texto), idx+300)]
                
                print(f"\nContexto: ...{contexto_depois[:200]}...")
                
                # Procurar número
                match_num = re.search(r'ATACIRCUNSTANCIADA\s*DA\s*(\d+)[ªa°º]?', contexto_depois)
                if match_num:
                    print(f"✅ Número: {match_num.group(1)}")
                
                # Procurar tipo de sessão
                match_tipo = re.search(r'SESS[ÃA]O\s*(ORDIN[ÁA]RIA|EXTRAORDIN[ÁA]RIA|SOLENE|PREPARAT[ÓO]RIA|ESPECIAL)', contexto_depois)
                if match_tipo:
                    print(f"✅ Tipo: {match_tipo.group(1)}")
                else:
                    print(f"❌ Tipo NÃO encontrado")
                
                # Procurar data
                match_data = re.search(r'(?:EM|REALIZADA)\s*(\d{1,2})\s*DE\s*(\w+)\s*DE\s*(200\d)', contexto_depois)
                if match_data:
                    print(f"✅ Data: {match_data.group(1)}/{match_data.group(2)}/{match_data.group(3)}")
                else:
                    print(f"❌ Data NÃO encontrada")
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

