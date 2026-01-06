#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORRIGIR NOMENCLATURA - TIPO DE SESSÃO
"""

import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

print("\n" + "="*70)
print("CORRIGIR NOMENCLATURA - TIPO DE SESSÃO")
print("="*70)

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"\nTotal de atas: {len(atas)}")

# Mapeamento de correções
correcoes = {
    '003': ('ORDINÁRIA', '2007-04-18-1-SO-003-2-AC.pdf'),
    '008': ('EXTRAORDINÁRIA', '2007-09-27-2-SE-008-2-AC.pdf'),
    '018': ('EXTRAORDINÁRIA', '2007-09-18-2-SE-018-2-AC.pdf'),
    '022': ('EXTRAORDINÁRIA', '2007-10-17-2-SE-022-2-AC.pdf'),
    '027': ('EXTRAORDINÁRIA', '2007-11-13-2-SE-027-2-AC.pdf'),
    '048': ('ORDINÁRIA', '2007-09-26-1-SO-048-2-AC.pdf'),
    '058': ('ORDINÁRIA', '2007-09-29-1-SO-058-2-AC.pdf'),
    '068': ('ORDINÁRIA', '2007-11-20-1-SO-068-2-AC.pdf'),
    '088': ('ORDINÁRIA', '2007-10-04-1-SO-088-2-AC.pdf'),
    '093': ('ORDINÁRIA', '2007-05-10-1-SO-093-2-AC.pdf'),
}

corrigidas = 0

for sessao_num, (tipo_esperado, nomenclatura_correta) in correcoes.items():
    for ata in atas:
        if ata['sessao_num'] == sessao_num:
            if ata['nomenclatura'] != nomenclatura_correta:
                print(f"\nCorrigindo {sessao_num}:")
                print(f"  Antes: {ata['nomenclatura']}")
                print(f"  Depois: {nomenclatura_correta}")
                ata['nomenclatura'] = nomenclatura_correta
                corrigidas += 1
            break

# Ordenar por sessão_num
atas_sorted = sorted(atas, key=lambda x: int(x['sessao_num']))

# Salvar JSON
with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
    json.dump(atas_sorted, f, ensure_ascii=False, indent=2)

print(f"\nJSON atualizado com sucesso!")
print(f"Total de atas corrigidas: {corrigidas}")

print(f"\n" + "="*70)

