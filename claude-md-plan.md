# CLAUDE.md - Plano de Implementação Acelerada para Sistema de Classificação de Conteúdo Sensível em Letras Musicais

Este documento é um guia para iniciar o desenvolvimento do sistema de classificação de conteúdo sensível em letras musicais, projetado especificamente para um prazo de implementação extremamente curto (15 dias). O documento integra engenharia de prompt, configuração de ambiente, desenvolvimento de MVP e priorização de tarefas para otimizar o tempo limitado disponível.

## Contexto do Projeto

Este projeto visa desenvolver um sistema de Machine Learning capaz de classificar conteúdo sensível em letras de música, identificando categorias como misoginia, incitação à violência, depressão, suicídio, racismo, homofobia e relacionamentos tóxicos em contexto cultural. O sistema deve ser desenvolvido com uma abordagem ágil, permitindo entregas incrementais e adaptação rápida, considerando o prazo extremamente curto de 15 dias até 17/06/2025.

## Objetivo deste Documento

Este documento serve como um blueprint para inicialização do projeto e guia para o trabalho do Claude Code e da equipe. O objetivo é proporcionar:

1. Estrutura inicial do repositório e ambiente de desenvolvimento
2. Estratégia de MVP com priorização clara
3. Abordagem técnica recomendada
4. Distribuição de responsabilidades para a equipe
5. Timeline detalhada para os 15 dias disponíveis

## Estrutura do Repositório

A estrutura inicial do repositório deve ser criada com os seguintes diretórios e arquivos:

```
text-classification-sensitive-content/
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   ├── raw/
│   ├── processed/
│   └── labeled/
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_model_training.ipynb
│   └── 04_model_evaluation.ipynb
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── data_collection.py
│   │   ├── data_preprocessing.py
│   │   └── data_labeling.py
│   ├── features/
│   │   ├── __init__.py
│   │   └── feature_engineering.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── model_training.py
│   │   └── model_evaluation.py
│   └── visualization/
│       ├── __init__.py
│       └── visualize.py
├── tests/
│   ├── __init__.py
│   ├── test_data.py
│   └── test_models.py
├── app/
│   ├── __init__.py
│   ├── app.py
│   └── static/
├── docs/
│   └── model_card.md
├── .gitignore
├── README.md
├── requirements.txt
├── setup.py
└── Makefile
```

## Estratégia de MVP e Priorização

Considerando o prazo extremamente curto de 15 dias, é essencial adotar uma estratégia de MVP focada e com priorização clara. Utilizando o método MoSCoW de priorização:

### MUST (Obrigatório)
- Dataset mínimo mas representativo (~500 exemplos rotulados)
- Pipeline de pré-processamento básico para texto
- Modelo de classificação binary (sensível/não-sensível) baseado em Transfer Learning (DistilBERT)
- Interface básica de linha de comando para teste
- Documentação mínima de uso

### SHOULD (Deveria ter)
- Métricas básicas de avaliação (precision, recall, F1)
- Matriz de confusão e visualizações básicas
- Dataset expandido (~1000 exemplos)
- Pequena interface web com Streamlit
- Classificação multi-label para pelo menos 3 categorias principais (ex: misoginia, violência, depressão)

### COULD (Poderia ter)
- Dashboard de análise com visualizações mais completas
- Classificação para todas as categorias propostas
- API REST básica para integração
- Relatórios detalhados por categoria
- Testes unitários e de integração

### WON'T (Não terá nesta versão)
- Sistema de feedback do usuário
- Interface gráfica elaborada
- Integração com outros sistemas
- Módulos avançados de explicabilidade de modelo
- Monitoramento contínuo de performance

## Estratégia Técnica

Para maximizar a velocidade de desenvolvimento, recomendamos:

### 1. Dataset & Rotulagem
- Utilizar um conjunto pequeno mas representativo de letras musicais (~500 exemplos)
- Empregar técnicas de rotulagem rápida:
  - Uso de keywords para rotulagem semi-automática
  - Rotulagem manual distribuída entre equipe
  - Possível uso de classificação zero-shot com LLMs para pré-rotulagem

### 2. Modelagem
- Utilizar modelos pré-treinados do Hugging Face
  - Recomendação: DistilBERT para equilíbrio entre performance e velocidade
  - Alternativa leve: FastText para casos extremos de limitação de recursos
