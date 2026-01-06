#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print("\nAtas com 094:")
for ata in atas:
    if '094' in str(ata['sessao_num']):
        print(f"  {ata['sessao_num']} | {ata['data_real']} | {ata['dcl_original']}")

print("\nAtas com 024:")
for ata in atas:
    if '024' in str(ata['sessao_num']):
        print(f"  {ata['sessao_num']} | {ata['data_real']} | {ata['dcl_original']}")

print("\nAtas com 23/10/2007:")
for ata in atas:
    if ata['data_real'] == '23/10/2007':
        print(f"  {ata['sessao_num']} | {ata['dcl_original']}")

print("\nAtas com 24/10/2007:")
for ata in atas:
    if ata['data_real'] == '24/10/2007':
        print(f"  {ata['sessao_num']} | {ata['dcl_original']}")

print("\nAtas com 6/11/2007:")
for ata in atas:
    if ata['data_real'] == '6/11/2007':
        print(f"  {ata['sessao_num']} | {ata['dcl_original']}")

