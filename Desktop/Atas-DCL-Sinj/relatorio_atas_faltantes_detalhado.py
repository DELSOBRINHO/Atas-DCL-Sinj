#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime

USUARIO = "omega"
ARQUIVO_JSON = Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/fase2_atas_2007_final.json")

print("\n" + "="*80)
print("RELATÓRIO DETALHADO DE ATAS FALTANTES")
print("="*80)

with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
    atas = json.load(f)

# Mapa de datas das atas sucintas (baseado no site da CLDF)
datas_sucintas = {
    # EXTRAORDINÁRIAS
    1: "04/04/2007",
    2: "02/05/2007",
    3: "02/05/2007",
    4: "03/05/2007",
    5: "09/05/2007",
    6: "10/05/2007",
    7: "16/05/2007",
    8: "16/05/2007",
    9: "06/06/2007",
    10: "13/06/2007",
    11: "19/06/2007",
    12: "27/06/2007",
    13: "29/06/2007",
    14: "29/06/2007",
    15: "02/10/2007",
    16: "12/09/2007",
    17: "13/09/2007",
    18: "18/09/2007",
    19: "19/09/2007",
    20: "27/09/2007",
    21: "02/10/2007",
    22: "17/10/2007",
    23: "18/10/2007",
    24: "23/10/2007",
    25: "25/10/2007",
    26: "31/10/2007",
    27: "13/11/2007",
    28: "27/11/2007",
    29: "28/11/2007",
    30: "29/11/2007",
    31: "04/12/2007",
    32: "05/12/2007",
    33: "11/12/2007",
    34: "12/12/2007",
    35: "13/12/2007",
    36: "14/12/2007",
    37: "14/12/2007",
    38: "15/12/2007",
}

# Datas das ordinárias (aproximadas)
datas_ordinarias = {
    5: "13/02/2007",
    8: "22/02/2007",
    9: "27/02/2007",
    22: "28/03/2007",
    37: "08/05/2007",
    39: "10/05/2007",
    41: "16/05/2007",
    50: "06/06/2007",
    57: "26/06/2007",
    60: "01/08/2007",
    71: "28/08/2007",
    72: "29/08/2007",
    73: "30/08/2007",
    74: "04/09/2007",
    75: "05/09/2007",
    76: "06/09/2007",
    77: "11/09/2007",
    78: "12/09/2007",
    79: "13/09/2007",
    80: "18/09/2007",
    81: "19/09/2007",
    82: "20/09/2007",
    83: "25/09/2007",
    84: "26/09/2007",
    85: "27/09/2007",
    86: "02/10/2007",
    97: "25/10/2007",
    99: "31/10/2007",
    107: "21/11/2007",
    110: "28/11/2007",
    112: "04/12/2007",
    113: "05/12/2007",
    114: "06/12/2007",
    115: "11/12/2007",
    116: "12/12/2007",
    117: "13/12/2007",
}

# Extrair atas que temos
atas_existentes = {}
for ata in atas:
    sessao_num = int(ata['sessao_num'])
    tipo = ata['tipo_sessao']
    
    if tipo == 'EXTRAORDINÁRIA':
        atas_existentes[sessao_num] = ata
    else:
        atas_existentes[100 + sessao_num] = ata

# Gerar relatório
relatorio = []
relatorio.append("ATAS CIRCUNSTANCIADAS FALTANTES - RELATÓRIO DETALHADO")
relatorio.append("="*80)
relatorio.append("")

# EXTRAORDINÁRIAS FALTANTES
extraordinarias_faltantes = [1, 4, 11, 12, 15, 19, 20, 26, 31, 32, 33, 34, 35, 36, 37, 38]
relatorio.append(f"EXTRAORDINÁRIAS FALTANTES ({len(extraordinarias_faltantes)}):")
relatorio.append("-"*80)
for num in extraordinarias_faltantes:
    data = datas_sucintas.get(num, "Data não disponível")
    relatorio.append(f"  {num:2d}ª Sessão Extraordinária - {data}")

relatorio.append("")

# ORDINÁRIAS FALTANTES
ordinarias_faltantes = [5, 8, 9, 22, 37, 39, 41, 50, 57, 60, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 97, 99, 107, 110, 112, 113, 114, 115, 116, 117]
relatorio.append(f"ORDINÁRIAS FALTANTES ({len(ordinarias_faltantes)}):")
relatorio.append("-"*80)
for num in ordinarias_faltantes:
    data = datas_ordinarias.get(num, "Data não disponível")
    relatorio.append(f"  {num:3d}ª Sessão Ordinária - {data}")

relatorio.append("")
relatorio.append("="*80)
relatorio.append(f"TOTAL DE ATAS FALTANTES: {len(extraordinarias_faltantes) + len(ordinarias_faltantes)}")
relatorio.append("="*80)

# Salvar relatório
with open(Path(f"C:/Users/{USUARIO}/Desktop/Atas-DCL-Sinj/atas_faltantes_detalhado.txt"), 'w', encoding='utf-8') as f:
    f.write("\n".join(relatorio))

print("\n".join(relatorio))

