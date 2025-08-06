import streamlit as st
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime
from streamlit_autorefresh import st_autorefresh 
from io import BytesIO
import base64
from PIL import Image
import plotly.express as px
import streamlit.components.v1 as components
from datetime import datetime
st.session_state.page_height = 900  # ou use st.window_height, futuramente
import locale
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
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
@@ -365,6 +372,36 @@
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
@@ -588,28 +625,28 @@
        </div>
        <div class="glass-card fade-in-up" style="text-align: center; margin-bottom: 15px;">
            <h3 style='background: linear-gradient(45deg, #C5A45A, #D4AF37); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 1rem; font-weight: bold; text-shadow: 0 0 8px rgba(197, 164, 90, 0.3);'>
                Segunda-feira - 28/07/2025
                {formatar_data_pt_br()}
            </h3>
        </div>
    """, unsafe_allow_html=True)

    # Título das campanhas + sino
    st.markdown("""
        <div class="glass-card fade-in-up" style="text-align: center; margin-bottom: 15px;">
            <h2 style='background: linear-gradient(45deg, #D4AF37, #FFD700); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; text-shadow: 0 0 8px rgba(212, 175, 55, 0.3);'>Campanhas Ativas</h2>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="glass-card fade-in-up" style='text-align: center; margin-bottom: 15px;'>
            <img src="data:image/png;base64,{sino_b64}" width="100px;" style="filter: drop-shadow(0 0 8px rgba(255, 215, 0, 0.4)); animation: pulse 2s ease-in-out infinite;">
        </div>
    """, unsafe_allow_html=True)

    # Lista de campanhas
    campanhas_ativas = df_campanhas[df_campanhas["status_campanha"] == True]
    for i, (_, campanha) in enumerate(campanhas_ativas.iterrows()):
        st.markdown(f"""
            <div class="glass-card fade-in-up" style="display: flex; justify-content: center; align-items: center; text-align: center; margin-bottom: 8px; padding: 12px; animation-delay: {i * 0.2}s;">
                <span style="font-size: 1.2rem; background: linear-gradient(45deg, #FFF, #FFD700); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; text-shadow: 0 0 8px rgba(255, 255, 255, 0.3);">{campanha['nome_campanha']}</span>
            </div>
