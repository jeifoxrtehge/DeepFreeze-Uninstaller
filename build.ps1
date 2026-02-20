# Build script for DeepFreeze Uninstaller
$VERSION = "v1.0.0"
$OUTPUT_DIR = "DeepFreeze-Uninstaller-$VERSION"

Write-Host "========================================" -ForegroundColor Green
Write-Host "   Build DeepFreeze Uninstaller" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Create output directory
Write-Host "[*] Creating output directory..." -ForegroundColor Cyan
if (Test-Path $OUTPUT_DIR) {
    Remove-Item -Recurse -Force $OUTPUT_DIR
}
New-Item -ItemType Directory -Path $OUTPUT_DIR | Out-Null

# Copy files
Write-Host "[*] Copying files..." -ForegroundColor Cyan
Copy-Item "README.md" $OUTPUT_DIR
Copy-Item "LICENSE" $OUTPUT_DIR
Copy-Item "启动器.bat" $OUTPUT_DIR
Copy-Item "一键斩杀冰点还原.bat" $OUTPUT_DIR
Copy-Item "强力uninstall 冰点还原.py" $OUTPUT_DIR
Copy-Item "强力uninstall 冰点还原_GUI.py" $OUTPUT_DIR
Copy-Item "强力uninstall 冰点还原_专业版.py" $OUTPUT_DIR

# Check PyInstaller
try {
    $pyinstaller = Get-Command pyinstaller -ErrorAction Stop
    Write-Host "[*] Building executables..." -ForegroundColor Cyan
    
    # Build CLI version
    Write-Host "[*] Building CLI version..." -ForegroundColor Cyan
    pyinstaller --onefile --name "DeepFreeze_Uninstaller_CLI" "强力uninstall 冰点还原.py" | Out-Null
    
    # Build GUI version
    Write-Host "[*] Building GUI version..." -ForegroundColor Cyan
    pyinstaller --onefile --windowed --name "DeepFreeze_Uninstaller_GUI" "强力uninstall 冰点还原_GUI.py" | Out-Null
    
    # Build Pro version
    Write-Host "[*] Building Pro version..." -ForegroundColor Cyan
    pyinstaller --onefile --name "DeepFreeze_Uninstaller_Pro" "强力uninstall 冰点还原_专业版.py" | Out-Null
    
    # Copy executables
    if (Test-Path "dist\DeepFreeze_Uninstaller_CLI.exe") {
        Copy-Item "dist\DeepFreeze_Uninstaller_CLI.exe" $OUTPUT_DIR
        Write-Host "[+] CLI build success" -ForegroundColor Green
    }
    
    if (Test-Path "dist\DeepFreeze_Uninstaller_GUI.exe") {
        Copy-Item "dist\DeepFreeze_Uninstaller_GUI.exe" $OUTPUT_DIR
        Write-Host "[+] GUI build success" -ForegroundColor Green
    }
    
    if (Test-Path "dist\DeepFreeze_Uninstaller_Pro.exe") {
        Copy-Item "dist\DeepFreeze_Uninstaller_Pro.exe" $OUTPUT_DIR
        Write-Host "[+] Pro build success" -ForegroundColor Green
    }
    
    # Cleanup
    Write-Host "[*] Cleaning temp files..." -ForegroundColor Cyan
    Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue
    Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
    Remove-Item *.spec -ErrorAction SilentlyContinue
}
catch {
    Write-Host "[!] PyInstaller not found, skipping exe build" -ForegroundColor Yellow
    Write-Host "[*] Install: pip install pyinstaller" -ForegroundColor Cyan
}

# Create zip
Write-Host "[*] Creating zip archive..." -ForegroundColor Cyan
$ZIP_NAME = "$OUTPUT_DIR.zip"
if (Test-Path $ZIP_NAME) {
    Remove-Item $ZIP_NAME
}

Compress-Archive -Path $OUTPUT_DIR -DestinationPath $ZIP_NAME

# Cleanup
Write-Host "[*] Cleaning up..." -ForegroundColor Cyan
Remove-Item -Recurse -Force $OUTPUT_DIR

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   Build Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Output: $ZIP_NAME" -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to exit"
