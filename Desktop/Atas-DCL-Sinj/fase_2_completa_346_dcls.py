#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FASE 2 COMPLETA - MAPEAMENTO DE TODAS AS ATAS (346 DCLs)
=========================================================

Objetivo: Processar todos os 346 DCLs e extrair TODAS as atas circunstanciadas
com informações completas (data, tipo, páginas inicial e final).

Uso:
    python fase_2_completa_346_dcls.py

Autor: Sistema de Automação CLDF
Data: 2025-12-22
"""

import os
import re
import json
from pathlib import Path

# ======================================================================
# CONFIGURAÇÕES
# ======================================================================

USUARIO = "omega"
DIR_DOWNLOADS = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/downloads_2007")
ARQUIVO_SAIDA_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_todas_atas_346_dcls.json")
ARQUIVO_SAIDA_TXT = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_todas_atas_346_dcls.txt")

# Mapeamento de meses
MESES_MAP = {
    'JANEIRO': '01', 'FEVEREIRO': '02', 'MARÇO': '03', 'MARCO': '03', 'ABRIL': '04',
    'MAIO': '05', 'JUNHO': '06', 'JULHO': '07', 'AGOSTO': '08', 'SETEMBRO': '09',
    'OUTUBRO': '10', 'NOVEMBRO': '11', 'DEZEMBRO': '12'
}

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

def instalar_dependencias():
    """Instala dependências necessárias"""
    print("📦 Verificando dependências...")
    
    import subprocess
    
    pacotes = {
        "pdfplumber": "pdfplumber",
        "pandas": "pandas"
    }
    
    for modulo, pacote in pacotes.items():
        try:
            __import__(modulo)
            print(f"   ✅ {pacote} já instalado")
        except ImportError:
            print(f"   ⬇️  Instalando {pacote}...")
            subprocess.check_call([__import__('sys').executable, "-m", "pip", "install", pacote, "-q"])
            print(f"   ✅ {pacote} instalado")

def extrair_todas_atas_pdf(nome_arquivo):
    """Extrai TODAS as atas circunstanciadas de um PDF"""
    import pdfplumber
    import pandas as pd
    
    caminho = DIR_DOWNLOADS / nome_arquivo
    lista_atas = []
    
    if not caminho.exists():
        return []
    
    try:
        with pdfplumber.open(caminho) as pdf:
            total_paginas = len(pdf.pages)
            
            # Procurar por "ATA CIRCUNSTANCIADA" em todo o PDF
            for num_p, pagina in enumerate(pdf.pages, 1):
                texto_raw = (pagina.extract_text() or "").upper()
                # Normaliza espaços
                texto = " ".join(texto_raw.split())
                
                # Procura por "ATACIRCUNSTANCIADA"
                for match in re.finditer(r'ATACIRCUNSTANCIADA', texto):
                    idx = match.start()
                    
                    # Procura pelo número DEPOIS de ATACIRCUNSTANCIADA
                    contexto_depois = texto[idx:min(len(texto), idx+500)]
                    match_num = re.search(r'ATACIRCUNSTANCIADA\s*DA\s*(\d+)[ªa°º]?', contexto_depois)
                    
                    if not match_num:
                        continue
                    
                    num_sessao = match_num.group(1).zfill(3)
                    
                    # Procura pelo tipo de sessão DEPOIS de ATACIRCUNSTANCIADA
                    match_tipo = re.search(r'SESS[ÃA]O\s*(ORDIN[ÁA]RIA|EXTRAORDIN[ÁA]RIA|SOLENE|PREPARAT[ÓO]RIA|ESPECIAL)', contexto_depois)
                    
                    if not match_tipo:
                        continue
                    
                    tipo_sessao_txt = match_tipo.group(1)
                    
                    # Procura pela data DEPOIS de ATACIRCUNSTANCIADA
                    match_data = re.search(
                        r'(?:EM|REALIZADA)\s*(\d{1,2})\s*DE\s*(\w+)\s*DE\s*(200\d)',
                        contexto_depois
                    )
                    
                    if match_data:
                        dia, mes_ext, ano = match_data.groups()
                        data_iso = f"{ano}-{MESES_MAP.get(mes_ext, '00')}-{dia.zfill(2)}"
                        data_real = f"{dia}/{MESES_MAP.get(mes_ext, '00')}/{ano}"
                    else:
                        data_iso = "2006-01-01"
                        data_real = "SEM DATA"
                    
                    # Mapeamento de tipo de sessão
                    c_sessao, s_sessao = MAPA_SESSAO.get(tipo_sessao_txt, ("0", "XX"))
                    
                    nome_final = f"{data_iso}-{c_sessao}-{s_sessao}-{num_sessao}-2-AC.pdf"
                    
                    lista_atas.append({
                        "dcl_original": nome_arquivo,
                        "pag_inicio": num_p,
                        "sessao_num": num_sessao,
                        "tipo_sessao": tipo_sessao_txt,
                        "data_real": data_real,
                        "nomenclatura": nome_final
                    })
        
        # --- LÓGICA DE PÁGINA FINAL ---
        if lista_atas:
            df_temp = pd.DataFrame(lista_atas)
            # Remover duplicatas por nomenclatura
            df_temp = df_temp.drop_duplicates(subset=['nomenclatura'], keep='first')
            lista_atas = df_temp.to_dict('records')
            
            for i in range(len(lista_atas)):
                if i < len(lista_atas) - 1:
                    pag_fim_calc = lista_atas[i+1]["pag_inicio"] - 1
                    lista_atas[i]["pag_fim"] = max(lista_atas[i]["pag_inicio"], pag_fim_calc)
                else:
                    lista_atas[i]["pag_fim"] = total_paginas
    
    except Exception as e:
        print(f"❌ Erro em {nome_arquivo}: {e}")
    
    return lista_atas

def main():
    """Função principal"""
    print("\n" + "="*70)
    print("FASE 2 COMPLETA - MAPEAMENTO DE TODAS AS ATAS (346 DCLs)")
    print("="*70)
    
    # Instalar dependências
    instalar_dependencias()
    
    # Listar todos os PDFs
    arquivos = sorted([f for f in os.listdir(DIR_DOWNLOADS) if f.lower().endswith('.pdf')])
    
    print(f"\n✅ {len(arquivos)} DCLs encontrados")
    
    # Processar todos os DCLs
    print(f"\n📊 PROCESSANDO {len(arquivos)} DCLs")
    print("="*70 + "\n")
    
    resultados_teste = []
    
    for i, arquivo in enumerate(arquivos, 1):
        res = extrair_todas_atas_pdf(arquivo)
        resultados_teste.extend(res)
        
        if i % 50 == 0:
            print(f"[{i}/{len(arquivos)}] {arquivo}... ✅ {len(res)} atas")
    
    # Salvar JSON
    print(f"\n💾 SALVANDO RESULTADOS")
    print("="*70)
    
    with open(ARQUIVO_SAIDA_JSON, 'w', encoding='utf-8') as f:
        json.dump(resultados_teste, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON salvo em: {ARQUIVO_SAIDA_JSON}")
    
    # Salvar TXT formatado
    with open(ARQUIVO_SAIDA_TXT, 'w', encoding='utf-8') as f:
        f.write("FASE 2 - MAPEAMENTO COMPLETO DE TODAS AS ATAS (346 DCLs)\n")
        f.write("="*70 + "\n\n")
        
        f.write(f"Total de atas encontradas: {len(resultados_teste)}\n\n")
        
        f.write("Nome da Sessão,Tipo de Ata,Data da Sessão,Pág. Inicial,Pág. Final,Nomenclatura Padrão\n")
        
        for ata in resultados_teste:
            tipo_sessao = ata['tipo_sessao']
            data = ata['data_real']
            pag_ini = ata['pag_inicio']
            pag_fim = ata['pag_fim']
            nomenclatura = ata['nomenclatura']
            sessao_num = ata['sessao_num']
            
            f.write(f"{sessao_num}ª {tipo_sessao},Circunstanciada,{data},{pag_ini},{pag_fim},{nomenclatura}\n")
    
    print(f"✅ TXT salvo em: {ARQUIVO_SAIDA_TXT}")
    
    # Estatísticas
    print(f"\n📊 ESTATÍSTICAS")
    print("="*70)
    
    print(f"   Total de atas encontradas: {len(resultados_teste)}")
    
    # Agrupar por ano
    por_ano = {}
    for ata in resultados_teste:
        ano = ata['nomenclatura'].split('-')[0]
        if ano not in por_ano:
            por_ano[ano] = 0
        por_ano[ano] += 1
    
    print(f"\n   Distribuição por ano:")
    for ano in sorted(por_ano.keys()):
        print(f"      {ano}: {por_ano[ano]} atas")
    
    print(f"\n✅ FASE 2 CONCLUÍDA!")

if __name__ == "__main__":
    main()

