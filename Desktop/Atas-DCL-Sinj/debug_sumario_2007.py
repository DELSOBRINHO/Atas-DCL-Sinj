# -*- coding: utf-8 -*-
"""
DEBUG DO SUMÁRIO - 2007
=======================

Mostra exatamente o que está no sumário dos PDFs
"""

import pdfplumber
from pathlib import Path

DIR_DOWNLOADS = Path("C:/Users/omega/Desktop/Atas-DCL-Sinj/downloads_2007")

# Verificar o PDF 3 que tem ata circunstanciada
pdf_path = DIR_DOWNLOADS / "DCL_2007-03.pdf"

print(f"Analisando: {pdf_path.name}\n")

with pdfplumber.open(pdf_path) as pdf:
    primeira_pagina = pdf.pages[0]
    texto = primeira_pagina.extract_text()
    
    # Salvar em arquivo para análise
    with open("sumario_debug.txt", "w", encoding="utf-8") as f:
        f.write(texto)
    
    print("TEXTO COMPLETO DO SUMÁRIO:")
    print("=" * 70)
    print(texto)
    print("=" * 70)
    
    # Procurar por linhas com "Ata"
    print("\nLINHAS COM 'ATA':")
    for i, linha in enumerate(texto.split('\n')):
        if 'ata' in linha.lower() or 'circ' in linha.lower():
            print(f"Linha {i}: {linha}")

