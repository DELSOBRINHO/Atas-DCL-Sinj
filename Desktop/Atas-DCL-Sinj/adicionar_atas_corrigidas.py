#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

print("\n" + "="*70)
print("ADICIONAR ATAS CORRIGIDAS")
print("="*70)

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"\nTotal de atas antes: {len(atas)}")

# Atas a adicionar/corrigir
atas_para_adicionar = [
    ("036", "ORDINÁRIA", "07/05/2007", 1, 2, "DCL_2007-05-1766368920.pdf"),
    ("037", "ORDINÁRIA", "08/05/2007", 2, 12, "DCL_2007-05-1766368920.pdf"),
    ("112", "ORDINÁRIA", "04/12/2007", 1, 17, "DCL_2008-02-176636937.pdf"),
    ("113", "ORDINÁRIA", "05/12/2007", 17, 33, "DCL_2008-02-176636937.pdf"),
    ("114", "ORDINÁRIA", "06/12/2007", 33, 49, "DCL_2008-02-176636937.pdf"),
    ("031", "EXTRAORDINÁRIA", "04/12/2007", 49, 50, "DCL_2008-02-176636937.pdf"),
    ("032", "EXTRAORDINÁRIA", "05/12/2007", 50, 52, "DCL_2008-02-176636937.pdf"),
]

# Verificar quais já existem
atas_existentes = {a['sessao_num']: a for a in atas}

adicionadas = 0
atualizadas = 0

for sessao_num, tipo, data, pag_inicio, pag_fim, dcl in atas_para_adicionar:
    if sessao_num in atas_existentes:
        # Atualizar
        atas_existentes[sessao_num]['data_real'] = data
        atas_existentes[sessao_num]['pag_inicio'] = pag_inicio
        atas_existentes[sessao_num]['pag_fim'] = pag_fim
        atas_existentes[sessao_num]['dcl_original'] = dcl
        print(f"\n✏️  Atualizada ATA {sessao_num} {tipo} ({data})")
        print(f"   Páginas: {pag_inicio}-{pag_fim} | DCL: {dcl}")
        atualizadas += 1
    else:
        # Adicionar
        ata = {
            "sessao_num": sessao_num,
            "tipo_sessao": tipo,
            "data_real": data,
            "pag_inicio": pag_inicio,
            "pag_fim": pag_fim,
            "dcl_original": dcl,
            "nomenclatura": f"{data.split('/')[2]}-{data.split('/')[1]}-{data.split('/')[0]}-1-S{tipo[0]}-{sessao_num}-2-AC.pdf"
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
print(f"Total de atas atualizadas: {atualizadas}")
print(f"Total de atas depois: {len(atas_sorted)}")
print(f"{'='*70}\n")

