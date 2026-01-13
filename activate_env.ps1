# PowerShell script to activate hands-on-aai conda environment
# Usage: .\activate_env.ps1
#
# 配置说明：
# 1. 如果您的conda安装在默认位置，脚本会自动检测
# 2. 如果conda安装在自定义位置，请修改下面的CONDA_PATH变量
# 3. 或者直接使用 conda activate hands-on-aai 命令

Write-Host "Activating conda environment: hands-on-aai" -ForegroundColor Green

# ============================================
# 配置区域：根据您的conda安装路径修改
# ============================================
# 常见的conda安装路径（按优先级尝试）：
$CONDA_PATHS = @(
    "$env:USERPROFILE\Anaconda3",
    "$env:USERPROFILE\miniconda3",
    "C:\Anaconda3",
    "C:\Anaconda",
    "C:\ProgramData\Anaconda3",
    "C:\ProgramData\miniconda3"
)

# 如果您的conda安装在其他位置，请取消注释并修改下面这行：
# $CUSTOM_CONDA_PATH = "C:\Your\Custom\Conda\Path"

# ============================================
# 自动检测conda路径
# ============================================
$CONDA_FOUND = $false
$CONDA_PATH = $null

# 检查自定义路径（如果设置了）
if ($CUSTOM_CONDA_PATH -and (Test-Path "$CUSTOM_CONDA_PATH\Scripts\conda.exe")) {
    $CONDA_PATH = $CUSTOM_CONDA_PATH
    $CONDA_FOUND = $true
}

# 自动检测conda路径
if (-not $CONDA_FOUND) {
    foreach ($path in $CONDA_PATHS) {
        if (Test-Path "$path\Scripts\conda.exe") {
            $CONDA_PATH = $path
            $CONDA_FOUND = $true
            break
        }
    }
}

# 初始化conda
if ($CONDA_FOUND) {
    Write-Host "Found conda at: $CONDA_PATH" -ForegroundColor Cyan
    & "$CONDA_PATH\Scripts\conda.exe" "shell.powershell" "hook" | Out-String | Invoke-Expression
} elseif (Get-Command conda -ErrorAction SilentlyContinue) {
    Write-Host "Using system conda command" -ForegroundColor Cyan
    # conda已在PATH中
} else {
    Write-Host "Warning: Could not find conda. Please ensure conda is installed and in PATH." -ForegroundColor Yellow
    Write-Host "You can manually activate the environment with: conda activate hands-on-aai" -ForegroundColor Yellow
    exit 1
}

# Activate the environment
try {
    conda activate hands-on-aai
    Write-Host "Successfully activated environment: hands-on-aai" -ForegroundColor Green
} catch {
    Write-Host "Error activating environment. Make sure it exists:" -ForegroundColor Red
    Write-Host "  conda create -n hands-on-aai python=3.10 -y" -ForegroundColor Yellow
    exit 1
}

# Verify activation
Write-Host "`nEnvironment Information:" -ForegroundColor Cyan
Write-Host "  Current conda environment: $env:CONDA_DEFAULT_ENV" -ForegroundColor Cyan
Write-Host "  Python path: $(python -c 'import sys; print(sys.executable)')" -ForegroundColor Cyan

# Check PyTorch CUDA
Write-Host "`nChecking PyTorch CUDA availability..." -ForegroundColor Yellow
try {
    python -c "import torch; print('PyTorch version:', torch.__version__); print('CUDA available:', torch.cuda.is_available())"
} catch {
    Write-Host "PyTorch not installed. Install with: pip install -r requirements.txt" -ForegroundColor Yellow
}
