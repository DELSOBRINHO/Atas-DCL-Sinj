#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORRIGIR - Atas com tipo de sessão inválido
============================================

Objetivo: Corrigir atas com tipo de sessão 0-XX

Uso:
    python corrigir_atas_invalidas.py

Autor: Sistema de Automação CLDF
Data: 2025-12-22
"""

import json
from pathlib import Path

# ======================================================================
# CONFIGURAÇÕES
# ======================================================================

USUARIO = "omega"
ARQUIVO_JSON_ENTRADA = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_final_117.json")
ARQUIVO_JSON_SAIDA = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_final_117_corrigido.json")
ARQUIVO_TXT_SAIDA = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_final_117_corrigido.txt")

# Mapeamento de tipos de sessão
MAPA_SESSAO = {
    "ORDINÁRIA": ("1", "SO"),
    "EXTRAORDINÁRIA": ("2", "SE"),
    "SOLENE": ("3", "SS"),
    "PREPARATÓRIA": ("4", "SP"),
    "ESPECIAL": ("5", "SE")
}

# ======================================================================
# FUNÇÕES PRINCIPAIS
# ======================================================================

def main():
    """Função principal"""
    print("\n" + "="*70)
    print("CORRIGIR - Atas com tipo de sessão inválido")
    print("="*70)
    
    # Carregar JSON
    with open(ARQUIVO_JSON_ENTRADA, 'r', encoding='utf-8') as f:
        atas = json.load(f)
    
    print(f"\nTotal de atas antes: {len(atas)}")
    
    # Corrigir atas com tipo de sessão inválido
    corrigidas = 0
    for ata in atas:
        if "-0-XX-" in ata['nomenclatura']:
            # Obter o tipo de sessão correto
            tipo_sessao = ata['tipo_sessao']
            c_sessao, s_sessao = MAPA_SESSAO.get(tipo_sessao, ("0", "XX"))
            
            # Corrigir a nomenclatura
            nomenclatura_antiga = ata['nomenclatura']
            ata['nomenclatura'] = ata['nomenclatura'].replace("-0-XX-", f"-{c_sessao}-{s_sessao}-")
            
            print(f"\n🔧 Corrigindo ata {ata['sessao_num']}ª {tipo_sessao}")
            print(f"   De: {nomenclatura_antiga}")
            print(f"   Para: {ata['nomenclatura']}")
            
            corrigidas += 1
    
    print(f"\n📊 RESUMO:")
    print("="*70)
    print(f"   Total de atas: {len(atas)}")
    print(f"   Atas corrigidas: {corrigidas}")
    
    # Salvar JSON corrigido
    with open(ARQUIVO_JSON_SAIDA, 'w', encoding='utf-8') as f:
        json.dump(atas, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ JSON salvo em: {ARQUIVO_JSON_SAIDA}")
    
    # Salvar TXT formatado
    with open(ARQUIVO_TXT_SAIDA, 'w', encoding='utf-8') as f:
        f.write("FASE 2 - ATAS CIRCUNSTANCIADAS FINAL (117 ATAS)\n")
        f.write("="*70 + "\n\n")
        
        f.write(f"Total de atas encontradas: {len(atas)}\n\n")
        
        f.write("Nome da Sessão,Tipo de Ata,Data da Sessão,Pág. Inicial,Pág. Final,Nomenclatura Padrão\n")
        
        for ata in atas:
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

