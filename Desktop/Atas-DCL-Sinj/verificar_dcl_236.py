#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print("\n" + "="*70)
print("ATAS NO DCL_2007-01-236.pdf")
print("="*70 + "\n")

atas_dcl = [a for a in atas if a['dcl_original'] == 'DCL_2007-01-236.pdf' and a['tipo_sessao'] == 'ORDINÁRIA']
atas_dcl = sorted(atas_dcl, key=lambda x: x['pag_inicio'])

for ata in atas_dcl:
    print(f"{ata['sessao_num']} - {ata['data_real']} - pag {ata['pag_inicio']}-{ata['pag_fim']}")

print(f"\n{'='*70}\n")

