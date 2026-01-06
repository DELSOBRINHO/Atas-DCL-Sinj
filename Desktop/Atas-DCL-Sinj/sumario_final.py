#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

# Atas faltantes originais
faltantes_ordinarias = [37, 39, 41, 50, 57, 60, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 97, 99, 112, 113, 114, 115, 116, 117]
faltantes_extraordinarias = [37]

# Atas existentes
atas_existentes = set(int(a['sessao_num']) for a in atas)

# Atas ainda faltando
ordinarias_ainda_faltando = [n for n in faltantes_ordinarias if n not in atas_existentes]
extraordinarias_ainda_faltando = [n for n in faltantes_extraordinarias if n not in atas_existentes]

print("\n" + "="*70)
print("SUMÁRIO FINAL - FASE 2")
print("="*70)

print(f"\nTotal de atas no JSON: {len(atas)}")
print(f"Atas ordinárias ainda faltando: {len(ordinarias_ainda_faltando)}")
print(f"Atas extraordinárias ainda faltando: {len(extraordinarias_ainda_faltando)}")
print(f"Total ainda faltando: {len(ordinarias_ainda_faltando) + len(extraordinarias_ainda_faltando)}")

print(f"\n{'='*70}")
print("ATAS ORDINÁRIAS AINDA FALTANDO:")
print(f"{'='*70}")
for num in ordinarias_ainda_faltando:
    print(f"  {num:3d}ª")

print(f"\n{'='*70}")
print("ATAS EXTRAORDINÁRIAS AINDA FALTANDO:")
print(f"{'='*70}")
for num in extraordinarias_ainda_faltando:
    print(f"  {num:2d}ª")

print(f"\n{'='*70}\n")

