# 🚀 Tutorial Completo - Como Assumir o Projeto

Este tutorial te guiará passo a passo para executar o projeto de detecção de misoginia em letras de música usando CNN.

## 📋 Pré-requisitos

### Sistema
- **Python 3.8+** (testado com 3.8, 3.9, 3.10)
- **Git** para clonar o repositório
- **8GB RAM** mínimo recomendado
- **2GB espaço em disco** para dados e modelos

### Verificar Instalações
```bash
# Verificar Python
python3 --version
# Deve mostrar: Python 3.8.x ou superior

# Verificar Git
git --version
# Deve mostrar versão do Git

# Verificar pip
python3 -m pip --version
```

## 🔧 Instalação Completa (10 minutos)

### Passo 1: Clonar e Configurar
```bash
# 1. Clonar repositório
git clone <URL_DO_SEU_REPOSITORIO>
cd sensitive-content-machine-learning

# 2. Verificar estrutura
ls -la
# Deve mostrar: src/, data/, models/, README.md, etc.

# 3. Criar ambiente virtual (opcional mas recomendado)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 4. Atualizar pip
python3 -m pip install --upgrade pip
```

### Passo 2: Instalar Dependências
```bash
# Instalar todas as dependências necessárias
python3 -m pip install -r requirements.txt

# OU instalar manualmente (se requirements.txt não funcionar):
python3 -m pip install tensorflow==2.13.1 pandas numpy scikit-learn matplotlib seaborn kagglehub jupyter

# Verificar instalação do TensorFlow
python3 -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__)"
```

### Passo 3: Executar Script de Verificação
```bash
# Executar script de verificação (criado abaixo)
python3 scripts/verify_setup.py

# Deve mostrar: ✅ Todas as verificações passaram!
```

## 🎯 Execução Rápida (5 minutos)

### Opção A: Testar Modelo Pré-treinado
```bash
# Se os modelos já estão prontos
python3 scripts/quick_test.py

# Deve mostrar predições de exemplo
```

### Opção B: Pipeline Completo (primeira vez)
```bash
# Executar pipeline completo
python3 scripts/run_full_pipeline.py

# Isso vai:
# 1. Baixar dados (se necessário)
# 2. Preprocessar
# 3. Treinar modelo
# 4. Salvar resultados
```

## 📊 Testando Seus Próprios Dados

### Teste Interativo
```bash
# Executar teste interativo
python3 scripts/interactive_test.py

# Permite inserir suas próprias letras e ver scores
```

### Teste em Lote
```bash
# Criar arquivo com suas letras
echo "I love and respect women
Women are smart and capable
She belongs in the kitchen
Shut up and obey me" > my_lyrics.txt

# Testar em lote
python3 scripts/batch_test.py my_lyrics.txt

# Ver resultados
cat results/my_lyrics_scores.csv
```

## 📈 Análises Disponíveis

### Visualizações Prontas
```bash
# Gerar todas as visualizações
python3 scripts/generate_visualizations.py

# Ver resultados em data/figures/
ls data/figures/
```

### Análise do Dataset Completo
```bash
# Aplicar modelo ao dataset completo (6,292 músicas)
python3 scripts/analyze_full_dataset.py

# Gera ranking das músicas mais misóginas
# Resultados em: results/misogyny_rankings.csv
```

### Análise Temporal
```bash
# Análise por décadas
python3 scripts/temporal_analysis.py

# Gera trends por década
# Resultados em: results/decade_analysis.csv
```

## 🔍 Explorando Resultados

### Ver Dataset Rotulado
```bash
# Examinar 40 músicas rotuladas manualmente
python3 scripts/explore_labeled_data.py

# Mostra estatísticas e exemplos
```

### Performance do Modelo
```bash
# Ver métricas detalhadas do modelo
python3 scripts/model_performance.py

# Mostra MSE, MAE, correlação, etc.
```

### Top Rankings
```bash
# Ver top 10 músicas mais/menos misóginas
python3 scripts/show_rankings.py

# Mostra rankings com justificativas
```

## 🛠️ Desenvolvimento e Customização

