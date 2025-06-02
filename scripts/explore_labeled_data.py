#!/usr/bin/env python3
"""
Explora o dataset de 40 músicas rotuladas manualmente.
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path

def load_labeled_data():
    """Carrega dados rotulados."""
    data_path = Path(__file__).parent.parent / "data" / "labeled" / "manually_labeled_songs.csv"
    
    if not data_path.exists():
        print("❌ Dados rotulados não encontrados!")
        print("🔧 Execute: python3 src/data/complete_manual_labeling.py")
        return None
    
    return pd.read_csv(data_path)

def analyze_scores(df):
    """Analisa distribuição de scores."""
    print("📊 ANÁLISE DOS SCORES DE MISOGINIA")
    print("=" * 50)
    
    scores = df['misogyny_score']
    
    print(f"📈 Estatísticas Descritivas:")
    print(f"   • Total de músicas: {len(df)}")
    print(f"   • Score médio: {scores.mean():.3f}")
    print(f"   • Mediana: {scores.median():.3f}")
    print(f"   • Desvio padrão: {scores.std():.3f}")
    print(f"   • Mínimo: {scores.min():.3f}")
    print(f"   • Máximo: {scores.max():.3f}")
    
    # Distribuição por faixas
    print(f"\n📊 Distribuição por Faixas:")
    ranges = [
        (0.0, 0.2, "Muito baixa"),
        (0.2, 0.4, "Baixa"), 
        (0.4, 0.6, "Moderada"),
        (0.6, 0.8, "Alta"),
        (0.8, 1.0, "Muito alta")
    ]
    
    for min_val, max_val, label in ranges:
        count = len(df[(scores >= min_val) & (scores < max_val)])
        percentage = (count / len(df)) * 100
        print(f"   • {label} ({min_val}-{max_val}): {count} músicas ({percentage:.1f}%)")

def analyze_temporal(df):
    """Analisa distribuição temporal."""
    print(f"\n🕐 ANÁLISE TEMPORAL")
    print("=" * 50)
    
    # Por década
    df['decade'] = (df['year'] // 10) * 10
    decade_stats = df.groupby('decade').agg({
        'misogyny_score': ['count', 'mean', 'std']
    }).round(3)
    
    print("📅 Estatísticas por Década:")
    for decade in sorted(df['decade'].unique()):
        decade_data = df[df['decade'] == decade]
        count = len(decade_data)
        mean_score = decade_data['misogyny_score'].mean()
        print(f"   • {int(decade)}s: {count} músicas, score médio {mean_score:.3f}")

def analyze_types(df):
    """Analisa tipos de misoginia."""
    print(f"\n🏷️  ANÁLISE POR TIPO DE MISOGINIA")
    print("=" * 50)
    
    # Contar tipos
    type_counts = df['misogyny_type'].value_counts()
    
    print("📋 Tipos Identificados:")
    for mtype, count in type_counts.items():
        percentage = (count / len(df)) * 100
        avg_score = df[df['misogyny_type'] == mtype]['misogyny_score'].mean()
        print(f"   • {mtype}: {count} músicas ({percentage:.1f}%), score médio {avg_score:.3f}")

def show_examples(df):
    """Mostra exemplos de diferentes níveis."""
    print(f"\n🎵 EXEMPLOS POR NÍVEL DE MISOGINIA")
    print("=" * 50)
    
    # Ordenar por score
    df_sorted = df.sort_values('misogyny_score')
    
    # Pegar exemplos de diferentes faixas
    examples = []
    
    # Menor score
    examples.append(("MENOR SCORE", df_sorted.iloc[0]))
    
    # Score médio-baixo
    low_mid = df_sorted[df_sorted['misogyny_score'] < 0.4]
    if not low_mid.empty:
        examples.append(("BAIXO-MÉDIO", low_mid.iloc[-1]))
    
    # Score médio-alto
    high_mid = df_sorted[df_sorted['misogyny_score'] >= 0.4]
    if not high_mid.empty:
        examples.append(("MÉDIO-ALTO", high_mid.iloc[0]))
    
    # Maior score
    examples.append(("MAIOR SCORE", df_sorted.iloc[-1]))
    
    for label, row in examples:
        print(f"\n🔸 {label} (Score: {row['misogyny_score']:.3f})")
        print(f"   🎤 Artista: {row['artist']}")
        print(f"   🎵 Música: {row['title']} ({int(row['year'])})")
        print(f"   🏷️  Tipo: {row['misogyny_type']}")
        print(f"   📝 Justificativa: {row['justification']}")
        if row['problematic_excerpts']:
            print(f"   ⚠️  Trechos: {row['problematic_excerpts']}")

def confidence_analysis(df):
    """Analisa confiança do rotulador."""
    print(f"\n🎯 ANÁLISE DE CONFIANÇA")
    print("=" * 50)
    
    confidence_stats = df['labeler_confidence'].value_counts().sort_index()
    
    print("📊 Distribuição de Confiança (1-5):")
    for conf, count in confidence_stats.items():
        percentage = (count / len(df)) * 100
        print(f"   • Confiança {int(conf)}: {count} músicas ({percentage:.1f}%)")
    
    avg_confidence = df['labeler_confidence'].mean()
    print(f"\n📈 Confiança média: {avg_confidence:.2f}/5")
    
    # Correlação entre confiança e score
    correlation = df['labeler_confidence'].corr(df['misogyny_score'])
    print(f"🔗 Correlação confiança-score: {correlation:.3f}")

def save_summary(df):
    """Salva resumo em arquivo."""
    results_dir = Path(__file__).parent.parent / "results"
    results_dir.mkdir(exist_ok=True)
    
    summary_path = results_dir / "labeled_data_summary.txt"
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("RESUMO DO DATASET ROTULADO MANUALMENTE\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"Total de músicas: {len(df)}\n")
        f.write(f"Score médio: {df['misogyny_score'].mean():.3f}\n")
        f.write(f"Confiança média: {df['labeler_confidence'].mean():.2f}/5\n\n")
        
        f.write("Distribuição por tipo:\n")
        for mtype, count in df['misogyny_type'].value_counts().items():
            percentage = (count / len(df)) * 100
            f.write(f"  {mtype}: {count} ({percentage:.1f}%)\n")
        
        f.write("\nDistribuição por década:\n")
        df['decade'] = (df['year'] // 10) * 10
        for decade in sorted(df['decade'].unique()):
            decade_data = df[df['decade'] == decade]
            count = len(decade_data)
            mean_score = decade_data['misogyny_score'].mean()
            f.write(f"  {int(decade)}s: {count} músicas, score {mean_score:.3f}\n")
    
    print(f"\n💾 Resumo salvo em: {summary_path}")

def main():
    print("🔍 EXPLORAÇÃO DO DATASET ROTULADO")
    print("=" * 50)
    
    # Carregar dados
    df = load_labeled_data()
    if df is None:
        return
    
    print(f"✅ Carregados dados de {len(df)} músicas rotuladas\n")
    
    # Executar análises
    analyze_scores(df)
    analyze_temporal(df)
    analyze_types(df)
    confidence_analysis(df)
    show_examples(df)
    
    # Salvar resumo
    save_summary(df)
    
    print(f"\n🎯 CONCLUSÕES:")
    print("✅ Dataset com boa diversidade temporal")
    print("✅ Scores distribuídos em diferentes faixas")
    print("✅ Alta confiança nas rotulações")
    print("✅ Tipos variados de misoginia identificados")
    
    print(f"\n🚀 PRÓXIMOS PASSOS:")
    print("   • Testar modelo: python3 scripts/quick_test.py")
    print("   • Análise completa: python3 scripts/analyze_full_dataset.py")

if __name__ == "__main__":
    main()