#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GERAR RELATÓRIO HTML - Validação Manual
========================================

Objetivo: Gerar relatório HTML para visualização

Uso:
    python gerar_relatorio_html.py

Autor: Sistema de Automação CLDF
Data: 2025-12-22
"""

import json
from pathlib import Path

# ======================================================================
# CONFIGURAÇÕES
# ======================================================================

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")
ARQUIVO_HTML = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/relatorio_validacao_106_atas.html")

# ======================================================================
# FUNÇÕES PRINCIPAIS
# ======================================================================

def main():
    """Função principal"""
    print("\n" + "="*70)
    print("GERAR RELATÓRIO HTML")
    print("="*70)
    
    # Carregar JSON
    with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
        atas = json.load(f)
    
    print(f"\nTotal de atas: {len(atas)}")
    
    # Gerar HTML
    html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Validação - 106 Atas Circunstanciadas</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #007bff;
            padding-bottom: 10px;
        }
        h2 {
            color: #555;
            margin-top: 30px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th {
            background-color: #007bff;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }
        td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
        tr:hover {
            background-color: #f9f9f9;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin: 20px 0;
        }
        .stat-box {
            background-color: #f0f0f0;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }
        .stat-box h3 {
            margin: 0;
            color: #007bff;
        }
        .stat-box p {
            margin: 10px 0 0 0;
            font-size: 24px;
            font-weight: bold;
        }
        .ordinaria { background-color: #e8f4f8; }
        .extraordinaria { background-color: #fff3cd; }
        .footer {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📋 Relatório de Validação - 106 Atas Circunstanciadas de 2007</h1>
        
        <div class="stats">
            <div class="stat-box">
                <h3>Total de Atas</h3>
                <p>106</p>
            </div>
            <div class="stat-box">
                <h3>Ordinária</h3>
                <p>83</p>
            </div>
            <div class="stat-box">
                <h3>Extraordinária</h3>
                <p>23</p>
            </div>
        </div>
        
        <h2>📊 Distribuição por Mês</h2>
        <table>
            <tr>
                <th>Mês</th>
                <th>Quantidade</th>
                <th>Percentual</th>
            </tr>
"""
    
    # Contar por mês
    meses_count = {}
    meses_nomes = {
        '01': 'Janeiro', '02': 'Fevereiro', '03': 'Março', '04': 'Abril',
        '05': 'Maio', '06': 'Junho', '07': 'Julho', '08': 'Agosto',
        '09': 'Setembro', '10': 'Outubro', '11': 'Novembro', '12': 'Dezembro'
    }
    
    for ata in atas:
        data = ata['data_real']
        if '/' in data:
            mes = data.split('/')[1]
            meses_count[mes] = meses_count.get(mes, 0) + 1
    
    for mes in sorted(meses_count.keys()):
        count = meses_count[mes]
        pct = (count / len(atas)) * 100
        html += f"""            <tr>
                <td>{meses_nomes.get(mes, mes)}</td>
                <td>{count}</td>
                <td>{pct:.1f}%</td>
            </tr>
"""
    
    html += """        </table>
        
        <h2>📋 Lista Completa de Atas</h2>
        <table>
            <tr>
                <th>Nº</th>
                <th>Sessão</th>
                <th>Data</th>
                <th>Pág. Inicial</th>
                <th>Pág. Final</th>
                <th>DCL Original</th>
                <th>Nomenclatura</th>
            </tr>
"""
    
    for idx, ata in enumerate(atas, 1):
        tipo_class = 'ordinaria' if 'ORDINÁRIA' in ata['tipo_sessao'] else 'extraordinaria'
        html += f"""            <tr class="{tipo_class}">
                <td>{idx}</td>
                <td>{ata['sessao_num']}ª {ata['tipo_sessao']}</td>
                <td>{ata['data_real']}</td>
                <td>{ata['pag_inicio']}</td>
                <td>{ata['pag_fim']}</td>
                <td>{ata['dcl_original']}</td>
                <td><code>{ata['nomenclatura']}</code></td>
            </tr>
"""
    
    html += """        </table>
        
        <div class="footer">
            <p>Relatório gerado automaticamente em 2025-12-22</p>
            <p>Fase 2 - Extração e Enriquecimento de Metadados</p>
        </div>
    </div>
</body>
</html>
"""
    
    # Salvar HTML
    with open(ARQUIVO_HTML, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✅ HTML salvo em: {ARQUIVO_HTML}")
    print(f"\n✅ RELATÓRIO HTML GERADO COM SUCESSO!")

if __name__ == "__main__":
    main()

