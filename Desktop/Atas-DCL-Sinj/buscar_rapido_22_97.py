#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BUSCAR RÁPIDO 22ª E 97ª
=======================
"""

import pdfplumber
from pathlib import Path
import re

USUARIO = "omega"
PASTA = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/downloads_2007")

def buscar(dcl_nome, num):
    caminho = PASTA / dcl_nome
    print(f"\n🔍 Buscando {num}ª em {dcl_nome}...")
    
    try:
        with pdfplumber.open(caminho) as pdf:
            for pag_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                
                # Procurar "22ª" ou "97ª"
                if f"{num}ª" in text or f"{num}a" in text or f"{num}°" in text:
                    print(f"✅ Encontrado na página {pag_num}")
                    
                    # Mostrar contexto
                    idx = text.find(f"{num}ª")
                    if idx == -1:
                        idx = text.find(f"{num}a")
                    if idx == -1:
                        idx = text.find(f"{num}°")
                    
                    if idx >= 0:
                        inicio = max(0, idx - 100)
                        fim = min(len(text), idx + 200)
                        print(f"Contexto: ...{text[inicio:fim]}...")
                    return True
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print(f"❌ Não encontrado")
    return False

print("="*70)
print("BUSCAR 22ª E 97ª")
print("="*70)

buscar("DCL_2007-01-231.pdf", 22)
buscar("DCL_2007-12-1766369304.pdf", 97)

