#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ADICIONAR 97ª AO JSON
====================

Objetivo: Adicionar a ata 97ª que foi encontrada

Uso:
    python adicionar_97_ao_json.py

Autor: Sistema de Automação CLDF
Data: 2025-12-24
"""

import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

print("\n" + "="*70)
print("ADICIONAR 97ª AO JSON")
print("="*70)

# Carregar JSON
with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"\nTotal de atas antes: {len(atas)}")

# Criar nova ata 97ª
nova_ata = {
    "sessao_num": "097",
    "tipo_sessao": "ORDINÁRIA",
    "data_real": "25/10/2007",
    "pag_inicio": 1,
    "pag_fim": 6,
    "dcl_original": "DCL_2007-12-1766369304.pdf",
    "nomenclatura": "2007-10-25-1-SO-097-2-AC.pdf"
}

print(f"\n✅ Nova ata a adicionar:")
print(f"   Sessão: {nova_ata['sessao_num']}ª")
print(f"   Tipo: {nova_ata['tipo_sessao']}")
print(f"   Data: {nova_ata['data_real']}")
print(f"   Páginas: {nova_ata['pag_inicio']}-{nova_ata['pag_fim']}")
print(f"   DCL: {nova_ata['dcl_original']}")
print(f"   Nomenclatura: {nova_ata['nomenclatura']}")

# Adicionar à lista
atas.append(nova_ata)

# Ordenar por sessão_num
atas_sorted = sorted(atas, key=lambda x: int(x['sessao_num']))

# Salvar JSON
with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
    json.dump(atas_sorted, f, ensure_ascii=False, indent=2)

print(f"\n✅ JSON atualizado com sucesso!")
print(f"Total de atas depois: {len(atas_sorted)}")

print(f"\n" + "="*70)

