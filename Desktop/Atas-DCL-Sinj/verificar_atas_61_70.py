#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print("\n" + "="*70)
print("VERIFICAR ATAS 61-70")
print("="*70 + "\n")

atas_61_70 = [a for a in atas if int(a['sessao_num']) >= 61 and int(a['sessao_num']) <= 70 and a['tipo_sessao'] == 'ORDINÁRIA']

for ata in sorted(atas_61_70, key=lambda x: int(x['sessao_num'])):
    print(f"{ata['sessao_num']} - {ata['data_real']} - pag {ata['pag_inicio']}-{ata['pag_fim']} - {ata['dcl_original']}")

print(f"\n{'='*70}\n")

