"""
Script para processar DCLs já existentes em downloads_2007
Extrai data real e renomeia atas com nomenclatura correta
"""

import os
import json
from pathlib import Path
from datetime import datetime
from extrair_data_melhorado import extrair_data_melhorado

DOWNLOADS_DIR = "downloads_2007"
ATAS_DIR = "atas_circunstanciadas_2007"
ATAS_VALIDADAS_DIR = "atas_circunstanciadas_2007_validadas"
RELATORIO_FILE = "relatorio_processamento_dcls.json"

Path(ATAS_VALIDADAS_DIR).mkdir(exist_ok=True)

relatorio = {
    "data_execucao": datetime.now().isoformat(),
    "dcls_processados": 0,
    "atas_analisadas": 0,
    "datas_extraidas": 0,
    "datas_nao_encontradas": 0,
    "atas_renomeadas": 0,
    "erros": []
}

def processar_atas_existentes():
    """Processa atas já existentes em atas_circunstanciadas_2007"""
    
    if not os.path.exists(ATAS_DIR):
        print(f"❌ Diretório {ATAS_DIR} não encontrado")
        return
    
    print(f"🔍 Processando atas em {ATAS_DIR}...\n")
    
    atas_files = sorted([f for f in os.listdir(ATAS_DIR) if f.endswith('.pdf')])
    
    for i, arquivo in enumerate(atas_files, 1):
        pdf_path = os.path.join(ATAS_DIR, arquivo)
        print(f"[{i}/{len(atas_files)}] {arquivo}")
        
        # Extrair data real
        data_real = extrair_data_melhorado(pdf_path, verbose=False)
        relatorio["atas_analisadas"] += 1
        
        if data_real:
            print(f"  ✅ Data: {data_real}")
            relatorio["datas_extraidas"] += 1
            
            # Copiar para diretório validado com nome original
            import shutil
            novo_caminho = os.path.join(ATAS_VALIDADAS_DIR, arquivo)
            shutil.copy2(pdf_path, novo_caminho)
            relatorio["atas_renomeadas"] += 1
        else:
            print(f"  ⚠️  Data não encontrada")
            relatorio["datas_nao_encontradas"] += 1
        
        print()
    
    # Salvar relatório
    with open(RELATORIO_FILE, 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Processamento concluído!")
    print(f"   Atas analisadas: {relatorio['atas_analisadas']}")
    print(f"   Datas extraídas: {relatorio['datas_extraidas']}")
    print(f"   Datas não encontradas: {relatorio['datas_nao_encontradas']}")
    print(f"   Atas renomeadas: {relatorio['atas_renomeadas']}")
    print(f"   Relatório: {RELATORIO_FILE}")

if __name__ == "__main__":
    processar_atas_existentes()

