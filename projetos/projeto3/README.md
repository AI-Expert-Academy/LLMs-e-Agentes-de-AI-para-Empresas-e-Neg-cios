# 📄 Sistema de Triagem e Análise de Currículos

Um sistema inteligente e automatizado para análise de currículos utilizando LLMs (Large Language Models) e IA. A aplicação processa currículos em formato PDF ou documento, extrai informações estruturadas e realiza análise comparativa com vagas em aberto.

## 🎯 Funcionalidades

- **Processamento Automático de Currículos**: Converte documentos PDF em texto estruturado e extrai informações principais
- **Análise com IA**: Utiliza modelos de linguagem (Llama 3.3 70B) para análise profunda de perfis
- **Extração de Dados Estruturados**: Captura automática de:
  - Dados pessoais do candidato
  - Área de atuação profissional
  - Resumo do perfil
  - Habilidades técnicas
  - Formação acadêmica
  - Perguntas sugeridas para entrevista
  - Pontos fortes e áreas de desenvolvimento
  - Recomendações finais
  - Score de compatibilidade (0.0 a 10.0)
  
- **Scoring Inteligente**: Avaliação automática de candidatos com critérios ponderados:
  - Experiência (35%)
  - Habilidades Técnicas (25%)
  - Educação (15%)
  - Pontos Fortes (15%)
  - Desconto por Pontos Fracos (até 10%)

- **Interface Interativa**: Aplicação web responsiva com Streamlit
- **Armazenamento Persistente**: Banco de dados em JSON para consultas futuras

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Função |
|-----------|--------|
| **Streamlit** | Interface de usuário web interativa |
| **LangChain** | Orquestração de LLMs e prompts |
| **Groq** | Provedor de LLM (Llama 3.3 70B) |
| **Docling** | Processamento e conversão de documentos |
| **Pandas** | Manipulação de dados e arquivos CSV |
| **Python 3.x** | Linguagem base |

## 📋 Arquivos do Projeto

```
projeto3/
├── app.py                  # Aplicação principal Streamlit
├── utils_proj03.py         # Funções utilitárias e helpers
├── curriculos.json         # 🔴 BANCO DE DADOS - Armazena currículos processados
├── vagas.csv               # Base de vagas disponíveis
└── README.md               # Este arquivo
```

### 📌 Descrição dos Arquivos

#### `app.py`
Arquivo principal que contém a lógica da aplicação Streamlit:
- Configuração da interface
- Definição da vaga padrão (Desenvolvedor Full Stack)
- Schema JSON para estrutura de dados dos currículos
- Critérios de scoring
- Integração com LLM

#### `utils_proj03.py`
Funções utilitárias reutilizáveis:
- `load_llm()` - Carrega o modelo de linguagem
- `parse_doc()` - Converte documentos para markdown
- `parse_res_llm()` - Faz parsing da resposta do LLM
- `save_json_cv()` - Salva currículos no banco de dados
- `load_json_cv()` - Carrega currículos do banco
- `show_cv_result()` - Formata resultados para exibição

#### `vagas.csv`
Arquivo CSV com as vagas disponíveis no formato:
```
title;description;details
Desenvolvedor(a) Full Stack;descrição...;detalhes...
```

#### `curriculos.json` - 🔴 **BANCO DE DADOS IMPORTANTE**
> ⚠️ **ATENÇÃO**: Este é o arquivo principal de armazenamento!

Armazena todos os currículos processados em formato JSON estruturado:
```json
[
  {
    "name": "João Silva",
    "area": "Desenvolvimento",
    "summary": "...",
    "skills": ["Python", "React", "..."],
    "education": "...",
    "interview_questions": ["...", "...", "..."],
    "strengths": ["..."],
    "areas_for_development": ["..."],
    "important_considerations": ["..."],
    "final_recommendations": "...",
    "score": 8.5
  },
  ...
]
```

## 🚀 Como Usar

### 1. Instalação de Dependências

```bash
pip install streamlit python-dotenv langchain-groq docling pandas
```

### 2. Configuração de Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:
```
GROQ_API_KEY=sua_chave_groq_aqui
```

Obtenha sua chave em: https://console.groq.com/keys

### 3. Executar a Aplicação

```bash
streamlit run app.py
```

A aplicação abrirá em `http://localhost:8501`

### 4. Usar a Aplicação

1. **Upload de Currículo**: Selecione um arquivo PDF ou documento
2. **Processamento**: Clique em "Analisar Currículo"
3. **Visualização**: A análise aparecerá na tela com:
   - Informações estruturadas
   - Pontuação de compatibilidade
   - Recomendações
