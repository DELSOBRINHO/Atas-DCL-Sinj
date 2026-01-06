# -*- coding: utf-8 -*-
"""
Script para criar estrutura completa de pastas - Cadernos Anais CLDF
Execute este script UMA VEZ para criar toda a estrutura do zero.

Autor: Sistema de Automação CLDF
Data: 2025
"""

import os
from pathlib import Path
import sys
from datetime import datetime

# ======================================================================
# CONFIGURAÇÕES
# ======================================================================
USUARIO = "omega"
ONEDRIVE_NAME = "OneDrive - Câmara Legislativa do Distrito Federal - CLDF"
BASE_PATH = Path(f"C:/Users/{USUARIO}/{ONEDRIVE_NAME}")

# Verificar se o caminho base existe
if not BASE_PATH.exists():
    print(f"❌ ERRO: Caminho base não encontrado: {BASE_PATH}")
    print(f"   Verifique se o OneDrive está configurado corretamente.")
    sys.exit(1)

# ======================================================================
# DEFINIÇÃO DA ESTRUTURA DE PASTAS
# ======================================================================

# Timestamp de início
inicio_execucao = datetime.now()

print("="*80)
print("CRIAÇÃO COMPLETA DA ESTRUTURA DE PASTAS - CADERNOS ANAIS CLDF")
print("="*80)
print(f"⏰ Início: {inicio_execucao.strftime('%Y-%m-%d %H:%M:%S')}")
print("\n📋 Este script cria TODA a estrutura de pastas do zero.")
print("   Inclui:")
print("   - 9 Legislaturas (1991-2026)")
print("   - Pastas para PDFs (Unicos, Pacotes, Mês, Individuais, Trimestrais ⭐)")
print("   - Pastas para Dados JSON (Consolidados, Mensais, Pacotes, Unicos, Trimestrais ⭐)")
print("   - Pastas para Relatórios (CSV e XLSX)")
print("   - Pastas para Sumários")
print("   - Outras compilações e documentação")
print("\n" + "="*80)

PASTA_BASE = 'Cadernos_Anais_CLDF'

# Mapeamento de Legislaturas (1991-2026)
LEGISLATURAS = {
    1: {'periodo': '1991-1994', 'anos': [1991, 1992, 1993, 1994]},
    2: {'periodo': '1995-1998', 'anos': [1995, 1996, 1997, 1998]},
    3: {'periodo': '1999-2002', 'anos': [1999, 2000, 2001, 2002]},
    4: {'periodo': '2003-2006', 'anos': [2003, 2004, 2005, 2006]},
    5: {'periodo': '2007-2010', 'anos': [2007, 2008, 2009, 2010]},
    6: {'periodo': '2011-2014', 'anos': [2011, 2012, 2013, 2014]},
    7: {'periodo': '2015-2018', 'anos': [2015, 2016, 2017, 2018]},
    8: {'periodo': '2019-2022', 'anos': [2019, 2020, 2021, 2022]},
    9: {'periodo': '2023-2026', 'anos': [2023, 2024, 2025, 2026]}
}

TEMAS = [
    'Orcamento_Financeiro',
    'Projetos_de_Lei',
    'Sessoes_Solenes',
    'Comissoes_Permanentes',
    'Comissoes_Temporarias',
    'Votacoes_Importantes',
    'Outros_Temas'
]

