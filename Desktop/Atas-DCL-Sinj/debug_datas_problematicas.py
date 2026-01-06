#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEBUG - Analisar datas com problemas
====================================

Objetivo: Identificar atas com datas problemáticas (mês 00)

Uso:
    python debug_datas_problematicas.py

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
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_todas_atas_346_dcls.json")

# ======================================================================
# FUNÇÕES PRINCIPAIS
# ======================================================================

def main():
    """Função principal"""
    print("\n" + "="*70)
    print("DEBUG - Analisar datas com problemas")
    print("="*70)
    
    # Carregar JSON
    with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
        atas = json.load(f)
    
    print(f"\nTotal de atas: {len(atas)}\n")
    
    # Analisar datas problemáticas
    print("📋 ATAS COM DATAS PROBLEMÁTICAS (mês 00):")
    print("="*70)
    
    datas_problematicas = []
    for ata in atas:
        if "-00-" in ata['nomenclatura']:
            datas_problematicas.append(ata)
    
    print(f"\nTotal com mês 00: {len(datas_problematicas)}\n")
    
    for ata in datas_problematicas:
        print(f"DCL: {ata['dcl_original']}")
        print(f"  Sessão: {ata['sessao_num']}ª {ata['tipo_sessao']}")
        print(f"  Data extraída: {ata['data_real']}")
        print(f"  Nomenclatura: {ata['nomenclatura']}")
        print()
    
    # Analisar números de sessão > 117
    print("\n📋 ATAS COM NÚMERO DE SESSÃO > 117:")
    print("="*70)
    
    sessoes_altas = []
    for ata in atas:
        try:
            num_sessao = int(ata['sessao_num'])
            if num_sessao > 117:
                sessoes_altas.append(ata)
        except:
            pass
    
    print(f"\nTotal com número > 117: {len(sessoes_altas)}\n")
    
    for ata in sessoes_altas[:20]:  # Mostrar apenas os 20 primeiros
        print(f"DCL: {ata['dcl_original']}")
        print(f"  Sessão: {ata['sessao_num']}ª {ata['tipo_sessao']}")
        print(f"  Data: {ata['data_real']}")
        print(f"  Nomenclatura: {ata['nomenclatura']}")
        print()
    
    if len(sessoes_altas) > 20:
        print(f"... e mais {len(sessoes_altas) - 20} atas com número > 117")
    
    # Agrupar por tipo de sessão
    print("\n📊 DISTRIBUIÇÃO POR TIPO DE SESSÃO:")
    print("="*70)
    
    por_tipo = defaultdict(int)
    for ata in atas:
        por_tipo[ata['tipo_sessao']] += 1
    
    for tipo in sorted(por_tipo.keys()):
        print(f"  {tipo}: {por_tipo[tipo]} atas")
    
    # Agrupar por ano
    print("\n📊 DISTRIBUIÇÃO POR ANO:")
    print("="*70)
    
    por_ano = defaultdict(int)
    for ata in atas:
        ano = ata['nomenclatura'].split('-')[0]
        por_ano[ano] += 1
    
    for ano in sorted(por_ano.keys()):
        print(f"  {ano}: {por_ano[ano]} atas")

if __name__ == "__main__":
    main()

