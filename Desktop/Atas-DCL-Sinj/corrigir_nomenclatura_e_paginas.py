#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from collections import defaultdict

# Carregar o arquivo principal
script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, 'fase2_atas_2007_final.json')

print("📖 Carregando arquivo JSON...")
with open(json_path, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"✅ {len(atas)} atas carregadas\n")

# PASSO 1: Renomear data_publicacao_dcl para data_publicacao_ata
print("=" * 80)
print("PASSO 1: Renomeando data_publicacao_dcl → data_publicacao_ata")
print("=" * 80)

for ata in atas:
    if 'data_publicacao_dcl' in ata:
        ata['data_publicacao_ata'] = ata.pop('data_publicacao_dcl')

print("✅ Campo renomeado em todas as atas\n")

# PASSO 2: Implementar lógica inteligente de página final
print("=" * 80)
print("PASSO 2: Implementando lógica inteligente de página final")
print("=" * 80)

# Agrupar atas por DCL
atas_por_dcl = defaultdict(list)
for ata in atas:
    dcl = ata['dcl_original']
    atas_por_dcl[dcl].append(ata)

# Processar cada DCL
for dcl, atas_dcl in atas_por_dcl.items():
    # Ordenar por página inicial
    atas_dcl.sort(key=lambda x: int(x['pag_inicio']))
    
    print(f"\n📄 DCL: {dcl}")
    print(f"   Total de atas: {len(atas_dcl)}")
    
    for i, ata in enumerate(atas_dcl):
        sessao = str(ata['sessao_num']).zfill(3)
        tipo = ata['tipo_sessao']
        pag_inicio = int(ata['pag_inicio'])
        pag_fim_atual = int(ata['pag_fim'])

        # Determinar página final inteligente
        if i < len(atas_dcl) - 1:
            # Não é a última ata do DCL
            proxima_ata = atas_dcl[i + 1]
            pag_proxima = int(proxima_ata['pag_inicio'])
            pag_fim_inteligente = pag_proxima - 1
            motivo = "Próxima ata encontrada"
        else:
            # É a última ata do DCL
            pag_fim_inteligente = pag_fim_atual
            motivo = "Última ata do DCL"

        # Atualizar página final se mudou
        if pag_fim_inteligente != pag_fim_atual:
            print(f"   ✏️  Sessão {sessao} ({tipo:15s}): Pág {pag_inicio}-{pag_fim_atual} → {pag_inicio}-{pag_fim_inteligente} ({motivo})")
            ata['pag_fim'] = pag_fim_inteligente
        else:
            print(f"   ✅ Sessão {sessao} ({tipo:15s}): Pág {pag_inicio}-{pag_fim_inteligente} (OK)")

# Salvar JSON atualizado
print("\n" + "=" * 80)
print("💾 Salvando arquivo JSON atualizado...")
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(atas, f, ensure_ascii=False, indent=2)

print(f"✅ Arquivo salvo: {json_path}")
print(f"✅ Total de atas processadas: {len(atas)}")
print(f"✅ Campo renomeado: data_publicacao_dcl → data_publicacao_ata")
print(f"✅ Lógica de página final implementada")

