#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print("\nAtas com 23 no DCL_2007-01-231.pdf:")
for ata in atas:
    if 'DCL_2007-01-231' in ata['dcl_original']:
        print(f"Sessão: {ata['sessao_num']} | Data: {ata['data_real']} | Pág: {ata['pag_inicio']}-{ata['pag_fim']}")
        if '23' in str(ata['sessao_num']):
            print(f"  ✅ ENCONTRADA! Nomenclatura: {ata['nomenclatura']}")

