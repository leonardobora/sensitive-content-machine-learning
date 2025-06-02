#!/usr/bin/env python3
"""
Teste rápido do modelo CNN de detecção de misoginia.
Carrega o modelo treinado e faz predições em exemplos.
"""

import sys
import os
from pathlib import Path

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent.parent / "src"))

try:
    import tensorflow as tf
    import pickle
    import numpy as np
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    import warnings
    warnings.filterwarnings('ignore')
    
    print("🚀 TESTE RÁPIDO DO MODELO CNN")
    print("=" * 50)
    
    # Verificar se modelos existem
    model_path = Path(__file__).parent.parent / "models" / "cnn_misogyny_final.h5"
    tokenizer_path = Path(__file__).parent.parent / "models" / "tokenizer_final.pkl"
    
    if not model_path.exists():
        print("❌ Modelo não encontrado em:", model_path)
        print("🔧 Execute: python3 scripts/run_full_pipeline.py")
        sys.exit(1)
    
    if not tokenizer_path.exists():
        print("❌ Tokenizer não encontrado em:", tokenizer_path)
        print("🔧 Execute: python3 scripts/run_full_pipeline.py")
        sys.exit(1)
    
    print("📥 Carregando modelo CNN...")
    
    # Carregar modelo
    try:
        model = tf.keras.models.load_model(str(model_path))
        print(f"   ✅ Modelo carregado ({model.count_params():,} parâmetros)")
    except Exception as e:
        print(f"   ❌ Erro ao carregar modelo: {e}")
        sys.exit(1)
    
    # Carregar tokenizer
    try:
        with open(tokenizer_path, 'rb') as f:
            tokenizer = pickle.load(f)
        vocab_size = len(tokenizer.word_index)
        print(f"   ✅ Tokenizer carregado ({vocab_size:,} palavras no vocabulário)")
    except Exception as e:
        print(f"   ❌ Erro ao carregar tokenizer: {e}")
        sys.exit(1)
    
    print("\n🎵 Testando com letras de exemplo...")
    
    # Letras de teste
    test_lyrics = [
        # Baixo score esperado
        "I love and respect you deeply, you are amazing and intelligent",
        "Dancing together under the beautiful stars tonight",
        "You are strong, independent, and capable of anything",
        
        # Score médio esperado
        "She's pretty but not very smart, typical woman behavior",
        "Girls are emotional and can't handle serious work",
        "You look sexy in that dress, come here baby",
        
        # Score alto esperado
        "Shut up bitch, know your place in the kitchen",
        "Women are stupid whores, only good for one thing",
        "I'll teach you to obey me, you worthless slut"
    ]
    
    def predict_scores(lyrics_list):
        """Prediz scores para lista de letras."""
        # Tokenizar
        sequences = tokenizer.texts_to_sequences(lyrics_list)
        
        # Padding
        max_length = 300  # Mesmo usado no treinamento
        X = pad_sequences(sequences, maxlen=max_length, padding='post', truncating='post')
        
        # Predizer
        scores = model.predict(X, verbose=0).flatten()
        
        return scores
    
    # Fazer predições
    print("🔮 Fazendo predições...")
    scores = predict_scores(test_lyrics)
    
    print("\n📊 RESULTADOS:")
    print("-" * 80)
    
    categories = [
        "😊 BAIXA MISOGINIA (esperado 0.0-0.3)",
        "😊 BAIXA MISOGINIA (esperado 0.0-0.3)", 
        "😊 BAIXA MISOGINIA (esperado 0.0-0.3)",
        "⚠️  MISOGINIA MODERADA (esperado 0.3-0.6)",
        "⚠️  MISOGINIA MODERADA (esperado 0.3-0.6)",
        "⚠️  MISOGINIA MODERADA (esperado 0.3-0.6)",
        "🚨 MISOGINIA ALTA (esperado 0.6-1.0)",
        "🚨 MISOGINIA ALTA (esperado 0.6-1.0)",
        "🚨 MISOGINIA ALTA (esperado 0.6-1.0)"
    ]
    
    for i, (lyric, score, category) in enumerate(zip(test_lyrics, scores, categories)):
        # Determinar nível baseado no score
        if score < 0.3:
            level = "BAIXO"
            emoji = "😊"
        elif score < 0.6:
            level = "MÉDIO"
            emoji = "⚠️"
        else:
            level = "ALTO"
            emoji = "🚨"
        
        print(f"\n{i+1:2d}. {emoji} Score: {score:.3f} ({level})")
        print(f"    Categoria: {category}")
        print(f"    Texto: \"{lyric[:60]}{'...' if len(lyric) > 60 else ''}\"")
    
    print("\n" + "=" * 80)
    print("📈 ESTATÍSTICAS DO TESTE:")
    print(f"   • Score médio: {np.mean(scores):.3f}")
    print(f"   • Score mínimo: {np.min(scores):.3f}")
    print(f"   • Score máximo: {np.max(scores):.3f}")
    print(f"   • Desvio padrão: {np.std(scores):.3f}")
    
    # Contar por categoria
    baixo = sum(1 for s in scores if s < 0.3)
    medio = sum(1 for s in scores if 0.3 <= s < 0.6)
    alto = sum(1 for s in scores if s >= 0.6)
    
    print(f"\n📊 DISTRIBUIÇÃO:")
    print(f"   • Baixa misoginia: {baixo}/{len(scores)} ({baixo/len(scores)*100:.1f}%)")
    print(f"   • Misoginia moderada: {medio}/{len(scores)} ({medio/len(scores)*100:.1f}%)")
    print(f"   • Alta misoginia: {alto}/{len(scores)} ({alto/len(scores)*100:.1f}%)")
    
    print("\n✅ TESTE CONCLUÍDO COM SUCESSO!")
    print("\n🎯 PRÓXIMOS PASSOS:")
    print("   • Testar suas letras: python3 scripts/interactive_test.py")
    print("   • Ver dataset completo: python3 scripts/explore_labeled_data.py")
    print("   • Gerar rankings: python3 scripts/analyze_full_dataset.py")
    
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("🔧 Execute: pip install tensorflow pandas numpy")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
    print("🔧 Verifique o setup: python3 scripts/verify_setup.py")
    sys.exit(1)