#!/usr/bin/env python3
"""
Teste em lote - analisa múltiplas letras de um arquivo.
"""

import sys
import os
from pathlib import Path
import pandas as pd

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
    
    def predict_batch(model, tokenizer, lyrics_list):
        """Prediz scores para lista de letras."""
        if not lyrics_list:
            return []
        
        # Tokenizar
        sequences = tokenizer.texts_to_sequences(lyrics_list)
        
        # Padding
        X = pad_sequences(sequences, maxlen=300, padding='post', truncating='post')
        
        # Predizer
        scores = model.predict(X, verbose=0).flatten()
        
        return scores
    
    def interpret_score(score):
        """Interpreta o score."""
        if score < 0.2:
            return "MUITO BAIXA", "😊"
        elif score < 0.4:
            return "BAIXA", "🙂"
        elif score < 0.6:
            return "MODERADA", "⚠️"
        elif score < 0.8:
            return "ALTA", "🚨"
        else:
            return "MUITO ALTA", "💀"
    
    def load_lyrics_file(file_path):
        """Carrega letras de arquivo."""
        if not Path(file_path).exists():
            print(f"❌ Arquivo não encontrado: {file_path}")
            return []
        
        lyrics = []
        
        # Tentar diferentes formatos
        if file_path.endswith('.csv'):
            # CSV com coluna 'lyrics'
            try:
                df = pd.read_csv(file_path)
                if 'lyrics' in df.columns:
                    lyrics = df['lyrics'].fillna('').tolist()
                else:
                    print("❌ CSV deve ter coluna 'lyrics'")
                    return []
            except Exception as e:
                print(f"❌ Erro ao ler CSV: {e}")
                return []
        
        else:
            # Arquivo texto simples
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lyrics = [line.strip() for line in f if line.strip()]
            except Exception as e:
                print(f"❌ Erro ao ler arquivo: {e}")
                return []
        
        return lyrics
    
    def save_results(results, output_path):
        """Salva resultados em CSV."""
        df = pd.DataFrame(results)
        
        # Criar diretório se não existir
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"💾 Resultados salvos em: {output_path}")
    
    def main():
        if len(sys.argv) != 2:
            print("🎵 TESTE EM LOTE - DETECÇÃO DE MISOGINIA")
            print("=" * 50)
            print("Uso: python3 scripts/batch_test.py <arquivo_letras>")
            print("\nFormatos suportados:")
            print("• Arquivo texto (.txt) - uma letra por linha")
            print("• CSV (.csv) - coluna 'lyrics' obrigatória")
            print("\nExemplo:")
            print("  python3 scripts/batch_test.py my_lyrics.txt")
            print("  python3 scripts/batch_test.py data.csv")
            return
        
        input_file = sys.argv[1]
        
        print(f"🎵 TESTE EM LOTE - {input_file}")
        print("=" * 60)
        
        # Carregar modelo
        print("📥 Carregando modelo...")
        model, tokenizer = load_model()
        if model is None:
            return
        
        # Carregar letras
        print(f"📖 Carregando letras de {input_file}...")
        lyrics_list = load_lyrics_file(input_file)
        
        if not lyrics_list:
            print("❌ Nenhuma letra encontrada no arquivo.")
            return
        
        print(f"✅ Carregadas {len(lyrics_list)} letras")
        
        # Filtrar letras muito curtas
        valid_lyrics = [(i, lyric) for i, lyric in enumerate(lyrics_list) if len(lyric.strip()) >= 3]
        
        if len(valid_lyrics) != len(lyrics_list):
            print(f"⚠️  {len(lyrics_list) - len(valid_lyrics)} letras muito curtas foram ignoradas")
        
        if not valid_lyrics:
            print("❌ Nenhuma letra válida encontrada.")
            return
        
        # Fazer predições
        print(f"🔮 Analisando {len(valid_lyrics)} letras...")
        
        indices, lyrics_clean = zip(*valid_lyrics)
        scores = predict_batch(model, tokenizer, lyrics_clean)
        
        # Processar resultados
        results = []
        
        print(f"\n📊 RESULTADOS:")
        print("-" * 80)
        
        for i, (orig_idx, lyric, score) in enumerate(zip(indices, lyrics_clean, scores)):
            level, emoji = interpret_score(score)
            
            # Truncar letra para display
            lyric_display = lyric[:60] + "..." if len(lyric) > 60 else lyric
            
            print(f"{i+1:3d}. {emoji} {score:.3f} ({level:>10}) - \"{lyric_display}\"")
            
            results.append({
                'index': orig_idx + 1,
                'lyrics': lyric,
                'misogyny_score': round(score, 4),
                'level': level,
                'emoji': emoji
            })
        
        # Estatísticas
        print(f"\n📈 ESTATÍSTICAS:")
        print(f"   • Score médio: {np.mean(scores):.3f}")
        print(f"   • Score mínimo: {np.min(scores):.3f}")
        print(f"   • Score máximo: {np.max(scores):.3f}")
        print(f"   • Desvio padrão: {np.std(scores):.3f}")
        
        # Distribuição
        muito_baixa = sum(1 for s in scores if s < 0.2)
        baixa = sum(1 for s in scores if 0.2 <= s < 0.4)
        moderada = sum(1 for s in scores if 0.4 <= s < 0.6)
        alta = sum(1 for s in scores if 0.6 <= s < 0.8)
        muito_alta = sum(1 for s in scores if s >= 0.8)
        
        total = len(scores)
        
        print(f"\n📊 DISTRIBUIÇÃO:")
        print(f"   • Muito baixa: {muito_baixa}/{total} ({muito_baixa/total*100:.1f}%)")
        print(f"   • Baixa: {baixa}/{total} ({baixa/total*100:.1f}%)")
        print(f"   • Moderada: {moderada}/{total} ({moderada/total*100:.1f}%)")
        print(f"   • Alta: {alta}/{total} ({alta/total*100:.1f}%)")
        print(f"   • Muito alta: {muito_alta}/{total} ({muito_alta/total*100:.1f}%)")
        
        # Salvar resultados
        output_file = Path("results") / f"{Path(input_file).stem}_scores.csv"
        save_results(results, output_file)
        
        # Top e bottom 3
        results_sorted = sorted(results, key=lambda x: x['misogyny_score'])
        
        print(f"\n🏆 TOP 3 MENOS MISÓGINAS:")
        for i, result in enumerate(results_sorted[:3], 1):
            lyric_short = result['lyrics'][:50] + "..." if len(result['lyrics']) > 50 else result['lyrics']
            print(f"   {i}. {result['misogyny_score']:.3f} - \"{lyric_short}\"")
        
        print(f"\n🚨 TOP 3 MAIS MISÓGINAS:")
        for i, result in enumerate(results_sorted[-3:], 1):
            lyric_short = result['lyrics'][:50] + "..." if len(result['lyrics']) > 50 else result['lyrics']
            print(f"   {i}. {result['misogyny_score']:.3f} - \"{lyric_short}\"")
        
        print(f"\n✅ ANÁLISE CONCLUÍDA!")
        print(f"📁 Resultados detalhados em: {output_file}")

if __name__ == "__main__":
    main()

except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("🔧 Execute: pip install tensorflow pandas numpy")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
    import traceback
    traceback.print_exc()