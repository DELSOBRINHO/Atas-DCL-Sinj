#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

# Verificar tipos das atas problemáticas
problematicas = ['003', '008', '018', '022', '023', '025', '058', '068', '093']

for sessao in problematicas:
    for ata in atas:
        if ata['sessao_num'] == sessao:
            print(f"{sessao}: {ata['tipo_sessao']} | {ata['data_real']} | {ata['nomenclatura']}")
            break

