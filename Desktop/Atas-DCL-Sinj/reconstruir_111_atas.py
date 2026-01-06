#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

print("\n" + "="*70)
print("RECONSTRUIR 111 ATAS")
print("="*70)

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"\nTotal de atas antes: {len(atas)}")

# Atas que faltam (que foram adicionadas antes)
atas_faltantes = [
    {
        "sessao_num": "100",
        "tipo_sessao": "ORDINÁRIA",
        "data_real": "01/11/2007",
        "pag_inicio": 1,
        "pag_fim": 1,
        "dcl_original": "DCL_2007-01-235.pdf",
        "nomenclatura": "2007-11-01-1-SO-100-2-AC.pdf"
    },
    {
        "sessao_num": "102",
        "tipo_sessao": "ORDINÁRIA",
        "data_real": "07/11/2007",
        "pag_inicio": 8,
        "pag_fim": 23,
        "dcl_original": "DCL_2007-01-235.pdf",
        "nomenclatura": "2007-11-07-1-SO-102-2-AC.pdf"
    },
    {
        "sessao_num": "103",
        "tipo_sessao": "ORDINÁRIA",
        "data_real": "08/11/2007",
        "pag_inicio": 23,
        "pag_fim": 37,
        "dcl_original": "DCL_2007-01-235.pdf",
        "nomenclatura": "2007-11-08-1-SO-103-2-AC.pdf"
    },
    {
        "sessao_num": "105",
        "tipo_sessao": "ORDINÁRIA",
        "data_real": "14/11/2007",
        "pag_inicio": 43,
        "pag_fim": 54,
        "dcl_original": "DCL_2007-01-235.pdf",
        "nomenclatura": "2007-11-14-1-SO-105-2-AC.pdf"
    },
    {
        "sessao_num": "106",
        "tipo_sessao": "ORDINÁRIA",
        "data_real": "20/11/2007",
        "pag_inicio": 54,
        "pag_fim": 55,
        "dcl_original": "DCL_2007-01-235.pdf",
        "nomenclatura": "2007-11-20-1-SO-106-2-AC.pdf"
    }
]

# Adicionar atas faltantes
for ata in atas_faltantes:
    atas.append(ata)
    print(f"✅ Adicionada: {ata['sessao_num']}ª")

# Ordenar por sessão_num
atas_sorted = sorted(atas, key=lambda x: int(x['sessao_num']))

# Salvar JSON
with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
    json.dump(atas_sorted, f, ensure_ascii=False, indent=2)

print(f"\n✅ JSON atualizado com sucesso!")
print(f"Total de atas depois: {len(atas_sorted)}")

print(f"\n" + "="*70)

