#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print("\n" + "="*70)
print("CORRIGIR NOMENCLATURA - APENAS ATAS MENCIONADAS")
print("="*70)

# Mapeamento preciso: (sessao, data_real) -> nova_nomenclatura
# Baseado nas datas reais encontradas no JSON
correcoes = {
    ('003', '7/02/2007'): '2007-02-07-1-SO-003-2-AC.pdf',
    ('003', '2/05/2007'): '2007-05-02-2-SE-003-2-AC.pdf',
    ('008', '22/02/2007'): '2007-02-22-1-SO-008-2-AC.pdf',
    ('008', '16/05/2007'): '2007-05-16-2-SE-008-2-AC.pdf',
    ('018', '20/03/2007'): '2007-03-20-1-SO-018-2-AC.pdf',
    ('018', '18/09/2007'): '2007-09-18-2-SE-018-2-AC.pdf',
    ('022', '17/10/2007'): '2007-10-17-2-SE-022-2-AC.pdf',
    ('022', '28/03/2007'): '2007-03-28-1-SO-022-2-AC.pdf',
    ('027', '13/11/2007'): '2007-11-13-2-SE-027-2-AC.pdf',
    ('027', '11/04/2007'): '2007-04-11-1-SO-027-2-AC.pdf',
    ('048', '26/09/2007'): '2007-09-26-1-SO-048-2-AC.pdf',
    ('058', '27/06/2007'): '2007-06-27-1-SO-058-2-AC.pdf',
    ('058', '29/09/2007'): '2007-09-29-1-SO-058-2-AC.pdf',
    ('068', '20/11/2007'): '2007-11-20-1-SO-068-2-AC.pdf',
    ('068', '2/10/2007'): '2007-10-02-1-SO-068-2-AC.pdf',
    ('088', '4/10/2007'): '2007-10-04-1-SO-088-2-AC.pdf',
    ('093', '17/10/2007'): '2007-10-17-1-SO-093-2-AC.pdf',
    ('093', '10/05/2007'): '2007-05-10-1-SO-093-2-AC.pdf',
}

corrigidas = 0

for ata in atas:
    chave = (ata['sessao_num'], ata['data_real'])

    if chave in correcoes:
        nova_nomenclatura = correcoes[chave]
        if ata['nomenclatura'] != nova_nomenclatura:
            print(f"\nCorrigindo {ata['sessao_num']} ({ata['data_real']}):")
            print(f"   Antes: {ata['nomenclatura']}")
            print(f"   Depois: {nova_nomenclatura}")
            ata['nomenclatura'] = nova_nomenclatura
            corrigidas += 1

# Ordenar por sessão_num
atas_sorted = sorted(atas, key=lambda x: int(x['sessao_num']))

# Salvar JSON
with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
    json.dump(atas_sorted, f, ensure_ascii=False, indent=2)

print(f"\nJSON atualizado com sucesso!")
print(f"Total de atas corrigidas: {corrigidas}")

print(f"\n" + "="*70)

