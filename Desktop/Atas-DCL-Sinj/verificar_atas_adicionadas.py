#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print("\n" + "="*70)
print("VERIFICAÇÃO DE ATAS ADICIONADAS")
print("="*70)

print(f"\nTotal de atas no JSON: {len(atas)}")

# Verificar as 3 atas adicionadas
atas_107 = [a for a in atas if a['sessao_num'] == '107']
atas_110 = [a for a in atas if a['sessao_num'] == '110']
atas_48 = [a for a in atas if a['sessao_num'] == '048']

print(f"\n107ª encontrada: {len(atas_107)}")
if atas_107:
    print(f"  Data: {atas_107[0]['data_real']}")
    print(f"  Páginas: {atas_107[0]['pag_inicio']}-{atas_107[0]['pag_fim']}")
    print(f"  DCL: {atas_107[0]['dcl_original']}")

print(f"\n110ª encontrada: {len(atas_110)}")
if atas_110:
    print(f"  Data: {atas_110[0]['data_real']}")
    print(f"  Páginas: {atas_110[0]['pag_inicio']}-{atas_110[0]['pag_fim']}")
    print(f"  DCL: {atas_110[0]['dcl_original']}")

print(f"\n48ª encontrada: {len(atas_48)}")
if atas_48:
    print(f"  Data: {atas_48[0]['data_real']}")
    print(f"  Páginas: {atas_48[0]['pag_inicio']}-{atas_48[0]['pag_fim']}")
    print(f"  DCL: {atas_48[0]['dcl_original']}")

print(f"\n{'='*70}\n")

