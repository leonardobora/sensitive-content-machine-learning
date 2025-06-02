import pandas as pd
import numpy as np
import re
from pathlib import Path
import json
from typing import Dict, List, Tuple
import random

class MisogynyLabelingSystem:
    """
    Sistema para rotulagem manual de misoginia e violência contra a mulher em letras de música.
    
    Baseado nos critérios de:
    - UNESCO (2019): Guidelines for Countering Online Violence Against Women Journalists
    - UN Women (2020): Technology-facilitated gender-based violence
    - Anzovino et al. (2018): Automatic Misogyny Identification
    """
    
    def __init__(self, data_path=None):
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.raw_data_path = data_path or self.data_dir / "raw" / "songs_lyrics_dataset.csv"
        self.labeled_data_path = self.data_dir / "labeled"
        self.labeled_data_path.mkdir(exist_ok=True)
        
        # Critérios de pontuação baseados em literatura acadêmica
        self.labeling_criteria = {
            "0.0": {
                "description": "Nenhum conteúdo misógino ou violento",
                "examples": ["Música sobre amor respeitoso", "Letra neutra sem menções de gênero"],
                "indicators": []
            },
            "0.1-0.2": {
                "description": "Linguagem levemente estereotipada",
                "examples": ["Papéis de gênero tradicionais suaves", "Objetificação muito sutil"],
                "indicators": ["ela é uma princesa", "doce menina", "frágil como uma flor"]
            },
            "0.3-0.4": {
                "description": "Objetificação ou estereótipos moderados",
                "examples": ["Redução da mulher à aparência física", "Papéis submissos explícitos"],
                "indicators": ["só serve para", "corpo perfeito", "ela obedece", "made for me"]
            },
            "0.5-0.6": {
                "description": "Linguagem claramente depreciativa",
                "examples": ["Insultos baseados em gênero", "Desvalorização de capacidades"],
                "indicators": ["mulherzinha", "não serve para nada", "só sabe chorar", "burra", "histérica"]
            },
            "0.7-0.8": {
                "description": "Ameaças ou incitação à violência psicológica",
                "examples": ["Ameaças de abandono", "Chantagem emocional", "Controle psicológico"],
                "indicators": ["vou te ensinar", "você vai me obedecer", "não vale nada", "ninguém vai te querer"]
            },
            "0.9-1.0": {
                "description": "Violência física explícita ou incitação criminal",
                "examples": ["Descrição de agressão física", "Ameaças de morte", "Violência sexual"],
                "indicators": ["vou te bater", "merece apanhar", "vou te matar", "força física contra mulher"]
            }
        }
        
        # Dicionário de termos específicos para misoginia
        self.misogyny_keywords = {
            'objectification': [
                'gostosa', 'safada', 'novinha', 'buceta', 'peitos', 'bunda', 'rabuda',
                'sexy', 'hot', 'piece of meat', 'toy', 'objeto', 'boneca'
            ],
            'derogatory_terms': [
                'vadia', 'puta', 'piranha', 'galinha', 'vagabunda', 'prostituta',
                'bitch', 'whore', 'slut', 'hoe', 'thot', 'mulherzinha'
            ],
            'stereotypes': [
                'lugar da mulher', 'fogão', 'cozinha', 'limpar', 'servir',
                'frágil', 'sensível demais', 'histérica', 'louca', 'emotional'
            ],
            'violence': [
                'bater na mulher', 'dar uma surra', 'calar a boca', 'ensinar o lugar',
                'meter a mão', 'socar', 'espancar', 'agredir', 'violentar'
            ]
        }
    
    def load_dataset(self):
        """Carrega o dataset completo."""
        df = pd.read_csv(self.raw_data_path)
        print("Dataset carregado: {} músicas".format(len(df)))
        return df
    
    def preselect_songs_for_labeling(self, df, num_songs=50):
        """
        Pré-seleciona músicas para rotulagem manual baseado em keywords e diversidade temporal.
        """
        print("Pré-selecionando músicas para rotulagem manual...")
        
        # Criar coluna de score preliminar baseado em keywords
        df['misogyny_keywords_count'] = 0
        df['lyrics_lower'] = df['Lyrics'].fillna('').str.lower()
        
        # Contar keywords de misoginia
        all_keywords = []
        for category, keywords in self.misogyny_keywords.items():
            all_keywords.extend(keywords)
        
        for keyword in all_keywords:
            df['misogyny_keywords_count'] += df['lyrics_lower'].str.contains(keyword, na=False).astype(int)
        
        # Estratificar por década e nível de keywords
        df['decade'] = (df['Year'] // 10) * 10
        
        selected_songs = []
        
        # 1. Selecionar músicas com alta probabilidade de misoginia (30% do total)
        high_prob = df[df['misogyny_keywords_count'] >= 2].sample(
            min(int(num_songs * 0.3), len(df[df['misogyny_keywords_count'] >= 2])),
            random_state=42
        )
        selected_songs.append(high_prob)
        
        # 2. Selecionar músicas com probabilidade média (25% do total)
        medium_prob = df[df['misogyny_keywords_count'] == 1].sample(
            min(int(num_songs * 0.25), len(df[df['misogyny_keywords_count'] == 1])),
            random_state=42
        )
        selected_songs.append(medium_prob)
        
        # 3. Selecionar músicas aparentemente neutras (20% do total)
        neutral = df[df['misogyny_keywords_count'] == 0].sample(
            min(int(num_songs * 0.2), len(df[df['misogyny_keywords_count'] == 0])),
            random_state=42
        )
        selected_songs.append(neutral)
        
        # 4. Selecionar aleatoriamente para diversidade (25% restante)
        remaining_indices = df.index.difference(
            pd.concat(selected_songs).index if selected_songs else pd.Index([])
        )
        random_selection = df.loc[remaining_indices].sample(
            min(int(num_songs * 0.25), len(remaining_indices)),
            random_state=42
        )
        selected_songs.append(random_selection)
        
        # Combinar todas as seleções
        preselected = pd.concat(selected_songs, ignore_index=True)
        
        # Garantir diversidade temporal
        decade_counts = preselected['decade'].value_counts()
        print("Distribuição por década das músicas pré-selecionadas:")
        for decade, count in decade_counts.sort_index().items():
            print("  {}: {} músicas".format(decade, count))
        
        print("Pré-selecionadas {} músicas para rotulagem manual".format(len(preselected)))
        
        return preselected[['Artist', 'Song Title', 'Year', 'Lyrics', 'misogyny_keywords_count', 'decade']]
    
    def create_labeling_interface(self, songs_df):
        """
        Cria interface de rotulagem manual e arquivo para preenchimento.
        """
        labeling_template = {
            'metadata': {
                'labeling_criteria': self.labeling_criteria,
                'instructions': """
                INSTRUÇÕES PARA ROTULAGEM MANUAL:
                
                1. Leia cada letra cuidadosamente
                2. Considere o contexto completo da música
                3. Atribua um score de 0.0 a 1.0 baseado nos critérios
                4. Justifique sua pontuação com trechos específicos
                5. Identifique o tipo de misoginia (se houver)
                
                CRITÉRIOS DE PONTUAÇÃO:
                0.0 = Nenhum conteúdo problemático
                0.1-0.2 = Estereótipos leves
                0.3-0.4 = Objetificação moderada
                0.5-0.6 = Linguagem depreciativa
                0.7-0.8 = Ameaças psicológicas
                0.9-1.0 = Violência física explícita
                
                IMPORTANTE: Base sua pontuação em evidências textuais específicas!
                """
            },
            'songs': []
        }
        
        # Preparar dados para rotulagem
        for idx, row in songs_df.iterrows():
            song_data = {
                'id': idx,
                'artist': row['Artist'],
                'title': row['Song Title'],
                'year': int(row['Year']) if pd.notna(row['Year']) else None,
                'lyrics': row['Lyrics'],
                'keywords_count': int(row['misogyny_keywords_count']),
                
                # Campos para preenchimento manual
                'misogyny_score': None,  # Valor de 0.0 a 1.0
                'justification': "",     # Justificativa da pontuação
                'problematic_excerpts': [],  # Trechos específicos problemáticos
                'misogyny_type': "",     # Tipo: objectification, derogatory, stereotypes, violence
                'labeler_confidence': None,  # Confiança do rotulador (1-5)
                'notes': ""              # Observações adicionais
            }
            labeling_template['songs'].append(song_data)
        
        # Salvar template para rotulagem
        template_path = self.labeled_data_path / "labeling_template.json"
        with open(template_path, 'w', encoding='utf-8') as f:
            json.dump(labeling_template, f, indent=2, ensure_ascii=False)
        
        print("Template de rotulagem criado: {}".format(template_path))
        
        # Criar também uma versão em CSV para facilitar
        csv_data = []
        for song in labeling_template['songs']:
            csv_data.append({
                'id': song['id'],
                'artist': song['artist'],
                'title': song['title'],
                'year': song['year'],
                'keywords_count': song['keywords_count'],
                'lyrics_preview': song['lyrics'][:200] + "..." if len(song['lyrics']) > 200 else song['lyrics'],
                'misogyny_score': '',
                'justification': '',
                'problematic_excerpts': '',
                'misogyny_type': '',
                'labeler_confidence': '',
                'notes': ''
            })
        
        csv_df = pd.DataFrame(csv_data)
        csv_path = self.labeled_data_path / "songs_to_label.csv"
        csv_df.to_csv(csv_path, index=False, encoding='utf-8')
        
        print("Arquivo CSV para rotulagem criado: {}".format(csv_path))
        
        return template_path, csv_path
    
    def display_sample_songs(self, songs_df, num_samples=5):
        """Exibe algumas músicas de exemplo para demonstrar a diversidade."""
        print("\n=== AMOSTRAS DE MÚSICAS PARA ROTULAGEM ===")
        
        # Selecionar amostras representativas
        samples = songs_df.sample(num_samples, random_state=42)
        
        for idx, row in samples.iterrows():
            print("\n" + "="*60)
            print("MÚSICA {}: {} - {} ({})".format(
                idx, row['Artist'], row['Song Title'], int(row['Year']) if pd.notna(row['Year']) else 'N/A'
            ))
            print("Keywords detectadas: {}".format(row['misogyny_keywords_count']))
            print("\nLETRA (primeiros 300 caracteres):")
            lyrics_preview = str(row['Lyrics'])[:300] + "..." if len(str(row['Lyrics'])) > 300 else str(row['Lyrics'])
            print(lyrics_preview)
            print("-" * 60)
        
        print("\nEssas são apenas algumas amostras. O arquivo completo contém {} músicas.".format(len(songs_df)))
    
    def analyze_preselection_statistics(self, songs_df):
        """Analisa estatísticas da pré-seleção."""
        print("\n=== ESTATÍSTICAS DA PRÉ-SELEÇÃO ===")
        
        print("Total de músicas selecionadas: {}".format(len(songs_df)))
        
        # Distribuição por década
        print("\nDistribuição temporal:")
        decade_dist = songs_df['decade'].value_counts().sort_index()
        for decade, count in decade_dist.items():
            percentage = (count / len(songs_df)) * 100
            print("  {}: {} músicas ({:.1f}%)".format(decade, count, percentage))
        
        # Distribuição por keywords
        print("\nDistribuição por keywords de misoginia:")
        keyword_dist = songs_df['misogyny_keywords_count'].value_counts().sort_index()
        for count, freq in keyword_dist.items():
            percentage = (freq / len(songs_df)) * 100
            print("  {} keywords: {} músicas ({:.1f}%)".format(count, freq, percentage))
        
        # Artistas mais frequentes
        print("\nArtistas mais frequentes na seleção:")
        artist_counts = songs_df['Artist'].value_counts().head(10)
        for artist, count in artist_counts.items():
            print("  {}: {} músicas".format(artist, count))
    
    def run_preselection_process(self, num_songs=50):
        """Executa o processo completo de pré-seleção."""
        print("Iniciando processo de pré-seleção para rotulagem manual...")
        
        # Carregar dataset
        df = self.load_dataset()
        
        # Pré-selecionar músicas
        selected_songs = self.preselect_songs_for_labeling(df, num_songs)
        
        # Analisar estatísticas
        self.analyze_preselection_statistics(selected_songs)
        
        # Criar interface de rotulagem
        template_path, csv_path = self.create_labeling_interface(selected_songs)
        
        # Exibir amostras
        self.display_sample_songs(selected_songs)
        
        print("\n" + "="*70)
        print("PRÉ-SELEÇÃO CONCLUÍDA!")
        print("="*70)
        print("Próximos passos:")
        print("1. Abra o arquivo: {}".format(csv_path))
        print("2. Rotule manualmente as {} músicas".format(len(selected_songs)))
        print("3. Use os critérios definidos para pontuação 0.0-1.0")
        print("4. Salve o arquivo com as pontuações preenchidas")
        print("\nArquivos criados:")
        print("- Template JSON: {}".format(template_path))
        print("- Planilha CSV: {}".format(csv_path))
        
        return selected_songs, template_path, csv_path

if __name__ == "__main__":
    labeling_system = MisogynyLabelingSystem()
    selected_songs, template_path, csv_path = labeling_system.run_preselection_process(num_songs=40)