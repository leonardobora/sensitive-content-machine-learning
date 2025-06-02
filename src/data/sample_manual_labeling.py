import pandas as pd
import json
from pathlib import Path

def demonstrate_manual_labeling():
    """
    Demonstra o processo de rotulagem manual com exemplos reais.
    Seguindo critérios acadêmicos para misoginia e violência contra mulheres.
    """
    
    # Carregar os dados para rotulagem
    data_dir = Path(__file__).parent.parent.parent / "data"
    csv_path = data_dir / "labeled" / "songs_to_label.csv"
    df = pd.read_csv(csv_path)
    
    # Exemplos de rotulagem manual baseados em análise das letras
    manual_labels = []
    
    print("=== DEMONSTRAÇÃO DE ROTULAGEM MANUAL ===")
    print("Analisando as primeiras músicas da lista...")
    
    # Exemplo 1: "Let Me Blow Ya Mind" - Eve feat. Gwen Stefani (2001)
    print("\n1. Eve feat. Gwen Stefani - Let Me Blow Ya Mind (2001)")
    print("Análise: Contém linguagem agressiva ('bitch'), mas em contexto de empoderamento feminino")
    print("Score: 0.3 - Objetificação/linguagem moderada")
    manual_labels.append({
        'id': 0,
        'misogyny_score': 0.3,
        'justification': 'Uso da palavra "bitch" em contexto agressivo, mas representa empoderamento feminino, não degradação',
        'problematic_excerpts': ['bitch, I\'m drastic'],
        'misogyny_type': 'derogatory_language_mild',
        'labeler_confidence': 4,
        'notes': 'Contexto de empoderamento feminino atenua o impacto misógino'
    })
    
    # Exemplo 2: "Time Today" - Moneybagg Yo (2021)
    print("\n2. Moneybagg Yo - Time Today (2021)")
    print("Análise: Linguagem geral agressiva, sem foco específico em mulheres")
    print("Score: 0.1 - Linguagem estereotipada leve")
    manual_labels.append({
        'id': 1,
        'misogyny_score': 0.1,
        'justification': 'Linguagem agressiva geral, mas sem direcionamento específico contra mulheres',
        'problematic_excerpts': [],
        'misogyny_type': 'none',
        'labeler_confidence': 5,
        'notes': 'Agressividade geral não constitui misoginia específica'
    })
    
    # Exemplo 3: "G.D.F.R." - Flo Rida (2015)
    print("\n3. Flo Rida - G.D.F.R. (2015)")
    print("Análise: Objetificação sexual clara ('freak', 'bust it open')")
    print("Score: 0.5 - Linguagem claramente depreciativa")
    manual_labels.append({
        'id': 2,
        'misogyny_score': 0.5,
        'justification': 'Objetificação sexual explícita, redução da mulher a objeto sexual',
        'problematic_excerpts': ['if you\'re a freak', 'bust it open', 'let me see you get loose'],
        'misogyny_type': 'objectification',
        'labeler_confidence': 5,
        'notes': 'Clara objetificação sexual sem violência física'
    })
    
    # Exemplo 4: "Romeo And Juliet" - Sylk-E Fyne (1998)
    print("\n4. Sylk-E Fyne - Romeo And Juliet (1998)")
    print("Análise: Conteúdo sexual explícito mas consensual")
    print("Score: 0.2 - Linguagem levemente estereotipada")
    manual_labels.append({
        'id': 3,
        'misogyny_score': 0.2,
        'justification': 'Conteúdo sexual, mas em contexto consensual e sem degradação',
        'problematic_excerpts': ['Hot sex on a platta'],
        'misogyny_type': 'mild_sexual_content',
        'labeler_confidence': 4,
        'notes': 'Sexualidade consensual não constitui misoginia significativa'
    })
    
    # Exemplo 5: "Princess Diana" - Ice Spice and Nicki Minaj (2023)
    print("\n5. Ice Spice and Nicki Minaj - Princess Diana (2023)")
    print("Análise: Linguagem agressiva mas em contexto de empoderamento feminino")
    print("Score: 0.2 - Linguagem estereotipada leve")
    manual_labels.append({
        'id': 4,
        'misogyny_score': 0.2,
        'justification': 'Linguagem agressiva por artistas femininas em contexto de empoderamento',
        'problematic_excerpts': ['Bitches move wock'],
        'misogyny_type': 'reclaimed_language',
        'labeler_confidence': 4,
        'notes': 'Linguagem reclamada por artistas femininas em contexto de poder'
    })
    
    # Exemplo 6: "All About That Bass" - Meghan Trainor (2014)
    print("\n6. Meghan Trainor - All About That Bass (2014)")
    print("Análise: Mensagem de body positivity, anti-misógina")
    print("Score: 0.0 - Nenhum conteúdo misógino")
    manual_labels.append({
        'id': 7,
        'misogyny_score': 0.0,
        'justification': 'Mensagem de aceitação corporal e empoderamento feminino positivo',
        'problematic_excerpts': [],
        'misogyny_type': 'none',
        'labeler_confidence': 5,
        'notes': 'Mensagem explicitamente anti-misógina e de empoderamento'
    })
    
    # Criar DataFrame com exemplos rotulados
    sample_labeled = pd.DataFrame(manual_labels)
    
    # Salvar exemplos
    labeled_path = data_dir / "labeled" / "sample_manual_labels.csv"
    sample_labeled.to_csv(labeled_path, index=False)
    
    print("\n=== ESTATÍSTICAS DOS EXEMPLOS ROTULADOS ===")
    print("Distribuição de scores:")
    score_distribution = sample_labeled['misogyny_score'].value_counts().sort_index()
    for score, count in score_distribution.items():
        print("  Score {}: {} músicas".format(score, count))
    
    print("\nTipos de misoginia identificados:")
    type_distribution = sample_labeled['misogyny_type'].value_counts()
    for mtype, count in type_distribution.items():
        print("  {}: {} músicas".format(mtype, count))
    
    print("\nConfiança média do rotulador: {:.1f}/5".format(
        sample_labeled['labeler_confidence'].mean()
    ))
    
    print("\nArquivo de exemplo salvo em: {}".format(labeled_path))
    
    return sample_labeled

