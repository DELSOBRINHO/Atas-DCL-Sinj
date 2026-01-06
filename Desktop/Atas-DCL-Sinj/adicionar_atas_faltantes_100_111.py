#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

print("\n" + "="*70)
print("ADICIONAR ATAS FALTANTES 100-111")
print("="*70)

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"\nTotal de atas antes: {len(atas)}")

# Atas a adicionar (baseado no que o usuário informou)
atas_para_adicionar = [
    ("100", "ORDINÁRIA", "01/11/2007", 1, 1, "DCL_2007-01-235.pdf"),
    ("102", "ORDINÁRIA", "07/11/2007", 8, 23, "DCL_2007-01-235.pdf"),
    ("103", "ORDINÁRIA", "08/11/2007", 23, 37, "DCL_2007-01-235.pdf"),
    ("105", "ORDINÁRIA", "14/11/2007", 43, 54, "DCL_2007-01-235.pdf"),
    ("106", "ORDINÁRIA", "20/11/2007", 54, 55, "DCL_2007-01-235.pdf"),
    ("107", "ORDINÁRIA", "21/10/2007", 1, 6, "DCL_2007-01-236.pdf"),
    ("110", "ORDINÁRIA", "28/11/2007", 23, 30, "DCL_2007-01-236.pdf"),
]

# Verificar quais já existem
atas_existentes = {(a['sessao_num'], a['tipo_sessao']): a for a in atas}

adicionadas = 0
for sessao_num, tipo, data, pag_inicio, pag_fim, dcl in atas_para_adicionar:
    chave = (sessao_num, tipo)
    if chave not in atas_existentes:
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

