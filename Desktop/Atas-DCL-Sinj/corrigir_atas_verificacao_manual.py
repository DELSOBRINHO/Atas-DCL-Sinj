#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORRIGIR ATAS - VERIFICAÇÃO MANUAL
===================================

Objetivo: Corrigir atas conforme verificação manual do usuário

Uso:
    python corrigir_atas_verificacao_manual.py

Autor: Sistema de Automação CLDF
Data: 2025-12-24
"""

import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

print("\n" + "="*70)
print("CORRIGIR ATAS - VERIFICAÇÃO MANUAL")
print("="*70)

# Carregar JSON
with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"\nTotal de atas antes: {len(atas)}")

# CORREÇÃO 1: 094ª → 095ª (23/10/2007)
print("\n1️⃣  CORREÇÃO: 094ª → 095ª")
for ata in atas:
    if (ata['sessao_num'] == '094' and 
        ata['data_real'] == '23/10/2007' and
        'DCL_2007-01-231' in ata['dcl_original']):
        print(f"   Encontrada: {ata['sessao_num']}ª")
        ata['sessao_num'] = '095'
        ata['nomenclatura'] = '2007-10-23-1-SO-095-2-AC.pdf'
        print(f"   ✅ Corrigida para: {ata['sessao_num']}ª")
        break

# CORREÇÃO 2: 024ª → 096ª (24/10/2007, DCL_2007-01-232.pdf)
print("\n2️⃣  CORREÇÃO: 024ª → 096ª (24/10/2007)")
for ata in atas:
    if (ata['sessao_num'] == '024' and 
        ata['data_real'] == '24/10/2007' and
        'DCL_2007-01-232' in ata['dcl_original']):
        print(f"   Encontrada: {ata['sessao_num']}ª")
        ata['sessao_num'] = '096'
        ata['nomenclatura'] = '2007-10-24-1-SO-096-2-AC.pdf'
        print(f"   ✅ Corrigida para: {ata['sessao_num']}ª")
        break

# CORREÇÃO 3: 024ª → 101ª (6/11/2007, DCL_2007-01-235.pdf)
print("\n3️⃣  CORREÇÃO: 024ª → 101ª (6/11/2007)")
for ata in atas:
    if (ata['sessao_num'] == '024' and 
        ata['data_real'] == '6/11/2007' and
        'DCL_2007-01-235' in ata['dcl_original']):
        print(f"   Encontrada: {ata['sessao_num']}ª")
        ata['sessao_num'] = '101'
        ata['nomenclatura'] = '2007-11-06-1-SO-101-2-AC.pdf'
        print(f"   ✅ Corrigida para: {ata['sessao_num']}ª")
        break

# CORREÇÃO 4: Corrigir páginas da 104ª (37-43)
print("\n4️⃣  CORREÇÃO: Páginas da 104ª")
for ata in atas:
    if ata['sessao_num'] == '104':
        print(f"   Encontrada: {ata['sessao_num']}ª")
        print(f"   Páginas antes: {ata['pag_inicio']}-{ata['pag_fim']}")
        ata['pag_inicio'] = 37
        ata['pag_fim'] = 43
        print(f"   ✅ Páginas corrigidas para: {ata['pag_inicio']}-{ata['pag_fim']}")
        break

# ADIÇÃO 1: 100ª (1/11/2007, páginas 1-1)
print("\n5️⃣  ADIÇÃO: 100ª")
nova_ata_100 = {
    "sessao_num": "100",
    "tipo_sessao": "ORDINÁRIA",
    "data_real": "01/11/2007",
    "pag_inicio": 1,
    "pag_fim": 1,
    "dcl_original": "DCL_2007-01-235.pdf",
    "nomenclatura": "2007-11-01-1-SO-100-2-AC.pdf"
}
atas.append(nova_ata_100)
print(f"   ✅ Adicionada: 100ª (01/11/2007, páginas 1-1)")

# ADIÇÃO 2: 102ª (7/11/2007, páginas 8-23)
print("\n6️⃣  ADIÇÃO: 102ª")
nova_ata_102 = {
    "sessao_num": "102",
    "tipo_sessao": "ORDINÁRIA",
    "data_real": "07/11/2007",
    "pag_inicio": 8,
    "pag_fim": 23,
    "dcl_original": "DCL_2007-01-235.pdf",
    "nomenclatura": "2007-11-07-1-SO-102-2-AC.pdf"
}
atas.append(nova_ata_102)
print(f"   ✅ Adicionada: 102ª (07/11/2007, páginas 8-23)")

# ADIÇÃO 3: 103ª (8/11/2007, páginas 23-37)
print("\n7️⃣  ADIÇÃO: 103ª")
nova_ata_103 = {
    "sessao_num": "103",
    "tipo_sessao": "ORDINÁRIA",
    "data_real": "08/11/2007",
    "pag_inicio": 23,
    "pag_fim": 37,
    "dcl_original": "DCL_2007-01-235.pdf",
    "nomenclatura": "2007-11-08-1-SO-103-2-AC.pdf"
}
atas.append(nova_ata_103)
print(f"   ✅ Adicionada: 103ª (08/11/2007, páginas 23-37)")

# ADIÇÃO 4: 105ª (14/11/2007, páginas 43-54)
print("\n8️⃣  ADIÇÃO: 105ª")
nova_ata_105 = {
    "sessao_num": "105",
    "tipo_sessao": "ORDINÁRIA",
    "data_real": "14/11/2007",
    "pag_inicio": 43,
    "pag_fim": 54,
    "dcl_original": "DCL_2007-01-235.pdf",
    "nomenclatura": "2007-11-14-1-SO-105-2-AC.pdf"
}
atas.append(nova_ata_105)
print(f"   ✅ Adicionada: 105ª (14/11/2007, páginas 43-54)")

# ADIÇÃO 5: 106ª (20/11/2007, páginas 54-55)
print("\n9️⃣  ADIÇÃO: 106ª")
nova_ata_106 = {
    "sessao_num": "106",
    "tipo_sessao": "ORDINÁRIA",
    "data_real": "20/11/2007",
    "pag_inicio": 54,
    "pag_fim": 55,
    "dcl_original": "DCL_2007-01-235.pdf",
    "nomenclatura": "2007-11-20-1-SO-106-2-AC.pdf"
}
atas.append(nova_ata_106)
print(f"   ✅ Adicionada: 106ª (20/11/2007, páginas 54-55)")

# Ordenar por sessão_num
atas_sorted = sorted(atas, key=lambda x: int(x['sessao_num']))

# Salvar JSON
with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
    json.dump(atas_sorted, f, ensure_ascii=False, indent=2)

print(f"\n✅ JSON atualizado com sucesso!")
print(f"Total de atas depois: {len(atas_sorted)}")

print(f"\n" + "="*70)

