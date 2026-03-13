@echo off
chcp 65001 >nul
echo ========================================
echo   智能内容分发助手 v3.0
echo ========================================
echo.

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查依赖
echo [1/3] 检查依赖...
if not exist venv (
    echo 创建虚拟环境...
    python -m venv venv
)

call venv\Scripts\activate.bat

REM 安装依赖
echo [2/3] 安装/更新依赖...
pip install -q -r requirements.txt

REM 启动应用
echo [3/3] 启动应用...
echo.
echo 应用将在浏览器中打开...
echo 如未自动打开，请访问: http://localhost:8501
echo.
streamlit run main.py

pause