### Treinar Novo Modelo
```bash
# Re-treinar com parâmetros diferentes
python3 scripts/retrain_model.py --epochs 100 --batch_size 8

# Comparar modelos
python3 scripts/compare_models.py
```

### Adicionar Novas Músicas
```bash
# Rotular novas músicas manualmente
python3 scripts/label_new_songs.py

# Adiciona ao dataset rotulado
```

### Exportar Resultados
```bash
# Exportar para apresentação
python3 scripts/export_results.py

# Gera relatório em PDF/HTML
```

## 📂 Estrutura de Arquivos Importante

```
sensitive-content-machine-learning/
├── 📁 scripts/                    # Scripts utilitários (criados neste tutorial)
│   ├── verify_setup.py           # Verificar instalação
│   ├── quick_test.py             # Teste rápido
│   ├── run_full_pipeline.py      # Pipeline completo
│   ├── interactive_test.py       # Teste interativo
│   └── ...
├── 📁 data/
│   ├── raw/                      # Dataset original (6,292 músicas)
│   ├── labeled/                  # 40 músicas rotuladas manualmente
│   ├── processed_continuous/     # Dados processados para CNN
│   └── figures/                  # Visualizações
├── 📁 models/
│   ├── cnn_misogyny_final.h5     # Modelo CNN treinado
│   ├── tokenizer_final.pkl       # Tokenizer do texto
│   └── model_final_metadata.json # Metadados do modelo
├── 📁 src/                       # Código fonte principal
├── 📁 results/                   # Resultados das análises (criado automaticamente)
└── 📁 notebooks/                 # Jupyter notebooks (opcionais)
```

## ⚡ Comandos Mais Usados

```bash
# Teste rápido
python3 scripts/quick_test.py

# Ver rankings
python3 scripts/show_rankings.py

# Analisar suas letras
python3 scripts/interactive_test.py

# Gerar visualizações
python3 scripts/generate_visualizations.py

# Pipeline completo
python3 scripts/run_full_pipeline.py
```

## 🚨 Solução de Problemas

### Erro: "No module named tensorflow"
```bash
pip install tensorflow==2.13.1
# ou
conda install tensorflow=2.13.1
```

### Erro: "No such file or directory"
```bash
# Verificar se está no diretório correto
pwd
ls README.md  # Deve existir

# Executar scripts de setup
python3 scripts/setup_directories.py
```

### Erro: "Model not found"
```bash
# Re-treinar modelo
python3 scripts/run_full_pipeline.py

# ou baixar modelo pré-treinado
python3 scripts/download_pretrained.py
```

### Performance lenta
```bash
# Usar versão CPU otimizada
export TF_CPP_MIN_LOG_LEVEL=2
python3 scripts/quick_test.py
```

## 📊 O Que Você Pode Fazer Agora

### ✅ Imediato (2 minutos)
- [x] Testar modelo com letras de exemplo
- [x] Ver dataset de 40 músicas rotuladas
- [x] Verificar performance do modelo

### ✅ Análises (10 minutos)
- [x] Ranking das músicas mais misóginas
- [x] Análise temporal por décadas
- [x] Visualizações do dataset

### ✅ Personalização (30 minutos)
- [x] Testar suas próprias letras
- [x] Ajustar parâmetros do modelo
- [x] Gerar relatórios customizados

## 🎯 Próximos Passos Sugeridos

1. **Começar com**: `python3 scripts/quick_test.py`
2. **Explorar**: `python3 scripts/explore_labeled_data.py`
3. **Analisar**: `python3 scripts/analyze_full_dataset.py`
4. **Personalizar**: `python3 scripts/interactive_test.py`

## 📞 Suporte

Se encontrar problemas:

1. **Verificar setup**: `python3 scripts/verify_setup.py`
2. **Ver logs**: Arquivos em `logs/`
3. **Checar documentação**: `README.md` e `CHECKPOINT.md`
4. **Executar diagnóstico**: `python3 scripts/diagnose.py`

---

🎉 **Pronto!** Você agora tem tudo para assumir e executar o projeto completamente.

**Comando de início recomendado:**
```bash
python3 scripts/quick_test.py
```