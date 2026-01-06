#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

print("\n" + "="*70)
print("CORRIGIR PÁGINAS FINAIS 61-70")
print("="*70)

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"\nTotal de atas: {len(atas)}")

# Criar dicionário para acesso rápido
atas_dict = {(int(a['sessao_num']), a['tipo_sessao']): a for a in atas}

# Correções específicas baseadas na análise
correcoes = [
    (61, "ORDINÁRIA", 8),   # 061 vai até 8, próxima é 062 na página 9
    (62, "ORDINÁRIA", 11),  # 062 vai até 11, próxima é 063 na página 12
    (63, "ORDINÁRIA", 22),  # 063 vai até 22, próxima é 064 na página 23
    (64, "ORDINÁRIA", 23),  # 064 vai até 23, próxima é 065 na página 24
    (65, "ORDINÁRIA", 30),  # 065 vai até 30, próxima é 066 na página 31
    (66, "ORDINÁRIA", 37),  # 066 vai até 37, próxima é 067 na página 38
    (67, "ORDINÁRIA", 47),  # 067 vai até 47, próxima é 068 na página 48
    (68, "ORDINÁRIA", 52),  # 068 vai até 52, próxima é 069 em outro DCL
    (69, "ORDINÁRIA", 9),   # 069 vai até 9, próxima é 070 na página 10
    (70, "ORDINÁRIA", 28),  # 070 vai até 28
]

corrigidas = 0
for sessao_num, tipo, pag_fim_esperado in correcoes:
    chave = (sessao_num, tipo)
    if chave in atas_dict:
        ata = atas_dict[chave]
        if ata['pag_fim'] != pag_fim_esperado:
            print(f"\n✏️  Corrigida ATA {sessao_num:3d} {tipo}")
            print(f"   Página final: {ata['pag_fim']} → {pag_fim_esperado}")
            ata['pag_fim'] = pag_fim_esperado
            corrigidas += 1

# Salvar JSON
with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
    json.dump(atas, f, ensure_ascii=False, indent=2)

print(f"\n{'='*70}")
print(f"Total de atas corrigidas: {corrigidas}")
print(f"Total de atas depois: {len(atas)}")
print(f"{'='*70}\n")

