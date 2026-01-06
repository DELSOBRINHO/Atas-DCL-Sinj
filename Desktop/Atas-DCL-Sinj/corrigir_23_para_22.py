#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORRIGIR 23ª PARA 22ª
====================

Objetivo: Corrigir a ata 23ª que deveria ser 22ª

Uso:
    python corrigir_23_para_22.py

Autor: Sistema de Automação CLDF
Data: 2025-12-24
"""

import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")
ARQUIVO_BACKUP = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final_BACKUP.json")

print("\n" + "="*70)
print("CORRIGIR 23ª PARA 22ª")
print("="*70)

# Carregar JSON
with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"\nTotal de atas: {len(atas)}")

# Fazer backup
with open(ARQUIVO_BACKUP, 'w', encoding='utf-8') as f:
    json.dump(atas, f, ensure_ascii=False, indent=2)

print(f"✅ Backup criado: {ARQUIVO_BACKUP.name}")

# Procurar e corrigir
encontrada = False
for ata in atas:
    if (ata['sessao_num'] == '023' and
        'DCL_2007-01-231' in ata['dcl_original'] and
        ata['data_real'] == '17/10/2007'):
        
        print(f"\n🔍 Encontrada ata para correção:")
        print(f"   Sessão: {ata['sessao_num']}ª")
        print(f"   Data: {ata['data_real']}")
        print(f"   DCL: {ata['dcl_original']}")
        print(f"   Nomenclatura atual: {ata['nomenclatura']}")
        
        # Corrigir
        ata['sessao_num'] = '022'
        ata['nomenclatura'] = ata['nomenclatura'].replace('-023-223-', '-022-222-')
        
        print(f"\n✅ Corrigida para:")
        print(f"   Sessão: {ata['sessao_num']}ª")
        print(f"   Nomenclatura nova: {ata['nomenclatura']}")
        
        encontrada = True
        break

if encontrada:
    # Salvar JSON corrigido
    with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
        json.dump(atas, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ JSON atualizado com sucesso!")
else:
    print(f"\n❌ Ata não encontrada para correção")

print(f"\n" + "="*70)

