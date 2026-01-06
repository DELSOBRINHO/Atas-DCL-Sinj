#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

print("\n" + "="*70)
print("CORRIGIR ATAS 105-106 E EXTRAORDINÁRIAS 16-17")
print("="*70)

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"\nTotal de atas: {len(atas)}")

# Criar dicionário para acesso rápido
atas_dict = {(int(a['sessao_num']), a['tipo_sessao']): a for a in atas}

# Correções
correcoes = [
    (105, "ORDINÁRIA", 54),  # 105 vai até 54, próxima é 106 na página 54
    (106, "ORDINÁRIA", 54),  # 106 vai até 54 (última ata do DCL)
    (16, "EXTRAORDINÁRIA", 22),  # 16 vai até 22, próxima é 17 na página 22
    (17, "EXTRAORDINÁRIA", 24),  # 17 vai até 24
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
print(f"Total de atas corrigidas: {corrigidas}")
print(f"Total de atas depois: {len(atas)}")
print(f"{'='*70}\n")

