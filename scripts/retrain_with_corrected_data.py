#!/usr/bin/env python3
"""
Script para retreinar o modelo CNN com o dataset corrigido.
"""

import sys
from pathlib import Path

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent.parent))

from src.models.cnn_misogyny_final import CNNMisogynyFinal

def main():
    print("="*70)
    print("🔄 RETREINANDO MODELO COM DATASET CORRIGIDO")
    print("="*70)
    
    # Inicializar modelo
    cnn = CNNMisogynyFinal()
    
    # Carregar e preparar dados
    data = cnn.load_and_prepare_data()
    
    # Construir modelo
    cnn.build_optimized_cnn()
    
    # Treinar modelo
    print("\n📊 Iniciando treinamento...")
    cnn.train_with_augmentation(
        data,
        epochs=100,
        batch_size=16
    )
    
    # Avaliar modelo
    print("\n📈 Avaliando modelo...")
    results, y_pred = cnn.comprehensive_evaluation(data)
    
    # Salvar modelo
    print("\n💾 Salvando modelo...")
    model_paths = cnn.save_final_model()
    
    # Visualizar resultados
    plot_path = cnn.create_comprehensive_plots(data, y_pred)
    
    print("\n✅ Retreinamento concluído com sucesso!")
    print(f"MSE no teste: {results['teste']['mse']:.4f}")
    print(f"MAE no teste: {results['teste']['mae']:.4f}")
    
    # Testar com alguns exemplos
    print("\n🧪 Testando com exemplos:")
    test_lyrics = [
        "I love and respect all women",
        "She belongs in the kitchen making me food",
        "Independent woman doing her own thing"
    ]
    
    scores = cnn.predict_songs(test_lyrics)
    for lyrics, score in zip(test_lyrics, scores):
        level = "BAIXO" if score < 0.3 else "MÉDIO" if score < 0.6 else "ALTO"
        print(f"  '{lyrics[:50]}...' -> Score: {score:.2f} ({level})")

if __name__ == "__main__":
    main()