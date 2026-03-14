@echo off
chcp 65001 >nul
echo ========================================
echo   智能内容分发助手 - GitHub一键发布工具
echo ========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo [1/6] 检查Git是否已安装...
git --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Git，请先安装Git
    echo 下载地址: https://git-scm.com/downloads
    pause
    exit /b 1
)

echo [2/6] 检查Git配置...
git config user.name >nul 2>&1
if errorlevel 1 (
    set /p git_username="请输入Git用户名: "
    if "%git_username%"=="" (
        echo [错误] 必须输入Git用户名
        pause
        exit /b 1
    )
    git config user.name "%git_username%"
)

git config user.email >nul 2>&1
if errorlevel 1 (
    set /p git_email="请输入Git邮箱: "
    if "%git_email%"=="" (
        echo [错误] 必须输入Git邮箱
        pause
        exit /b 1
    )
    git config user.email "%git_email%"
)

echo [3/6] 获取GitHub信息...
set /p github_username="请输入你的GitHub用户名: "
if "%github_username%"=="" (
    echo [错误] 必须输入GitHub用户名
    pause
    exit /b 1
)

echo.
echo ========================================
echo      创建GitHub仓库指引
echo ========================================
echo.
echo 请按以下步骤创建GitHub仓库:
echo.
echo 1. 访问: https://github.com/new
echo 2. 填写仓库信息:
echo    - Repository name: smart-content-publisher
echo    - Description: 智能内容分发助手 - 支持微信公众号、飞书、小红书的自动内容分发工具
echo    - 选择 Public (公开) 或 Private (私有)
echo    - 不要勾选 'Add a README file' (我们已经有了)
echo    - 点击 Create repository
echo.
echo 3. 创建完成后，返回此窗口继续
echo.
pause

echo [4/6] 配置远程仓库...
git remote remove origin >nul 2>&1
git remote add origin "https://github.com/%github_username%/smart-content-publisher.git"
if errorlevel 1 (
    echo [错误] 添加远程仓库失败
    pause
    exit /b 1
)

echo [5/6] 推送代码到GitHub...
git branch -M main
git push -u origin main
if errorlevel 1 (
    echo.
    echo [警告] 推送失败，可能是以下原因:
    echo 1. GitHub仓库尚未创建
    echo 2. 认证失败 (使用双因素认证需要个人访问令牌)
    echo.
    echo [解决方案]
    echo 1. 确保已按指引创建仓库
    echo 2. 生成PAT: GitHub Settings ^> Developer settings ^> Personal access tokens
    echo 3. 手动执行: git push -u origin main
    echo.
    pause
    exit /b 1
)

echo [6/6] 创建发布标签...
set /p create_tag="是否创建v3.0.0发布标签? (y/N): "
if /i "%create_tag%"=="y" (
    git tag -a v3.0.0 -m "Release version 3.0.0 - Initial MVP"
    git push origin v3.0.0
    if errorlevel 1 (
        echo [警告] 标签推送失败，但代码已成功推送
    ) else (
        echo [成功] 标签创建并推送成功!
    )
)

echo.
echo ========================================
echo        发布完成!
echo ========================================
echo.
echo [OK] 代码已推送到GitHub
echo [REPO] 仓库地址: https://github.com/%github_username%/smart-content-publisher
echo.
echo [NEXT] 下一步操作:
echo 1. 访问你的GitHub仓库查看代码
echo 2. 进入 Actions 标签查看自动构建状态
echo 3. 构建完成后可以下载可执行文件
echo.
echo [TOOLS] 使用方式:
echo   直接运行: streamlit run main.py
echo   或双击: 启动.bat
echo   打包使用: python build_exe.py --mode onedir
echo.
pause
