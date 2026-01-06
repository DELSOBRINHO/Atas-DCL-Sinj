#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

print("\n" + "="*70)
print("CORRIGIR ATAS 108-111")
print("="*70)

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"\nTotal de atas antes: {len(atas)}")

# Remover a ata 011 ordinária duplicada (28/11/2007)
atas_para_remover = []
for i, ata in enumerate(atas):
    if (ata['sessao_num'] == '011' and ata['tipo_sessao'] == 'ORDINÁRIA' and 
        ata['data_real'] == '28/11/2007'):
        atas_para_remover.append(i)
        print(f"\n🗑️  Removida ATA 011 ORDINÁRIA (28/11/2007) - duplicada")

# Remover em ordem reversa
for i in sorted(atas_para_remover, reverse=True):
    atas.pop(i)

# Criar dicionário para acesso rápido
atas_dict = {(int(a['sessao_num']), a['tipo_sessao']): a for a in atas}

# Correções
correcoes = [
    (108, "ORDINÁRIA", 12),  # 108 vai até 12, próxima é 109 na página 13
    (109, "ORDINÁRIA", 22),  # 109 vai até 22, próxima é 110 na página 23
    (110, "ORDINÁRIA", 30),  # 110 vai até 30, próxima é 111 na página 31
    (111, "ORDINÁRIA", 34),  # 111 vai até 34
]

corrigidas = 0
for sessao_num, tipo, pag_fim_novo in correcoes:
    chave = (sessao_num, tipo)
    if chave in atas_dict:
        ata = atas_dict[chave]
        if ata['pag_fim'] != pag_fim_novo:
            print(f"\n✏️  Corrigida ATA {sessao_num:3d} {tipo}")
            print(f"   Página final: {ata['pag_fim']} → {pag_fim_novo}")
            ata['pag_fim'] = pag_fim_novo
            corrigidas += 1

# Salvar JSON
with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
    json.dump(atas, f, ensure_ascii=False, indent=2)

print(f"\n{'='*70}")
print(f"Total de atas removidas: {len(atas_para_remover)}")
print(f"Total de atas corrigidas: {corrigidas}")
print(f"Total de atas depois: {len(atas)}")
print(f"{'='*70}\n")