def gerar_lista_pastas_completa():
    """Gera lista completa de caminhos de pastas com metadados - Abordagem 2: Por Legislatura"""
    lista_pastas = []

    # Legislaturas como nível 1
    for num, info in LEGISLATURAS.items():
        leg_folder = f"{str(num).zfill(2)}_Legislatura_{info['periodo']}"

        # Pasta da legislatura (nível 1)
        lista_pastas.append({
            'nome_pasta': leg_folder,
            'caminho_completo': leg_folder,
            'pasta_pai': PASTA_BASE,
            'nivel': 1,
            'tipo': 'legislatura'
        })

        # ========== CADERNOS PDF ==========
        lista_pastas.append({
            'nome_pasta': 'Cadernos_PDF',
            'caminho_completo': f"{leg_folder}/Cadernos_PDF",
            'pasta_pai': leg_folder,
            'nivel': 2,
            'tipo': 'pdf_base'
        })

        # Subpastas de PDFs
        subpastas_pdf = ['Cadernos_Unicos_Ano', 'Cadernos_Por_Pacote', 'Cadernos_Por_Mes', 'PDFs_Individuais', 'Trimestrais']
        # Mapeamento para normalizar tipos de pasta de anos
        tipo_ano_map = {
            'Cadernos_Unicos_Ano': 'ano_cadernos_unicos_ano',
            'Cadernos_Por_Pacote': 'ano_cadernos_por_pacote',
            'Cadernos_Por_Mes': 'ano_cadernos_por_mes',
            'PDFs_Individuais': 'ano_pdfs_individuais',
            'Trimestrais': 'ano_trimestrais'
        }

        for subpasta in subpastas_pdf:
            lista_pastas.append({
                'nome_pasta': subpasta,
                'caminho_completo': f"{leg_folder}/Cadernos_PDF/{subpasta}",
                'pasta_pai': f"{leg_folder}/Cadernos_PDF",
                'nivel': 3,
                'tipo': 'subpasta_pdf'
            })

            # Pastas por ano dentro de cada subpasta (GARANTIR PARA TODAS AS LEGISLATURAS)
            tipo_ano = tipo_ano_map.get(subpasta, f'ano_{subpasta.lower().replace(" ", "_")}')
            for ano in info['anos']:
                lista_pastas.append({
                    'nome_pasta': str(ano),
                    'caminho_completo': f"{leg_folder}/Cadernos_PDF/{subpasta}/{ano}",
                    'pasta_pai': f"{leg_folder}/Cadernos_PDF/{subpasta}",
                    'nivel': 4,
                    'tipo': tipo_ano
                })

        # ========== DADOS JSON ==========
        lista_pastas.append({
            'nome_pasta': 'Dados_JSON',
            'caminho_completo': f"{leg_folder}/Dados_JSON",
            'pasta_pai': leg_folder,
            'nivel': 2,
            'tipo': 'json_base'
        })

        # Consolidados
        lista_pastas.append({
            'nome_pasta': 'Consolidados',
            'caminho_completo': f"{leg_folder}/Dados_JSON/Consolidados",
            'pasta_pai': f"{leg_folder}/Dados_JSON",
            'nivel': 3,
            'tipo': 'json_consolidados'
        })

        # Mensais
        lista_pastas.append({
            'nome_pasta': 'Mensais',
            'caminho_completo': f"{leg_folder}/Dados_JSON/Mensais",
            'pasta_pai': f"{leg_folder}/Dados_JSON",
            'nivel': 3,
            'tipo': 'json_mensais'
        })

        # Pastas de anos em Mensais (GARANTIR PARA TODAS AS LEGISLATURAS)
        for ano in info['anos']:
            lista_pastas.append({
                'nome_pasta': str(ano),
                'caminho_completo': f"{leg_folder}/Dados_JSON/Mensais/{ano}",
                'pasta_pai': f"{leg_folder}/Dados_JSON/Mensais",
                'nivel': 4,
                'tipo': 'json_ano_mensais'
            })

        # Pacotes (NOVO)
        lista_pastas.append({
            'nome_pasta': 'Pacotes',
            'caminho_completo': f"{leg_folder}/Dados_JSON/Pacotes",
            'pasta_pai': f"{leg_folder}/Dados_JSON",
            'nivel': 3,
            'tipo': 'json_pacotes'
        })

        # Pastas de anos em Pacotes
        for ano in info['anos']:
            lista_pastas.append({
                'nome_pasta': str(ano),
                'caminho_completo': f"{leg_folder}/Dados_JSON/Pacotes/{ano}",
                'pasta_pai': f"{leg_folder}/Dados_JSON/Pacotes",
                'nivel': 4,
                'tipo': 'json_ano_pacotes'
            })

        # Unicos (NOVO)
        lista_pastas.append({
            'nome_pasta': 'Unicos',
            'caminho_completo': f"{leg_folder}/Dados_JSON/Unicos",
            'pasta_pai': f"{leg_folder}/Dados_JSON",
            'nivel': 3,
            'tipo': 'json_unicos'
        })

        # Pastas de anos em Unicos
        for ano in info['anos']:
            lista_pastas.append({
                'nome_pasta': str(ano),
                'caminho_completo': f"{leg_folder}/Dados_JSON/Unicos/{ano}",
                'pasta_pai': f"{leg_folder}/Dados_JSON/Unicos",
                'nivel': 4,
                'tipo': 'json_ano_unicos'
            })

        # Trimestrais (NOVO)
        lista_pastas.append({
            'nome_pasta': 'Trimestrais',
            'caminho_completo': f"{leg_folder}/Dados_JSON/Trimestrais",
            'pasta_pai': f"{leg_folder}/Dados_JSON",
            'nivel': 3,
            'tipo': 'json_trimestrais'
        })

        # Pastas de anos em Trimestrais
        for ano in info['anos']:
            lista_pastas.append({
                'nome_pasta': str(ano),
                'caminho_completo': f"{leg_folder}/Dados_JSON/Trimestrais/{ano}",
                'pasta_pai': f"{leg_folder}/Dados_JSON/Trimestrais",
                'nivel': 4,
                'tipo': 'json_ano_trimestrais'
            })

        # ========== RELATÓRIOS CSV ==========
        lista_pastas.append({
            'nome_pasta': 'Relatorios_CSV',
            'caminho_completo': f"{leg_folder}/Relatorios_CSV",
            'pasta_pai': leg_folder,
            'nivel': 2,
            'tipo': 'csv_base'
        })

        # Pastas por ano em CSV (GARANTIR PARA TODAS AS LEGISLATURAS)
        for ano in info['anos']:
            lista_pastas.append({
                'nome_pasta': str(ano),
                'caminho_completo': f"{leg_folder}/Relatorios_CSV/{ano}",
                'pasta_pai': f"{leg_folder}/Relatorios_CSV",
                'nivel': 3,
                'tipo': 'csv_ano'
            })

            # Subpasta sumarios dentro de cada ano (NOVO)
            lista_pastas.append({
                'nome_pasta': 'sumarios',
                'caminho_completo': f"{leg_folder}/Relatorios_CSV/{ano}/sumarios",
                'pasta_pai': f"{leg_folder}/Relatorios_CSV/{ano}",
                'nivel': 4,
                'tipo': 'csv_sumarios'
            })

        # ========== RELATÓRIOS XLSX ==========
        lista_pastas.append({
            'nome_pasta': 'Relatorios_XLSX',
            'caminho_completo': f"{leg_folder}/Relatorios_XLSX",
            'pasta_pai': leg_folder,
            'nivel': 2,
            'tipo': 'xlsx_base'
        })

        # Pastas por ano em XLSX
        for ano in info['anos']:
            lista_pastas.append({
                'nome_pasta': str(ano),
                'caminho_completo': f"{leg_folder}/Relatorios_XLSX/{ano}",
                'pasta_pai': f"{leg_folder}/Relatorios_XLSX",
                'nivel': 3,
                'tipo': 'xlsx_ano'
            })

    # ========== OUTRAS COMPILAÇÕES ==========
    lista_pastas.append({
        'nome_pasta': 'Outras_Compilacoes',
        'caminho_completo': 'Outras_Compilacoes',
        'pasta_pai': PASTA_BASE,
        'nivel': 1,
        'tipo': 'outras_compilacoes_base'
    })

    outras_compilacoes = [
        ('Cadernos_PDF', 'Outras_Compilacoes', 2),
        ('Cadernos_por_Tipo_Sessao', 'Outras_Compilacoes/Cadernos_PDF', 3),
        ('Cadernos_por_Tipo_Ata', 'Outras_Compilacoes/Cadernos_PDF', 3),
        ('Cadernos_Especiais', 'Outras_Compilacoes/Cadernos_PDF', 3),
        ('Cadernos_Tematicos', 'Outras_Compilacoes/Cadernos_PDF', 3),
        ('Por_Tema', 'Outras_Compilacoes/Cadernos_PDF/Cadernos_Tematicos', 4),
        ('Por_Periodo', 'Outras_Compilacoes/Cadernos_PDF/Cadernos_Tematicos', 4),
        ('Por_Decada', 'Outras_Compilacoes/Cadernos_PDF/Cadernos_Tematicos/Por_Periodo', 5),
        ('Por_Gestao', 'Outras_Compilacoes/Cadernos_PDF/Cadernos_Tematicos/Por_Periodo', 5)
    ]

    for nome, pai, nivel in outras_compilacoes:
        lista_pastas.append({
            'nome_pasta': nome,
            'caminho_completo': f"{pai}/{nome}" if pai else nome,
            'pasta_pai': pai,
            'nivel': nivel,
            'tipo': 'outras_compilacoes'
        })

    # Temas
    for tema in TEMAS:
        lista_pastas.append({
            'nome_pasta': tema,
            'caminho_completo': f"Outras_Compilacoes/Cadernos_PDF/Cadernos_Tematicos/Por_Tema/{tema}",
            'pasta_pai': 'Outras_Compilacoes/Cadernos_PDF/Cadernos_Tematicos/Por_Tema',
            'nivel': 5,
            'tipo': 'tema'
        })

    # ========== ARQUIVOS HTML ==========
    lista_pastas.append({
        'nome_pasta': 'Arquivos_HTML',
        'caminho_completo': 'Arquivos_HTML',
        'pasta_pai': PASTA_BASE,
        'nivel': 1,
        'tipo': 'html_base'
    })
    lista_pastas.append({
        'nome_pasta': 'Versoes',
        'caminho_completo': 'Arquivos_HTML/Versoes',
        'pasta_pai': 'Arquivos_HTML',
        'nivel': 2,
        'tipo': 'html_versoes'
    })
    lista_pastas.append({
        'nome_pasta': 'Templates',
        'caminho_completo': 'Arquivos_HTML/Templates',
        'pasta_pai': 'Arquivos_HTML',
        'nivel': 2,
        'tipo': 'html_templates'
    })

    # ========== DOCUMENTAÇÃO ==========
    lista_pastas.append({
        'nome_pasta': 'Documentacao',
        'caminho_completo': 'Documentacao',
        'pasta_pai': PASTA_BASE,
        'nivel': 1,
        'tipo': 'doc_base'
    })
    lista_pastas.append({
        'nome_pasta': 'Guias',
        'caminho_completo': 'Documentacao/Guias',
        'pasta_pai': 'Documentacao',
        'nivel': 2,
        'tipo': 'doc_guias'
    })
    lista_pastas.append({
        'nome_pasta': 'Scripts',
        'caminho_completo': 'Documentacao/Scripts',
        'pasta_pai': 'Documentacao',
        'nivel': 2,
        'tipo': 'doc_scripts'
    })
    lista_pastas.append({
        'nome_pasta': 'Listas',
        'caminho_completo': 'Documentacao/Listas',
        'pasta_pai': 'Documentacao',
        'nivel': 2,
        'tipo': 'doc_listas'
    })

    # ========== BUSCA DE REGISTROS (JSON) ==========
    lista_pastas.append({
        'nome_pasta': 'Busca_Registros',
        'caminho_completo': 'Busca_Registros',
        'pasta_pai': PASTA_BASE,
        'nivel': 1,
        'tipo': 'json_busca'
    })

    # ========== CONSOLIDADOS (CSV e XLSX) ==========
    lista_pastas.append({
        'nome_pasta': 'Consolidados_CSV',
        'caminho_completo': 'Consolidados_CSV',
        'pasta_pai': PASTA_BASE,
        'nivel': 1,
        'tipo': 'csv_consolidados'
    })
    lista_pastas.append({
        'nome_pasta': 'Consolidados_XLSX',
        'caminho_completo': 'Consolidados_XLSX',
        'pasta_pai': PASTA_BASE,
        'nivel': 1,
        'tipo': 'xlsx_consolidados'
    })

    return lista_pastas

