#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

print("\n" + "="*70)
print("CORRIGIR PÁGINAS FINAIS - VERSÃO CORRETA")
print("="*70)

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"\nTotal de atas: {len(atas)}")

# Criar dicionário para acesso rápido
atas_dict = {(int(a['sessao_num']), a['tipo_sessao']): a for a in atas}

# Correções específicas baseadas nas informações do usuário
correcoes = [
    (101, "ORDINÁRIA", 8),      # página final deve ser 8 (não 22)
    (104, "ORDINÁRIA", 42),     # página final deve ser 42 (próxima é 105 na página 43)
    (105, "ORDINÁRIA", 54),     # página final deve ser 54 (próxima é 106 na página 54)
    (106, "ORDINÁRIA", 54),     # página final deve ser 54 (última do DCL)
    (107, "ORDINÁRIA", 6),      # página final deve ser 6
    (110, "ORDINÁRIA", 30),     # página final deve ser 30
    (111, "ORDINÁRIA", 34),     # página final deve ser 34
    (16, "EXTRAORDINÁRIA", 22), # página final deve ser 22
    (17, "EXTRAORDINÁRIA", 24), # página final deve ser 24
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

