#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANÁLISE - 124 atas vs 117 esperadas
===================================

Objetivo: Entender por que temos 124 atas em vez de 117

Uso:
    python analise_124_atas.py

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
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_final_117_corrigido.json")

# ======================================================================
# FUNÇÕES PRINCIPAIS
# ======================================================================

def main():
    """Função principal"""
    print("\n" + "="*70)
    print("ANÁLISE - 124 atas vs 117 esperadas")
    print("="*70)
    
    # Carregar JSON
    with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
        atas = json.load(f)
    
    print(f"\nTotal de atas: {len(atas)}\n")
    
    # Agrupar por ano
    por_ano = defaultdict(list)
    for ata in atas:
        ano = ata['nomenclatura'].split('-')[0]
        por_ano[ano].append(ata)
    
    print("📊 DISTRIBUIÇÃO POR ANO:")
    print("="*70)
    
    for ano in sorted(por_ano.keys()):
        print(f"\n{ano}: {len(por_ano[ano])} atas")
        
        # Agrupar por tipo de sessão
        por_tipo = defaultdict(int)
        for ata in por_ano[ano]:
            por_tipo[ata['tipo_sessao']] += 1
        
        for tipo in sorted(por_tipo.keys()):
            print(f"  {tipo}: {por_tipo[tipo]}")
    
    # Procurar por atas sem data
    print(f"\n📋 ATAS SEM DATA:")
    print("="*70)
    
    sem_data = [ata for ata in atas if ata['data_real'] == 'SEM DATA']
    print(f"\nTotal: {len(sem_data)}\n")
    
    for ata in sem_data:
        print(f"  {ata['sessao_num']}ª {ata['tipo_sessao']} - {ata['dcl_original']}")
    
    # Procurar por atas com data 2006-01-01 (data padrão)
    print(f"\n📋 ATAS COM DATA PADRÃO (2006-01-01):")
    print("="*70)
    
    data_padrao = [ata for ata in atas if ata['nomenclatura'].startswith('2006-01-01')]
    print(f"\nTotal: {len(data_padrao)}\n")
    
    for ata in data_padrao:
        print(f"  {ata['sessao_num']}ª {ata['tipo_sessao']} - {ata['dcl_original']}")

if __name__ == "__main__":
    main()

