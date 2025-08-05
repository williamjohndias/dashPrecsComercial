# 🚀 Deploy Dashboard PRECS - Windows PowerShell

## ⚡ Deploy no Windows em 5 Passos

### 1. 📁 Instalar Git (se necessário)
```powershell
# Baixe e instale o Git para Windows
# https://git-scm.com/download/win
```

### 2. 📁 Preparar Repositório
```powershell
# Navegue para o diretório do dashboard
cd C:\Users\user\Desktop\dashboard

# Inicializar git
git init

# Adicionar arquivos
git add .

# Fazer commit inicial
git commit -m "Dashboard PRECS - Deploy inicial"
```

### 3. 📤 Push para GitHub
```powershell
# Criar branch main
git branch -M main

# Adicionar repositório remoto (substitua SEU-USUARIO/SEU-REPO)
git remote add origin https://github.com/SEU-USUARIO/SEU-REPO.git

# Push para GitHub
git push -u origin main
```

### 4. 🌐 Acessar Streamlit Cloud
- Vá para: https://share.streamlit.io
- Faça login com sua conta GitHub
- Clique em "New app"

### 5. ⚙️ Configurar App
- **Repository**: Seu repositório
- **Branch**: main
- **Main file path**: `app.py`
- **App URL**: (será gerado automaticamente)

## 🔧 Configurar Variáveis de Ambiente

No painel do Streamlit Cloud, adicione estas variáveis:

| Variável | Valor |
|----------|-------|
| `DB_HOST` | `precsinstance.c8p0mgum6ow9.us-east-1.rds.amazonaws.com` |
| `DB_PORT` | `5432` |
| `DB_NAME` | `dashmetas` |
| `DB_USER` | `postgres` |
| `DB_PASSWORD` | `precs2025` |

## ✅ Checklist de Deploy

### Arquivos Necessários
- [x] `app.py` - Aplicação principal
- [x] `requirements.txt` - Dependências
- [x] `.streamlit/config.toml` - Configurações
- [x] `README.md` - Documentação
- [x] `.gitignore` - Arquivos ignorados
- [x] `precs2.png` - Logo da empresa
- [x] `sino.png` - Ícone de sino
- [x] `medalha.png` - Ícone de medalha

### Configurações
- [x] Variáveis de ambiente configuradas
- [x] Repositório conectado ao GitHub
- [x] Caminho do arquivo principal correto
- [x] SSL habilitado para produção

## 🚀 Comandos PowerShell

### Verificar Git
```powershell
git --version
```

### Verificar Status
```powershell
git status
```

### Adicionar Alterações
```powershell
git add .
git commit -m "Atualização do dashboard"
git push origin main
```

### Teste Local
```powershell
# Instalar dependências
pip install -r requirements.txt

# Executar localmente
streamlit run app.py
```

## 🔍 Troubleshooting Windows

### Erro: "git não é reconhecido"
**Solução**: Instale o Git para Windows e reinicie o PowerShell

### Erro: "pip não é reconhecido"
**Solução**: Instale o Python e adicione ao PATH

### Erro: "streamlit não é reconhecido"
**Solução**: `pip install streamlit`

### Erro: "Permissão negada"
**Solução**: Execute o PowerShell como administrador

## 📊 Monitoramento

### Logs de Aplicação
- Acesse o painel do Streamlit Cloud
- Vá em "Manage app" > "Logs"
- Monitore erros e performance

### Métricas
- **Uptime**: Tempo de disponibilidade
- **Requests**: Número de acessos
- **Performance**: Tempo de resposta

## 🎯 URLs Importantes

- **Streamlit Cloud**: https://share.streamlit.io
- **Documentação**: https://docs.streamlit.io
- **Comunidade**: https://discuss.streamlit.io
- **Git para Windows**: https://git-scm.com/download/win

## 📋 Passos Detalhados

### 1. Criar Repositório GitHub
1. Acesse https://github.com
2. Clique em "New repository"
3. Nome: `dashboard-precs`
4. Descrição: "Dashboard PRECS - Streamlit"
5. Público ou privado (sua escolha)
6. Clique em "Create repository"

### 2. Configurar Git Local
```powershell
# Configurar usuário Git
git config --global user.name "Seu Nome"
git config --global user.email "seu-email@exemplo.com"
```

### 3. Push Inicial
```powershell
git add .
git commit -m "Dashboard PRECS - Deploy inicial"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/dashboard-precs.git
git push -u origin main
```

### 4. Deploy Streamlit Cloud
1. Acesse https://share.streamlit.io
2. Login com GitHub
3. "New app"
4. Repository: `SEU-USUARIO/dashboard-precs`
5. Branch: `main`
6. Main file path: `app.py`
7. Deploy!

---

**Dashboard PRECS** - Deploy no Windows! 🎉 