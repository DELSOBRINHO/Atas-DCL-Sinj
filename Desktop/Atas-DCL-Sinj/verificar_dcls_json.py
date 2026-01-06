#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIFICAR DCLs NO JSON
======================
"""

import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print("\n" + "="*70)
print("ATAS DO DCL_2007-01-231.pdf:")
print("="*70)

encontradas_01 = []
for ata in atas:
    if 'DCL_2007-01-231' in ata['dcl_original']:
        encontradas_01.append(int(ata['sessao_num']))
        print(f"  {ata['sessao_num']}ª - {ata['data_real']} - Páginas {ata['pag_inicio']}-{ata['pag_fim']}")

print(f"\nTotal: {len(encontradas_01)}")
print(f"Números: {sorted(encontradas_01)}")

print("\n" + "="*70)
print("ATAS DO DCL_2007-12-1766369304.pdf:")
print("="*70)

encontradas_12 = []
for ata in atas:
    if 'DCL_2007-12-1766369304' in ata['dcl_original']:
        encontradas_12.append(int(ata['sessao_num']))
        print(f"  {ata['sessao_num']}ª - {ata['data_real']} - Páginas {ata['pag_inicio']}-{ata['pag_fim']}")

print(f"\nTotal: {len(encontradas_12)}")
print(f"Números: {sorted(encontradas_12)}")

print("\n" + "="*70)
print("ANÁLISE:")
print("="*70)
print(f"\n22ª encontrada em DCL_2007-01-231.pdf? {22 in encontradas_01}")
print(f"97ª encontrada em DCL_2007-12-1766369304.pdf? {97 in encontradas_12}")

