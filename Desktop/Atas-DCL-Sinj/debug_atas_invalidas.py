#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEBUG - Atas com tipo de sessão inválido
=========================================

Objetivo: Encontrar atas com tipo de sessão 0-XX

Uso:
    python debug_atas_invalidas.py

Autor: Sistema de Automação CLDF
Data: 2025-12-22
"""

import json
from pathlib import Path

# ======================================================================
# CONFIGURAÇÕES
# ======================================================================

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_final_117.json")

# ======================================================================
# FUNÇÕES PRINCIPAIS
# ======================================================================

def main():
    """Função principal"""
    print("\n" + "="*70)
    print("DEBUG - Atas com tipo de sessão inválido")
    print("="*70)
    
    # Carregar JSON
    with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
        atas = json.load(f)
    
    print(f"\nTotal de atas: {len(atas)}\n")
    
    # Procurar por atas com tipo de sessão inválido
    invalidas = []
    for ata in atas:
        if "-0-XX-" in ata['nomenclatura']:
            invalidas.append(ata)
    
    print(f"📋 ATAS COM TIPO DE SESSÃO INVÁLIDO (0-XX):")
    print("="*70)
    
    print(f"\nTotal: {len(invalidas)}\n")
    
    for ata in invalidas:
        print(f"DCL: {ata['dcl_original']}")
        print(f"  Sessão: {ata['sessao_num']}ª {ata['tipo_sessao']}")
        print(f"  Data: {ata['data_real']}")
        print(f"  Nomenclatura: {ata['nomenclatura']}")
        print()

if __name__ == "__main__":
    main()

