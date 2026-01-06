#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GERAR RELATÓRIO - Validação Manual
===================================

Objetivo: Gerar relatório Excel para validação manual das 106 atas

Uso:
    python gerar_relatorio_validacao.py

Autor: Sistema de Automação CLDF
Data: 2025-12-22
"""

import json
from pathlib import Path
import pandas as pd

# ======================================================================
# CONFIGURAÇÕES
# ======================================================================

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")
ARQUIVO_EXCEL = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/relatorio_validacao_106_atas.xlsx")
ARQUIVO_CSV = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/relatorio_validacao_106_atas.csv")

# ======================================================================
# FUNÇÕES PRINCIPAIS
# ======================================================================

def main():
    """Função principal"""
    print("\n" + "="*70)
    print("GERAR RELATÓRIO - Validação Manual")
    print("="*70)
    
    # Carregar JSON
    with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
        atas = json.load(f)
    
    print(f"\nTotal de atas: {len(atas)}")
    
    # Preparar dados para DataFrame
    dados = []
    for idx, ata in enumerate(atas, 1):
        dados.append({
            'Nº': idx,
            'Sessão': f"{ata['sessao_num']}ª {ata['tipo_sessao']}",
            'Tipo Sessão': ata['tipo_sessao'],
            'Data': ata['data_real'],
            'Pág. Inicial': ata['pag_inicio'],
            'Pág. Final': ata['pag_fim'],
            'DCL Original': ata['dcl_original'],
            'Nomenclatura': ata['nomenclatura'],
            'Validado': '',
            'Observações': ''
        })
    
    # Criar DataFrame
    df = pd.DataFrame(dados)
    
    # Converter para string com encoding correto
    df = df.astype(str)

    # Salvar Excel
    with pd.ExcelWriter(ARQUIVO_EXCEL, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Atas', index=False)
        
        # Formatar Excel
        workbook = writer.book
        worksheet = writer.sheets['Atas']
        
        # Ajustar largura das colunas
        worksheet.column_dimensions['A'].width = 5
        worksheet.column_dimensions['B'].width = 25
        worksheet.column_dimensions['C'].width = 18
        worksheet.column_dimensions['D'].width = 12
        worksheet.column_dimensions['E'].width = 12
        worksheet.column_dimensions['F'].width = 12
        worksheet.column_dimensions['G'].width = 30
        worksheet.column_dimensions['H'].width = 35
        worksheet.column_dimensions['I'].width = 12
        worksheet.column_dimensions['J'].width = 30
        
        # Congelar primeira linha
        worksheet.freeze_panes = 'A2'
    
    print(f"\n✅ Excel salvo em: {ARQUIVO_EXCEL}")
    
    # Gerar estatísticas
    print(f"\n📊 ESTATÍSTICAS:")
    print("="*70)
    
    por_tipo = df['Tipo Sessão'].value_counts()
    print(f"\nPor tipo de sessão:")
    for tipo, count in por_tipo.items():
        print(f"  {tipo}: {count}")
    
    por_mes = df['Data'].str.extract(r'(\d+)/(\d+)/')[1].value_counts().sort_index()
    print(f"\nPor mês:")
    meses = {
        '01': 'Janeiro', '02': 'Fevereiro', '03': 'Março', '04': 'Abril',
        '05': 'Maio', '06': 'Junho', '07': 'Julho', '08': 'Agosto',
        '09': 'Setembro', '10': 'Outubro', '11': 'Novembro', '12': 'Dezembro'
    }
    for mes, count in por_mes.items():
        print(f"  {meses.get(mes, mes)}: {count}")
    
    print(f"\n✅ RELATÓRIO GERADO COM SUCESSO!")

if __name__ == "__main__":
    main()

