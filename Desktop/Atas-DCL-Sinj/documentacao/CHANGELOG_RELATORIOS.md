# 📝 CHANGELOG - RELATÓRIOS DE CONFERÊNCIA

**Arquivo Base:** `relatorio_atas_2007_atualizado.xlsx`

---

## 📋 HISTÓRICO DE VERSÕES

### v1.3 - 2026-01-07 (ATUAL) ✅
**Data de Criação:** 2026-01-07
**Arquivo:** `v1.3_2026-01-07.xlsx`
**Status:** ✅ Disponível

#### Características
- Total de atas: 111 (87 ordinárias + 22 extraordinárias)
- **Nova Coluna:** Data Publicação DCL
- Colunas: Sessão, Tipo, Data Real, **Data Publicação DCL**, Pág Início, Pág Fim, DCL Original, Nomenclatura, Validado, Observação, Ações
- Atas extraordinárias 20 e 21 adicionadas

#### Mudanças
- Adicionada coluna "Data Publicação DCL" extraída do nome do arquivo
- Padrão de extração: DCL_YYYY-MM-NNNNNNNNNN.pdf → 01/MM/YYYY
- Campo `data_publicacao_dcl` adicionado ao JSON
- Atas 20 e 21 extraordinárias incluídas (27/09/2007 e 02/10/2007)

#### Benefícios
- Rastreamento de quando cada ata foi publicada no DCL
- Identificação de atrasos entre data da sessão e publicação
- Melhor organização cronológica dos documentos

---

### v1.0 - 2026-01-06 (INICIAL)
**Data de Criação:** 2026-01-06  
**Arquivo:** `v1.0_2026-01-06.xlsx`  
**Status:** ✅ Disponível

#### Características
- Total de atas: 108
- Colunas: Sessão, Tipo, Data Real, Pág Início, Pág Fim, DCL Original, Nomenclatura
- Duplicatas removidas: 10
- Atas adicionadas: 3 (84, 85, 86)
- Atas faltando: 35 (25 ord + 10 ext)

#### Mudanças
- Criação do relatório inicial após limpeza de dados
- Remoção de 10 duplicatas
- Adição de atas 84, 85, 86
- Correção de páginas finais de 6 atas

---

### v1.2 - 2026-01-06 ✅
**Data de Criação:** 2026-01-06
**Arquivo:** `v1.2_2026-01-06.xlsx`
**Status:** ✅ Disponível

#### Características
- Total de atas: 111 (87 ordinárias + 22 extraordinárias)
- Colunas: Sessão, Tipo, Data Real, Pág Início, Pág Fim, DCL Original, Nomenclatura, Validado, Observação, Ações
- Atas extraordinárias 20 e 21 adicionadas

#### Mudanças
- Adicionadas Sessões 20 e 21 (EXTRAORDINÁRIAS)
- Sessão 20: 27/09/2007 - Pág 1-2
- Sessão 21: 02/10/2007 - Pág 2-3
- DCL Original: DCL_2007-11-1766369269.pdf

---

### v1.1 - 2026-01-06
**Data de Criação:** 2026-01-06
**Arquivo:** `v1.1_2026-01-06.xlsx`
**Status:** ✅ Disponível

#### Características
- Total de atas: 109 (adicionada ata 001)
- Colunas: Sessão, Tipo, Data Real, Pág Início, Pág Fim, DCL Original, Nomenclatura, Validado, Observação, Ações
- Ata 001 adicionada na primeira posição

#### Mudanças
- Adicionada Sessão 001 (ORDINÁRIA) - 01/02/2007 - Pág 10-22
- Ata inserida na primeira posição da tabela
- Nomenclatura: 2007-02-01-1-SO-001-2-AC.pdf
- DCL Original: DCL_2007-03-044.pdf

#### Critérios de Validação
- [x] Data real confirmada: 01/02/2007
- [x] Páginas inicial e final confirmadas: 10-22
- [x] DCL original confirmado: DCL_2007-03-044.pdf
- [x] Nomenclatura correta: 2007-02-01-1-SO-001-2-AC.pdf

---

### v1.2 - 2026-01-06 (ATUAL)
**Data de Criação:** 2026-01-06
**Arquivo:** `v1.2_2026-01-06.xlsx`
**Status:** ✅ Disponível

#### Características
- Total de atas: 111 (adicionadas atas 20 e 21 extraordinárias)
- Colunas: Sessão, Tipo, Data Real, Pág Início, Pág Fim, DCL Original, Nomenclatura, Validado, Observação, Ações
- Atas extraordinárias 20 e 21 adicionadas

#### Mudanças
- Adicionada Sessão 20 (EXTRAORDINÁRIA) - 27/09/2007 - Pág 1-2
- Adicionada Sessão 21 (EXTRAORDINÁRIA) - 02/10/2007 - Pág 2-3
- DCL Original: DCL_2007-11-1766369269.pdf
- Nomenclaturas: 2007-09-27-2-SE-020-2-AC.pdf e 2007-10-02-2-SE-021-2-AC.pdf

#### Critérios de Validação
- [x] Data real confirmada: 27/09/2007 e 02/10/2007
- [x] Páginas inicial e final confirmadas: 1-2 e 2-3
- [x] DCL original confirmado: DCL_2007-11-1766369269.pdf
- [x] Nomenclaturas corretas: 2007-09-27-2-SE-020-2-AC.pdf e 2007-10-02-2-SE-021-2-AC.pdf

---

### v1.3 - 2026-01-27 (PLANEJADO)
**Data Prevista:** 2026-01-27  
**Arquivo:** `v1.3_2026-01-27.xlsx`  
**Status:** ⏳ Pendente

#### Mudanças Planejadas
- Adicionar todas as 35 atas faltantes
- Corrigir páginas finais das atas 104, 108, 109, 16, 17
- Validação completa de todas as atas

---

## 🔄 PROCESSO DE VERSIONAMENTO

### Nomenclatura
```
v{MAJOR}.{MINOR}_{YYYY-MM-DD}.xlsx
```

### Regras
1. **MAJOR:** Incrementar quando há mudanças significativas (ex: adição de 10+ atas)
2. **MINOR:** Incrementar para correções e ajustes menores
3. **Data:** Data da criação da versão

### Backup
- Manter todas as versões anteriores
- Permitir rollback se necessário
- Documentar motivo de cada versão

---

## 📊 COMPARAÇÃO DE VERSÕES

| Versão | Data | Atas | Ord | Ext | Validadas | Faltando | Status |
|--------|------|------|-----|-----|-----------|----------|--------|
| v1.0 | 2026-01-06 | 108 | 86 | 20 | 0 | 34 | ✅ |
| v1.1 | 2026-01-06 | 109 | 87 | 20 | 1 | 34 | ✅ |
| v1.2 | 2026-01-06 | 111 | 87 | 22 | 2 | 32 | ✅ |
| v1.3 | 2026-01-27 | 120+ | 96 | 30+ | 120+ | 15 | ⏳ |

---

## 🔍 COMO FAZER ROLLBACK

Se precisar voltar para uma versão anterior:

1. Abrir a pasta `documentacao/relatorios_conferencia/`
2. Localizar a versão desejada (ex: `v1.0_2026-01-06.xlsx`)
3. Copiar para a pasta principal como `relatorio_atas_2007_atualizado.xlsx`
4. Atualizar o JSON correspondente se necessário
5. Documentar o motivo do rollback neste arquivo

---

**Última Atualização:** 2026-01-06

