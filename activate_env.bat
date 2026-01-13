@echo off
REM Batch script to activate hands-on-aai conda environment
REM Usage: activate_env.bat
REM
REM 配置说明：
REM 1. 如果您的conda安装在默认位置，脚本会自动尝试常见路径
REM 2. 如果conda安装在自定义位置，请修改下面的CONDA_PATH变量
REM 3. 或者直接使用 conda activate hands-on-aai 命令

echo Activating conda environment: hands-on-aai

REM ============================================
REM 配置区域：根据您的conda安装路径修改
REM ============================================
REM 如果您的conda安装在自定义位置，取消注释并修改下面这行：
REM set CUSTOM_CONDA_PATH=C:\Your\Custom\Conda\Path

REM ============================================
REM 自动检测conda路径
REM ============================================
set CONDA_FOUND=0
set CONDA_PATH=

REM 检查自定义路径（如果设置了）
if defined CUSTOM_CONDA_PATH (
    if exist "%CUSTOM_CONDA_PATH%\Scripts\activate.bat" (
        set CONDA_PATH=%CUSTOM_CONDA_PATH%
        set CONDA_FOUND=1
    )
)

REM 自动检测常见conda路径
if %CONDA_FOUND%==0 (
    if exist "%USERPROFILE%\Anaconda3\Scripts\activate.bat" (
        set CONDA_PATH=%USERPROFILE%\Anaconda3
        set CONDA_FOUND=1
    ) else if exist "%USERPROFILE%\miniconda3\Scripts\activate.bat" (
        set CONDA_PATH=%USERPROFILE%\miniconda3
        set CONDA_FOUND=1
    ) else if exist "C:\Anaconda3\Scripts\activate.bat" (
        set CONDA_PATH=C:\Anaconda3
        set CONDA_FOUND=1
    ) else if exist "C:\Anaconda\Scripts\activate.bat" (
        set CONDA_PATH=C:\Anaconda
        set CONDA_FOUND=1
    ) else if exist "C:\ProgramData\Anaconda3\Scripts\activate.bat" (
        set CONDA_PATH=C:\ProgramData\Anaconda3
        set CONDA_FOUND=1
    )
)

REM 初始化conda
if %CONDA_FOUND%==1 (
    echo Found conda at: %CONDA_PATH%
    call "%CONDA_PATH%\Scripts\activate.bat"
) else (
    echo Warning: Could not find conda at common locations.
    echo Trying to use conda from PATH...
    where conda >nul 2>&1
    if errorlevel 1 (
        echo Error: conda not found. Please ensure conda is installed and in PATH.
        echo You can manually activate the environment with: conda activate hands-on-aai
        pause
        exit /b 1
    )
)

REM Activate the environment
call conda activate hands-on-aai
if errorlevel 1 (
    echo Error activating environment. Make sure it exists:
    echo   conda create -n hands-on-aai python=3.10 -y
    pause
    exit /b 1
)

REM Verify activation
echo.
echo Environment Information:
echo   Current conda environment: %CONDA_DEFAULT_ENV%
python -c "import sys; print('  Python path:', sys.executable)"

REM Check PyTorch CUDA
echo.
echo Checking PyTorch CUDA availability...
python -c "import torch; print('PyTorch version:', torch.__version__); print('CUDA available:', torch.cuda.is_available())" 2>nul
if errorlevel 1 (
    echo PyTorch not installed. Install with: pip install -r requirements.txt
)

REM Keep the window open
cmd /k
