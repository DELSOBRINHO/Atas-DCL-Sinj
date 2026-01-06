# -*- coding: utf-8 -*-
"""
Lista as atas circunstanciadas extraídas de 2007
"""

from pathlib import Path

DIR_ATAS = Path("atas_circunstanciadas_2007")

print("\n" + "="*80)
print("ATAS CIRCUNSTANCIADAS EXTRAÍDAS DE 2007")
print("="*80 + "\n")

arquivos = sorted(DIR_ATAS.glob("*.pdf"))

total_tamanho = 0
for i, arquivo in enumerate(arquivos, 1):
    tamanho_mb = arquivo.stat().st_size / (1024 * 1024)
    total_tamanho += tamanho_mb
    print(f"{i:2d}. {arquivo.name:50s} {tamanho_mb:8.2f} MB")

print("\n" + "-"*80)
print(f"Total: {len(arquivos)} atas circunstanciadas")
print(f"Tamanho total: {total_tamanho:.2f} MB")
print("="*80 + "\n")

