#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GERAR ANÁLISE DETALHADA - Validação Manual
"""

import json
from pathlib import Path

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")
ARQUIVO_ANALISE = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/ANALISE_DETALHADA_VALIDACAO.txt")

def main():
    print("\n" + "="*70)
    print("GERAR ANÁLISE DETALHADA")
    print("="*70)
    
    with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
        atas = json.load(f)
    
    print(f"\nTotal de atas: {len(atas)}")
    
    with open(ARQUIVO_ANALISE, 'w', encoding='utf-8') as f:
        f.write("ANÁLISE DETALHADA - VALIDAÇÃO MANUAL DAS 106 ATAS\n")
        f.write("="*70 + "\n\n")
        
        f.write("RESUMO EXECUTIVO\n")
        f.write("="*70 + "\n\n")
        f.write(f"Total de atas: {len(atas)}\n")
        f.write(f"Ordinária: {len([a for a in atas if 'ORDINÁRIA' in a['tipo_sessao']])}\n")
        f.write(f"Extraordinária: {len([a for a in atas if 'EXTRAORDINÁRIA' in a['tipo_sessao']])}\n\n")
        
        f.write("ATAS COM NOMENCLATURA ANÔMALA (0-XX):\n")
        f.write("="*70 + "\n\n")
        
        anomalas = [ata for ata in atas if '-0-XX-' in ata['nomenclatura']]
        if anomalas:
            for ata in anomalas:
                f.write(f"{ata['sessao_num']}ª {ata['tipo_sessao']} - {ata['data_real']}\n")
                f.write(f"  DCL: {ata['dcl_original']}\n")
                f.write(f"  Nomenclatura: {ata['nomenclatura']}\n\n")
        else:
            f.write("✅ Nenhuma ata com nomenclatura anômala\n\n")
        
        f.write("ATAS COM ENCODING DIFERENTE (EXTRAORDINARIA):\n")
        f.write("="*70 + "\n\n")
        
        encoding_diff = [ata for ata in atas if 'EXTRAORDINARIA' in ata['tipo_sessao']]
        if encoding_diff:
            for ata in encoding_diff:
                f.write(f"{ata['sessao_num']}ª {ata['tipo_sessao']} - {ata['data_real']}\n")
                f.write(f"  DCL: {ata['dcl_original']}\n\n")
        else:
            f.write("✅ Nenhuma ata com encoding diferente\n\n")
        
        f.write("ATAS COM PÁGINAS IGUAIS (pag_inicio == pag_fim):\n")
        f.write("="*70 + "\n\n")
        
        pag_iguais = [ata for ata in atas if ata['pag_inicio'] == ata['pag_fim']]
        f.write(f"Total: {len(pag_iguais)} atas\n\n")
        
        for ata in pag_iguais[:15]:
            f.write(f"{ata['sessao_num']}ª {ata['tipo_sessao']} - Página {ata['pag_inicio']}\n")
        
        if len(pag_iguais) > 15:
            f.write(f"... e mais {len(pag_iguais) - 15} atas\n")
        
        f.write("\n\nDISTRIBUIÇÃO POR MÊS:\n")
        f.write("="*70 + "\n\n")
        
        meses_count = {}
        for ata in atas:
            data = ata['data_real']
            if '/' in data:
                mes = data.split('/')[1]
                meses_count[mes] = meses_count.get(mes, 0) + 1
        
        meses_nomes = {
            '01': 'Janeiro', '02': 'Fevereiro', '03': 'Março', '04': 'Abril',
            '05': 'Maio', '06': 'Junho', '07': 'Julho', '08': 'Agosto',
            '09': 'Setembro', '10': 'Outubro', '11': 'Novembro', '12': 'Dezembro'
        }
        
        for mes in sorted(meses_count.keys()):
            count = meses_count[mes]
            pct = (count / len(atas)) * 100
            f.write(f"{meses_nomes.get(mes, mes):12} : {count:3} atas ({pct:5.1f}%)\n")
    
    print(f"\n✅ Análise salva em: {ARQUIVO_ANALISE}")

if __name__ == "__main__":
    main()

