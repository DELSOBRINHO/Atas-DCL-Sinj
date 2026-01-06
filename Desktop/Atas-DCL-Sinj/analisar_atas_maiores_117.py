#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANALISAR - Atas com número > 117
================================

Objetivo: Analisar atas com número > 117 para corrigir OCR

Uso:
    python analisar_atas_maiores_117.py

Autor: Sistema de Automação CLDF
Data: 2025-12-22
"""

import json
from pathlib import Path

# ======================================================================
# CONFIGURAÇÕES
# ======================================================================

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_corrigidas_117.json")

# ======================================================================
# FUNÇÕES PRINCIPAIS
# ======================================================================

def main():
    """Função principal"""
    print("\n" + "="*70)
    print("ANALISAR - Atas com número > 117")
    print("="*70)
    
    # Carregar JSON
    with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
        atas = json.load(f)
    
    # Procurar por atas com número > 117
    maiores_117 = [ata for ata in atas if int(ata['sessao_num']) > 117]
    
    print(f"\nTotal de atas com número > 117: {len(maiores_117)}\n")
    
    print("📋 ATAS COM NÚMERO > 117:")
    print("="*70)
    
    for ata in sorted(maiores_117, key=lambda x: int(x['sessao_num'])):
        sessao_num = int(ata['sessao_num'])
        tipo_sessao = ata['tipo_sessao']
        data = ata['data_real']
        dcl = ata['dcl_original']
        ano = ata['nomenclatura'].split('-')[0]
        
        # Tentar corrigir o número
        # Exemplos: 223 -> 23, 278 -> 78, 303 -> 03, 393 -> 93, etc.
        possibilidades = []
        
        # Remover primeiro dígito
        if sessao_num >= 100:
            possibilidades.append(sessao_num % 100)
        
        # Remover último dígito
        possibilidades.append(sessao_num // 10)
        
        # Remover primeiro e último dígito
        if sessao_num >= 100:
            possibilidades.append((sessao_num % 100) // 10)
        
        print(f"\n{sessao_num}ª {tipo_sessao}")
        print(f"  Data: {data}")
        print(f"  Ano: {ano}")
        print(f"  DCL: {dcl}")
        print(f"  Possíveis correções: {sorted(set(possibilidades))}")

if __name__ == "__main__":
    main()

