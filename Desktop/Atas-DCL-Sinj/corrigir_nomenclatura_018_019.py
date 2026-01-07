#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corrige a nomenclatura das sessões 018 e 019 EXTRAORDINÁRIAS.
Também corrige o tipo_sessao de EXTRAORDINARIA para EXTRAORDINÁRIA.
"""

import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, 'fase2_atas_2007_final.json')

print("=" * 70)
print("CORRIGIR NOMENCLATURA DAS SESSÕES 018 E 019 EXTRAORDINÁRIAS")
print("=" * 70)

# Carregar JSON
with open(json_path, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"\n📋 Total de atas: {len(atas)}")

# Correções
correcoes = [
    {
        'sessao_num': '018',
        'tipo_sessao_antigo': 'EXTRAORDINARIA',
        'tipo_sessao_novo': 'EXTRAORDINÁRIA',
        'nomenclatura_antiga': '2007-09-18-0-XX-018-2-AC.pdf',
        'nomenclatura_nova': '2007-09-18-2-SE-018-2-AC.pdf'
    },
    {
        'sessao_num': '019',
        'tipo_sessao_antigo': 'EXTRAORDINARIA',
        'tipo_sessao_novo': 'EXTRAORDINÁRIA',
        'nomenclatura_antiga': '2007-09-19-0-XX-019-2-AC.pdf',
        'nomenclatura_nova': '2007-09-19-2-SE-019-2-AC.pdf'
    }
]

corrigidas = 0
for ata in atas:
    for correcao in correcoes:
        if (str(ata.get('sessao_num')) == correcao['sessao_num'] and 
            ata.get('tipo_sessao') == correcao['tipo_sessao_antigo']):
            
            print(f"\n✏️ Corrigindo Sessão {correcao['sessao_num']} EXTRAORDINÁRIA:")
            print(f"   Tipo: {ata['tipo_sessao']} → {correcao['tipo_sessao_novo']}")
            print(f"   Nomenclatura: {ata['nomenclatura']}")
            print(f"              → {correcao['nomenclatura_nova']}")
            
            ata['tipo_sessao'] = correcao['tipo_sessao_novo']
            ata['nomenclatura'] = correcao['nomenclatura_nova']
            corrigidas += 1

# Salvar JSON atualizado
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(atas, f, ensure_ascii=False, indent=2)

print(f"\n{'=' * 70}")
print(f"RESULTADO")
print(f"{'=' * 70}")
print(f"✅ Atas corrigidas: {corrigidas}")
print(f"💾 JSON salvo: fase2_atas_2007_final.json")

