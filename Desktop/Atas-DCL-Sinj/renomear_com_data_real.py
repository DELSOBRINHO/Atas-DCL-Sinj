"""
Script para renomear atas com data REAL extraída do PDF
Usa padrão: YYYY-MM-DD-C-TT-NNN-T-TA.pdf
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from extrair_data_melhorado import extrair_data_melhorado

ATAS_DIR = "atas_circunstanciadas_2007"
ATAS_VALIDADAS_DIR = "atas_circunstanciadas_2007_validadas"
RELATORIO_FILE = "relatorio_renomeacao_data_real.json"

Path(ATAS_VALIDADAS_DIR).mkdir(exist_ok=True)

relatorio = {
    "data_execucao": datetime.now().isoformat(),
    "atas_processadas": 0,
    "atas_renomeadas": 0,
    "atas_sem_data": 0,
    "erros": [],
    "renomeacoes": []
}

def extrair_componentes_nome(nome_arquivo):
    """Extrai componentes do nome do arquivo"""
    # Padrão: YYYY-MM-DD-C-TT-NNN-T-TA.pdf ou variações
    pattern = r'(\d{4})-(\d{2})-(\d{2})?-?(\d)?-?(SO|SE|SS|SP)?-?(\d+)?-?(\d)?-(AC|AS)?'
    match = re.search(pattern, nome_arquivo)
    
    if match:
        return {
            'ano': match.group(1),
            'mes': match.group(2),
            'dia': match.group(3),
            'codigo_tipo': match.group(4),
            'tipo_sessao': match.group(5),
            'numero_sessao': match.group(6),
            'codigo_ata': match.group(7),
            'tipo_ata': match.group(8)
        }
    
    return None

def criar_novo_nome(data_real, componentes_originais):
    """Cria novo nome com data real"""
    # Padrão: YYYY-MM-DD-C-TT-NNN-T-TA.pdf
    
    # Usar data real
    ano, mes, dia = data_real.split('-')
    
    # Usar componentes originais se disponíveis
    codigo_tipo = componentes_originais.get('codigo_tipo', '1') if componentes_originais else '1'
    tipo_sessao = componentes_originais.get('tipo_sessao', 'SO') if componentes_originais else 'SO'
    numero_sessao = componentes_originais.get('numero_sessao', '001') if componentes_originais else '001'
    codigo_ata = componentes_originais.get('codigo_ata', '2') if componentes_originais else '2'
    tipo_ata = componentes_originais.get('tipo_ata', 'AC') if componentes_originais else 'AC'
    
    # Formatar número de sessão com 3 dígitos
    numero_sessao = str(numero_sessao).zfill(3)
    
    novo_nome = f"{ano}-{mes}-{dia}-{codigo_tipo}-{tipo_sessao}-{numero_sessao}-{codigo_ata}-{tipo_ata}.pdf"
    return novo_nome

def processar_e_renomear():
    """Processa atas e renomeia com data real"""
    
    if not os.path.exists(ATAS_DIR):
        print(f"❌ Diretório {ATAS_DIR} não encontrado")
        return
    
    print(f"🔍 Renomeando atas com data REAL...\n")
    
    atas_files = sorted([f for f in os.listdir(ATAS_DIR) if f.endswith('.pdf')])
    
    for i, arquivo in enumerate(atas_files, 1):
        pdf_path = os.path.join(ATAS_DIR, arquivo)
        print(f"[{i}/{len(atas_files)}] {arquivo}")
        
        relatorio["atas_processadas"] += 1
        
        # Extrair data real
        data_real = extrair_data_melhorado(pdf_path, verbose=False)
        
        if not data_real:
            print(f"  ⚠️  Data não encontrada")
            relatorio["atas_sem_data"] += 1
            print()
            continue
        
        # Extrair componentes do nome original
        componentes = extrair_componentes_nome(arquivo)
        
        # Criar novo nome
        novo_nome = criar_novo_nome(data_real, componentes)
        
        print(f"  Data real: {data_real}")
        print(f"  Novo nome: {novo_nome}")
        
        # Copiar para diretório validado com novo nome
        import shutil
        novo_caminho = os.path.join(ATAS_VALIDADAS_DIR, novo_nome)
        
        try:
            shutil.copy2(pdf_path, novo_caminho)
            relatorio["atas_renomeadas"] += 1
            relatorio["renomeacoes"].append({
                "original": arquivo,
                "novo": novo_nome,
                "data_real": data_real
            })
            print(f"  ✅ Renomeado")
        except Exception as e:
            print(f"  ❌ Erro: {e}")
            relatorio["erros"].append(f"{arquivo}: {str(e)}")
        
        print()
    
    # Salvar relatório
    with open(RELATORIO_FILE, 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Renomeação concluída!")
    print(f"   Atas processadas: {relatorio['atas_processadas']}")
    print(f"   Atas renomeadas: {relatorio['atas_renomeadas']}")
    print(f"   Atas sem data: {relatorio['atas_sem_data']}")
    print(f"   Relatório: {RELATORIO_FILE}")

if __name__ == "__main__":
    processar_e_renomear()

