#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

print("\n" + "="*70)
print("PROCURAR TODAS AS ATAS FALTANTES")
print("="*70)

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

# Atas faltantes
faltantes_ordinarias = [5, 8, 9, 22, 37, 39, 41, 50, 57, 60, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 97, 99, 112, 113, 114, 115, 116, 117]
faltantes_extraordinarias = [1, 4, 11, 12, 15, 19, 20, 26, 31, 32, 33, 34, 35, 36, 37, 38]

# Verificar quais já estão no JSON
atas_existentes = set(int(a['sessao_num']) for a in atas)

print(f"\nTotal de atas no JSON: {len(atas)}")
print(f"Total de atas faltantes: {len(faltantes_ordinarias) + len(faltantes_extraordinarias)}")

# Verificar quais faltantes já foram adicionadas
ordinarias_ainda_faltando = [n for n in faltantes_ordinarias if n not in atas_existentes]
extraordinarias_ainda_faltando = [n for n in faltantes_extraordinarias if n not in atas_existentes]

print(f"\nAtas ordinárias ainda faltando: {len(ordinarias_ainda_faltando)}")
print(f"Atas extraordinárias ainda faltando: {len(extraordinarias_ainda_faltando)}")

if ordinarias_ainda_faltando:
    print(f"\nOrdinárias faltando: {ordinarias_ainda_faltando}")
if extraordinarias_ainda_faltando:
    print(f"Extraordinárias faltando: {extraordinarias_ainda_faltando}")

print(f"\n{'='*70}\n")

