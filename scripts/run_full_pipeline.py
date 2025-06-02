#!/usr/bin/env python3
"""
Script para executar o pipeline completo do projeto.
Baixa dados, processa, treina modelo e salva resultados.
"""

import sys
import os
import subprocess
from pathlib import Path
import time

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent.parent / "src"))

def run_command(command, description):
    """Executa comando e mostra progresso."""
    print(f"\n🔄 {description}...")
    print(f"   Comando: {command}")
    
    start_time = time.time()
    
    try:
        # Executar comando
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print(f"   ✅ Concluído em {elapsed:.1f}s")
            return True
        else:
            print(f"   ❌ Erro (código {result.returncode})")
            print(f"   Stdout: {result.stdout[-500:]}")  # Últimas 500 chars
            print(f"   Stderr: {result.stderr[-500:]}")
            return False
            
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"   ❌ Erro após {elapsed:.1f}s: {e}")
        return False

def check_file_exists(file_path, description):
    """Verifica se arquivo existe."""
    if Path(file_path).exists():
        size = Path(file_path).stat().st_size / (1024 * 1024)  # MB
        print(f"   ✅ {description} existe ({size:.1f}MB)")
        return True
    else:
        print(f"   ⚠️  {description} não encontrado")
        return False

def main():
    print("🚀 PIPELINE COMPLETO - DETECÇÃO DE MISOGINIA EM LETRAS")
    print("=" * 70)
    print("Este script executará todo o pipeline do projeto:")
    print("1. Download do dataset Kaggle")
    print("2. Preprocessamento dos dados")
    print("3. Rotulagem manual (simulada)")
    print("4. Sistema de pontuação contínua")
    print("5. Treinamento do modelo CNN")
    print("6. Análise exploratória")
    print("\n⏱️  Tempo estimado: 10-15 minutos")
    
    response = input("\n▶️  Continuar? (y/N): ").strip().lower()
    if response not in ['y', 'yes', 's', 'sim']:
        print("❌ Pipeline cancelado.")
        return
    
    print("\n" + "=" * 70)
    print("🏁 INICIANDO PIPELINE")
    print("=" * 70)
    
    # Lista de comandos para executar
    pipeline_steps = [
        {
            'command': 'python3 src/data/kaggle_loader.py',
            'description': 'Baixando dataset do Kaggle (6,292 músicas)',
            'check_file': 'data/raw/songs_lyrics_dataset.csv',
            'check_desc': 'Dataset principal'
        },
        {
            'command': 'python3 src/data/lyrics_preprocessor.py',
            'description': 'Preprocessando letras e criando features',
            'check_file': 'data/processed/train.csv',
            'check_desc': 'Dados preprocessados'
        },
        {
            'command': 'python3 src/data/complete_manual_labeling.py',
            'description': 'Executando rotulagem manual simulada',
            'check_file': 'data/labeled/manually_labeled_songs.csv',
            'check_desc': 'Músicas rotuladas manualmente'
        },
        {
            'command': 'MPLBACKEND=Agg python3 src/models/continuous_scoring_system.py',
            'description': 'Criando sistema de pontuação contínua',
            'check_file': 'data/processed_continuous/metadata.json',
            'check_desc': 'Sistema de pontuação'
        },
        {
            'command': 'MPLBACKEND=Agg python3 src/models/cnn_misogyny_final.py',
            'description': 'Treinando modelo CNN (pode demorar 5-10 min)',
            'check_file': 'models/cnn_misogyny_final.h5',
            'check_desc': 'Modelo CNN treinado'
        },
        {
            'command': 'MPLBACKEND=Agg python3 src/data/exploratory_analysis.py',
            'description': 'Gerando análise exploratória e visualizações',
            'check_file': 'data/figures/data_exploration.png',
            'check_desc': 'Visualizações'
        }
    ]
    
    # Executar cada passo
    success_count = 0
    total_steps = len(pipeline_steps)
    
    for i, step in enumerate(pipeline_steps, 1):
        print(f"\n{'='*70}")
        print(f"PASSO {i}/{total_steps}: {step['description']}")
        print(f"{'='*70}")
        
        # Verificar se arquivo já existe
        if check_file_exists(step['check_file'], step['check_desc']):
            response = input(f"   ▶️  Arquivo existe. Pular este passo? (Y/n): ").strip().lower()
            if response in ['', 'y', 'yes', 's', 'sim']:
                print(f"   ⏭️  Passo {i} pulado.")
                success_count += 1
                continue
        
        # Executar comando
        success = run_command(step['command'], step['description'])
        
        if success:
            # Verificar se arquivo foi criado
            if check_file_exists(step['check_file'], step['check_desc']):
                success_count += 1
            else:
                print(f"   ⚠️  Comando executou mas arquivo esperado não foi encontrado")
        else:
            print(f"   ❌ Passo {i} falhou!")
            response = input("   ▶️  Continuar mesmo assim? (y/N): ").strip().lower()
            if response not in ['y', 'yes', 's', 'sim']:
                print("❌ Pipeline interrompido.")
                break
    
    # Resumo final
    print("\n" + "=" * 70)
    print("📊 RESUMO DO PIPELINE")
    print("=" * 70)
    
    print(f"✅ Passos concluídos: {success_count}/{total_steps}")
    
    if success_count == total_steps:
        print("🎉 PIPELINE COMPLETO COM SUCESSO!")
        print("\n🎯 PRÓXIMOS PASSOS:")
        print("   • Teste rápido: python3 scripts/quick_test.py")
        print("   • Teste interativo: python3 scripts/interactive_test.py")
        print("   • Ver dados rotulados: python3 scripts/explore_labeled_data.py")
        print("   • Analisar dataset completo: python3 scripts/analyze_full_dataset.py")
        
        # Verificar arquivos importantes
        print("\n📁 ARQUIVOS CRIADOS:")
        important_files = [
            ('models/cnn_misogyny_final.h5', 'Modelo CNN'),
            ('models/tokenizer_final.pkl', 'Tokenizer'),
            ('data/labeled/manually_labeled_songs.csv', '40 músicas rotuladas'),
            ('data/figures/data_exploration.png', 'Visualizações'),
            ('data/processed_continuous/metadata.json', 'Metadados')
        ]
        
        for file_path, desc in important_files:
            if Path(file_path).exists():
                size = Path(file_path).stat().st_size / (1024 * 1024)
                print(f"   ✅ {desc}: {file_path} ({size:.1f}MB)")
            else:
                print(f"   ❌ {desc}: {file_path} (não encontrado)")
    
    elif success_count >= total_steps * 0.7:  # 70% ou mais
        print("⚠️  PIPELINE PARCIALMENTE CONCLUÍDO")
        print("Você pode tentar usar os componentes que funcionaram.")
        print("Execute: python3 scripts/verify_setup.py")
    
    else:
        print("❌ PIPELINE FALHOU")
        print("Muitos passos falharam. Verifique:")
        print("1. Dependências: pip install -r requirements.txt")
        print("2. Setup: python3 scripts/verify_setup.py")
        print("3. Logs de erro acima")

if __name__ == "__main__":
    main()