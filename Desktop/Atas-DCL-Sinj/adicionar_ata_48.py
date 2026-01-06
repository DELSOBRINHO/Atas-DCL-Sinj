#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

print("\n" + "="*70)
print("ADICIONAR ATA 48ª")
print("="*70)

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"\nTotal de atas antes: {len(atas)}")

# Verificar se já existe
atas_48 = [a for a in atas if a['sessao_num'] == '048']

print(f"48ª encontrada: {len(atas_48)}")

# Adicionar 48ª ORDINÁRIA
if len(atas_48) == 0:
    ata_48 = {
        "sessao_num": "048",
        "tipo_sessao": "ORDINÁRIA",
        "data_real": "31/05/2007",
        "pag_inicio": 9,
        "pag_fim": 22,
        "dcl_original": "DCL_2007-07-128.pdf",
        "nomenclatura": "2007-05-31-1-SO-048-2-AC.pdf"
    }
    atas.append(ata_48)
    print("\n✅ Adicionada ATA 48ª ORDINÁRIA (31/05/2007)")
    print(f"   Páginas: 9-22 | DCL: DCL_2007-07-128.pdf")

# Ordenar por sessão_num
atas_sorted = sorted(atas, key=lambda x: int(x['sessao_num']))

# Salvar JSON
with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
    json.dump(atas_sorted, f, ensure_ascii=False, indent=2)

print(f"\n{'='*70}")
print(f"Total de atas depois: {len(atas_sorted)}")
print(f"{'='*70}\n")