4. **Armazenamento**: O currículo é automaticamente salvo em `curriculos.json`

## ⚙️ Configuração Personalizada

Você pode editar em `app.py`:

```python
# Modelo de LLM
id_model = "llama-3.3-70b-versatile"

# Criatividade da resposta (0.0 = determinístico, 1.0 = criativo)
temperature = 0.7

# Arquivos
json_file = 'curriculos.json'
path_job_csv = "vagas.csv"
```

## 🔄 Reprocessar Currículos

### 🔴 **IMPORTANTE - LEIA COM ATENÇÃO**

Se você deseja **reprocessar todos os currículos do zero** (por exemplo, após atualizar o prompt ou critérios de scoring):

**É necessário apagar o arquivo `curriculos.json`:**

```bash
# Linux/Mac
rm curriculos.json

# Windows
del curriculos.json
```

Ou delete manualmente pela pasta do projeto.

**Após apagar:**
1. O arquivo será recriado automaticamente
2. Execute novamente o processamento de currículos
3. Os dados serão armazenados com a nova lógica

⚠️ **CUIDADO**: Esta ação é irreversível! Faça backup antes se necessário.

```bash
# Fazer backup antes
cp curriculos.json curriculos.json.backup
```

## 📊 Schema de Dados

Cada currículo analisado segue este schema:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `name` | string | Nome completo do candidato |
| `area` | string | Área principal: Desenvolvimento, Marketing, Vendas, Financeiro, Administrativo, Outros |
| `summary` | string | Resumo objetivo do perfil profissional |
| `skills` | array | Lista de competências técnicas |
| `education` | string | Resumo da formação acadêmica |
| `interview_questions` | array | 3+ perguntas para entrevista |
| `strengths` | array | Pontos fortes e alinhamentos |
| `areas_for_development` | array | Lacunas e pontos a desenvolver |
| `important_considerations` | array | Observações específicas importantes |
| `final_recommendations` | string | Recomendações finais e próximos passos |
| `score` | float | Pontuação de 0.0 a 10.0 |

## 📈 Critérios de Scoring

A pontuação é calculada considerando:

1. **Experiência (35%)**: Posições anteriores, tempo de atuação, similaridade com responsabilidades
2. **Habilidades Técnicas (25%)**: Alinhamento com requisitos técnicos da vaga
3. **Educação (15%)**: Relevância de graduação/certificações
4. **Pontos Fortes (15%)**: Alinhamento dos diferenciais com a vaga
5. **Pontos Fracos (-10%)**: Gravidade dos desalinhamentos

- **10.0**: Candidato supera todas as expectativas
- **8-9**: Muito bem alinhado
- **6-7**: Bom alinhamento
- **4-5**: Alinhamento moderado
- **<4**: Não recomendado

## 🐛 Troubleshooting

### Erro: "API key not found"
- Verifique se o arquivo `.env` está criado
- Confirme que `GROQ_API_KEY` está configurada corretamente

### Erro ao processar documento
- Certifique-se que o PDF não está corrompido
- Tente com outro documento
- Verifique se `docling` está instalada corretamente

### Currículo não aparece após upload
- Verifique se `curriculos.json` tem permissões de escrita
- Confirme que o LLM respondeu corretamente (veja os logs)
- Tente novamente com um documento diferente

## 📝 Exemplos de Uso

### Analisar um novo currículo
```
1. Clique em "Browse files"
2. Selecione um PDF com currículo
3. Aguarde o processamento
4. Veja os resultados estruturados
```

### Consultar currículos armazenados
O arquivo `curriculos.json` pode ser aberto em qualquer editor de texto ou ferramenta JSON.

### Exportar dados
```python
import json

with open('curriculos.json', 'r', encoding='utf-8') as f:
    curriculos = json.load(f)

# Usar pandas para análise
import pandas as pd
df = pd.DataFrame(curriculos)
df.to_csv('curriculos_export.csv', index=False)
```

## 🔒 Segurança e Privacidade

- ✅ Dados armazenados localmente (sem envio para servidores externos além da API da Groq)
- ✅ Chaves de API protegidas em `.env`
- ⚠️ Currículos contêm dados pessoais - proteja o arquivo `curriculos.json`
- 📋 Recomenda-se fazer backup regular dos dados

## 📚 Referências

- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [Groq Console](https://console.groq.com/)
- [Docling Package](https://github.com/DS4SD/docling)

## 📄 Licença

Este projeto é parte do currículo de "LLMs para Empresas e Negócios" da AI Expert Academy.

## 👥 Autor

Desenvolvido para o projeto de Recursos Humanos - IA Expert Academy

---

**Última atualização**: Junho 2026

**Versão**: 1.0

