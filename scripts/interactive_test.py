#!/usr/bin/env python3
"""
Teste interativo do modelo - permite inserir suas próprias letras.
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
    
    def load_model():
        """Carrega modelo e tokenizer."""
        model_path = Path(__file__).parent.parent / "models" / "cnn_misogyny_final.h5"
        tokenizer_path = Path(__file__).parent.parent / "models" / "tokenizer_final.pkl"
        
        if not model_path.exists() or not tokenizer_path.exists():
            print("❌ Modelos não encontrados!")
            print("🔧 Execute: python3 scripts/run_full_pipeline.py")
            return None, None
        
        model = tf.keras.models.load_model(str(model_path))
        
        with open(tokenizer_path, 'rb') as f:
            tokenizer = pickle.load(f)
        
        return model, tokenizer
    
    def predict_lyrics(model, tokenizer, lyrics_text):
        """Prediz score de misoginia para um texto."""
        # Tokenizar
        sequences = tokenizer.texts_to_sequences([lyrics_text])
        
        # Padding
        X = pad_sequences(sequences, maxlen=300, padding='post', truncating='post')
        
        # Predizer
        score = model.predict(X, verbose=0)[0][0]
        
        return score
    
    def interpret_score(score):
        """Interpreta o score e retorna descrição."""
        if score < 0.2:
            return "😊 MUITO BAIXA", "Conteúdo respeitoso e não-misógino"
        elif score < 0.4:
            return "🙂 BAIXA", "Alguns estereótipos leves possíveis"
        elif score < 0.6:
            return "⚠️  MODERADA", "Objetificação ou linguagem depreciativa moderada"
        elif score < 0.8:
            return "🚨 ALTA", "Linguagem claramente depreciativa contra mulheres"
        else:
            return "💀 MUITO ALTA", "Conteúdo extremamente misógino ou violento"
    
    def main():
        print("🎵 TESTE INTERATIVO - DETECÇÃO DE MISOGINIA")
        print("=" * 60)
        print("Insira letras de música para analisar o nível de misoginia")
        print("Digite 'quit' para sair, 'help' para ajuda\n")
        
        # Carregar modelo
        print("📥 Carregando modelo...")
        model, tokenizer = load_model()
        
        if model is None:
            return
        
        print("✅ Modelo carregado com sucesso!\n")
        
        # Loop interativo
        while True:
            print("-" * 60)
            lyrics = input("🎤 Digite a letra da música (ou comando): ").strip()
            
            if lyrics.lower() in ['quit', 'exit', 'sair']:
                print("👋 Obrigado por usar o detector de misoginia!")
                break
            
            elif lyrics.lower() == 'help':
                print("\n📖 AJUDA:")
                print("• Digite qualquer letra de música para análise")
                print("• O sistema retornará um score de 0.0 a 1.0")
                print("• 0.0 = Não misógino, 1.0 = Extremamente misógino")
                print("• Comandos: 'quit' (sair), 'help' (ajuda), 'examples' (exemplos)")
                continue
            
            elif lyrics.lower() == 'examples':
                print("\n📝 EXEMPLOS PARA TESTAR:")
                examples = [
                    "I love and respect you deeply",
                    "She's beautiful and intelligent",  
                    "Women belong in the kitchen",
                    "Shut up and do what I say"
                ]
                for i, ex in enumerate(examples, 1):
                    print(f"   {i}. \"{ex}\"")
                print("\nCopie e cole qualquer exemplo acima para testar.")
                continue
            
            elif len(lyrics) < 3:
                print("⚠️  Texto muito curto. Digite pelo menos 3 caracteres.")
                continue
            
            # Fazer predição
            print("\n🔮 Analisando...")
            try:
                score = predict_lyrics(model, tokenizer, lyrics)
                level, description = interpret_score(score)
                
                print(f"\n📊 RESULTADO:")
                print(f"   Score: {score:.3f}")
                print(f"   Nível: {level}")
                print(f"   Descrição: {description}")
                
                # Explicação adicional
                if score < 0.3:
                    print("   💡 Este texto mostra linguagem respeitosa.")
                elif score < 0.6:
                    print("   💡 Detectados alguns elementos problemáticos.")
                else:
                    print("   💡 ATENÇÃO: Conteúdo com misoginia significativa detectada.")
                
                # Mostrar palavras tokenizadas (para debug)
                sequences = tokenizer.texts_to_sequences([lyrics])
                word_indices = sequences[0] if sequences[0] else []
                
                if len(word_indices) > 0:
                    # Mostrar algumas palavras reconhecidas
                    index_to_word = {v: k for k, v in tokenizer.word_index.items()}
                    recognized_words = [index_to_word.get(idx, f"<{idx}>") for idx in word_indices[:10]]
                    print(f"   🔤 Palavras reconhecidas: {', '.join(recognized_words)}")
                else:
                    print("   ⚠️  Poucas palavras reconhecidas pelo modelo.")
                
            except Exception as e:
                print(f"❌ Erro na análise: {e}")
                continue
    
    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("🔧 Execute: pip install tensorflow pandas numpy")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
    print("🔧 Verifique o setup: python3 scripts/verify_setup.py")