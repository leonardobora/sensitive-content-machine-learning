#!/usr/bin/env python3
"""
Script para criar estrutura de diretórios necessária.
"""

from pathlib import Path

def create_directory_structure():
    """Cria toda a estrutura de diretórios necessária."""
    base_dir = Path(__file__).parent.parent
    
    directories = [
        # Diretórios principais
        "data",
        "data/raw",
        "data/processed", 
        "data/processed_continuous",
        "data/labeled",
        "data/figures",
        
        # Modelos
        "models",
        
        # Resultados
        "results",
        
        # Logs
        "logs",
        
        # Notebooks
        "notebooks",
        
        # Scripts (já existe)
        "scripts",
        
        # Source code (já existe)
        "src",
        "src/data",
        "src/models",
        "src/features",
        "src/visualization"
    ]
    
    print("📁 Criando estrutura de diretórios...")
    
    created = 0
    existed = 0
    
    for dir_path in directories:
        full_path = base_dir / dir_path
        
        if full_path.exists():
            print(f"   ✅ {dir_path}/ (já existe)")
            existed += 1
        else:
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"   ✨ {dir_path}/ (criado)")
            created += 1
    
    print(f"\n📊 Resumo:")
    print(f"   • Criados: {created} diretórios")
    print(f"   • Já existiam: {existed} diretórios")
    print(f"   • Total: {created + existed} diretórios")
    
    # Criar arquivos .gitkeep para diretórios vazios
    gitkeep_dirs = [
        "data/raw",
        "results", 
        "logs"
    ]
    
    print(f"\n📝 Criando arquivos .gitkeep...")
    for dir_path in gitkeep_dirs:
        gitkeep_path = base_dir / dir_path / ".gitkeep"
        if not gitkeep_path.exists():
            gitkeep_path.touch()
            print(f"   ✨ {dir_path}/.gitkeep")
    
    print(f"\n✅ Estrutura de diretórios criada com sucesso!")

if __name__ == "__main__":
    create_directory_structure()