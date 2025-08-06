from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from datetime import datetime
from streamlit_autorefresh import st_autorefresh 
from io import BytesIO
import base64
from PIL import Image
import locale
import plotly.express as px
import streamlit.components.v1 as components
from datetime import datetime
st.session_state.page_height = 900  # ou use st.window_height, futuramente
# Configuração de locale removida para compatibilidade com Streamlit Cloud
# import locale
# try:
#     locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
# except (locale.Error, OSError):
#     try:
#         locale.setlocale(locale.LC_TIME, 'pt_BR')
#     except (locale.Error, OSError):
#         pass

# ---- Tela cheia + tema escuro da PRECS ----
st.set_page_config(page_title="Precs Propostas", layout="wide")

# Estilo elegante com tema escuro e dourado
st.markdown("""
    <style>
    /* Reset e configurações gerais */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Esconder header do Streamlit */
    header {
        visibility: hidden;
    }
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# ==============
# CONFIGURAÇÃO
# ==============
load_dotenv()

st.set_page_config(
    page_title="📊 Dashboard Precs | Movimentações Financeiras",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Configuração do banco de dados
DB_HOST = os.getenv("DB_HOST", "bdunicoprecs.c50cwuocuwro.sa-east-1.rds.amazonaws.com")
DB_NAME = os.getenv("DB_NAME", "Movimentacoes")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Q62^S7v<yK-\\5LHm2PxQ")
DB_PORT = os.getenv("DB_PORT", "5432")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL)

# locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# ==============
# FUNÇÕES
# ==============

@st.cache_data(ttl=600, show_spinner=False)
def carregar_dados_movimentacoes(data_inicio=None, data_fim=None):
    query = """
        SELECT id, municipio, data_movimentacao, saldo_anterior_valor, saldo_atualizado_valor
        FROM movimentacoes
        WHERE data_movimentacao IS NOT NULL
    """

    # Filtro inteligente baseado nos parâmetros ou padrão amplo
    if data_inicio and data_fim:
        filtros = [f"data_movimentacao BETWEEN '{data_inicio}' AND '{data_fim}'"]
    else:
        # Filtro padrão: últimos 3 anos para garantir dados suficientes
        from datetime import datetime, timedelta
        data_limite = (datetime.now() - timedelta(days=1095)).strftime('%Y-%m-%d')
        filtros = [f"data_movimentacao >= '{data_limite}'"]

    if filtros:
        query += " AND " + " AND ".join(filtros)

    query += " ORDER BY municipio, data_movimentacao, id"

    df = pd.read_sql(query, engine)
    df = df.dropna(subset=['municipio', 'data_movimentacao']).copy()
    df['data_movimentacao'] = pd.to_datetime(df['data_movimentacao'], errors='coerce')
    df['data_only'] = df['data_movimentacao'].dt.date
    df['municipio'] = df['municipio'].str.strip()
    return df


@st.cache_data(ttl=60, show_spinner=False)
def carregar_dados_brutos():
    query = "SELECT * FROM movimentacoes ORDER BY data_movimentacao DESC, id DESC"
    df = pd.read_sql(query, engine)
    return df

def calcular_saldos(df, data_hoje, data_ref):
    resultados = []

    # Verifica se o DataFrame não está vazio
    if df.empty:
        return pd.DataFrame(columns=['Município', f'Saldo ({data_ref.strftime("%d/%m/%Y")})', 
                                   f'Saldo ({data_hoje.strftime("%d/%m/%Y")})', 'Movimentação'])

    for municipio, grupo in df.groupby('municipio'):
        grupo = grupo.sort_values(['data_only', 'id'])

        # Data referência
        df_ref = grupo[grupo['data_only'] <= data_ref]
        saldo_ref = None
        if not df_ref.empty:
            data_ref_real = df_ref['data_only'].max()
            linhas_ref = df_ref[df_ref['data_only'] == data_ref_real]
            if data_ref_real == data_ref:
                linha = linhas_ref.loc[linhas_ref['id'].idxmin()]
                saldo_ref = linha['saldo_anterior_valor']
            else:
                linha = linhas_ref.loc[linhas_ref['id'].idxmax()]
                saldo_ref = linha['saldo_atualizado_valor']

        # Data hoje
        df_hoje = grupo[grupo['data_only'] <= data_hoje]
        saldo_hoje = None
        if not df_hoje.empty:
            data_hoje_real = df_hoje['data_only'].max()
            linhas_hoje = df_hoje[df_hoje['data_only'] == data_hoje_real]
            linha = linhas_hoje.loc[linhas_hoje['id'].idxmax()]
            saldo_hoje = linha['saldo_atualizado_valor']

        # Diferença
        movimentacao = None
        if saldo_ref is not None and saldo_hoje is not None:
            movimentacao = saldo_ref - saldo_hoje

        resultados.append({
            'Município': municipio,
            f'Saldo ({data_ref.strftime("%d/%m/%Y")})': saldo_ref,
            f'Saldo ({data_hoje.strftime("%d/%m/%Y")})': saldo_hoje,
            'Movimentação': movimentacao
        })

    df_result = pd.DataFrame(resultados)
    
    # Verifica se o DataFrame resultante não está vazio e se a coluna existe
    col_hoje = f'Saldo ({data_hoje.strftime("%d/%m/%Y")})'
    if not df_result.empty and col_hoje in df_result.columns:
        return df_result.sort_values(by=col_hoje, ascending=False)
    else:
        return df_result

def formatar_brl(valor):
    if pd.isna(valor):
        return "-"
    try:
        return locale.currency(valor, grouping=True)
    except:
        # fallback caso locale falhe
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def criar_metricas_resumo(df_resultado):
    """Cria métricas de resumo do dashboard"""
    if df_resultado.empty:
        return 0, 0, 0, 0
        
    total_municipios = len(df_resultado)
    col_valores = [col for col in df_resultado.columns if 'Saldo' in col]
    
    if len(col_valores) >= 2:
        try:
            saldo_total_atual = df_resultado[col_valores[1]].fillna(0).sum()
            saldo_total_ref = df_resultado[col_valores[0]].fillna(0).sum()
            variacao_total = df_resultado['Movimentação'].fillna(0).sum() if 'Movimentação' in df_resultado.columns else 0
        except (KeyError, IndexError):
            saldo_total_atual = saldo_total_ref = variacao_total = 0
    else:
        saldo_total_atual = saldo_total_ref = variacao_total = 0
    
    return total_municipios, saldo_total_atual, saldo_total_ref, variacao_total

def criar_grafico_top_municipios(df_resultado, top_n=10):
    """Cria gráfico dos top municípios por saldo"""
    if df_resultado.empty:
        return None
    
    col_valores = [col for col in df_resultado.columns if 'Saldo' in col]
    if not col_valores:
        return None
    
    df_top = df_resultado.nlargest(top_n, col_valores[-1]).copy()
    
    fig = px.bar(
        df_top,
        x='Município',
        y=col_valores[-1],
        title=f"📈 Top {top_n} Municípios por Saldo Atual",
        color=col_valores[-1],
        color_continuous_scale='viridis'
    )

    /* Fundo escuro elegante */
    body {
        background: #0a0a0a !important;
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        overflow-x: hidden;
    }
    fig.update_layout(
        height=400,
        xaxis_title="Município",
        yaxis_title="Saldo (R$)",
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    /* Container principal */
    fig.update_xaxes(tickangle=45)
    return fig

def aplicar_css_customizado():
    """Aplica CSS customizado para melhor visual"""
    st.markdown("""
    <style>
    /* Estilo geral */
   .main {
        background: #0a0a0a !important;
        padding: 0;
    }
    
    .stApp {
        background: #0a0a0a !important;
        padding: 1rem;
        max-width: 100%;
    }
    
    /* Títulos com gradiente dourado */
    h1, h2, h3, h4 {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
        padding-top: 2rem;
   }
   
    /* Botões modernos */
    .stButton>button {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        color: #000;
    /* Header customizado */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
       border-radius: 15px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 14px;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
        transition: all 0.3s ease;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
   }
   
    .stButton>button:hover {
        background: linear-gradient(45deg, #FFA500, #FFD700);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.5);
    }
    
    /* Container principal */
    .block-container {
        background: #1a1a1a;
        border-radius: 15px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    /* Sidebar estilizada */
    .css-1v0mbdj {
        background: #1a1a1a !important;
    .header-title {
       color: white;
        border-right: 2px solid #FFD700;
    }
    
    .css-1d391kg {
        background: #1a1a1a !important;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
   }
   
    /* DataFrames */
    .stDataFrame {
        background: rgba(26, 26, 26, 0.9);
        color: white;
        border-radius: 15px;
        border: 1px solid rgba(255, 215, 0, 0.3);
    .header-subtitle {
        color: #f0f0f0;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 1rem;
   }
   
    /* Cards simples */
    .glass-card {
        background: #1a1a1a;
    /* Cartões de métricas */
    .metric-card {
        background: white;
        padding: 1.5rem;
       border-radius: 12px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
   }
   
    /* Animações suaves */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
   }
   
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 0.5rem;
   }
   
    .slide-in-left {
        animation: slideInLeft 0.8s ease-out;
    .metric-label {
        color: #666;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
   }
   
    /* Scrollbar personalizada */
    ::-webkit-scrollbar {
        width: 8px;
    /* Animação de loading */
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px;
   }
   
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
        border-radius: 4px;
    .spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
   }
   
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        border-radius: 4px;
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
   }
   
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #FFA500, #FFD700);
    /* Seções */
    .section-header {
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem;
        font-weight: bold;
        margin: 2rem 0 1rem 0;
   }
   
    /* Responsividade otimizada para 100% de escala */
    @media screen and (min-width: 1400px) {
        .stApp {
            padding: 1.5rem;
    /* Responsividade */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2rem;
       }
        
        .block-container {
            padding: 2rem;
        }
        
        .glass-card {
            padding: 20px;
        }
        
        h1 { font-size: 2.5rem !important; }
        h2 { font-size: 2rem !important; }
        h3 { font-size: 1.8rem !important; }
        h4 { font-size: 1.3rem !important; }
        
        table {
            font-size: 0.9rem !important;
        }
        
        .stButton>button {
            font-size: 0.9rem !important;
            padding: 10px 20px !important;
        .metric-value {
            font-size: 1.8rem;
       }
   }
   
    @media screen and (min-width: 1200px) and (max-width: 1399px) {
        .stApp {
            padding: 1rem;
        }
        
        .block-container {
            padding: 1.5rem;
        }
        
        .glass-card {
            padding: 18px;
        }
        
        h1 { font-size: 2.2rem !important; }
        h2 { font-size: 1.8rem !important; }
        h3 { font-size: 1.5rem !important; }
        h4 { font-size: 1.1rem !important; }
        
        table {
            font-size: 0.85rem !important;
        }
        
        .stButton>button {
            font-size: 0.85rem !important;
            padding: 8px 16px !important;
        }
    /* Estilo para dataframes */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
   }
    </style>
    """, unsafe_allow_html=True)

# ==============
# INTERFACE
# ==============

def main():
    # CSS customizado
    aplicar_css_customizado()

    @media screen and (max-width: 1199px) {
        .stApp {
            padding: 0.8rem;
        }
    # Header principal
    st.markdown("""
    <div class="header-container">
        <div class="header-title">📊 Dashboard Precs</div>
        <div class="header-subtitle">💰 Movimentações Financeiras Municipais | Análise Comparativa de Saldos</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Spinner de loading
    with st.spinner('🔄 Carregando dados...'):
        time.sleep(0.5)  # Simula loading
    
    # Seção de filtros de data com design melhorado
    st.markdown('<h2 class="section-header">🕰️ Configuração de Período</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        data_ref = st.date_input(
            "📅 Data de Referência", 
            value=datetime.today().date(),
            help="Data inicial para comparação dos saldos"
        )
    with col2:
        data_hoje = st.date_input(
            "📆 Data Atual", 
            value=datetime.today().date(),
            help="Data final para comparação dos saldos"
        )
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("♾️ Reset", help="Restaurar datas para hoje"):
            st.rerun()

    # Validação das datas
    hoje = datetime.today().date()
    
    if data_hoje < data_ref:
        st.warning("⚠️ A data atual é menor que a data de referência. Ajustando para a mesma data.")
        data_hoje = data_ref

    if data_hoje > hoje:
        st.warning("⚠️ A data atual não pode ser maior que hoje. Ajustando para hoje.")
        data_hoje = hoje

        .block-container {
            padding: 1.2rem;
    if data_ref > hoje:
        st.warning("⚠️ A data de referência não pode ser maior que hoje. Ajustando para hoje.")
        data_ref = hoje

    # Loading customizado e otimizado
    loading_placeholder = st.empty()
    
    with loading_placeholder.container():
        st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; padding: 2rem;">
            <div style="text-align: center;">
                <div style="
                    width: 50px; height: 50px; border: 4px solid #f3f3f3;
                    border-top: 4px solid #667eea; border-radius: 50%;
                    animation: spin 1s linear infinite; margin: 0 auto 1rem auto;
                "></div>
                <p style="color: #667eea; font-weight: bold;">💰 Carregando dashboard financeiro...</p>
                <p style="color: #999; font-size: 0.9rem;">Aguarde alguns instantes</p>
            </div>
        </div>
        <style>
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
       }
        </style>
        """, unsafe_allow_html=True)
    
    # Carregamento otimizado dos dados baseado nas datas selecionadas
    try:
        # Expandir significativamente o período para garantir dados suficientes
        data_inicio_query = min(data_ref, data_hoje) - pd.DateOffset(days=180)  # 6 meses antes
        data_fim_query = max(data_ref, data_hoje) + pd.DateOffset(days=30)     # 1 mês depois

        .glass-card {
            padding: 15px;
        }
        df = carregar_dados_movimentacoes(data_inicio_query.date(), data_fim_query.date())
        df_resultado = calcular_saldos(df, data_hoje, data_ref)

        h1 { font-size: 2rem !important; }
        h2 { font-size: 1.6rem !important; }
        h3 { font-size: 1.3rem !important; }
        h4 { font-size: 1rem !important; }
        # Remove loading
        loading_placeholder.empty()

        table {
            font-size: 0.8rem !important;
        }
        # Debug info
        st.info(f"📊 **Dados carregados:** {len(df)} registros encontrados | Período: {data_inicio_query.date()} a {data_fim_query.date()}")

        .stButton>button {
            font-size: 0.8rem !important;
            padding: 8px 14px !important;
        }
    }
    
    /* Ajustes específicos para 100% de escala */
    @media screen and (min-width: 1000px) {
        .stColumns {
            gap: 1rem !important;
        }
        # Verifica se não há dados para o período
        if df_resultado.empty:
            st.warning("⚠️ Não foram encontrados dados para o período selecionado.")
            if len(df) == 0:
                st.error("❌ Nenhum registro encontrado no banco de dados para este período.")
            else:
                st.info(f"💡 Encontrados {len(df)} registros, mas nenhum para as datas específicas: {data_ref.strftime('%d/%m/%Y')} e {data_hoje.strftime('%d/%m/%Y')}")
            return
            
    except Exception as e:
        loading_placeholder.empty()
        st.error(f"❌ Erro ao carregar dados: {str(e)}")
        st.info("💡 Tente selecionar um período diferente ou verifique a conexão com o banco.")
        return
    
    # Métricas de resumo
    if not df_resultado.empty:
        total_municipios, saldo_atual, saldo_ref, variacao = criar_metricas_resumo(df_resultado)

        .glass-card {
            margin: 8px 0 !important;
        }
        st.markdown('<h2 class="section-header">📈 Resumo Executivo</h2>', unsafe_allow_html=True)

        /* Reduzir tamanho das imagens */
        img {
            max-width: 100% !important;
            height: auto !important;
        }
        col1, col2, col3, col4 = st.columns(4)

        /* Ajustar altura da tabela */
        .tabela-container {
            max-height: 70vh !important;
            overflow-y: auto !important;
        }
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_municipios}</div>
                <div class="metric-label">🏢 Municípios</div>
            </div>
            """, unsafe_allow_html=True)

        /* Otimizar espaçamentos */
        .block-container {
            margin: 0.5rem 0 !important;
        }
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{formatar_brl(saldo_atual)}</div>
                <div class="metric-label">💰 Saldo Total Atual</div>
            </div>
            """, unsafe_allow_html=True)

        /* Reduzir padding dos cards */
        .glass-card {
            padding: 15px !important;
        }
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{formatar_brl(saldo_ref)}</div>
                <div class="metric-label">📅 Saldo Referência</div>
            </div>
            """, unsafe_allow_html=True)

        /* Ajustar tamanho das fontes */
        h1 { font-size: 2rem !important; }
        h2 { font-size: 1.6rem !important; }
        h3 { font-size: 1.4rem !important; }
        h4 { font-size: 1.1rem !important; }
        with col4:
            cor_variacao = "#e74c3c" if variacao < 0 else "#27ae60"
            icone_variacao = "🔻" if variacao < 0 else "🔺"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: {cor_variacao}">{formatar_brl(variacao)}</div>
                <div class="metric-label">{icone_variacao} Variação Total</div>
            </div>
            """, unsafe_allow_html=True)

        /* Otimizar tabela */
        table {
            font-size: 0.85rem !important;
        }
        # Gráfico dos top municípios
        fig = criar_grafico_top_municipios(df_resultado)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

        /* Reduzir altura das barras de progresso */
        .progress-bar {
            height: 14px !important;
        }
    }
    
    /* Animação de pulse para o sino */
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
            filter: drop-shadow(0 0 10px rgba(255, 215, 0, 0.4));
        }
        50% {
            transform: scale(1.5);
            filter: drop-shadow(0 0 15px rgba(255, 215, 0, 0.6));
        }
    }
    
    /* Barras de progresso contornadas */
    .progress-bar {
        background: #2C2C2C;
        border-radius: 6px;
        border: 2px solid #FFD700;
        overflow: hidden;
        position: relative;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.3);
        margin: 2px;
    }
    
    .progress-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.8s ease;
        position: relative;
        border: 1px solid rgba(255, 215, 0, 0.5);
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Efeitos de brilho sutis */
    .glow {
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.3);
    }
    
    .glow:hover {
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.5);
    }
    </style>
""", unsafe_allow_html=True)



# ---- Autoatualização (a cada 10 segundos) ----
st_autorefresh(interval=70 * 1000, key="atualizacao")

print(f"Página atualizada em: {datetime.now().strftime('%H:%M:%S')}")

def image_to_base64(image_path):
    img = Image.open(image_path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode()
    return img_b64

def formatar_data_pt_br():
    """Formata a data atual em português brasileiro sem depender de locale"""
    from datetime import datetime
    hoje = datetime.now()
    
    # Mapeamento de dias da semana
    dias_semana = {
        0: "Segunda-feira",
        1: "Terça-feira", 
        2: "Quarta-feira",
        3: "Quinta-feira",
        4: "Sexta-feira",
        5: "Sábado",
        6: "Domingo"
    }
    
    # Mapeamento de meses
    meses = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }
    
    dia_semana = dias_semana[hoje.weekday()]
    dia = hoje.day
    mes = meses[hoje.month]
    ano = hoje.year
    
    return f"{dia_semana} - {dia:02d}/{hoje.month:02d}/{ano}"

# ---- Carrega variáveis do .env ----
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# ---- Conectar ao PostgreSQL ----
def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        sslmode="require"
    )

