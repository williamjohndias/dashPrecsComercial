# 🚀 Dashboard PRECS - Deploy Streamlit Cloud

## 📊 Descrição
Dashboard interativo para visualização de propostas e campanhas da PRECS, com tema escuro elegante e barras de progresso contornadas.

## 🎯 Funcionalidades
- **Visualização em tempo real** das propostas diárias
- **Barras de progresso contornadas** para melhor visualização
- **Filtros dinâmicos** por proprietário, etapa e data
- **Gestão de campanhas** ativas
- **Tema escuro** com gradientes dourados
- **Responsivo** para 100% de escala

## 🚀 Deploy no Streamlit Cloud

### 1. Preparação do Repositório
```bash
# Estrutura necessária para deploy
dashboard/
├── app.py                 # Aplicação principal
├── requirements.txt       # Dependências
├── .streamlit/
│   └── config.toml       # Configurações
├── README.md             # Este arquivo
└── assets/              # Imagens (opcional)
    ├── precs2.png
    ├── sino.png
    └── medalha.png
```

### 2. Configuração das Variáveis de Ambiente
No Streamlit Cloud, configure as seguintes variáveis:

```env
DB_HOST=precsinstance.c8p0mgum6ow9.us-east-1.rds.amazonaws.com
DB_PORT=5432
DB_NAME=dashmetas
DB_USER=postgres
DB_PASSWORD=precs2025
```

### 3. Deploy no Streamlit Cloud

#### Opção A: Deploy via GitHub
1. **Faça push do código para GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Dashboard PRECS - Deploy inicial"
   git branch -M main
   git remote add origin https://github.com/seu-usuario/seu-repo.git
   git push -u origin main
   ```

2. **Acesse [share.streamlit.io](https://share.streamlit.io)**
3. **Conecte sua conta GitHub**
4. **Selecione o repositório**
5. **Configure o caminho:** `app.py`
6. **Adicione as variáveis de ambiente**
7. **Clique em "Deploy"**

#### Opção B: Deploy via Streamlit CLI
```bash
# Instale o Streamlit CLI
pip install streamlit

# Faça login
streamlit login

# Deploy
streamlit deploy app.py
```

### 4. Configurações Importantes

#### Variáveis de Ambiente (Streamlit Cloud)
- **DB_HOST**: Host do PostgreSQL
- **DB_PORT**: Porta do banco (5432)
- **DB_NAME**: Nome do banco (dashmetas)
- **DB_USER**: Usuário do banco
- **DB_PASSWORD**: Senha do banco

#### Configurações de Rede
- **SSL**: Habilitado para conexão segura
- **Porta**: 8501 (padrão)
- **CORS**: Desabilitado para segurança

### 5. Monitoramento e Logs
- **Logs de aplicação**: Acessíveis no painel do Streamlit Cloud
- **Métricas**: Visualização de uso e performance
- **Erros**: Monitoramento automático de erros

## 🔧 Tecnologias Utilizadas
- **Streamlit**: Framework web para Python
- **PostgreSQL**: Banco de dados principal
- **Pandas**: Manipulação de dados
- **CSS**: Estilização personalizada
- **HTML**: Componentes customizados

## 📁 Estrutura do Projeto
```
dashboard/
├── app.py                 # Aplicação principal
├── requirements.txt       # Dependências Python
├── .streamlit/
│   └── config.toml       # Configurações Streamlit
├── servidorDB.py         # Servidor Flask (opcional)
├── aa.py                 # Webhook handler (opcional)
├── config.py             # Configurações (opcional)
├── credenciais.json      # Credenciais Google (opcional)
├── precs2.png           # Logo da empresa
├── sino.png             # Ícone de sino
├── medalha.png          # Ícone de medalha
└── README.md            # Documentação
```

## 🎨 Características Visuais
- **Tema escuro** (#0a0a0a)
- **Gradientes dourados** (#FFD700, #FFA500)
- **Barras contornadas** com bordas visíveis
- **Cards simples** sem glassmorphism
- **Responsivo** para 100% de escala
- **Animações suaves** de entrada

## 🚀 Comandos de Deploy

### Deploy Local (Teste)
```bash
cd dashboard
streamlit run app.py
```

### Deploy Streamlit Cloud
1. **GitHub**: Push para repositório
2. **Streamlit Cloud**: Conectar repositório
3. **Configurar**: Variáveis de ambiente
4. **Deploy**: Automático

## 📊 Funcionalidades do Dashboard
- **Filtros dinâmicos** por proprietário e etapa
- **Visualização de campanhas** ativas
- **Barras de progresso** contornadas
- **Medalhas** para metas atingidas
- **Auto-atualização** a cada 70 segundos
- **Layout responsivo** para diferentes telas

## 🔒 Segurança
- **Variáveis de ambiente** para credenciais
- **CORS desabilitado** para produção
- **SSL obrigatório** para conexões
- **Autenticação** via Streamlit Cloud

## 📈 Monitoramento
- **Logs de aplicação** em tempo real
- **Métricas de uso** e performance
- **Alertas** para erros críticos
- **Backup automático** de configurações

## 🎯 Próximos Passos
1. **Deploy inicial** no Streamlit Cloud
2. **Configuração** das variáveis de ambiente
3. **Teste** de conectividade com banco
4. **Monitoramento** de performance
5. **Otimizações** conforme necessário

---

**Dashboard PRECS** - Visualização moderna e eficiente de propostas e campanhas! 🚀 