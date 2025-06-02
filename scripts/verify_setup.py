#!/usr/bin/env python3
"""
Script de verificação do setup do projeto.
Verifica se todas as dependências e arquivos estão presentes.
"""

import sys
import os
import importlib
from pathlib import Path

def check_python_version():
    """Verifica versão do Python."""
    print("🐍 Verificando versão do Python...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} - Requer Python 3.8+")
        return False

def check_dependencies():
    """Verifica se todas as dependências estão instaladas."""
    print("\n📦 Verificando dependências...")
    
    required_packages = {
        'tensorflow': 'TensorFlow',
        'pandas': 'Pandas',
        'numpy': 'NumPy',
        'sklearn': 'Scikit-learn',
        'matplotlib': 'Matplotlib',
        'seaborn': 'Seaborn'
    }
    
    all_good = True
    for package, name in required_packages.items():
        try:
            mod = importlib.import_module(package)
            version = getattr(mod, '__version__', 'unknown')
            print(f"   ✅ {name} {version} - OK")
        except ImportError:
            print(f"   ❌ {name} - NÃO INSTALADO")
            all_good = False
    
    return all_good

def check_project_structure():
    """Verifica estrutura de arquivos do projeto."""
    print("\n📁 Verificando estrutura do projeto...")
    
    required_dirs = [
        'src',
        'src/data',
        'src/models',
        'data',
        'models',
        'scripts',
        'results'
    ]
    
    required_files = [
        'README.md',
        'CHECKPOINT.md',
        'SETUP_TUTORIAL.md',
        'src/data/kaggle_loader.py',
        'src/models/cnn_misogyny_final.py'
    ]
    
    all_good = True
    
    # Verificar diretórios
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"   ✅ Diretório {dir_path}/ - OK")
        else:
            print(f"   ❌ Diretório {dir_path}/ - NÃO ENCONTRADO")
            all_good = False
    
    # Verificar arquivos
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"   ✅ Arquivo {file_path} - OK")
        else:
            print(f"   ❌ Arquivo {file_path} - NÃO ENCONTRADO")
            all_good = False
    
    return all_good

def check_data_files():
    """Verifica se arquivos de dados estão presentes."""
    print("\n💾 Verificando arquivos de dados...")
    
    data_files = {
        'data/raw/songs_lyrics_dataset.csv': 'Dataset principal (6,292 músicas)',
        'data/labeled/manually_labeled_songs.csv': 'Músicas rotuladas manualmente (40)',
        'data/processed_continuous/metadata.json': 'Metadados do processamento'
    }
    
    for file_path, description in data_files.items():
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            size_mb = size / (1024 * 1024)
            print(f"   ✅ {description} - {size_mb:.1f}MB")
        else:
            print(f"   ⚠️  {description} - NÃO ENCONTRADO (será baixado se necessário)")

def check_model_files():
    """Verifica se modelos treinados estão presentes."""
    print("\n🧠 Verificando modelos treinados...")
    
    model_files = {
        'models/cnn_misogyny_final.h5': 'Modelo CNN principal',
        'models/tokenizer_final.pkl': 'Tokenizer do texto',
        'models/model_final_metadata.json': 'Metadados do modelo'
    }
    
    for file_path, description in model_files.items():
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            size_mb = size / (1024 * 1024)
            print(f"   ✅ {description} - {size_mb:.1f}MB")
        else:
            print(f"   ⚠️  {description} - NÃO ENCONTRADO (será treinado se necessário)")

def check_tensorflow():
    """Verifica instalação específica do TensorFlow."""
    print("\n🔥 Verificando TensorFlow...")
    
    try:
        import tensorflow as tf
        print(f"   ✅ TensorFlow {tf.__version__}")
        
        # Verificar se GPU está disponível
        if tf.config.list_physical_devices('GPU'):
            print("   🚀 GPU disponível para TensorFlow")
        else:
            print("   💻 Usando CPU (normal para este projeto)")
        
        # Teste simples
        try:
            x = tf.constant([[1.0, 2.0]])
            print("   ✅ TensorFlow funcionando corretamente")
            return True
        except Exception as e:
            print(f"   ❌ Erro no TensorFlow: {e}")
            return False
            
    except ImportError:
        print("   ❌ TensorFlow não instalado")
        return False

def main():
    """Função principal de verificação."""
    print("🔍 VERIFICAÇÃO DO SETUP DO PROJETO")
    print("=" * 50)
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_tensorflow(),
        check_project_structure(),
        check_data_files(),
        check_model_files()
    ]
    
    print("\n" + "=" * 50)
    print("📋 RESUMO DA VERIFICAÇÃO")
    
    if all(checks[:4]):  # Verificações críticas
        print("✅ SETUP BÁSICO: COMPLETO")
        print("🚀 Você pode executar: python3 scripts/quick_test.py")
    else:
        print("❌ SETUP BÁSICO: INCOMPLETO")
        print("🔧 Execute: pip install -r requirements.txt")
    
    if checks[4]:  # Dados
        print("✅ DADOS: DISPONÍVEIS")
    else:
        print("⚠️  DADOS: Execute python3 src/data/kaggle_loader.py")
    
    if checks[5]:  # Modelos
        print("✅ MODELOS: DISPONÍVEIS")
    else:
        print("⚠️  MODELOS: Execute python3 scripts/run_full_pipeline.py")
    
    print("\n📖 Para mais ajuda: README.md ou SETUP_TUTORIAL.md")

if __name__ == "__main__":
    main()