#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print("\nAtas com problemas de nomenclatura:")
problematicas = ['003', '008', '018', '022', '027', '048', '058', '068', '088', '093']

for ata in atas:
    if ata['sessao_num'] in problematicas:
        print(f"{ata['sessao_num']} | {ata['data_real']} | {ata['nomenclatura']}")

