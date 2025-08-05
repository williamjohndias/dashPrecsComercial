# 🚀 Guia Rápido - Deploy Dashboard PRECS

## ⚡ Deploy em 5 Passos

### 1. 📁 Preparar Repositório
```bash
# Execute o script de deploy
chmod +x deploy.sh
./deploy.sh
```

### 2. 📤 Push para GitHub
```bash
# Substitua SEU-USUARIO e SEU-REPO pelos seus dados
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/SEU-REPO.git
git push -u origin main
```

### 3. 🌐 Acessar Streamlit Cloud
- Vá para: https://share.streamlit.io
- Faça login com sua conta GitHub
- Clique em "New app"

### 4. ⚙️ Configurar App
- **Repository**: Seu repositório
- **Branch**: main
- **Main file path**: `app.py`
- **App URL**: (será gerado automaticamente)

### 5. 🔧 Configurar Variáveis de Ambiente
No painel do Streamlit Cloud, adicione:

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

### Configurações
- [x] Variáveis de ambiente configuradas
- [x] Repositório conectado ao GitHub
- [x] Caminho do arquivo principal correto
- [x] SSL habilitado para produção

## 🔍 Troubleshooting

### Erro: "Module not found"
**Solução**: Verifique se todas as dependências estão no `requirements.txt`

### Erro: "Database connection failed"
**Solução**: Verifique as variáveis de ambiente no Streamlit Cloud

### Erro: "Images not loading"
**Solução**: Certifique-se de que as imagens estão no repositório

### Erro: "App not deploying"
**Solução**: Verifique os logs no painel do Streamlit Cloud

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

## 🚀 Comandos Úteis

### Deploy Local (Teste)
```bash
streamlit run app.py
```

### Verificar Dependências
```bash
pip install -r requirements.txt
```

### Atualizar Deploy
```bash
git add .
git commit -m "Atualização"
git push origin main
```

---

**Dashboard PRECS** - Deploy rápido e eficiente! 🎉 