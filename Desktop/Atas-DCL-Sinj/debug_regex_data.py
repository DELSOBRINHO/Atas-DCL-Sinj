#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEBUG - Testar regex de data
============================

Objetivo: Entender por que o regex não está funcionando

Uso:
    python debug_regex_data.py

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

# Mapeamento de meses
MESES_MAP = {
    'JANEIRO': '01', 'FEVEREIRO': '02', 'MARÇO': '03', 'MARCO': '03', 'ABRIL': '04',
    'MAIO': '05', 'JUNHO': '06', 'JULHO': '07', 'AGOSTO': '08', 'SETEMBRO': '09',
    'OUTUBRO': '10', 'NOVEMBRO': '11', 'DEZEMBRO': '12'
}

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
    print("DEBUG - Testar regex de data")
    print("="*70)
    
    # Instalar dependências
    instalar_dependencias()
    
    try:
        import pdfplumber
        
        caminho = DIR_DOWNLOADS / "DCL_2008-02-1766369371.pdf"
        
        with pdfplumber.open(caminho) as pdf:
            # Página 17 (ata 113)
            pagina = pdf.pages[16]
            texto_raw = (pagina.extract_text() or "").upper()
            texto = " ".join(texto_raw.split())
            
            print(f"\n📄 Página 17 (Ata 113):")
            print("="*70)
            
            # Procurar por "EM"
            idx_em = texto.find("EM")
            if idx_em >= 0:
                contexto = texto[idx_em:idx_em+100]
                print(f"Contexto após 'EM': ...{contexto}...")
            
            # Testar diferentes padrões de regex
            padroes = [
                r'EM\s*(\d{1,2})\s*DE\s*(\w+)\s*DE\s*(200\d)',
                r'EM\s*(\d{1,2})\s*(\w+)\s*(200\d)',
                r'EM\s*(\d{1,2})\s*DEZEMBRO\s*(200\d)',
                r'(\d{1,2})\s*DEZEMBRO\s*(200\d)',
            ]
            
            for padrao in padroes:
                match = re.search(padrao, texto)
                if match:
                    print(f"\n✅ Padrão encontrado: {padrao}")
                    print(f"   Grupos: {match.groups()}")
                else:
                    print(f"\n❌ Padrão não encontrado: {padrao}")
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

