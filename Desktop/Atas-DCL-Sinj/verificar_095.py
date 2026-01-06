#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print("\nAtas com 095:")
for ata in atas:
    if '095' in str(ata['sessao_num']):
        print(f"  {ata['sessao_num']} | {ata['data_real']} | {ata['dcl_original']}")

print(f"\nTotal de atas: {len(atas)}")

