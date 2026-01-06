#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORRIGIR - Atas com número > 117
================================

Objetivo: Corrigir números de sessão lidos incorretamente pelo OCR

Uso:
    python corrigir_atas_maiores_117.py

Autor: Sistema de Automação CLDF
Data: 2025-12-22
"""

import json
from pathlib import Path
from collections import defaultdict

# ======================================================================
# CONFIGURAÇÕES
# ======================================================================

USUARIO = "omega"
ARQUIVO_JSON_ENTRADA = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_todas_atas_346_dcls.json")
ARQUIVO_JSON_SAIDA = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_corrigidas_v2.json")
ARQUIVO_TXT_SAIDA = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_corrigidas_v2.txt")

# Mapeamento de correções
CORRECOES = {
    208: 8,      # 208 -> 08
    223: 23,     # 223 -> 23
    258: 25,     # 258 -> 25
    278: 27,     # 278 -> 27
    303: 3,      # 303 -> 03
    318: 18,     # 318 -> 18
    328: 28,     # 328 -> 28
    393: 93,     # 393 -> 93
    413: 13,     # 413 -> 13
    848: 48,     # 848 -> 48
    858: 58,     # 858 -> 58
    868: 68,     # 868 -> 68
    888: 88,     # 888 -> 88
    1068: 68,    # 1068 -> 68
    1128: 28,    # 1128 -> 28
}

# ======================================================================
# FUNÇÕES PRINCIPAIS
# ======================================================================

def main():
    """Função principal"""
    print("\n" + "="*70)
    print("CORRIGIR - Atas com número > 117")
    print("="*70)
    
    # Carregar JSON
    with open(ARQUIVO_JSON_ENTRADA, 'r', encoding='utf-8') as f:
        atas = json.load(f)
    
    print(f"\nTotal de atas antes: {len(atas)}")
    
    # Corrigir atas
    atas_corrigidas = []
    atas_removidas = []
    
    for ata in atas:
        sessao_num = int(ata['sessao_num'])
        ano = ata['nomenclatura'].split('-')[0]
        
        # Se é 2006 e número > 117, remover
        if ano == '2006' and sessao_num > 117:
            atas_removidas.append(ata)
            continue
        
        # Se tem correção, aplicar
        if sessao_num in CORRECOES:
            novo_num = CORRECOES[sessao_num]
            ata['sessao_num'] = str(novo_num).zfill(3)
            
            # Atualizar nomenclatura
            partes = ata['nomenclatura'].split('-')
            partes[4] = str(novo_num).zfill(3)
            ata['nomenclatura'] = '-'.join(partes)
            
            print(f"\n🔧 Corrigindo: {sessao_num}ª → {novo_num}ª {ata['tipo_sessao']}")
            print(f"   Data: {ata['data_real']}")
            print(f"   Nomenclatura: {ata['nomenclatura']}")
        
        atas_corrigidas.append(ata)
    
    print(f"\n📊 RESUMO:")
    print("="*70)
    print(f"   Total antes: {len(atas)}")
    print(f"   Removidas (2006 > 117): {len(atas_removidas)}")
    print(f"   Total após: {len(atas_corrigidas)}")
    
    # Salvar JSON corrigido
    with open(ARQUIVO_JSON_SAIDA, 'w', encoding='utf-8') as f:
        json.dump(atas_corrigidas, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ JSON salvo em: {ARQUIVO_JSON_SAIDA}")
    
    # Salvar TXT formatado
    with open(ARQUIVO_TXT_SAIDA, 'w', encoding='utf-8') as f:
        f.write("FASE 2 - ATAS CIRCUNSTANCIADAS CORRIGIDAS V2\n")
        f.write("="*70 + "\n\n")
        
        f.write(f"Total de atas encontradas: {len(atas_corrigidas)}\n\n")
        
        f.write("Nome da Sessão,Tipo de Ata,Data da Sessão,Pág. Inicial,Pág. Final,Nomenclatura Padrão\n")
        
        for ata in atas_corrigidas:
            tipo_sessao = ata['tipo_sessao']
            data = ata['data_real']
            pag_ini = ata['pag_inicio']
            pag_fim = ata['pag_fim']
            nomenclatura = ata['nomenclatura']
            sessao_num = ata['sessao_num']
            
            f.write(f"{sessao_num}ª {tipo_sessao},Circunstanciada,{data},{pag_ini},{pag_fim},{nomenclatura}\n")
    
    print(f"✅ TXT salvo em: {ARQUIVO_TXT_SAIDA}")
    
    print(f"\n✅ CORREÇÃO CONCLUÍDA!")

if __name__ == "__main__":
    main()

