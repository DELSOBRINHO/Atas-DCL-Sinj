#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENCONTRAR DCLs COM ATAS CIRCUNSTANCIADAS
=========================================

Procura por DCLs que contêm atas circunstanciadas

Uso:
    python encontrar_dcls_com_atas_circunstanciadas.py

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
    
    pacotes = {
        "pdfplumber": "pdfplumber"
    }
    
    for modulo, pacote in pacotes.items():
        try:
            __import__(modulo)
            print(f"   ✅ {pacote} já instalado")
        except ImportError:
            print(f"   ⬇️  Instalando {pacote}...")
            subprocess.check_call([__import__('sys').executable, "-m", "pip", "install", pacote, "-q"])
            print(f"   ✅ {pacote} instalado")

def tem_ata_circunstanciada(caminho_pdf):
    """Verifica se um PDF tem ata circunstanciada"""
    try:
        import pdfplumber
        
        with pdfplumber.open(caminho_pdf) as pdf:
            for pagina in pdf.pages[:10]:  # Verifica primeiras 10 páginas
                texto = (pagina.extract_text() or "").upper()
                
                # Procura por "ATACIR" (radical de "ATA CIRCUNSTANCIADA")
                if re.search(r'ATACIR', texto):
                    return True
        
        return False
    
    except Exception as e:
        return False

def main():
    """Função principal"""
    print("\n" + "="*70)
    print("ENCONTRAR DCLs COM ATAS CIRCUNSTANCIADAS")
    print("="*70)
    
    # Instalar dependências
    instalar_dependencias()
    
    # Listar todos os PDFs
    print("\n📁 LISTANDO ARQUIVOS PDF")
    todos_pdfs = sorted(DIR_DOWNLOADS.glob('*.pdf'))
    
    print(f"✅ {len(todos_pdfs)} PDFs encontrados")
    
    if not todos_pdfs:
        print("❌ Nenhum PDF encontrado")
        return
    
    # Procurar por DCLs com atas circunstanciadas
    print(f"\n🔍 PROCURANDO POR ATAS CIRCUNSTANCIADAS")
    print("="*70 + "\n")
    
    dcls_com_atas = []
    
    for i, arquivo in enumerate(todos_pdfs, 1):
        if i % 50 == 0:
            print(f"[{i:3d}/{len(todos_pdfs)}] Verificados...")
        
        if tem_ata_circunstanciada(arquivo):
            dcls_com_atas.append(arquivo.name)
    
    print(f"[{len(todos_pdfs):3d}/{len(todos_pdfs)}] Verificados")
    
    # Resultados
    print(f"\n📊 RESULTADOS")
    print("="*70)
    
    print(f"\nTotal de DCLs com atas circunstanciadas: {len(dcls_com_atas)}")
    
    print(f"\n📋 PRIMEIROS 10 DCLs COM ATAS CIRCUNSTANCIADAS:")
    for i, dcl in enumerate(dcls_com_atas[:10], 1):
        print(f"   {i}. {dcl}")
    
    if len(dcls_com_atas) > 10:
        print(f"\n   ... e mais {len(dcls_com_atas) - 10} DCLs")
    
    # Salvar lista
    arquivo_saida = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/dcls_com_atas_circunstanciadas.txt")
    
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write("DCLs COM ATAS CIRCUNSTANCIADAS\n")
        f.write("="*70 + "\n\n")
        f.write(f"Total: {len(dcls_com_atas)}\n\n")
        
        for dcl in dcls_com_atas:
            f.write(f"{dcl}\n")
    
    print(f"\n✅ Lista salva em: {arquivo_saida}")

if __name__ == "__main__":
    main()

