#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print("\n" + "="*70)
print("RELATÓRIO FINAL - LOTE 3")
print("="*70)

# Contar ordinárias e extraordinárias
ordinárias = [a for a in atas if a['tipo_sessao'] == 'ORDINÁRIA']
extraordinárias = [a for a in atas if a['tipo_sessao'] == 'EXTRAORDINÁRIA']

atas_ord_nums = sorted([int(a['sessao_num']) for a in ordinárias])
atas_ext_nums = sorted([int(a['sessao_num']) for a in extraordinárias])

print(f"\n📊 TOTAL DE ATAS: {len(atas)}")
print(f"   Ordinárias: {len(ordinárias)}")
print(f"   Extraordinárias: {len(extraordinárias)}")

# Encontrar faltando
faltando_ord = []
for i in range(1, 120):
    if i not in atas_ord_nums:
        faltando_ord.append(i)

faltando_ext = []
for i in range(1, 30):
    if i not in atas_ext_nums:
        faltando_ext.append(i)

print(f"\n❌ ATAS AINDA FALTANDO:")
print(f"   Ordinárias: {len(faltando_ord)}")
if faltando_ord:
    print(f"   {', '.join(str(x) + 'ª' for x in faltando_ord)}")

print(f"\n   Extraordinárias: {len(faltando_ext)}")
if faltando_ext:
    print(f"   {', '.join(str(x) + 'ª' for x in faltando_ext)}")

print(f"\n{'='*70}\n")

