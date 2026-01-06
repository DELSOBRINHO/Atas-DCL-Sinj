#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para extração e separação de atas de um PDF do DCL
Usa o PDF: DCL nº 218 de 01 de dezembro de 2008 - Suplemento.pdf

Padrão de nomenclatura (conforme 7_9_Legis.ipynb):
YYYY-MM-DD-{codigo_tipo}-{tipo_sessao}-{numero_sessao}-{codigo_ata}-{tipo_ata_cod}.pdf

Onde:
- YYYY-MM-DD: Data da sessão
- codigo_tipo: 1=Ordinária, 2=Extraordinária, 3=Solene, 4=Preparatória, 5=Especial
- tipo_sessao: SO=Ordinária, SE=Extraordinária, SS=Solene, SP=Preparatória
- numero_sessao: Número da sessão (3 dígitos)
- codigo_ata: 1=Sucinta, 2=Circunstanciada
- tipo_ata_cod: AS=Sucinta, AC=Circunstanciada
"""

import pdfplumber
import PyPDF2
import re
import os
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from io import BytesIO

# Configuração
PDF_TESTE = 'DCL nº 218 de 01 de dezembro de 2008 - Suplemento.pdf'
PASTA_SAIDA = 'teste_atas_separadas'

def extrair_data_do_pdf(pdf_path):
    """Extrai a data do nome do arquivo PDF"""
    # Padrão: "DCL nº XXX de DD de MMMM de YYYY"
    # Exemplo: "DCL nº 218 de 01 de dezembro de 2008"

    nome_arquivo = os.path.basename(pdf_path)

    # Tenta extrair data no formato "DD de MMMM de YYYY"
    padrao_data = r'de\s+(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})'
    match = re.search(padrao_data, nome_arquivo, re.IGNORECASE)

    if match:
        dia = match.group(1).zfill(2)
        mes_nome = match.group(2).lower()
        ano = match.group(3)

        # Mapa de meses em português
        meses = {
            'janeiro': '01', 'fevereiro': '02', 'março': '03', 'abril': '04',
            'maio': '05', 'junho': '06', 'julho': '07', 'agosto': '08',
            'setembro': '09', 'outubro': '10', 'novembro': '11', 'dezembro': '12'
        }

        mes = meses.get(mes_nome, '01')
        return f"{ano}-{mes}-{dia}"

    # Se não conseguir extrair, retorna None
    return None

def extrair_info_cabecalho(pdf_path):
    """Extrai informações do cabeçalho do PDF (primeira página)"""
    info_cabecalho = {
        'numero_dcl': None,
        'data_formatada': None,
        'ano': None,
        'suplemento': False
    }

    nome_arquivo = os.path.basename(pdf_path)

    # Extrai número do DCL: "DCL nº XXX"
    match_dcl = re.search(r'DCL\s*nº\s*(\d+)', nome_arquivo, re.IGNORECASE)
    if match_dcl:
        info_cabecalho['numero_dcl'] = match_dcl.group(1)

    # Extrai data: "DD de MMMM de YYYY"
    match_data = re.search(r'de\s+(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})', nome_arquivo, re.IGNORECASE)
    if match_data:
        dia = match_data.group(1)
        mes_nome = match_data.group(2).lower()
        ano = match_data.group(3)

        # Mapa de meses em português
        meses = {
            'janeiro': 'janeiro', 'fevereiro': 'fevereiro', 'março': 'março', 'abril': 'abril',
            'maio': 'maio', 'junho': 'junho', 'julho': 'julho', 'agosto': 'agosto',
            'setembro': 'setembro', 'outubro': 'outubro', 'novembro': 'novembro', 'dezembro': 'dezembro'
        }

        mes_pt = meses.get(mes_nome, mes_nome)
        info_cabecalho['data_formatada'] = f"{dia} de {mes_pt} de {ano}"
        info_cabecalho['ano'] = ano

    # Verifica se é suplemento
    info_cabecalho['suplemento'] = 'Suplemento' in nome_arquivo

    return info_cabecalho

def desenhar_texto_alternado(canvas, x, y, texto, tamanho_grande, tamanho_pequeno, centralizado=True):
    """
    Desenha texto com letras alternadas em tamanhos diferentes.
    Exemplo: "SUPLEMENTO DO" com S, P, M, N, O em tamanho grande e u, l, e, t, d em tamanho pequeno
    """
    palavras = texto.split()
    y_atual = y

    for palavra in palavras:
        x_atual = x

        for i, letra in enumerate(palavra):
            # Alterna entre tamanho grande e pequeno
            if i % 2 == 0:
                tamanho = tamanho_grande
            else:
                tamanho = tamanho_pequeno

            canvas.setFont("Helvetica-Bold", tamanho)

            if centralizado:
                # Para texto centralizado, precisamos calcular a posição
                # Vamos desenhar letra por letra
                canvas.drawString(x_atual, y_atual, letra)
                # Estima a largura da letra para posicionar a próxima
                x_atual += tamanho * 0.5
            else:
                canvas.drawString(x_atual, y_atual, letra)
                x_atual += tamanho * 0.5

        y_atual -= (tamanho_grande + 2) * 0.1 * cm


def criar_cabecalho_pdf(info_cabecalho):
    """Cria uma página PDF com o cabeçalho do DCL com estilo alternado"""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    # Dimensões da página A4
    width, height = A4

    # Cabeçalho superior
    c.setFont("Helvetica", 9)
    c.drawString(1.5*cm, height - 1.5*cm, "Câmara Legislativa do DF")
    c.drawString(1.5*cm, height - 1.8*cm, "Biblioteca")

    # Título principal com estilo alternado: "SUPLEMENTO DO"
    # S(grande) u(pequeno) p(grande) l(pequeno) e(grande) m(pequeno) e(grande) n(pequeno) t(grande) o(pequeno) D(grande) O(pequeno)
    y_suplemento = height - 3.2*cm
    x_center = width / 2

    # Desenhar "SUPLEMENTO DO" com alternância
    texto_suplemento = "SUPLEMENTO DO"
    x_pos = x_center - len(texto_suplemento) * 3  # Aproximação para centralizar

    for i, letra in enumerate(texto_suplemento):
        if letra == ' ':
            x_pos += 8
            continue

        if i % 2 == 0:
            c.setFont("Helvetica-Bold", 16)  # Tamanho grande
        else:
            c.setFont("Helvetica-Bold", 12)  # Tamanho pequeno

        c.drawString(x_pos, y_suplemento, letra)
        x_pos += 8 if i % 2 == 0 else 6

    # Título principal: "DIÁRIO DA CÂMARA LEGISLATIVA" com estilo alternado
    y_diario = height - 4.2*cm
    texto_diario = "DIÁRIO DA CÂMARA LEGISLATIVA"
    x_pos = x_center - len(texto_diario) * 4

    for i, letra in enumerate(texto_diario):
        if letra == ' ':
            x_pos += 12
            continue

        if i % 2 == 0:
            c.setFont("Helvetica-Bold", 28)  # Tamanho grande
        else:
            c.setFont("Helvetica-Bold", 22)  # Tamanho pequeno

        c.drawString(x_pos, y_diario, letra)
        x_pos += 14 if i % 2 == 0 else 11

    # Subtítulo com estilo alternado: "Órgão Oficial do Poder Legislativo do Distrito Federal"
    y_orgao = height - 5.0*cm
    texto_orgao = "ÓRGÃO OFICIAL DO PODER LEGISLATIVO DO DISTRITO FEDERAL"
    x_pos = x_center - len(texto_orgao) * 2

    for i, letra in enumerate(texto_orgao):
        if letra == ' ':
            x_pos += 4
            continue

        if i % 2 == 0:
            c.setFont("Helvetica-Bold", 8)   # Tamanho grande
        else:
            c.setFont("Helvetica-Bold", 6)   # Tamanho pequeno

        c.drawString(x_pos, y_orgao, letra)
        x_pos += 4 if i % 2 == 0 else 3

    # Linha horizontal
    c.setLineWidth(2)
    c.line(1*cm, height - 5.5*cm, width - 1*cm, height - 5.5*cm)

    # Informações do DCL
    c.setFont("Helvetica", 10)

    if info_cabecalho['numero_dcl']:
        texto_dcl = f"Ano XVII Suplemento ao DCL Nº {info_cabecalho['numero_dcl']}"
        c.drawString(1.5*cm, height - 6.2*cm, texto_dcl)

    if info_cabecalho['data_formatada']:
        # Alinha à direita
        texto_data = f"Brasília, {info_cabecalho['data_formatada']}"
        c.drawRightString(width - 1.5*cm, height - 6.2*cm, texto_data)

    # Finaliza o canvas
    c.save()
    buffer.seek(0)

    return buffer

def extrair_sumario(pdf_path):
    """Extrai o sumário da primeira página do PDF"""
    print(f"\n{'='*70}")
    print(f"ANALISANDO PDF: {pdf_path}")
    print(f"{'='*70}\n")

    with pdfplumber.open(pdf_path) as pdf:
        total_paginas = len(pdf.pages)
        print(f"✓ Total de páginas: {total_paginas}\n")

        # Extrai texto da primeira página
        primeira_pagina = pdf.pages[0]
        texto_sumario = primeira_pagina.extract_text()

        return texto_sumario, total_paginas

def identificar_atas(texto_sumario):
    """Identifica as atas no sumário e suas páginas"""
    print(f"{'='*70}")
    print("IDENTIFICANDO ATAS NO SUMÁRIO")
    print(f"{'='*70}\n")

    atas = []

    # Padrões para identificar atas - MELHORADO para capturar variações
    # Procura por: "Ata Circ. da XXXa Sessão Ordinária/Extraordinária PAGE"
    # Também captura números de página com formatação especial (,..28)
    padrao = r'Ata\s*Circ\.?\s*da\s*(\d+)a?\s*Sessão\s*(Ordinária|Extraordinária)\s*[,.\s]*(\d+)'

    matches = re.finditer(padrao, texto_sumario, re.IGNORECASE)

    for match in matches:
        numero_sessao = match.group(1)
        tipo_sessao = match.group(2)
        pagina_inicio = int(match.group(3))

        ata = {
            'numero_sessao': numero_sessao,
            'tipo_sessao': tipo_sessao,
            'pagina_inicio': pagina_inicio,
            'tipo_ata': 'Circunstanciada'
        }
        atas.append(ata)

        print(f"✓ Ata encontrada:")
        print(f"  - Sessão: {numero_sessao}ª {tipo_sessao}")
        print(f"  - Tipo: {ata['tipo_ata']}")
        print(f"  - Página inicial: {pagina_inicio}")
        print()

    return atas

def calcular_paginas_finais(atas, total_paginas):
    """Calcula a página final de cada ata"""
    print(f"{'='*70}")
    print("CALCULANDO PÁGINAS FINAIS")
    print(f"{'='*70}\n")
    
    for i, ata in enumerate(atas):
        if i < len(atas) - 1:
            # Página final é a página anterior à próxima ata
            ata['pagina_final'] = atas[i + 1]['pagina_inicio']
        else:
            # Última ata vai até o final do documento
            ata['pagina_final'] = total_paginas
        
        print(f"✓ Ata {ata['numero_sessao']}ª {ata['tipo_sessao']}")
        print(f"  - Páginas: {ata['pagina_inicio']} a {ata['pagina_final']}")
        print(f"  - Total: {ata['pagina_final'] - ata['pagina_inicio'] + 1} páginas")
        print()
    
    return atas

def separar_pdf(pdf_path, atas, data_sessao, info_cabecalho=None):
    """Separa o PDF em PDFs individuais para cada ata com cabeçalho"""
    print(f"{'='*70}")
    print("SEPARANDO PDF EM ATAS INDIVIDUAIS")
    print(f"{'='*70}\n")

    # Cria pasta de saída
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    atas_criadas = []

    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        for ata in atas:
            # Cria novo PDF
            pdf_writer = PyPDF2.PdfWriter()

            # Adiciona cabeçalho se informações disponíveis
            if info_cabecalho:
                buffer_cabecalho = criar_cabecalho_pdf(info_cabecalho)
                pdf_cabecalho = PyPDF2.PdfReader(buffer_cabecalho)
                pdf_writer.add_page(pdf_cabecalho.pages[0])

            # Adiciona páginas (convertendo para índice 0-based)
            pagina_inicio = ata['pagina_inicio'] - 1
            pagina_final = ata['pagina_final'] - 1

            for pagina_num in range(pagina_inicio, pagina_final + 1):
                if pagina_num < len(pdf_reader.pages):
                    pdf_writer.add_page(pdf_reader.pages[pagina_num])

            # Gera nome do arquivo conforme padrão 7_9_Legis.ipynb
            # Formato: YYYY-MM-DD-{codigo_tipo}-{tipo_sessao}-{numero_sessao}-{codigo_ata}-{tipo_ata_cod}.pdf

            # Determina tipo de sessão
            if 'Extraordinária' in ata['tipo_sessao']:
                tipo_sessao_abrev = 'SE'
                codigo_tipo = '2'
            else:  # Ordinária
                tipo_sessao_abrev = 'SO'
                codigo_tipo = '1'

            # Tipo de ata (sempre Circunstanciada neste caso)
            tipo_ata_abrev = 'AC'
            codigo_ata = '2'

            # Número da sessão (3 dígitos)
            numero_sessao = str(int(ata['numero_sessao'])).zfill(3)

            # Monta o nome do arquivo
            nome_arquivo = f"{data_sessao}-{codigo_tipo}-{tipo_sessao_abrev}-{numero_sessao}-{codigo_ata}-{tipo_ata_abrev}.pdf"
            caminho_saida = os.path.join(PASTA_SAIDA, nome_arquivo)

            # Salva PDF
            with open(caminho_saida, 'wb') as output_file:
                pdf_writer.write(output_file)

            tamanho_kb = os.path.getsize(caminho_saida) / 1024

            ata['nome_arquivo'] = nome_arquivo
            ata['tamanho_kb'] = tamanho_kb
            atas_criadas.append(ata)

            print(f"✓ Criado: {nome_arquivo}")
            print(f"  - Páginas: {ata['pagina_inicio']} a {ata['pagina_final']}")
            print(f"  - Tamanho: {tamanho_kb:.1f} KB")
            print()

    return atas_criadas

def gerar_relatorio(pdf_path, atas_sumario, atas_criadas):
    """Gera relatório detalhado com checklist"""
    print(f"{'='*70}")
    print("GERANDO RELATÓRIO COM CHECKLIST")
    print(f"{'='*70}\n")

    # Cria nome do arquivo de relatório
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_relatorio = f"relatorio_extracao_{timestamp}.txt"

    with open(nome_relatorio, 'w', encoding='utf-8') as f:
        f.write("╔" + "="*68 + "╗\n")
        f.write("║" + " "*68 + "║\n")
        f.write("║" + "RELATÓRIO DE EXTRAÇÃO DE ATAS".center(68) + "║\n")
        f.write("║" + " "*68 + "║\n")
        f.write("╚" + "="*68 + "╝\n\n")

        f.write(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"Arquivo PDF: {pdf_path}\n")
        f.write(f"Relatório: {nome_relatorio}\n\n")

        f.write("="*70 + "\n")
        f.write("RESUMO EXECUTIVO\n")
        f.write("="*70 + "\n\n")

        f.write(f"Total de atas no sumário: {len(atas_sumario)}\n")
        f.write(f"Total de atas criadas: {len(atas_criadas)}\n")
        f.write(f"Status: {'✓ SUCESSO' if len(atas_sumario) == len(atas_criadas) else '✗ FALHA'}\n\n")

        f.write("="*70 + "\n")
        f.write("CHECKLIST DE ATAS\n")
        f.write("="*70 + "\n\n")

        # Cria dicionário de atas criadas para fácil lookup
        atas_criadas_dict = {int(a['numero_sessao']): a for a in atas_criadas}

        for ata in atas_sumario:
            numero = int(ata['numero_sessao'])
            tipo_sessao = ata['tipo_sessao']
            pagina_inicio = ata['pagina_inicio']

            if numero in atas_criadas_dict:
                ata_criada = atas_criadas_dict[numero]
                f.write(f"[✓] Ata {numero:03d}ª {tipo_sessao}\n")
                f.write(f"    Sumário: Página {pagina_inicio}\n")
                f.write(f"    Arquivo: {ata_criada['nome_arquivo']}\n")
                f.write(f"    Páginas: {ata_criada['pagina_inicio']} a {ata_criada['pagina_final']}\n")
                f.write(f"    Tamanho: {ata_criada['tamanho_kb']:.1f} KB\n")
            else:
                f.write(f"[✗] Ata {numero:03d}ª {tipo_sessao}\n")
                f.write(f"    Sumário: Página {pagina_inicio}\n")
                f.write(f"    Status: NÃO FOI CRIADA\n")
            f.write("\n")

        f.write("="*70 + "\n")
        f.write("DETALHES TÉCNICOS\n")
        f.write("="*70 + "\n\n")

        f.write("Atas encontradas no sumário:\n")
        for ata in atas_sumario:
            f.write(f"  - {ata['numero_sessao']}ª {ata['tipo_sessao']} (Página {ata['pagina_inicio']})\n")

        f.write("\nArquivos criados:\n")
        for ata in atas_criadas:
            f.write(f"  - {ata['nome_arquivo']}\n")

    print(f"✓ Relatório criado: {nome_relatorio}\n")
    return nome_relatorio

def main():
    """Função principal"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "TESTE DE EXTRAÇÃO E SEPARAÇÃO DE ATAS".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")

    # Verifica se o PDF existe
    if not os.path.exists(PDF_TESTE):
        print(f"\n✗ Erro: Arquivo não encontrado: {PDF_TESTE}")
        return

    # Extrai data do nome do PDF
    data_sessao = extrair_data_do_pdf(PDF_TESTE)
    if data_sessao:
        print(f"\n✓ Data extraída do PDF: {data_sessao}")
    else:
        print(f"\n⚠ Aviso: Não foi possível extrair a data do PDF")
        data_sessao = "2008-12-01"  # Fallback para o PDF de teste
        print(f"  Usando data padrão: {data_sessao}")

    # Extrai informações do cabeçalho
    info_cabecalho = extrair_info_cabecalho(PDF_TESTE)
    print(f"✓ Informações do cabeçalho extraídas:")
    print(f"  - DCL nº {info_cabecalho['numero_dcl']}")
    print(f"  - Data: {info_cabecalho['data_formatada']}")
    print(f"  - Suplemento: {'Sim' if info_cabecalho['suplemento'] else 'Não'}")

    # Extrai sumário
    texto_sumario, total_paginas = extrair_sumario(PDF_TESTE)

    # Identifica atas
    atas_sumario = identificar_atas(texto_sumario)

    if not atas_sumario:
        print("✗ Nenhuma ata encontrada no sumário")
        return

    # Calcula páginas finais
    atas_sumario = calcular_paginas_finais(atas_sumario, total_paginas)

    # Separa PDF com cabeçalho
    atas_criadas = separar_pdf(PDF_TESTE, atas_sumario, data_sessao, info_cabecalho)

    # Gera relatório
    gerar_relatorio(PDF_TESTE, atas_sumario, atas_criadas)

    # Resumo final
    print(f"{'='*70}")
    print("RESUMO FINAL")
    print(f"{'='*70}\n")
    print(f"✓ Total de atas encontradas: {len(atas_sumario)}")
    print(f"✓ Total de atas criadas: {len(atas_criadas)}")
    print(f"✓ PDFs criados em: {PASTA_SAIDA}/")
    print(f"✓ Padrão de nomenclatura: YYYY-MM-DD-{{codigo_tipo}}-{{tipo_sessao}}-{{numero_sessao}}-{{codigo_ata}}-{{tipo_ata_cod}}.pdf")
    print(f"✓ Teste concluído com sucesso!\n")

if __name__ == '__main__':
    main()

