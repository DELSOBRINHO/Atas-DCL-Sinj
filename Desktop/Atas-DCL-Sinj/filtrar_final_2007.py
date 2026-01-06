#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FILTRAR FINAL - Apenas 2007 e sem data 00
==========================================

Objetivo: Manter apenas atas de 2007 e remover as com mês 00

Uso:
    python filtrar_final_2007.py

Autor: Sistema de Automação CLDF
Data: 2025-12-22
"""

import json
from pathlib import Path

# ======================================================================
# CONFIGURAÇÕES
# ======================================================================

USUARIO = "omega"
ARQUIVO_JSON_ENTRADA = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_final_v2.json")
ARQUIVO_JSON_SAIDA = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")
ARQUIVO_TXT_SAIDA = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.txt")

# ======================================================================
# FUNÇÕES PRINCIPAIS
# ======================================================================

def main():
    """Função principal"""
    print("\n" + "="*70)
    print("FILTRAR FINAL - Apenas 2007 e sem data 00")
    print("="*70)
    
    # Carregar JSON
    with open(ARQUIVO_JSON_ENTRADA, 'r', encoding='utf-8') as f:
        atas = json.load(f)
    
    print(f"\nTotal de atas antes: {len(atas)}")
    
    # Filtrar
    atas_2007 = []
    atas_removidas = []
    
    for ata in atas:
        ano = ata['nomenclatura'].split('-')[0]
        data = ata['data_real']
        
        # Remover se não é 2007
        if ano != '2007':
            atas_removidas.append((ata, "Não é 2007"))
            continue
        
        # Remover se tem mês 00
        if '/00/' in data:
            atas_removidas.append((ata, "Mês 00"))
            continue
        
        atas_2007.append(ata)
    
    print(f"Atas removidas: {len(atas_removidas)}")
    print(f"Total após filtrar: {len(atas_2007)}")
    
    # Mostrar atas removidas
    if atas_removidas:
        print(f"\n📋 ATAS REMOVIDAS:")
        print("="*70)
        for ata, motivo in atas_removidas:
            print(f"  {ata['sessao_num']}ª {ata['tipo_sessao']} - {ata['data_real']} - {motivo}")
    
    # Salvar JSON final
    with open(ARQUIVO_JSON_SAIDA, 'w', encoding='utf-8') as f:
        json.dump(atas_2007, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ JSON salvo em: {ARQUIVO_JSON_SAIDA}")
    
    # Salvar TXT formatado
    with open(ARQUIVO_TXT_SAIDA, 'w', encoding='utf-8') as f:
        f.write("FASE 2 - ATAS CIRCUNSTANCIADAS DE 2007 FINAL\n")
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
    
    print(f"\n✅ FILTRAGEM FINAL CONCLUÍDA!")

if __name__ == "__main__":
    main()

