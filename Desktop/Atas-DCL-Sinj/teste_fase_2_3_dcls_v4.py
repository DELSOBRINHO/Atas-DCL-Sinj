#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TESTE FASE 2 - MAPEAMENTO COMPLETO DE ATAS (3 PRIMEIROS DCLs COM ATAS) v4
==========================================================================

Objetivo: Localizar TODAS as atas circunstanciadas nos 3 primeiros DCLs
e validar o modelo de cálculo de páginas.

Versão 4: Regex melhorado para capturar número ANTES de ATACIRCUNSTANCIADA

Uso:
    python teste_fase_2_3_dcls_v4.py

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
                    # Padrão: "ATACIRCUNSTANCIADADA108A" (sem espaço)
                    contexto_depois = texto[idx:min(len(texto), idx+500)]  # Aumentado para 500 para capturar datas mais distantes
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
                    else:
                        # Se não encontrar data, usar data padrão (será ajustada depois)
                        data_iso = "2006-01-01"  # Data padrão para atas sem data
                    
                    # Mapeamento de tipo de sessão
                    c_sessao, s_sessao = MAPA_SESSAO.get(tipo_sessao_txt, ("0", "XX"))
                    
                    nome_final = f"{data_iso}-{c_sessao}-{s_sessao}-{num_sessao}-2-AC.pdf"
                    
                    # Formatar data_real
                    if match_data:
                        dia, mes_ext, ano = match_data.groups()
                        data_real = f"{dia}/{MESES_MAP.get(mes_ext, '00')}/{ano}"
                    else:
                        data_real = "SEM DATA"

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
            # Remover duplicatas por nomenclatura (mesma ata não pode aparecer 2x)
            df_temp = df_temp.drop_duplicates(subset=['nomenclatura'], keep='first')
            lista_atas = df_temp.to_dict('records')

            for i in range(len(lista_atas)):
                if i < len(lista_atas) - 1:
                    # Página final é a página anterior à próxima ata
                    pag_fim_calc = lista_atas[i+1]["pag_inicio"] - 1
                    # Mas garante que não seja menor que a página inicial
                    lista_atas[i]["pag_fim"] = max(lista_atas[i]["pag_inicio"], pag_fim_calc)
                else:
                    lista_atas[i]["pag_fim"] = total_paginas
    
    except Exception as e:
        print(f"❌ Erro em {nome_arquivo}: {e}")
    
    return lista_atas

def main():
    """Função principal"""
    print("\n" + "="*70)
    print("TESTE FASE 2 - MAPEAMENTO COMPLETO DE ATAS (3 PRIMEIROS DCLs COM ATAS) v4")
    print("="*70)
    
    # Instalar dependências
    instalar_dependencias()
    
    # Ler lista de DCLs com atas circunstanciadas
    arquivo_lista = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/dcls_com_atas_circunstanciadas.txt")
    
    if not arquivo_lista.exists():
        print(f"❌ Arquivo {arquivo_lista} não encontrado")
        return
    
    with open(arquivo_lista, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    # Extrair nomes dos DCLs (pulando cabeçalho)
    dcls_com_atas = [linha.strip() for linha in linhas[4:] if linha.strip()]
    
    print(f"\n✅ {len(dcls_com_atas)} DCLs com atas circunstanciadas encontrados")
    
    # Selecionar os 3 primeiros
    test_files = dcls_com_atas[:3]
    
    print(f"\n🔍 TESTANDO COM OS 3 PRIMEIROS DCLs COM ATAS:")
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

if __name__ == "__main__":
    main()