# ---- Carregar dados ----
@st.cache_data(ttl=10)
def carregar_dados_propostas():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM dashmetas", conn)
    df["data"] = pd.to_datetime(df["data"])
    conn.close()
    return df

@st.cache_data(ttl=10)
def carregar_dados_campanhas():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM campanhas", conn)
    conn.close()
    return df
        st.markdown("---")

def atualizar_status_campanhas(campanhas_selecionadas):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE campanhas SET status_campanha = FALSE")
        for campanha in campanhas_selecionadas:
            cur.execute(
                "UPDATE campanhas SET status_campanha = TRUE WHERE nome_campanha = %s",
                (campanha,)
    # Filtro por município com design melhorado
    st.markdown('<h2 class="section-header">🗂️ Seleção de Municípios</h2>', unsafe_allow_html=True)
    with st.expander("Selecionar municípios para exibição", expanded=False):
        filtro_busca = st.text_input("🔍 Buscar município")
        municipios_ordenados = df_resultado['Município'].tolist()
        
        if filtro_busca:
            termo = filtro_busca.lower()
            municipios_filtrados = sorted(
                municipios_ordenados,
                key=lambda m: (termo not in m.lower(), m)
)
        conn.commit()
    except Exception as e:
        st.error(f"Erro ao atualizar status das campanhas: {e}")
    finally:
        cur.close()
        conn.close()

def contar_propostas(df, df_original):
    # Garante que a coluna 'data' é datetime
    df['data'] = pd.to_datetime(df['data'])

    # Ordena pela data (da mais recente primeiro)
    df_sorted = df.sort_values(by='data', ascending=False)

    # Mantém a última vez que cada negócio passou por cada etapa
    df_ultimos = df_sorted.drop_duplicates(subset=['id_negocio', 'id_etapa'], keep='first')


    # Lista de todos os proprietários (caso queira usar depois)
    all_proprietarios = df_original['proprietario'].unique()

    # Contagem de negócios que passaram pela etapa 'Cálculo' (última vez de cada um)
    df_adquiridas = df_ultimos[df_ultimos['id_etapa'] == 'Cálculo'] \
        .groupby('proprietario').agg(quantidade_adquiridas=('id_negocio', 'nunique')).reset_index()

    # Contagem de negócios que passaram pela etapa 'Negociações iniciadas' (última vez de cada um)
    df_apresentadas = df_ultimos[df_ultimos['id_etapa'] == 'Negociações iniciadas'] \
        .groupby('proprietario').agg(quantidade_apresentadas=('id_negocio', 'nunique')).reset_index()

    # Garante todos os proprietários no resultado final
    df_adquiridas_full = pd.DataFrame({'proprietario': all_proprietarios}) \
        .merge(df_adquiridas, on='proprietario', how='left').fillna(0)
    
    df_apresentadas_full = pd.DataFrame({'proprietario': all_proprietarios}) \
        .merge(df_apresentadas, on='proprietario', how='left').fillna(0)

    # Junta os resultados
    return pd.merge(df_adquiridas_full, df_apresentadas_full, on='proprietario', how='outer').fillna(0)

def get_cor_barra(valor, maximo=6):
    if valor >= maximo:
        return "background: linear-gradient(45deg, #FFD700, #FFA500); box-shadow: 0 0 10px rgba(255, 215, 0, 0.6), 0 0 20px rgba(255, 215, 0, 0.4), 0 0 30px rgba(255, 215, 0, 0.2);"
    return "background: linear-gradient(45deg, #c3a43e, #d4af37); box-shadow: 0 0 5px rgba(195, 164, 62, 0.4);"



df_original = carregar_dados_propostas()
df = df_original.copy()
df_campanhas = carregar_dados_campanhas()
        else:
            municipios_filtrados = municipios_ordenados

        if "checkbox_states" not in st.session_state:
            st.session_state.checkbox_states = {m: True for m in municipios_ordenados}
            st.session_state.selecionar_todos = True

        col1, col2 = st.columns(2)
        with col1:
            selecionar_todos = st.checkbox("Selecionar todos", value=st.session_state.selecionar_todos)

        if selecionar_todos != st.session_state.selecionar_todos:
            for m in municipios_filtrados:
                st.session_state.checkbox_states[m] = selecionar_todos
            st.session_state.selecionar_todos = selecionar_todos

        municipios_selecionados = []
        for municipio in municipios_filtrados:
            checked = st.checkbox(municipio, value=st.session_state.checkbox_states.get(municipio, True), key=f"check_{municipio}")
            st.session_state.checkbox_states[municipio] = checked
            if checked:
                municipios_selecionados.append(municipio)

    # Filtrar dataframe para exibição
    df_filtrado = df_resultado[df_resultado['Município'].isin(municipios_selecionados)]

    # Exibição da tabela principal
    st.markdown('<h2 class="section-header">💰 Comparativo Detalhado por Município</h2>', unsafe_allow_html=True)
    
    if df_filtrado.empty:
        st.warning("⚠️ Nenhum município selecionado ou dados disponíveis para o período.")
        return
    col_ref = f"Saldo ({data_ref.strftime('%d/%m/%Y')})"
    col_hoje = f"Saldo ({data_hoje.strftime('%d/%m/%Y')})"

    st.dataframe(
        df_filtrado.style.format({
            col_ref: formatar_brl,
            col_hoje: formatar_brl,
            'Movimentação': formatar_brl
        }).set_properties(**{'text-align': 'right'}),
        use_container_width=True,
        hide_index=True
    )
    st.caption("🔁 Se não houver movimentação exata na data, usa-se o valor mais próximo anterior.")

# ---- Sidebar ----
with st.sidebar:
    st.header("Filtros")
    mostrar_gestao = st.checkbox("Mostrar proprietário 'Gestão'", value=False)
    
    proprietarios_disponiveis = df["proprietario"].unique().tolist()
    if not mostrar_gestao:
        proprietarios_disponiveis = [p for p in proprietarios_disponiveis if p != "Gestão"]
    # Seção do histórico com tabs
    st.markdown("---")
    st.markdown('<h2 class="section-header">🧾 Histórico Detalhado</h2>', unsafe_allow_html=True)

    proprietarios = st.multiselect("Proprietário", options=proprietarios_disponiveis, default=proprietarios_disponiveis)
    etapas = st.multiselect("Etapa", df["id_etapa"].unique(), default=df["id_etapa"].unique())
    data_ini = st.date_input("Data inicial", df["data"].max().date())
    data_fim = st.date_input("Data final", df["data"].max().date())
    tab1, tab2 = st.tabs(["📋 Movimentações Completas", "📈 Análise Temporal"])

    campanhas_disponiveis = df_campanhas["nome_campanha"].tolist()
    campanhas_selecionadas = st.multiselect(
        "Campanhas",
        options=campanhas_disponiveis,
        default=df_campanhas[df_campanhas["status_campanha"] == True]["nome_campanha"].tolist(),
        key="campanhas_filtro"
    )
    with tab1:
        # Filtros
        municipios_disponiveis = ["Todos"] + sorted(df['municipio'].dropna().unique())
        municipio_filtro = st.selectbox("📍 Município (Histórico Bruto)", municipios_disponiveis)

atualizar_status_campanhas(campanhas_selecionadas)

if not mostrar_gestao:
    df = df[df["proprietario"] != "Gestão"]
    df_original = df_original[df_original["proprietario"] != "Gestão"]

df_filtrado = df.copy()
if proprietarios:
    df_filtrado = df_filtrado[df_filtrado["proprietario"].isin(proprietarios)]
if etapas:
    df_filtrado = df_filtrado[df_filtrado["id_etapa"].isin(etapas)]
df_filtrado = df_filtrado[
    (df_filtrado["data"].dt.date >= data_ini) &
    (df_filtrado["data"].dt.date <= data_fim)
]

df_propostas = contar_propostas(df_filtrado, df_original)
total_adquiridas = df_propostas['quantidade_adquiridas'].sum()
total_apresentadas = df_propostas['quantidade_apresentadas'].sum()

# Card de estatísticas removido conforme solicitado

# ---- Visualizações principais ----
col2, col1 = st.columns([1,3])

with col1:
    medalha_b64 = image_to_base64("medalha.png")
    if not df_propostas.empty:
        tabela_html = f"""
        <div class="glass-card fade-in-up" style="border: 1px solid rgba(255, 215, 0, 0.3); border-radius: 10px; overflow: hidden; margin: 10px 0;">
            <h2 style='background: linear-gradient(45deg, #FFD700, #FFA500); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; text-align: center; font-size: 2rem; margin: 10px 0; text-shadow: 0 0 8px rgba(255, 215, 0, 0.3);'>
                Propostas Diárias
            </h2>
            <table style="width: 100%; border-collapse: collapse; font-size: 0.8rem; background: #1a1a1a; border-radius: 8px; overflow: hidden;">
            <thead>
                <tr style="border-bottom: 1px solid rgba(255, 215, 0, 0.3); background: #000000;">
                    <th style="font-size: 1rem; text-align: left; background: #000000; color: #FFD700; padding: 8px 12px; text-shadow: 0 0 3px rgba(255, 215, 0, 0.3);">Nome</th>
                    <th style="font-size: 1rem; text-align: center; background: #1A1A1A; color: #FFD700; padding: 8px 12px; text-shadow: 0 0 3px rgba(255, 215, 0, 0.3);">Adquiridas: {int(total_adquiridas)}/90</th>
                    <th style="font-size: 1rem; text-align: center; background: #333333; color: #FFD700; padding: 8px 12px; text-shadow: 0 0 3px rgba(255, 215, 0, 0.3);">Apresentadas: {int(total_apresentadas)}/90</th>
                </tr>
            </thead>
            <tbody>
        # Filtro SQL pelo município
        filtro_sql = f"WHERE municipio = '{municipio_filtro}'" if municipio_filtro != "Todos" else ""

        # Controle de paginação para melhor performance
        st.markdown("📊 **Configurações de Exibição**")
        col1, col2 = st.columns(2)
        with col1:
            limite_registros = st.selectbox("📄 Registros por página", [100, 500, 1000, 2000], index=1)
        with col2:
            ordenacao = st.selectbox("📅 Ordenação", ["Mais recente primeiro", "Mais antigo primeiro"], index=0)
        
        ordem_sql = "DESC" if ordenacao == "Mais recente primeiro" else "ASC"
        
        query_paginada = f"""
            SELECT *
            FROM movimentacoes
            {filtro_sql}
            ORDER BY data_movimentacao {ordem_sql}, id {ordem_sql}
            LIMIT {limite_registros}
       """

        maximo = 6
        for _, row in df_propostas.iterrows():
            nome = row['proprietario']
            valor1 = int(row['quantidade_adquiridas'])
            valor2 = int(row['quantidade_apresentadas'])
            medalha_html = f"""<img src="data:image/png;base64,{medalha_b64}" width="18" style="margin-left: 6px; vertical-align: middle;">""" \
                if valor1 >= 6 or valor2 >= 6 else ""
            
            proporcao1 = min(valor1 / maximo, 1.0)
            proporcao2 = min(valor2 / maximo, 1.0)
            cor_barra1 = get_cor_barra(valor1)
            cor_barra2 = get_cor_barra(valor2)

            barra1 = f"""
            <div class="progress-bar" style='width: 100%; height: 12px; margin-bottom: 4px; border: 2px solid #FFD700;'>
                <div class="progress-fill" style='width: {proporcao1*100:.1f}%; {cor_barra1} height: 100%; border: 1px solid rgba(255, 215, 0, 0.6);'></div>
            </div>
            <span style='font-size: 0.8rem; color: #FFD700; font-weight: bold; text-shadow: 0 0 2px rgba(255, 215, 0, 0.3);'>{valor1}/{maximo}</span>
            """
        with st.spinner('📋 Carregando registros...'):
            df_bruto = pd.read_sql(query_paginada, engine)

            barra2 = f"""
            <div class="progress-bar" style='width: 100%; height: 12px; margin-bottom: 4px; border: 2px solid #FFD700;'>
                <div class="progress-fill" style='width: {proporcao2*100:.1f}%; {cor_barra2} height: 100%; border: 1px solid rgba(255, 215, 0, 0.6);'></div>
            </div>
            <span style='font-size: 0.8rem; color: #FFD700; font-weight: bold; text-shadow: 0 0 2px rgba(255, 215, 0, 0.3);'>{valor2}/{maximo}</span>
            """

            tabela_html += f"""
            <tr style="border-bottom: 1px solid rgba(255, 215, 0, 0.2); background: #2a2a2a;">
                <td style="font-size: 1.5rem; background: #000000; padding: 6px 10px; color: #FFF; vertical-align: middle; text-align: left; text-shadow: 0 0 2px rgba(255, 255, 255, 0.3);">
                    {nome} {medalha_html}
                </td>
                <td style="padding: 6px 10px; background: #1A1A1A; color: #FFD700; vertical-align: middle; text-align: center; text-shadow: 0 0 2px rgba(255, 215, 0, 0.3);">
                    {barra1}
                </td>
                <td style="padding: 6px 10px; background: #333333; color: #FFD700; vertical-align: middle; text-align: center; text-shadow: 0 0 2px rgba(255, 215, 0, 0.3);">
                    {barra2}
                </td>
            </tr>
            """

        tabela_html += "</tbody></table></div>"
        components.html(tabela_html, height=1000, scrolling=False)


with col2:
    logo_b64 = image_to_base64("precs2.png")
    sino_b64 = image_to_base64("sino.png")  # Seu arquivo de sino
    
    st.markdown(f"""
        <div class="glass-card slide-in-left" style="display: flex; justify-content: center; align-items: center; text-align: center; margin-bottom: 20px;"> 
            <img src="data:image/png;base64,{logo_b64}" width="200" style="border-radius: 12px; box-shadow: 0 8px 25px rgba(255, 215, 0, 0.2); filter: drop-shadow(0 0 6px rgba(255, 215, 0, 0.3));">
        </div> 
    """, unsafe_allow_html=True)
    
    # Cabeçalho com logo e título
    st.markdown(f"""
        <div class="glass-card fade-in-up" style="display: flex; justify-content: center; align-items: center; text-align: center; margin-bottom: 15px;">
            <h1 style="background: linear-gradient(45deg, #FFD700, #FFA500); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 2.5rem; margin: 0; text-shadow: 0 0 10px rgba(255, 215, 0, 0.3);">Precs Propostas</h1> 
        </div>
        <div class="glass-card fade-in-up" style="text-align: center; margin-bottom: 15px;">
            <h3 style='background: linear-gradient(45deg, #C5A45A, #D4AF37); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 1rem; font-weight: bold; text-shadow: 0 0 8px rgba(197, 164, 90, 0.3);'>
                {formatar_data_pt_br()}
            </h3>
        </div>
    """, unsafe_allow_html=True)
        # Remove duplicados considerando colunas específicas
        colunas_para_deduplicar = ['municipio', 'data_movimentacao', 'lancamento_valor']
        df_bruto = df_bruto.drop_duplicates(subset=colunas_para_deduplicar)

    # Título das campanhas + sino
    st.markdown("""
        <div class="glass-card fade-in-up" style="text-align: center; margin-bottom: 15px;">
            <h2 style='background: linear-gradient(45deg, #D4AF37, #FFD700); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; text-shadow: 0 0 8px rgba(212, 175, 55, 0.3);'>Campanhas Ativas</h2>
        </div>
    """, unsafe_allow_html=True)
        # Formatação dos valores em BRL
        for col in ['saldo_anterior_valor', 'saldo_atualizado_valor', 'lancamento_valor']:
            if col in df_bruto.columns:
                df_bruto[col] = df_bruto[col].apply(formatar_brl)

    st.markdown(f"""
        <div class="glass-card fade-in-up" style='text-align: center; margin-bottom: 15px;'>
            <img src="data:image/png;base64,{sino_b64}" width="100px;" style="filter: drop-shadow(0 0 8px rgba(255, 215, 0, 0.4)); animation: pulse 2s ease-in-out infinite;">
        </div>
    """, unsafe_allow_html=True)
        # Info do município selecionado
        if municipio_filtro != "Todos":
            st.info(f"🔍 Exibindo movimentações para: **{municipio_filtro}**")
        else:
            st.info("🔍 Exibindo movimentações para todos os municípios")
        
        # Estatísticas rápidas
        if not df_bruto.empty:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📄 Total de Registros", len(df_bruto))
            with col2:
                data_mais_antiga = df_bruto['data_movimentacao'].min() if 'data_movimentacao' in df_bruto.columns else None
                if data_mais_antiga:
                    st.metric("📅 Data Mais Antiga", pd.to_datetime(data_mais_antiga).strftime('%d/%m/%Y'))
            with col3:
                data_mais_recente = df_bruto['data_movimentacao'].max() if 'data_movimentacao' in df_bruto.columns else None
                if data_mais_recente:
                    st.metric("📆 Data Mais Recente", pd.to_datetime(data_mais_recente).strftime('%d/%m/%Y'))
        
        # Dataframe com melhor styling
        st.dataframe(
            df_bruto, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "data_movimentacao": st.column_config.DateColumn(
                    "Data",
                    format="DD/MM/YYYY",
                ),
            }
        )
    
    with tab2:
        st.markdown("🔄 **Análise temporal em desenvolvimento...**")
        st.info("💡 Funcionalidade para gráficos de tendência temporal será adicionada em breve.")


if __name__ == "__main__":
    main()

    # Lista de campanhas
    campanhas_ativas = df_campanhas[df_campanhas["status_campanha"] == True]
    for i, (_, campanha) in enumerate(campanhas_ativas.iterrows()):
        st.markdown(f"""
            <div class="glass-card fade-in-up" style="display: flex; justify-content: center; align-items: center; text-align: center; margin-bottom: 8px; padding: 12px; animation-delay: {i * 0.2}s;">
                <span style="font-size: 1.2rem; background: linear-gradient(45deg, #FFF, #FFD700); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; text-shadow: 0 0 8px rgba(255, 255, 255, 0.3);">{campanha['nome_campanha']}</span>
            </div>
        """, unsafe_allow_html=True)
