#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FILTRAR - Apenas atas de 2007
=============================

Objetivo: Manter apenas as 117 atas circunstanciadas de 2007

Uso:
    python filtrar_atas_2007.py

Autor: Sistema de Automação CLDF
Data: 2025-12-22
"""

import json
from pathlib import Path

# ======================================================================
# CONFIGURAÇÕES
# ======================================================================

USUARIO = "omega"
ARQUIVO_JSON_ENTRADA = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_final_117_corrigido.json")
ARQUIVO_JSON_SAIDA = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_117.json")
ARQUIVO_TXT_SAIDA = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_117.txt")

# ======================================================================
# FUNÇÕES PRINCIPAIS
# ======================================================================

def main():
    """Função principal"""
    print("\n" + "="*70)
    print("FILTRAR - Apenas atas de 2007")
    print("="*70)
    
    # Carregar JSON
    with open(ARQUIVO_JSON_ENTRADA, 'r', encoding='utf-8') as f:
        atas = json.load(f)
    
    print(f"\nTotal de atas antes: {len(atas)}")
    
    # Filtrar apenas atas de 2007
    atas_2007 = []
    atas_removidas = []
    
    for ata in atas:
        ano = ata['nomenclatura'].split('-')[0]
        
        if ano == '2007':
            atas_2007.append(ata)
        else:
            atas_removidas.append(ata)
    
    print(f"Atas removidas (não 2007): {len(atas_removidas)}")
    print(f"Total após filtrar: {len(atas_2007)}")
    
    # Mostrar atas removidas
    if atas_removidas:
        print(f"\n📋 ATAS REMOVIDAS (não 2007):")
        print("="*70)
        for ata in atas_removidas:
            ano = ata['nomenclatura'].split('-')[0]
            print(f"  {ano}: {ata['sessao_num']}ª {ata['tipo_sessao']} - {ata['dcl_original']}")
    
    # Salvar JSON filtrado
    with open(ARQUIVO_JSON_SAIDA, 'w', encoding='utf-8') as f:
        json.dump(atas_2007, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ JSON salvo em: {ARQUIVO_JSON_SAIDA}")
    
    # Salvar TXT formatado
    with open(ARQUIVO_TXT_SAIDA, 'w', encoding='utf-8') as f:
        f.write("FASE 2 - ATAS CIRCUNSTANCIADAS DE 2007 (117 ATAS)\n")
        f.write("="*70 + "\n\n")
        
        f.write(f"Total de atas encontradas: {len(atas_2007)}\n\n")
        
        f.write("Nome da Sessão,Tipo de Ata,Data da Sessão,Pág. Inicial,Pág. Final,Nomenclatura Padrão\n")
        
        for ata in atas_2007:
            tipo_sessao = ata['tipo_sessao']
            data = ata['data_real']
            pag_ini = ata['pag_inicio']
            pag_fim = ata['pag_fim']
            nomenclatura = ata['nomenclatura']
            sessao_num = ata['sessao_num']
            
            f.write(f"{sessao_num}ª {tipo_sessao},Circunstanciada,{data},{pag_ini},{pag_fim},{nomenclatura}\n")
    
    print(f"✅ TXT salvo em: {ARQUIVO_TXT_SAIDA}")
    
    print(f"\n✅ FILTRAGEM CONCLUÍDA!")

if __name__ == "__main__":
    main()

