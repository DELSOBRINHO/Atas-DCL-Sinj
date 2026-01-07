#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analisar DCLs para encontrar o fim real de cada sessão.
Prioridades:
1. Fim confirmado da sessão (marcadores de encerramento)
2. Encontro de uma nova ata
3. Final do DCL (último recurso)
"""

import json
import os
import re
import fitz  # PyMuPDF

# Marcadores de fim de sessão
MARCADORES_FIM_SESSAO = [
    r'[Ee]ncerrou[-\s]se a sess[aã]o',
    r'[Ff]oi encerrada a sess[aã]o',
    r'[Ee]ncerramento da sess[aã]o',
    r'[Ss]ess[aã]o encerrada',
    r'[Dd]eclaro encerrada',
    r'[Ee]ncerra[-\s]se a sess[aã]o',
    r'[Ff]inalizada a sess[aã]o',
    r'[Tt]ermina a sess[aã]o',
]

# Marcadores de início de nova ata
MARCADORES_NOVA_ATA = [
    r'ATA\s+(?:CIRCUNSTANCIADA\s+)?DA\s+\d+[ªº]?\s+SESS[AÃ]O',
    r'ATA\s+DA\s+(?:\d+[ªº]?\s+)?SESS[AÃ]O\s+(?:ORDIN[AÁ]RIA|EXTRAORDIN[AÁ]RIA)',
]

script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, 'fase2_atas_2007_final.json')
downloads_dir = os.path.join(script_dir, 'downloads_2007')

print("📖 Carregando arquivo JSON...")
with open(json_path, 'r', encoding='utf-8') as f:
    atas = json.load(f)
print(f"✅ {len(atas)} atas carregadas\n")

# Agrupar atas por DCL
from collections import defaultdict
atas_por_dcl = defaultdict(list)
for ata in atas:
    dcl = ata['dcl_original']
    atas_por_dcl[dcl].append(ata)

# Processar cada DCL
print("=" * 80)
print("ANALISANDO DCLs PARA ENCONTRAR FIM DE SESSÃO")
print("=" * 80)

alteracoes = []

for dcl_name, atas_dcl in atas_por_dcl.items():
    # Ordenar por página inicial
    atas_dcl.sort(key=lambda x: int(x['pag_inicio']))
    
    # Procurar PDF na pasta downloads_2007
    pdf_path = os.path.join(downloads_dir, dcl_name)
    
    if not os.path.exists(pdf_path):
        print(f"\n⚠️  DCL não encontrado: {dcl_name}")
        continue
    
    print(f"\n📄 DCL: {dcl_name}")
    print(f"   Atas: {len(atas_dcl)}")
    
    try:
        doc = fitz.open(pdf_path)
        total_paginas = doc.page_count
        
        for i, ata in enumerate(atas_dcl):
            sessao = str(ata['sessao_num']).zfill(3)
            tipo = ata['tipo_sessao']
            pag_inicio = int(ata['pag_inicio'])
            pag_fim_atual = int(ata['pag_fim'])
            
            # Determinar limite máximo
            if i < len(atas_dcl) - 1:
                proxima_ata = atas_dcl[i + 1]
                pag_limite = int(proxima_ata['pag_inicio']) - 1
            else:
                pag_limite = total_paginas
            
            # Procurar fim da sessão dentro do intervalo
            pag_fim_encontrado = None
            
            for pag_num in range(pag_inicio - 1, pag_limite):
                if pag_num >= total_paginas:
                    break
                page = doc[pag_num]
                texto = page.get_text()
                
                # Verificar marcadores de fim de sessão
                for marcador in MARCADORES_FIM_SESSAO:
                    if re.search(marcador, texto, re.IGNORECASE):
                        pag_fim_encontrado = pag_num + 1  # 1-based
                        break
                
                if pag_fim_encontrado:
                    break
            
            # Determinar página final
            if pag_fim_encontrado:
                pag_fim_nova = pag_fim_encontrado
                motivo = "Fim da sessão encontrado"
            elif i < len(atas_dcl) - 1:
                pag_fim_nova = pag_limite
                motivo = "Próxima ata"
            else:
                pag_fim_nova = pag_limite
                motivo = "Fim do DCL"
            
            # Registrar alteração
            if pag_fim_nova != pag_fim_atual:
                print(f"   ✏️  Sessão {sessao} ({tipo:15s}): {pag_inicio}-{pag_fim_atual} → {pag_inicio}-{pag_fim_nova} ({motivo})")
                ata['pag_fim'] = pag_fim_nova
                alteracoes.append({
                    'sessao': sessao,
                    'tipo': tipo,
                    'dcl': dcl_name,
                    'antes': pag_fim_atual,
                    'depois': pag_fim_nova,
                    'motivo': motivo
                })
            else:
                print(f"   ✅ Sessão {sessao} ({tipo:15s}): {pag_inicio}-{pag_fim_nova} ({motivo})")
        
        doc.close()
    except Exception as e:
        print(f"   ❌ Erro ao processar: {e}")

# Salvar JSON atualizado
print("\n" + "=" * 80)
print(f"💾 Salvando arquivo JSON...")
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(atas, f, ensure_ascii=False, indent=2)

print(f"✅ Arquivo salvo: {json_path}")
print(f"✅ Total de alterações: {len(alteracoes)}")