- Implementar fine-tuning rápido em dataset pequeno
- Focar em uma abordagem de classificação binária primeiro, expandindo depois

### 3. Infraestrutura & Ferramentas
- Hugging Face Transformers como biblioteca principal
- Pandas e scikit-learn para manipulação de dados e métricas
- Streamlit para interfaces rápidas
- GitHub para controle de versão e CI/CD simples
- Notebooks Jupyter/Colab para prototipagem rápida

### 4. Deployment
- Deployment local como MVP
- Streamlit para dashboard simples
- Arquivos de exemplo para demonstração offline

## Distribuição de Responsabilidades (conforme planejamento anterior)

### Leonardo (Tech Lead e Mentor Principal)
- Definição da arquitetura geral
- Setup inicial do repositório e ambientes
- Mentoria técnica da equipe
- Revisão de código crítico
- Definição do pipeline de ML

### Letícia (Product Owner Técnico e Especialista em Experimentação)
- Definição de critérios de aceitação para o modelo
- Gerenciamento do backlog técnico
- Experimentação com diferentes modelos
- Validação de resultados

### Nathan (Data Steward e Especialista em Engenharia de Features)
- Exploração e análise de dados
- Desenvolvimento do pipeline de pré-processamento
- Criação de features específicas para conteúdo sensível

### Luan (Desenvolvedor Júnior e Especialista em Implementação)
- Implementação de componentes de pré-processamento
- Desenvolvimento de scripts de treinamento
- Execução de experimentos

### Carlos (Desenvolvedor Júnior e Especialista em Testes e Validação)
- Implementação de testes para componentes
- Desenvolvimento de scripts de validação
- Criação de ferramentas para análise de resultados

## Timeline de 15 Dias (02/06/2025 - 17/06/2025)

### Dias 1-2 (02-03/06): Setup e Planejamento
- **Setup do repositório e ambiente**
  - Criar estrutura do repositório
  - Configurar ambiente virtual/Docker
  - Instalar dependências iniciais
  - Configurar CI/CD básico
- **Criação de dataset mínimo para testes iniciais**
  - Coletar ~50 exemplos para testes rápidos
  - Definir esquema de rotulagem
- **Planejamento detalhado de sprint**
  - Divisão detalhada de tarefas para a equipe
  - Estabelecer metas diárias

### Dias 3-5 (04-06/06): Coleta e Processamento de Dados
- **Coleta de dados principal**
  - Obter corpus de letras de músicas (~500 exemplos)
  - Garantir diversidade de gêneros e épocas
- **Rotulagem inicial**
  - Implementar rotulagem semi-automática por keywords
  - Distribuir rotulagem manual entre membros da equipe
- **Desenvolvimento do pipeline de processamento**
  - Implementar limpeza e normalização de texto
  - Criar tokenização e encoding básicos

### Dias 6-8 (07-09/06): Implementação do Modelo Básico
- **Implementação de baseline com DistilBERT**
  - Setup do modelo pré-treinado
  - Fine-tuning para classificação binária
- **Avaliação inicial do modelo**
  - Implementar métricas básicas
  - Analisar resultados preliminares
- **Ajustes e refinamentos**
  - Otimizar hiperparâmetros
  - Refinar pipeline de dados se necessário

### Dias 9-11 (10-12/06): Expansão para Multi-Label e Interface
- **Expansão para classificação multi-label**
  - Adaptar modelo para múltiplas categorias
  - Treinar com dataset expandido
- **Desenvolvimento de interface Streamlit**
  - Criar dashboard básico para demonstração
  - Implementar visualizações básicas
- **Documentação inicial**
  - Criar README e documentação de uso
  - Documentar modelo e abordagem

### Dias 12-13 (13-14/06): Refinamento e Testes
- **Refinamento de modelos**
  - Otimizar baseado nos resultados
  - Implementar técnicas de ensemble se viável
- **Testes extensivos**
  - Testar em diferentes tipos de letras
  - Validar categorias mais desafiadoras
- **Finalização da interface**
  - Adicionar funcionalidades adicionais se houver tempo
  - Polir visualizações

### Dias 14-15 (15-16/06): Finalização e Documentação
- **Revisão geral do código**
  - Garantir código limpo e bem documentado
  - Resolver qualquer bug pendente
- **Documentação final**
  - Completar documentação técnica
  - Criar model card detalhado
  - Documentar limitações e trabalhos futuros
