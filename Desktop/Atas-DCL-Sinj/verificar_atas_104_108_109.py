#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print("\n" + "="*70)
print("VERIFICAR ATAS 104, 108-109 E EXTRAORDINÁRIAS 16-17")
print("="*70 + "\n")

# Atas ordinárias
atas_ord = [a for a in atas if a['sessao_num'] in ['104', '108', '109'] and a['tipo_sessao'] == 'ORDINÁRIA']
print("ORDINÁRIAS:")
for ata in sorted(atas_ord, key=lambda x: int(x['sessao_num'])):
    print(f"{ata['sessao_num']} - {ata['data_real']} - pag {ata['pag_inicio']}-{ata['pag_fim']} - {ata['dcl_original']}")

# Atas extraordinárias
atas_ext = [a for a in atas if a['sessao_num'] in ['016', '017'] and a['tipo_sessao'] == 'EXTRAORDINÁRIA']
print("\nEXTRAORDINÁRIAS:")
for ata in sorted(atas_ext, key=lambda x: int(x['sessao_num'])):
    print(f"{ata['sessao_num']} - {ata['data_real']} - pag {ata['pag_inicio']}-{ata['pag_fim']} - {ata['dcl_original']}")

print(f"\n{'='*70}\n")

