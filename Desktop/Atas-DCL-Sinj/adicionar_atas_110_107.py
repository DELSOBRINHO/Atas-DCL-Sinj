#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

print("\n" + "="*70)
print("ADICIONAR ATAS 110ª E 107ª")
print("="*70)

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"\nTotal de atas antes: {len(atas)}")

# Verificar se já existem
atas_110 = [a for a in atas if a['sessao_num'] == '110']
atas_107 = [a for a in atas if a['sessao_num'] == '107']

print(f"110ª encontrada: {len(atas_110)}")
print(f"107ª encontrada: {len(atas_107)}")

# Adicionar 110ª ORDINÁRIA
if len(atas_110) == 0:
    ata_110 = {
        "sessao_num": "110",
        "tipo_sessao": "ORDINÁRIA",
        "data_real": "28/11/2007",
        "pag_inicio": 23,
        "pag_fim": 31,
        "dcl_original": "DCL_2007-01-236.pdf",
        "nomenclatura": "2007-11-28-1-SO-110-2-AC.pdf"
    }
    atas.append(ata_110)
    print("\n✅ Adicionada ATA 110ª ORDINÁRIA (28/11/2007)")
    print(f"   Páginas: 23-31 | DCL: DCL_2007-01-236.pdf")

# Adicionar 107ª ORDINÁRIA
if len(atas_107) == 0:
    ata_107 = {
        "sessao_num": "107",
        "tipo_sessao": "ORDINÁRIA",
        "data_real": "21/11/2007",
        "pag_inicio": 1,
        "pag_fim": 6,
        "dcl_original": "DCL_2007-01-236.pdf",
        "nomenclatura": "2007-11-21-1-SO-107-2-AC.pdf"
    }
    atas.append(ata_107)
    print("\n✅ Adicionada ATA 107ª ORDINÁRIA (21/11/2007)")
    print(f"   Páginas: 1-6 | DCL: DCL_2007-01-236.pdf")

# Ordenar por sessão_num
atas_sorted = sorted(atas, key=lambda x: int(x['sessao_num']))

# Salvar JSON
with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
    json.dump(atas_sorted, f, ensure_ascii=False, indent=2)

print(f"\n{'='*70}")
print(f"Total de atas depois: {len(atas_sorted)}")
print(f"{'='*70}\n")

