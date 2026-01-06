#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print("\n" + "="*70)
print("VERIFICAR ATAS 110 E 011")
print("="*70 + "\n")

# Ata 110
atas_110 = [a for a in atas if a['sessao_num'] == '110']
print("ATA 110:")
for ata in atas_110:
    print(f"  {ata['sessao_num']} - {ata['tipo_sessao']} - {ata['data_real']} - pag {ata['pag_inicio']}-{ata['pag_fim']} - {ata['dcl_original']}")

# Ata 011
atas_011 = [a for a in atas if a['sessao_num'] == '011']
print("\nATA 011:")
for ata in atas_011:
    print(f"  {ata['sessao_num']} - {ata['tipo_sessao']} - {ata['data_real']} - pag {ata['pag_inicio']}-{ata['pag_fim']} - {ata['dcl_original']}")

print(f"\n{'='*70}\n")

