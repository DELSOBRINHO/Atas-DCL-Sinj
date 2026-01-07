#!/usr/bin/env python3
import json

with open('fase2_atas_2007_final.json', 'r', encoding='utf-8') as f:
    atas = json.load(f)

print("=" * 90)
print("VERIFICAÇÃO DAS DATAS DE PUBLICAÇÃO DA ATA")
print("=" * 90)
print(f"{'Sessão':>6} | {'Tipo':^12} | {'Data Sessão':^12} | {'Data Pub Ata':^12} | {'DCL Original'}")
print("-" * 90)

# Agrupar por DCL para mostrar a correspondência
dcls_vistos = set()
for ata in sorted(atas, key=lambda x: (x['dcl_original'], int(str(x['sessao_num'])))):
    dcl = ata['dcl_original']
    
    # Mostrar apenas um exemplo de cada DCL
    if dcl not in dcls_vistos:
        dcls_vistos.add(dcl)
        sessao = str(ata['sessao_num']).zfill(3)
        tipo = "ORD" if "ORDINÁRIA" == ata['tipo_sessao'] else "EXT"
        data_real = ata['data_real']
        data_pub = ata.get('data_publicacao_ata', 'N/A')
        
        print(f"{sessao:>6} | {tipo:^12} | {data_real:^12} | {data_pub:^12} | {dcl}")

print("\n" + "=" * 90)
print(f"Total de DCLs verificados: {len(dcls_vistos)}")
print("=" * 90)

