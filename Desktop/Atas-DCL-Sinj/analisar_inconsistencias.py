#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print("\n" + "="*70)
print("ANÁLISE DE INCONSISTÊNCIAS")
print("="*70 + "\n")

# Encontrar atas duplicadas
from collections import defaultdict
atas_por_sessao = defaultdict(list)

for ata in atas:
    chave = (int(ata['sessao_num']), ata['tipo_sessao'])
    atas_por_sessao[chave].append(ata)

print("ATAS COM MÚLTIPLOS REGISTROS:\n")
for chave, registros in sorted(atas_por_sessao.items()):
    if len(registros) > 1:
        sessao_num, tipo = chave
        print(f"ATA {sessao_num:3d} {tipo}:")
        for i, ata in enumerate(registros, 1):
            print(f"  {i}. {ata['data_real']} - pag {ata['pag_inicio']}-{ata['pag_fim']} - {ata['dcl_original']}")
        print()

print(f"{'='*70}\n")

