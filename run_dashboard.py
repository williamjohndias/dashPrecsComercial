#!/usr/bin/env python3
"""
Script para executar o Dashboard PRECS com visual moderno
"""
import subprocess
import sys
import os

def main():
    print("🚀 Iniciando Dashboard PRECS - Visual Moderno")
    print("=" * 60)
    print("✨ Interface com Glassmorphism e Gradientes")
    print("🎨 Tema Escuro Elegante")
    print("📱 Design Responsivo")
    print("=" * 60)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("app.py"):
        print("❌ Erro: app.py não encontrado!")
        print("Certifique-se de estar no diretório do dashboard.")
        sys.exit(1)
    
    # Verificar se as dependências estão instaladas
    try:
        import streamlit
        import pandas
        import psycopg2
        print("✅ Dependências verificadas com sucesso!")
    except ImportError as e:
        print(f"❌ Erro: Dependência não encontrada: {e}")
        print("Execute: pip install streamlit pandas psycopg2-binary python-dotenv streamlit-autorefresh plotly Pillow flask")
        sys.exit(1)
    
    # Configurações do servidor
    cmd = [
        "streamlit", "run", "app.py",
        "--server.port", "8501",
        "--server.address", "localhost",
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false"
    ]
    
    print("🌐 Iniciando servidor na porta 8501...")
    print("📱 Acesse: http://localhost:8501")
    print("🎨 Visual moderno com glassmorphism ativo!")
    print("=" * 60)
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Dashboard encerrado pelo usuário.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar a aplicação: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 