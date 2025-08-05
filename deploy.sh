#!/bin/bash

echo "🚀 Dashboard PRECS - Deploy Script"
echo "=================================="

# Verificar se o git está instalado
if ! command -v git &> /dev/null; then
    echo "❌ Git não está instalado. Instale o Git primeiro."
    exit 1
fi

# Verificar se estamos no diretório correto
if [ ! -f "app.py" ]; then
    echo "❌ Arquivo app.py não encontrado. Execute este script no diretório do dashboard."
    exit 1
fi

echo "✅ Verificações iniciais concluídas"

# Inicializar git se não existir
if [ ! -d ".git" ]; then
    echo "📁 Inicializando repositório Git..."
    git init
    git add .
    git commit -m "Dashboard PRECS - Deploy inicial"
    echo "✅ Repositório Git inicializado"
else
    echo "📁 Repositório Git já existe"
    git add .
    git commit -m "Dashboard PRECS - Atualização"
    echo "✅ Alterações commitadas"
fi

echo ""
echo "🎯 Próximos passos para deploy:"
echo ""
echo "1. 📤 Faça push para GitHub:"
echo "   git branch -M main"
echo "   git remote add origin https://github.com/SEU-USUARIO/SEU-REPO.git"
echo "   git push -u origin main"
echo ""
echo "2. 🌐 Acesse Streamlit Cloud:"
echo "   https://share.streamlit.io"
echo ""
echo "3. ⚙️ Configure as variáveis de ambiente:"
echo "   DB_HOST=precsinstance.c8p0mgum6ow9.us-east-1.rds.amazonaws.com"
echo "   DB_PORT=5432"
echo "   DB_NAME=dashmetas"
echo "   DB_USER=postgres"
echo "   DB_PASSWORD=precs2025"
echo ""
echo "4. 🚀 Deploy automático após configuração"
echo ""
echo "📋 Checklist de deploy:"
echo "✅ app.py - Aplicação principal"
echo "✅ requirements.txt - Dependências"
echo "✅ .streamlit/config.toml - Configurações"
echo "✅ README.md - Documentação"
echo "✅ .gitignore - Arquivos ignorados"
echo ""

echo "🎉 Script de deploy concluído!"
echo "Agora siga os passos acima para fazer o deploy no Streamlit Cloud." 