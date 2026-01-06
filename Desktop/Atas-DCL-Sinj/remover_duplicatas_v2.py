#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REMOVER DUPLICATAS V2 - Com análise de duplicatas
==================================================

Objetivo: Remover duplicatas mantendo apenas uma por nomenclatura

Uso:
    python remover_duplicatas_v2.py

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
ARQUIVO_JSON_ENTRADA = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_corrigidas_v2.json")
ARQUIVO_JSON_SAIDA = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_final_v2.json")
ARQUIVO_TXT_SAIDA = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_final_v2.txt")

# ======================================================================
# FUNÇÕES PRINCIPAIS
# ======================================================================

def main():
    """Função principal"""
    print("\n" + "="*70)
    print("REMOVER DUPLICATAS V2")
    print("="*70)
    
    # Carregar JSON
    with open(ARQUIVO_JSON_ENTRADA, 'r', encoding='utf-8') as f:
        atas = json.load(f)
    
    print(f"\nTotal de atas antes: {len(atas)}")
    
    # Agrupar por nomenclatura
    por_nomenclatura = defaultdict(list)
    for ata in atas:
        por_nomenclatura[ata['nomenclatura']].append(ata)
    
    # Remover duplicatas
    atas_finais = []
    duplicatas = []
    
    for nomenclatura, grupo in por_nomenclatura.items():
        if len(grupo) > 1:
            # Manter a primeira, remover as outras
            atas_finais.append(grupo[0])
            duplicatas.extend(grupo[1:])
        else:
            atas_finais.append(grupo[0])
    
    print(f"Duplicatas removidas: {len(duplicatas)}")
    print(f"Total após remover duplicatas: {len(atas_finais)}")
    
    # Mostrar duplicatas
    if duplicatas:
        print(f"\n📋 DUPLICATAS REMOVIDAS:")
        print("="*70)
        for ata in duplicatas:
            print(f"  {ata['sessao_num']}ª {ata['tipo_sessao']} - {ata['data_real']} - {ata['dcl_original']}")
    
    # Salvar JSON final
    with open(ARQUIVO_JSON_SAIDA, 'w', encoding='utf-8') as f:
        json.dump(atas_finais, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ JSON salvo em: {ARQUIVO_JSON_SAIDA}")
    
    # Salvar TXT formatado
    with open(ARQUIVO_TXT_SAIDA, 'w', encoding='utf-8') as f:
        f.write("FASE 2 - ATAS CIRCUNSTANCIADAS FINAL V2\n")
        f.write("="*70 + "\n\n")
        
        f.write(f"Total de atas encontradas: {len(atas_finais)}\n\n")
        
        f.write("Nome da Sessão,Tipo de Ata,Data da Sessão,Pág. Inicial,Pág. Final,Nomenclatura Padrão\n")
        
        for ata in atas_finais:
            tipo_sessao = ata['tipo_sessao']
            data = ata['data_real']
            pag_ini = ata['pag_inicio']
            pag_fim = ata['pag_fim']
            nomenclatura = ata['nomenclatura']
            sessao_num = ata['sessao_num']
            
            f.write(f"{sessao_num}ª {tipo_sessao},Circunstanciada,{data},{pag_ini},{pag_fim},{nomenclatura}\n")
    
    print(f"✅ TXT salvo em: {ARQUIVO_TXT_SAIDA}")
    
    print(f"\n✅ REMOÇÃO DE DUPLICATAS CONCLUÍDA!")

if __name__ == "__main__":
    main()