def create_labeling_guidelines():
    """Cria diretrizes detalhadas para rotulagem manual."""
    
    guidelines = {
        "title": "Diretrizes para Rotulagem Manual - Misoginia em Letras de Música",
        "version": "1.0",
        "date": "2025",
        
        "theoretical_foundation": {
            "references": [
                "Anzovino, M., Fersini, E., & Rosso, P. (2018). Automatic misogyny identification",
                "UN Women (2020). Technology-facilitated gender-based violence",
                "UNESCO (2019). Guidelines for Countering Online Violence Against Women"
            ],
            "definition": "Misoginia é o ódio, aversão ou preconceito contra mulheres, manifestado através de atitudes, comportamentos ou sistemas que menosprezam, objetificam ou violentam mulheres."
        },
        
        "scoring_criteria": {
            "0.0": {
                "description": "Ausência completa de conteúdo misógino",
                "indicators": ["Linguagem respeitosa", "Igualdade de gênero", "Empoderamento feminino positivo"],
                "examples": ["Canções de amor respeitoso", "Temas neutros", "Mensagens de body positivity"]
            },
            "0.1-0.2": {
                "description": "Estereótipos de gênero leves ou linguagem levemente problemática",
                "indicators": ["Papéis tradicionais suaves", "Objetificação muito sutil", "Linguagem paternalista"],
                "examples": ["'ela é uma princesa'", "'doce menina'", "'precisa de proteção'"]
            },
            "0.3-0.4": {
                "description": "Objetificação moderada ou estereótipos claros",
                "indicators": ["Redução à aparência física", "Papéis submissos", "Sexualização sem contexto"],
                "examples": ["Foco apenas em atributos físicos", "Mulher como troféu", "Linguagem sexualizante"]
            },
            "0.5-0.6": {
                "description": "Linguagem claramente depreciativa",
                "indicators": ["Insultos baseados em gênero", "Desvalorização", "Linguagem degradante"],
                "examples": ["Termos depreciativos para mulheres", "Questionamento de capacidades", "Reducionismo extremo"]
            },
            "0.7-0.8": {
                "description": "Ameaças ou incitação à violência psicológica",
                "indicators": ["Ameaças de controle", "Chantagem emocional", "Intimidação psicológica"],
                "examples": ["'vou te ensinar o seu lugar'", "'você não vale nada'", "ameaças de abandono manipulativo"]
            },
            "0.9-1.0": {
                "description": "Violência física explícita ou incitação criminal",
                "indicators": ["Descrição de agressão", "Ameaças de morte", "Violência sexual"],
                "examples": ["Descrições de espancamento", "Ameaças de morte", "Incitação à violência sexual"]
            }
        },
        
        "special_considerations": {
            "context_matters": "O contexto é fundamental. Palavras que podem ser misóginas em um contexto podem ser empoderadoras em outro.",
            "artist_gender": "Considere o gênero do artista. Mulheres podem 'reclamar' linguagem degradante como forma de empoderamento.",
            "historical_context": "Músicas mais antigas podem refletir normas sociais da época, mas ainda devem ser pontuadas pelos padrões atuais.",
            "irony_and_criticism": "Distinção entre música que perpetua misoginia vs. música que critica misoginia.",
            "consensual_sexuality": "Conteúdo sexual consensual não é automaticamente misógino."
        },
        
        "labeling_process": [
            "1. Leia a letra completa pelo menos duas vezes",
            "2. Identifique trechos potencialmente problemáticos",
            "3. Analise o contexto geral da música",
            "4. Considere o gênero do artista e época",
            "5. Atribua pontuação baseada nos critérios",
            "6. Justifique com evidências textuais específicas",
            "7. Indique seu nível de confiança (1-5)"
        ]
    }
    
    # Salvar diretrizes
    data_dir = Path(__file__).parent.parent.parent / "data"
    guidelines_path = data_dir / "labeled" / "labeling_guidelines.json"
    
    with open(guidelines_path, 'w', encoding='utf-8') as f:
        json.dump(guidelines, f, indent=2, ensure_ascii=False)
    
    print("Diretrizes de rotulagem salvas em: {}".format(guidelines_path))
    return guidelines

if __name__ == "__main__":
    # Demonstrar rotulagem manual
    sample_labels = demonstrate_manual_labeling()
    
    # Criar diretrizes
    guidelines = create_labeling_guidelines()
    
    print("\n" + "="*70)
    print("ROTULAGEM MANUAL DEMONSTRADA!")
    print("="*70)
    print("Próximos passos para rotulagem completa:")
    print("1. Seguir as diretrizes criadas")
    print("2. Rotular as 40 músicas selecionadas")
    print("3. Manter consistência nos critérios")
    print("4. Documentar justificativas detalhadas")
    print("\nArquivos de referência criados:")
    print("- Exemplos: data/labeled/sample_manual_labels.csv")
    print("- Diretrizes: data/labeled/labeling_guidelines.json")