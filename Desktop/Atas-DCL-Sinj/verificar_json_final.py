#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"\nTotal de atas: {len(atas)}")

# Verificar atas com problemas de nomenclatura
print("\nAtas com nomenclatura corrigida:")
for ata in atas:
    if ata['sessao_num'] in ['003', '008', '018', '022', '027', '048', '058', '068', '088', '093']:
        print(f"  {ata['sessao_num']}ª | {ata['data_real']} | {ata['nomenclatura']}")

# Verificar duplicatas
print("\nVerificando duplicatas por nomenclatura:")
nomenclaturas = {}
for ata in atas:
    nom = ata['nomenclatura']
    if nom in nomenclaturas:
        print(f"  DUPLICATA: {nom}")
    else:
        nomenclaturas[nom] = ata['sessao_num']

