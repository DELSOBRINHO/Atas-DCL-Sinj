#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

# Atas faltantes
faltantes_ordinarias = [37, 39, 41, 50, 57, 60, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 97, 99, 112, 113, 114, 115, 116, 117]
faltantes_extraordinarias = [37]

print("\n" + "="*70)
print("RELATÓRIO ATUALIZADO DE ATAS FALTANTES")
print("="*70)
print(f"\nTotal de atas no JSON: {len(atas)}")
print(f"Atas ordinárias faltando: {len(faltantes_ordinarias)}")
print(f"Atas extraordinárias faltando: {len(faltantes_extraordinarias)}")
print(f"Total faltando: {len(faltantes_ordinarias) + len(faltantes_extraordinarias)}")

print(f"\n{'='*70}")
print("ATAS ORDINÁRIAS FALTANDO:")
print(f"{'='*70}")
for num in faltantes_ordinarias:
    print(f"  {num:3d}ª")

print(f"\n{'='*70}")
print("ATAS EXTRAORDINÁRIAS FALTANDO:")
print(f"{'='*70}")
for num in faltantes_extraordinarias:
    print(f"  {num:2d}ª")

print(f"\n{'='*70}\n")