- **Preparação para apresentação**
  - Selecionar exemplos demonstrativos
  - Preparar demonstração do sistema

### Dia 16 (17/06): Entrega Final
- **Entrega do MVP**
  - Garantir que todas as funcionalidades obrigatórias estão implementadas
  - Verificar documentação completa
- **Demonstração do sistema**
  - Apresentar resultados e funcionalidades
  - Mostrar exemplos reais de classificação

## Comandos Principais do Makefile

```makefile
setup:
	pip install -r requirements.txt

lint:
	flake8 src/ --max-line-length=88

test:
	pytest tests/

train:
	python src/models/model_training.py

evaluate:
	python src/models/model_evaluation.py

run-app:
	streamlit run app/app.py

all: lint test
```

## Prompts para Desenvolvimento Rápido com Claude Code

### Prompt para Configuração Inicial do Ambiente

```
Crie um arquivo requirements.txt para um projeto de classificação de texto para conteúdo sensível em letras musicais usando Hugging Face Transformers e Streamlit. O arquivo deve incluir todas as dependências necessárias para:
1. Processamento de dados textuais
2. Treinamento de modelos transformer (DistilBERT)
3. Avaliação de modelos
4. Visualização de resultados
5. Criação de dashboard com Streamlit
```

### Prompt para Criação de Pipeline de Processamento

```
Crie um script Python (data_preprocessing.py) para processar letras de músicas para classificação de conteúdo sensível. O script deve:
1. Limpar e normalizar o texto (remover pontuações especiais, converter para minúsculas, etc.)
2. Implementar tokenização básica
3. Preparar os dados para modelos de Hugging Face
4. Incluir funções para split train/validation/test
5. Lidar com possíveis desbalanceamentos de classe
```

### Prompt para Implementação de Modelo Rápido

```
Crie um script Python (model_training.py) para treinar um modelo DistilBERT para classificação de conteúdo sensível em letras musicais. O script deve:
1. Carregar um modelo pré-treinado do Hugging Face
2. Configurar o modelo para classificação binária (conteúdo sensível/não sensível)
3. Implementar função de fine-tuning com opções de hiperparâmetros configuráveis
4. Salvar o modelo treinado
5. Incluir log básico de métricas durante o treinamento
```

### Prompt para Dashboard Streamlit

```
Crie um aplicativo Streamlit (app.py) para demonstrar a classificação de conteúdo sensível em letras musicais. O aplicativo deve:
1. Permitir entrada de texto direta pelo usuário
2. Mostrar previsões do modelo treinado
3. Visualizar scores de confiança para diferentes categorias de conteúdo sensível
4. Incluir exemplos pré-carregados para demonstração rápida
5. Ter um design limpo e intuitivo
```

## Próximos Passos pós-MVP

Caso seja possível continuar o desenvolvimento após o MVP, sugerimos:

1. Expansão do dataset para maior representatividade
2. Refinamento dos modelos com técnicas avançadas
3. Implementação de explicabilidade (LIME, SHAP)
4. Criação de API robusta para integração
5. Desenvolvimento de interface mais sofisticada
6. Implementação de feedback loop para melhorias contínuas

## Considerações Éticas e Limitações

É fundamental documentar as limitações do sistema, especialmente considerando o prazo curto de desenvolvimento:

1. Viés potencial no dataset limitado
2. Precisão variável entre diferentes categorias de conteúdo sensível
3. Contexto cultural limitado pela amostragem
4. Necessidade de revisão humana para decisões importantes
5. Considerações sobre privacidade e uso responsável

## Conclusão

Este documento fornece um plano acelerado mas viável para implementação de um sistema MVP de classificação de conteúdo sensível em letras musicais no prazo de 15 dias. Seguindo a abordagem ágil proposta, com foco claro em prioridades e utilizando ferramentas modernas de ML, é possível entregar um sistema funcional que demonstre o conceito e forneça valor, mesmo com o prazo extremamente limitado.

O sucesso dependerá da execução focada, colaboração efetiva da equipe e adaptação rápida aos desafios que surgirem durante o desenvolvimento. Mesmo que nem todas as funcionalidades desejadas sejam implementadas no prazo, o objetivo é entregar um sistema que demonstre a viabilidade e o valor da classificação automatizada de conteúdo sensível em letras musicais.