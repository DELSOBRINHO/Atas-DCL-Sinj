#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

print("\n" + "="*70)
print("ADICIONAR ATAS ENCONTRADAS NOS DCLs")
print("="*70)

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"\nTotal de atas antes: {len(atas)}")

# Atas a adicionar (baseado na análise dos DCLs)
# Formato: (sessao_num, tipo, data, pag_inicio, pag_fim, dcl_original)
atas_para_adicionar = [
    # DCL_2007-07-128.pdf: entre 47 e 49 está a 50ª
    ("050", "ORDINÁRIA", "06/06/2007", 23, 30, "DCL_2007-07-128.pdf"),
]

# Verificar quais já existem
atas_existentes = set(a['sessao_num'] for a in atas)

adicionadas = 0
for sessao_num, tipo, data, pag_inicio, pag_fim, dcl in atas_para_adicionar:
    if sessao_num not in atas_existentes:
        ata = {
            "sessao_num": sessao_num,
            "tipo_sessao": tipo,
            "data_real": data,
            "pag_inicio": pag_inicio,
            "pag_fim": pag_fim,
            "dcl_original": dcl,
            "nomenclatura": f"{data.split('/')[2]}-{data.split('/')[1]}-{data.split('/')[0]}-1-SO-{sessao_num}-2-AC.pdf"
        }
        atas.append(ata)
        print(f"\n✅ Adicionada ATA {sessao_num} {tipo} ({data})")
        print(f"   Páginas: {pag_inicio}-{pag_fim} | DCL: {dcl}")
        adicionadas += 1

# Ordenar por sessão_num
atas_sorted = sorted(atas, key=lambda x: int(x['sessao_num']))

# Salvar JSON
with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
    json.dump(atas_sorted, f, ensure_ascii=False, indent=2)

print(f"\n{'='*70}")
print(f"Total de atas adicionadas: {adicionadas}")
print(f"Total de atas depois: {len(atas_sorted)}")
print(f"{'='*70}\n")

