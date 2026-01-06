#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMPARAR ATAS - Identificar Faltantes
======================================

Objetivo: Comparar atas circunstanciadas extraídas com lista de atas sucintas

Uso:
    python comparar_atas_faltantes.py

Autor: Sistema de Automação CLDF
Data: 2025-12-22
"""

import json
import pandas as pd
from pathlib import Path
import re

USUARIO = "omega"
ARQUIVO_CIRCUNSTANCIADAS = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")
ARQUIVO_SUCINTAS = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/relatorio_links_diretos_2007_2025.xlsx - Links_Diretos - relatorio_links_diretos_2007_2025.xlsx - Links_Diretos (1).csv")
ARQUIVO_SAIDA = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/ATAS_FALTANTES.txt")

def extrair_numero_sessao(texto):
    """Extrai número da sessão de texto como '1ª Sessão Extraordinária'"""
    match = re.search(r'(\d+)ª', str(texto))
    if match:
        return int(match.group(1))
    return None

def main():
    print("\n" + "="*70)
    print("COMPARAR ATAS - Identificar Faltantes")
    print("="*70)

    # Carregar atas circunstanciadas
    with open(ARQUIVO_CIRCUNSTANCIADAS, 'r', encoding='utf-8') as f:
        circunstanciadas = json.load(f)

    print(f"\nAtas circunstanciadas extraídas: {len(circunstanciadas)}")

    # Extrair números de sessão das circunstanciadas
    numeros_circunstanciadas = set()
    for ata in circunstanciadas:
        num = int(ata['sessao_num'])
        numeros_circunstanciadas.add(num)

    print(f"Números únicos: {len(numeros_circunstanciadas)}")
    print(f"Números: {sorted(numeros_circunstanciadas)}")

    # Carregar atas sucintas
    try:
        df_sucintas = pd.read_csv(ARQUIVO_SUCINTAS, encoding='utf-8')
    except:
        try:
            df_sucintas = pd.read_csv(ARQUIVO_SUCINTAS, encoding='latin-1')
        except:
            df_sucintas = pd.read_csv(ARQUIVO_SUCINTAS, encoding='cp1252')

    print(f"\nAtas sucintas no arquivo: {len(df_sucintas)}")
    print(f"Colunas: {list(df_sucintas.columns)}")

    # Procurar coluna com número da sessão (coluna "Sessão")
    col_sessao = 'Sessão' if 'Sessão' in df_sucintas.columns else df_sucintas.columns[1]

    print(f"Coluna de sessão: {col_sessao}")

    # Extrair números de sessão das sucintas
    numeros_sucintas = set()
    for val in df_sucintas[col_sessao]:
        num = extrair_numero_sessao(val)
        if num:
            numeros_sucintas.add(num)

    print(f"Números únicos em sucintas: {len(numeros_sucintas)}")
    print(f"Números: {sorted(numeros_sucintas)}")

    # Encontrar faltantes
    faltantes = sorted(numeros_sucintas - numeros_circunstanciadas)

    print(f"\n✅ ATAS FALTANTES: {len(faltantes)}")
    if faltantes:
        print(f"Números: {faltantes}")

    # Salvar relatório
    with open(ARQUIVO_SAIDA, 'w', encoding='utf-8') as f:
        f.write("ATAS CIRCUNSTANCIADAS FALTANTES\n")
        f.write("="*70 + "\n\n")

        f.write(f"Total de atas sucintas: {len(numeros_sucintas)}\n")
        f.write(f"Total de atas circunstanciadas extraídas: {len(numeros_circunstanciadas)}\n")
        f.write(f"Total de atas faltantes: {len(faltantes)}\n\n")

        if faltantes:
            f.write("ATAS FALTANTES:\n")
            f.write("="*70 + "\n\n")

            for num in faltantes:
                f.write(f"{num}ª\n")
        else:
            f.write("✅ NENHUMA ATA FALTANTE!\n\n")

        f.write("\n\nATAS ENCONTRADAS:\n")
        f.write("="*70 + "\n\n")

        for num in sorted(numeros_circunstanciadas):
            f.write(f"{num}ª\n")

    print(f"\n✅ Relatório salvo em: {ARQUIVO_SAIDA}")

if __name__ == "__main__":
    main()

