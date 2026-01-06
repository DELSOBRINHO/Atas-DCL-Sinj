# -*- coding: utf-8 -*-
"""
VERIFICADOR DE CONTEÚDO DOS DCLs 2007
=====================================

Verifica o conteúdo dos PDFs para entender a estrutura
"""

import pdfplumber
from pathlib import Path

DIR_DOWNLOADS = Path("C:/Users/omega/Desktop/Atas-DCL-Sinj/downloads_2007")

# Verificar alguns PDFs
pdfs = sorted(DIR_DOWNLOADS.glob("*.pdf"))[:3]

for pdf_path in pdfs:
    print(f"\n{'='*70}")
    print(f"Arquivo: {pdf_path.name}")
    print(f"{'='*70}\n")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Total de páginas: {len(pdf.pages)}\n")
            
            # Extrair texto da primeira página
            primeira_pagina = pdf.pages[0]
            texto = primeira_pagina.extract_text()
            
            print("PRIMEIRAS 1000 CARACTERES DA PRIMEIRA PÁGINA:")
            print("-" * 70)
            print(texto[:1000])
            print("-" * 70)
            
            # Procurar por palavras-chave
            print("\nPALAVRAS-CHAVE ENCONTRADAS:")
            if "Ata" in texto:
                print("✓ 'Ata' encontrada")
            if "Circunstanciada" in texto or "Circ." in texto:
                print("✓ 'Circunstanciada' encontrada")
            if "Sucinta" in texto:
                print("✓ 'Sucinta' encontrada")
            if "Ordinária" in texto:
                print("✓ 'Ordinária' encontrada")
            if "Extraordinária" in texto:
                print("✓ 'Extraordinária' encontrada")
                
    except Exception as e:
        print(f"❌ Erro ao processar: {e}")