def criar_pastas_locais():
    """
    Cria a estrutura completa de pastas no sistema de arquivos do zero.
    
    Esta função:
    - Cria todas as 549 pastas necessárias
    - Organiza por legislaturas (1991-2026)
    - Inclui pastas para PDFs, JSON, CSV, XLSX, Sumários, Trimestrais
    - Valida a criação de todas as pastas
    """
    print(f"🚀 Iniciando criação da estrutura completa em: {BASE_PATH}")
    print(f"📁 Pasta base: {PASTA_BASE}")
    print(f"⚠️  ATENÇÃO: Este script criará TODAS as pastas necessárias do zero.")
    print(f"   Se a estrutura já existir, as pastas serão verificadas/criadas novamente.")
    print(f"   Tempo estimado: 1-2 minutos\n")
    
    # Gerar lista de pastas
    LISTA_PASTAS = gerar_lista_pastas_completa()
    total_pastas = len(LISTA_PASTAS)
    print(f"✅ Estrutura gerada: {total_pastas} pastas a serem criadas/verificadas em '{PASTA_BASE}'.")

    # Criar pasta base
    pasta_base_path = BASE_PATH / PASTA_BASE
    try:
        os.makedirs(pasta_base_path, exist_ok=True)
        print(f"\n✅ Pasta base criada/verificada: {pasta_base_path}")
    except OSError as e:
        print(f"\n❌ ERRO ao criar pasta base {pasta_base_path}: {e}")
        return

    # Criar pastas da estrutura com progresso otimizado
    print(f"\n📂 Criando estrutura de pastas...")
    print(f"   Processando {total_pastas} pastas...\n")
    
    pastas_criadas = 0
    pastas_erro = 0
    pastas_ja_existiam = 0
    
    # Agrupar por nível para melhor organização do output
    pastas_por_nivel = {}
    for pasta_info in LISTA_PASTAS:
        nivel = pasta_info['nivel']
        if nivel not in pastas_por_nivel:
            pastas_por_nivel[nivel] = []
        pastas_por_nivel[nivel].append(pasta_info)
    
    # Criar pastas ordenadas por nível (garante que pastas pai sejam criadas primeiro)
    for nivel in sorted(pastas_por_nivel.keys()):
        pastas_nivel = pastas_por_nivel[nivel]
        for pasta_info in pastas_nivel:
            rel_path = pasta_info['caminho_completo']
            full_path = pasta_base_path / rel_path
            
            # Verificar se já existe
            ja_existia = full_path.exists()
            
            try:
                os.makedirs(full_path, exist_ok=True)
                pastas_criadas += 1
                if ja_existia:
                    pastas_ja_existiam += 1
                
                # Mostrar progresso a cada 50 pastas ou para pastas importantes (níveis 1-2)
                if pastas_criadas % 50 == 0 or nivel <= 2:
                    status = "✓" if ja_existia else "✅"
                    print(f"   [{pastas_criadas:3d}/{total_pastas}] {status} {rel_path}")
                    
            except OSError as e:
                pastas_erro += 1
                print(f"   ❌ Erro ao criar pasta {rel_path}: {e}")

    print(f"\n📊 RESUMO DA CRIAÇÃO:")
    print(f"   ✅ Total processado: {pastas_criadas}/{total_pastas}")
    if pastas_ja_existiam > 0:
        print(f"   ✓ Pastas que já existiam: {pastas_ja_existiam}")
        print(f"   ✅ Pastas novas criadas: {pastas_criadas - pastas_ja_existiam}")
    if pastas_erro > 0:
        print(f"   ❌ Erros encontrados: {pastas_erro}")
    else:
        print(f"   ✅ Nenhum erro encontrado!")
    print(f"\n🎉 Processo de criação de pastas concluído! 🎉")
    
    # Validações finais
    print("\n" + "="*80)
    print("VALIDAÇÃO FINAL DA ESTRUTURA CRIADA")
    print("="*80)
    
    # Verificar se a pasta base existe
    if pasta_base_path.exists():
        print(f"\n✅ Pasta base confirmada: {pasta_base_path}")
    else:
        print(f"\n❌ ERRO: Pasta base não foi criada!")
        return
    
    # Validação: Verificar estrutura por Legislatura
    print(f"\n🔍 Validação por Legislatura:")
    legislaturas = [p for p in LISTA_PASTAS if p['tipo'] == 'legislatura']
    print(f"   ✅ Total de legislaturas: {len(legislaturas)}")
    
    # Verificar se todas as pastas foram realmente criadas
    print(f"\n🔍 Verificando existência física das pastas...")
    pastas_verificadas = 0
    pastas_faltando = []
    
    for pasta_info in LISTA_PASTAS:
        rel_path = pasta_info['caminho_completo']
        full_path = pasta_base_path / rel_path
        if full_path.exists():
            pastas_verificadas += 1
        else:
            pastas_faltando.append(rel_path)
    
    print(f"   ✅ Pastas verificadas: {pastas_verificadas}/{total_pastas}")
    if pastas_faltando:
        print(f"   ⚠️  Pastas faltando: {len(pastas_faltando)}")
        for pasta_faltando in pastas_faltando[:10]:  # Mostrar apenas as primeiras 10
            print(f"      - {pasta_faltando}")
        if len(pastas_faltando) > 10:
            print(f"      ... e mais {len(pastas_faltando) - 10} pastas")
    else:
        print(f"   ✅ Todas as pastas foram criadas com sucesso!")

    # Validação detalhada por legislatura
    print(f"\n📊 Validação detalhada por legislatura:")
    for num, info in LEGISLATURAS.items():
        leg_folder = f"{str(num).zfill(2)}_Legislatura_{info['periodo']}"
        leg_pastas = [p for p in LISTA_PASTAS if leg_folder in p['caminho_completo']]

        # Contar pastas de anos em cada tipo
        anos_unicos = len([p for p in leg_pastas if p.get('tipo') == 'ano_cadernos_unicos_ano'])
        anos_pacote = len([p for p in leg_pastas if p.get('tipo') == 'ano_cadernos_por_pacote'])
        anos_mes = len([p for p in leg_pastas if p.get('tipo') == 'ano_cadernos_por_mes'])
        anos_pdfs = len([p for p in leg_pastas if p.get('tipo') == 'ano_pdfs_individuais'])
        anos_trimestrais = len([p for p in leg_pastas if p.get('tipo') == 'ano_trimestrais'])
        anos_json_mensais = len([p for p in leg_pastas if p.get('tipo') == 'json_ano_mensais'])
        anos_json_pacotes = len([p for p in leg_pastas if p.get('tipo') == 'json_ano_pacotes'])
        anos_json_unicos = len([p for p in leg_pastas if p.get('tipo') == 'json_ano_unicos'])
        anos_json_trimestrais = len([p for p in leg_pastas if p.get('tipo') == 'json_ano_trimestrais'])
        anos_csv = len([p for p in leg_pastas if p.get('tipo') == 'csv_ano'])
        sumarios_csv = len([p for p in leg_pastas if p.get('tipo') == 'csv_sumarios'])

        esperado_anos = len(info['anos'])
        # Validação: verificar se todas as pastas principais foram criadas
        status = "✅" if (anos_unicos == esperado_anos and anos_json_mensais == esperado_anos
                          and sumarios_csv == esperado_anos and anos_trimestrais == esperado_anos
                          and anos_json_trimestrais == esperado_anos) else "❌"

        print(f"   {status} {leg_folder}:")
        print(f"      PDFs - Unicos: {anos_unicos}/{esperado_anos}, Pacote: {anos_pacote}/{esperado_anos}, Mês: {anos_mes}/{esperado_anos}")
        print(f"      PDFs - Individuais: {anos_pdfs}/{esperado_anos}, Trimestrais: {anos_trimestrais}/{esperado_anos} ⭐ NOVO")
        print(f"      JSON - Mensais: {anos_json_mensais}/{esperado_anos}, Pacotes: {anos_json_pacotes}/{esperado_anos}, Unicos: {anos_json_unicos}/{esperado_anos}")
        print(f"      JSON - Trimestrais: {anos_json_trimestrais}/{esperado_anos} ⭐ NOVO")
        print(f"      CSV - Anos: {anos_csv}/{esperado_anos}, Sumários: {sumarios_csv}/{esperado_anos}")
    
    # Verificação especial da pasta Trimestrais (nova funcionalidade)
    print(f"\n" + "="*80)
    print(f"⭐ VERIFICAÇÃO ESPECIAL: PASTA TRIMESTRAIS")
    print(f"="*80)
    
    pastas_trimestrais_verificadas = 0
    for num, info in LEGISLATURAS.items():
        leg_folder = f"{str(num).zfill(2)}_Legislatura_{info['periodo']}"
        for ano in info['anos']:
            pasta_trimestral = pasta_base_path / leg_folder / "Cadernos_PDF" / "Trimestrais" / str(ano)
            if pasta_trimestral.exists():
                pastas_trimestrais_verificadas += 1
    
    total_anos = sum(len(info['anos']) for info in LEGISLATURAS.values())
    print(f"   ✅ Pastas Trimestrais verificadas: {pastas_trimestrais_verificadas}/{total_anos}")
    if pastas_trimestrais_verificadas == total_anos:
        print(f"   ✅ Todas as pastas Trimestrais foram criadas com sucesso!")
    else:
        print(f"   ⚠️  Algumas pastas Trimestrais podem estar faltando")
    
    # Calcular tempo de execução da função
    fim_execucao = datetime.now()
    tempo_execucao = (fim_execucao - inicio_execucao).total_seconds()
    
    # Resumo final
    print(f"\n" + "="*80)
    print(f"✅ ESTRUTURA COMPLETA CRIADA COM SUCESSO!")
    print(f"="*80)
    print(f"\n📊 Estatísticas Finais:")
    print(f"   - Total de pastas: {total_pastas}")
    print(f"   - Pastas criadas/verificadas: {pastas_criadas}")
    print(f"   - Legislaturas: {len(LEGISLATURAS)}")
    print(f"   - Anos cobertos: {total_anos}")
    print(f"   - Pastas Trimestrais: {pastas_trimestrais_verificadas}/{total_anos} ⭐")
    print(f"\n📁 Localização da estrutura:")
    print(f"   {pasta_base_path}")
    print(f"\n⏰ Tempo de execução: {tempo_execucao:.2f} segundos ({tempo_execucao/60:.2f} minutos)")
    print(f"\n💡 Próximos passos:")
    print(f"   1. ✅ Estrutura de pastas criada")
    print(f"   2. 📓 Execute o notebook 'Caderno_2008_ambiente_local.ipynb'")
    print(f"   3. 📁 Os cadernos trimestrais serão salvos em:")
    print(f"      Cadernos_PDF/Trimestrais/2008/")
    print(f"      (Caderno_1_2008.pdf, Caderno_2_2008.pdf, Caderno_3_2008.pdf, Caderno_4_2008.pdf)")
    print(f"="*80)

if __name__ == "__main__":
    print(f"\n🚀 Iniciando execução do script...\n")
    
    try:
        criar_pastas_locais()
        
        fim_total = datetime.now()
        tempo_total = (fim_total - inicio_execucao).total_seconds()
        
        print(f"\n" + "="*80)
        print(f"✅ SCRIPT EXECUTADO COM SUCESSO!")
        print(f"⏰ Tempo total: {tempo_total:.2f} segundos ({tempo_total/60:.2f} minutos)")
        print(f"📅 Concluído em: {fim_total.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"="*80)
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Execução interrompida pelo usuário (Ctrl+C).")
        print(f"   Algumas pastas podem ter sido criadas antes da interrupção.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ ERRO CRÍTICO durante a execução:")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Mensagem: {e}")
        print(f"\n📋 Detalhes do erro:")
        import traceback
        traceback.print_exc()
        print(f"\n💡 Verifique:")
        print(f"   - Permissões de escrita no diretório")
        print(f"   - Espaço em disco disponível")
        print(f"   - Caminho do OneDrive está correto")
        sys.exit(1)