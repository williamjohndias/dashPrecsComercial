@echo off
echo ========================================
echo    Dashboard PRECS - Visual Moderno
echo ========================================
echo.
echo ✨ Interface com Glassmorphism
echo 🎨 Tema Escuro Elegante  
echo 📱 Design Responsivo
echo.
echo Verificando dependencias...
pip install streamlit pandas psycopg2-binary python-dotenv streamlit-autorefresh plotly Pillow flask >nul 2>&1
if %errorlevel% neq 0 (
    echo Erro ao instalar dependencias!
    pause
    exit /b 1
)

echo.
echo Iniciando aplicacao...
echo Acesse: http://localhost:8501
echo.
echo Pressione Ctrl+C para parar a aplicacao
echo ========================================
echo.

python run_dashboard.py

pause 