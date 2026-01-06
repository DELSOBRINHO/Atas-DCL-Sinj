#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print("\n" + "="*70)
print("REMOVER DUPLICATAS")
print("="*70)

print(f"\nTotal de atas antes: {len(atas)}")

# Remover duplicatas por nomenclatura
vistas = set()
atas_unicas = []

for ata in atas:
    nomenclatura = ata['nomenclatura']
    if nomenclatura not in vistas:
        vistas.add(nomenclatura)
        atas_unicas.append(ata)
    else:
        print(f"Duplicata removida: {ata['sessao_num']} ({nomenclatura})")

# Ordenar por sessão_num
atas_sorted = sorted(atas_unicas, key=lambda x: int(x['sessao_num']))

# Salvar JSON
with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
    json.dump(atas_sorted, f, ensure_ascii=False, indent=2)

print(f"\nJSON atualizado com sucesso!")
print(f"Total de atas depois: {len(atas_sorted)}")

print(f"\n" + "="*70)

