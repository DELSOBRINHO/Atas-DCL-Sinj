# -*- coding: utf-8 -*-
"""
Debug dos links extraídos de 2007
"""

import json
from pathlib import Path

links_file = Path("links_2007/dcls_2007.json")

print(f"Arquivo: {links_file}")
print(f"Existe: {links_file.exists()}")
print(f"Tamanho: {links_file.stat().st_size} bytes\n")

with open(links_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Tipo de dados: {type(data)}")
print(f"Número de itens: {len(data)}\n")

if isinstance(data, dict):
    print("Estrutura do dicionário:")
    for key in list(data.keys())[:5]:
        print(f"  - {key}: {type(data[key])}")
    print()
    
    # Se for um dicionário com meses
    if all(isinstance(k, str) and k.isdigit() for k in list(data.keys())[:5]):
        print("Parece ser organizado por mês:")
        for mes, links in sorted(data.items()):
            print(f"  Mês {mes}: {len(links)} links")
        
        # Mostrar alguns links
        print("\nPrimeiros 3 links do mês 01:")
        for i, link in enumerate(data.get('01', [])[:3]):
            print(f"  {i+1}. {link}")

elif isinstance(data, list):
    print(f"É uma lista com {len(data)} itens")
    print("\nPrimeiros 3 links:")
    for i, link in enumerate(data[:3]):
        print(f"  {i+1}. {link}")

