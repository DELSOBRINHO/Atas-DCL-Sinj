#!/usr/bin/env python3
import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

print("CORRIGIR ERROS CRÍTICOS")
print("="*70)

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

print(f"\nTotal de atas antes: {len(atas)}")

# 1. Adicionar ATA 001ª (1ª SESSÃO ORDINÁRIA)
ata_001 = {
    "sessao_num": "001",
    "tipo_sessao": "ORDINÁRIA",
    "data_real": "1/02/2007",
    "pag_inicio": 10,
    "pag_fim": 22,
    "dcl_original": "DCL_2007-03-044.pdf",
    "nomenclatura": "2007-02-01-1-SO-001-2-AC.pdf"
}

# 2. Corrigir ATA 002ª EXTRAORDINÁRIA (página final deve ser 4, não 3)
# 3. Corrigir ATA 003ª ORDINÁRIA (página final deve ser 5, não 4)
# 4. Corrigir ATA 030ª (está como 003ª no índice 3)

correcoes = []

# Encontrar e corrigir
for i, ata in enumerate(atas):
    # Corrigir 002ª EXTRAORDINÁRIA
    if ata['sessao_num'] == '002' and ata['tipo_sessao'] == 'EXTRAORDINÁRIA':
        if ata['pag_fim'] == 3:
            print(f"\n✅ Corrigindo 002ª EXTRAORDINÁRIA: pag_fim 3 -> 4")
            ata['pag_fim'] = 4
            correcoes.append(f"002ª EXTRAORDINÁRIA: pag_fim 3 -> 4")
    
    # Corrigir 003ª ORDINÁRIA
    if ata['sessao_num'] == '003' and ata['tipo_sessao'] == 'ORDINÁRIA' and ata['data_real'] == '7/02/2007':
        if ata['pag_fim'] == 4:
            print(f"\n✅ Corrigindo 003ª ORDINÁRIA: pag_fim 4 -> 5")
            ata['pag_fim'] = 5
            correcoes.append(f"003ª ORDINÁRIA: pag_fim 4 -> 5")
    
    # Corrigir 030ª (está como 003ª)
    if ata['sessao_num'] == '003' and ata['tipo_sessao'] == 'ORDINÁRIA' and ata['data_real'] == '18/04/2007':
        print(f"\n✅ Corrigindo sessão 003 -> 030 (data 18/04/2007)")
        ata['sessao_num'] = '030'
        ata['nomenclatura'] = '2007-04-18-1-SO-030-2-AC.pdf'
        correcoes.append(f"Sessão 003 -> 030 (18/04/2007)")

# Adicionar ATA 001ª no início
atas.insert(0, ata_001)
print(f"\n✅ Adicionada ATA 001ª ORDINÁRIA (1/02/2007)")
correcoes.insert(0, "Adicionada ATA 001ª ORDINÁRIA")

# Ordenar por sessão_num
atas_sorted = sorted(atas, key=lambda x: int(x['sessao_num']))

# Salvar JSON
with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
    json.dump(atas_sorted, f, ensure_ascii=False, indent=2)

print(f"\n{'='*70}")
print(f"Total de atas depois: {len(atas_sorted)}")
print(f"Correções realizadas: {len(correcoes)}")
for corr in correcoes:
    print(f"  • {corr}")
print(f"{'='*70}")

