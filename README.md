# Atas DCL-Sinj 2007

Projeto de catalogação, análise e extração de Atas da Câmara Legislativa do Distrito Federal (CLDF) do ano de 2007.

## 📋 Descrição

Este repositório contém scripts e dados para:
- Extrair informações de Atas Circunstanciadas do SINJ (Sistema de Informações Normativas do Judiciário)
- Catalogar e organizar metadados das atas
- Validar e corrigir inconsistências nos dados
- Preparar arquivos para extração e processamento

## 📊 Status Atual - Fase 2

**Total de Atas Catalogadas: 112**
- Atas Ordinárias: 96
- Atas Extraordinárias: 24

### Atas Ainda Faltando: 35
- **Ordinárias (27):** 5ª, 8ª, 9ª, 11ª, 18ª, 22ª, 60ª, 71ª, 72ª, 73ª, 74ª, 75ª, 76ª, 77ª, 78ª, 79ª, 80ª, 81ª, 82ª, 83ª, 97ª, 99ª, 115ª, 116ª, 117ª, 118ª, 119ª
- **Extraordinárias (8):** 1ª, 4ª, 11ª, 12ª, 15ª, 19ª, 20ª, 26ª

## 📁 Estrutura do Projeto

```
Desktop/Atas-DCL-Sinj/
├── fase2_atas_2007_final.json          # Arquivo principal com metadados das atas
├── *.py                                 # Scripts de processamento
├── downloads_2007/                      # PDFs dos DCLs baixados
└── links_2007/                          # Links dos DCLs
```

## 🔧 Scripts Principais

### Fase 2 - Análise e Catalogação
- `adicionar_atas_lote2.py` - Adiciona atas encontradas
- `corrigir_atas_corretamente.py` - Corrige inconsistências
- `adicionar_atas_faltantes_100_111.py` - Adiciona atas faltantes
- `corrigir_paginas_finais_correto.py` - Corrige páginas finais

### Análise e Validação
- `analisar_inconsistencias.py` - Identifica duplicatas e erros
- `verificar_atas_*.py` - Verifica atas específicas
- `relatorio_final_lote3.py` - Gera relatório final

## 📝 Formato dos Dados

Cada ata no JSON contém:
```json
{
  "sessao_num": "001",
  "tipo_sessao": "ORDINÁRIA",
  "data_real": "01/02/2007",
  "pag_inicio": 10,
  "pag_fim": 22,
  "dcl_original": "DCL_2007-03-044.pdf",
  "nomenclatura": "2007-02-01-1-SO-001-2-AC.pdf"
}
```

## 🚀 Próximas Fases

- **Fase 3:** Extração de PDFs e renomeação de arquivos
- **Fase 4:** Processamento OCR e validação de conteúdo
- **Fase 5:** Indexação e disponibilização dos dados

## 📌 Últimas Correções (Lote 3)

- ✅ Adicionadas 7 atas faltantes (100, 102, 103, 105, 106, 107, 110)
- ✅ Corrigidas páginas finais de 4 atas
- ✅ Removidas duplicatas e registros inválidos
- ✅ Total de atas: 112

## 👤 Autor

DELMIR BARTOLOMEU SOBRINHO

## 📄 Licença

Este projeto é de código aberto e disponível sob a licença MIT.

