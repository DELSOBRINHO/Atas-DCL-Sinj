#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analisar DCLs v2 - Encontrar página REAL de encerramento de cada sessão.
REGRA: A página final é onde aparece o marcador de encerramento, não a anterior.
"""

import json
import os
import re
import fitz  # PyMuPDF

# Marcadores de fim de sessão EXPANDIDOS
MARCADORES_FIM_SESSAO = [
    # Padrão principal
    r'[Ee]st[aá]\s+encerrada\s+a\s+(?:presente\s+)?sess[aã]o',
    r'[Ee]ncerrou[-\s]se\s+a\s+sess[aã]o',
    r'[Dd]eclaro\s+encerrad[ao]\s+a\s+sess[aã]o',
    r'[Ee]ncerro\s+a\s+sess[aã]o',
    r'[Ee]ncerrada\s+a\s+sess[aã]o',
    r'[Ss]ess[aã]o\s+encerrada',
    # Variações
    r'[Nn]ada\s+mais\s+havendo\s+a\s+tratar.*encerrad',
    r'[Ee]ncerramento\s+da\s+sess[aã]o',
    r'[Ff]inaliz(?:o|ada)\s+a\s+sess[aã]o',
    r'[Ll]evanta[-\s]se\s+a\s+sess[aã]o',
    # Casos especiais
    r'vai\s+encerrar?\s+os\s+trabalhos',
    r'encerro\s+(?:os\s+)?trabalhos',
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

print("=" * 80)
print("ANALISANDO DCLs PARA ENCONTRAR FIM REAL DE CADA SESSÃO")
print("=" * 80)

alteracoes = []

for dcl_name, atas_dcl in atas_por_dcl.items():
    atas_dcl.sort(key=lambda x: int(x['pag_inicio']))
    
    pdf_path = os.path.join(downloads_dir, dcl_name)
    
    if not os.path.exists(pdf_path):
        continue
    
    print(f"\n📄 DCL: {dcl_name}")
    
    try:
        doc = fitz.open(pdf_path)
        total_paginas = doc.page_count
        
        for i, ata in enumerate(atas_dcl):
            sessao = str(ata['sessao_num']).zfill(3)
            tipo = ata['tipo_sessao']
            pag_inicio = int(ata['pag_inicio'])
            pag_fim_atual = int(ata['pag_fim'])
            
            # Determinar limite máximo de busca
            if i < len(atas_dcl) - 1:
                proxima_ata = atas_dcl[i + 1]
                pag_limite = int(proxima_ata['pag_inicio'])
            else:
                pag_limite = total_paginas + 1
            
            # Procurar fim da sessão - VARRER TODAS AS PÁGINAS até o limite
            pag_fim_encontrado = None
            
            for pag_num in range(pag_inicio - 1, min(pag_limite, total_paginas)):
                page = doc[pag_num]
                texto = page.get_text()
                
                # Verificar TODOS os marcadores de fim de sessão
                for marcador in MARCADORES_FIM_SESSAO:
                    if re.search(marcador, texto, re.IGNORECASE):
                        # A página onde encontramos o marcador É a página final
                        pag_fim_encontrado = pag_num + 1  # 1-based
                        break
                
                # NÃO parar ao primeiro marcador encontrado - continuar até última página com marcador
                # (não usamos break aqui para pegar a última ocorrência)
            
            # Determinar página final
            if pag_fim_encontrado:
                pag_fim_nova = pag_fim_encontrado
                motivo = "Marcador de encerramento"
            elif i < len(atas_dcl) - 1:
                pag_fim_nova = pag_limite - 1
                motivo = "Antes da próxima ata"
            else:
                pag_fim_nova = total_paginas
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
        print(f"   ❌ Erro: {e}")

print("\n" + "=" * 80)
print(f"💾 Salvando arquivo JSON...")
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(atas, f, ensure_ascii=False, indent=2)

print(f"✅ Arquivo salvo: {json_path}")
print(f"✅ Total de alterações: {len(alteracoes)}")

