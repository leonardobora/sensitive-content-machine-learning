# 🚀 COMECE AQUI - Guia de Início Rápido

**Bem-vindo ao projeto de Detecção de Misoginia em Letras de Música usando CNN!**

Este é seu guia de **5 minutos** para começar a usar o projeto imediatamente.

## ⚡ Início Ultra-Rápido (2 comandos)

```bash
# 1. Verificar se tudo está funcionando
python3 scripts/verify_setup.py

# 2. Testar o modelo imediatamente
python3 scripts/quick_test.py
```

Se ambos funcionarem, **parabéns!** O projeto está pronto para uso.

## 🔧 Se Algo Não Funcionar

### Problema: Dependências Faltando
```bash
# Instalar tudo que precisa
pip install -r requirements.txt

# OU instalar manualmente
pip install tensorflow pandas numpy scikit-learn matplotlib seaborn kagglehub
```

### Problema: Modelos Não Encontrados
```bash
# Executar pipeline completo (10-15 min)
python3 scripts/run_full_pipeline.py
```

### Problema: Estrutura de Diretórios
```bash
# Criar diretórios necessários
python3 scripts/setup_directories.py
```

## 🎯 O Que Você Pode Fazer AGORA

### 1. 🧪 Teste Rápido (30 segundos)
```bash
python3 scripts/quick_test.py
```
**O que faz:** Testa o modelo com 9 exemplos pré-definidos

### 2. 🎵 Teste Suas Letras (interativo)
```bash
python3 scripts/interactive_test.py
```
**O que faz:** Permite digitar suas próprias letras e ver o score

### 3. 📊 Ver Dataset Rotulado (1 minuto)
```bash
python3 scripts/explore_labeled_data.py
```
**O que faz:** Mostra as 40 músicas rotuladas manualmente

### 4. 📁 Teste em Lote (seus arquivos)
```bash
# Criar arquivo com suas letras
echo "I love you deeply
She belongs in kitchen
You are amazing" > my_lyrics.txt

# Analisar
python3 scripts/batch_test.py my_lyrics.txt

# Ver resultados
cat results/my_lyrics_scores.csv
```

## 📊 Entendendo os Resultados

### Scores de Misoginia (0.0 - 1.0)
- **0.0-0.2**: 😊 **Muito baixa** - Linguagem respeitosa
- **0.2-0.4**: 🙂 **Baixa** - Alguns estereótipos leves
- **0.4-0.6**: ⚠️ **Moderada** - Objetificação ou linguagem depreciativa
- **0.6-0.8**: 🚨 **Alta** - Linguagem claramente misógina
- **0.8-1.0**: 💀 **Muito alta** - Conteúdo extremamente problemático

### Exemplos de Cada Nível
```
😊 0.1 - "I love and respect you deeply"
🙂 0.3 - "She's pretty but not very smart"
⚠️ 0.5 - "Women belong in the kitchen"
🚨 0.7 - "Shut up bitch, know your place"
💀 0.9 - "I'll beat you into submission"
```

## 🏗️ Estrutura do Projeto

```
📁 sensitive-content-machine-learning/
├── 🚀 scripts/           # Scripts prontos para usar
│   ├── quick_test.py     # ← COMECE AQUI
│   ├── interactive_test.py
│   ├── batch_test.py
│   └── ...
├── 🧠 models/            # Modelos treinados
├── 📊 data/              # Datasets e análises
├── 📈 results/           # Seus resultados
└── 📚 docs/              # Documentação
```

## 🎯 Comandos Mais Úteis

```bash
# Verificar se tudo funciona
python3 scripts/verify_setup.py

# Teste rápido
python3 scripts/quick_test.py

# Teste interativo
python3 scripts/interactive_test.py

# Analisar arquivo
python3 scripts/batch_test.py meu_arquivo.txt

# Ver dados rotulados
python3 scripts/explore_labeled_data.py

# Pipeline completo (se necessário)
python3 scripts/run_full_pipeline.py
```

## 🚨 Solução Rápida de Problemas

### ❌ "No module named tensorflow"
```bash
pip install tensorflow==2.13.1
```

### ❌ "Model not found"
```bash
python3 scripts/run_full_pipeline.py
# Vai baixar dados e treinar modelo (10-15 min)
```

### ❌ "Permission denied"
```bash
chmod +x scripts/*.py
python3 scripts/verify_setup.py
```

### ❌ Muito lento
```bash
# Normal! O modelo roda em CPU
# Primeira execução é mais lenta
```

## 📖 Documentação Completa

- **📋 Setup detalhado**: `SETUP_TUTORIAL.md`
- **🔍 Status do projeto**: `CHECKPOINT.md`
- **📚 Documentação técnica**: `README.md`

## 🎉 Pronto para Começar!

**Comando recomendado para iniciar:**
```bash
python3 scripts/quick_test.py
```

Este comando vai:
1. ✅ Verificar se modelos existem
2. 🧠 Carregar CNN treinada
3. 🎵 Testar com 9 exemplos
4. 📊 Mostrar resultados detalhados
5. 🎯 Sugerir próximos passos

---

**🚀 Divirta-se explorando a detecção de misoginia em letras de música!**

**Dúvidas?** Consulte `SETUP_TUTORIAL.md` ou execute `python3 scripts/verify_setup.py`