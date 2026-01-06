#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TESTE FASE 2 - MAPEAMENTO COMPLETO DE ATAS (3 PRIMEIROS DCLs)
==============================================================

Objetivo: Localizar TODAS as atas circunstanciadas nos 3 primeiros DCLs
e validar o modelo de cálculo de páginas.

Entrada: 3 primeiros DCLs com atas circunstanciadas
Saída: Relatório com todas as atas encontradas

Uso:
    python teste_fase_2_3_dcls.py

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
ARQUIVO_SAIDA_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/teste_fase2_3_dcls_resultado.json")
ARQUIVO_SAIDA_TXT = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/teste_fase2_3_dcls_resultado.txt")

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
    
    caminho = DIR_DOWNLOADS / nome_arquivo
    lista_atas = []
    
    if not caminho.exists():
        return []
    
    try:
        with pdfplumber.open(caminho) as pdf:
            total_paginas = len(pdf.pages)
            
            for num_p, pagina in enumerate(pdf.pages, 1):
                texto_raw = (pagina.extract_text() or "").upper()
                # Normaliza espaços para tratar "ATACIRCU  NSTANCIADA"
                texto = " ".join(texto_raw.split())
                
                # Busca radical ATACIR (Ata Circunstanciada)
                for match in re.finditer(r'ATACIR', texto):
                    # Pega o contexto de 500 caracteres após o termo encontrado
                    contexto = texto[match.start():match.start()+500]
                    
                    # Regex flexível para Sessão e Data
                    ss_re = re.search(
                        r'(\d+)\s*[ª°ºA]?\s*(?:\(.*\))?\s*SESS[ÃA]O\s+(ORDIN[ÁA]RIA|EXTRAORDIN[ÁA]RIA|SOLENE|PREPARAT[ÓO]RIA|ESPECIAL)',
                        contexto
                    )
                    dt_re = re.search(
                        r'(?:EM|REALIZADA)\s*(\d{1,2})\s*DE\s*(\w+)\s*DE\s*(200\d)',
                        contexto
                    )
                    
                    if ss_re and dt_re:
                        num_sessao = ss_re.group(1).zfill(3)
                        tipo_sessao_txt = ss_re.group(2)
                        dia, mes_ext, ano = dt_re.groups()
                        
                        # Filtro de Ano 2007
                        if ano != "2007":
                            continue
                        
                        data_iso = f"{ano}-{MESES_MAP.get(mes_ext, '00')}-{dia.zfill(2)}"
                        
                        # Mapeamento de tipo de sessão
                        c_sessao, s_sessao = MAPA_SESSAO.get(tipo_sessao_txt, ("0", "XX"))
                        
                        nome_final = f"{data_iso}-{c_sessao}-{s_sessao}-{num_sessao}-2-AC.pdf"
                        
                        lista_atas.append({
                            "dcl_original": nome_arquivo,
                            "pag_inicio": num_p,
                            "sessao_num": num_sessao,
                            "tipo_sessao": tipo_sessao_txt,
                            "data_real": f"{dia}/{MESES_MAP.get(mes_ext, '00')}/{ano}",
                            "nomenclatura": nome_final
                        })
        
        # --- LÓGICA DE PÁGINA FINAL ---
        # Remove detecções duplicadas na mesma página para a mesma sessão
        if lista_atas:
            import pandas as pd
            df_temp = pd.DataFrame(lista_atas).drop_duplicates(subset=['nomenclatura', 'pag_inicio'])
            lista_atas = df_temp.to_dict('records')
            
            for i in range(len(lista_atas)):
                if i < len(lista_atas) - 1:
                    lista_atas[i]["pag_fim"] = lista_atas[i+1]["pag_inicio"] - 1
                else:
                    lista_atas[i]["pag_fim"] = total_paginas
    
    except Exception as e:
        print(f"❌ Erro em {nome_arquivo}: {e}")
    
    return lista_atas

def tem_ata_circunstanciada(caminho_pdf):
    """Verifica se um PDF tem ata circunstanciada"""
    try:
        import pdfplumber

        with pdfplumber.open(caminho_pdf) as pdf:
            for pagina in pdf.pages[:10]:  # Verifica primeiras 10 páginas
                texto = (pagina.extract_text() or "").upper()

                # Procura por "ATACIR" (radical de "ATA CIRCUNSTANCIADA")
                if re.search(r'ATACIR', texto):
                    return True

        return False

    except Exception as e:
        return False

def main():
    """Função principal"""
    print("\n" + "="*70)
    print("TESTE FASE 2 - MAPEAMENTO COMPLETO DE ATAS (3 PRIMEIROS DCLs COM ATAS)")
    print("="*70)

    # Instalar dependências
    instalar_dependencias()

    # Listar todos os PDFs
    print("\n📁 LISTANDO ARQUIVOS PDF")
    todos_pdfs = sorted([f.name for f in DIR_DOWNLOADS.glob('*.pdf')])

    print(f"✅ {len(todos_pdfs)} PDFs encontrados")

    if not todos_pdfs:
        print("❌ Nenhum PDF encontrado")
        return

    # Encontrar DCLs com atas circunstanciadas
    print("\n🔍 PROCURANDO POR DCLs COM ATAS CIRCUNSTANCIADAS...")
    dcls_com_atas = []

    for arquivo in todos_pdfs:
        if tem_ata_circunstanciada(DIR_DOWNLOADS / arquivo):
            dcls_com_atas.append(arquivo)

    print(f"✅ {len(dcls_com_atas)} DCLs com atas circunstanciadas encontrados")

    # Selecionar os 3 primeiros
    test_files = dcls_com_atas[:3]
    
    print(f"\n🔍 TESTANDO COM OS 3 PRIMEIROS DCLs:")
    for i, f in enumerate(test_files, 1):
        print(f"   {i}. {f}")
    
    # Processar os 3 primeiros
    print(f"\n📊 PROCESSANDO 3 DCLs")
    print("="*70 + "\n")
    
    resultados_teste = []
    
    for i, arquivo in enumerate(test_files, 1):
        print(f"[{i}/3] Processando {arquivo}...")
        res = extrair_todas_atas_pdf(arquivo)
        resultados_teste.extend(res)
        print(f"      ✅ {len(res)} atas encontradas")
    
    # Salvar JSON
    print(f"\n💾 SALVANDO RESULTADOS")
    print("="*70)
    
    with open(ARQUIVO_SAIDA_JSON, 'w', encoding='utf-8') as f:
        json.dump(resultados_teste, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON salvo em: {ARQUIVO_SAIDA_JSON}")
    
    # Salvar TXT formatado
    with open(ARQUIVO_SAIDA_TXT, 'w', encoding='utf-8') as f:
        f.write("TESTE FASE 2 - MAPEAMENTO COMPLETO DE ATAS (3 PRIMEIROS DCLs)\n")
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
    
    # Agrupar por DCL
    por_dcl = {}
    for ata in resultados_teste:
        dcl = ata['dcl_original']
        if dcl not in por_dcl:
            por_dcl[dcl] = 0
        por_dcl[dcl] += 1
    
    print(f"\n   Distribuição por DCL:")
    for dcl, count in por_dcl.items():
        print(f"      {dcl}: {count} atas")
    
    print(f"\n✅ TESTE CONCLUÍDO!")
    print(f"\n📋 Verifique os arquivos gerados:")
    print(f"   - {ARQUIVO_SAIDA_JSON}")
    print(f"   - {ARQUIVO_SAIDA_TXT}")

if __name__ == "__main__":
    main()

