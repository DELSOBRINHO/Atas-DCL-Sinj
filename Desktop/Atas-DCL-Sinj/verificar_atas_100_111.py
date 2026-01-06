#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"\nTotal de atas: {len(atas)}\n")

atas_100_111 = [a for a in atas if int(a['sessao_num']) >= 100 and int(a['sessao_num']) <= 111]
for ata in sorted(atas_100_111, key=lambda x: int(x['sessao_num'])):
    print(f"{ata['sessao_num']} - {ata['tipo_sessao']} - {ata['data_real']}")

