#!/bin/bash
# AGMS Enterprise Launcher

echo ""
echo "================================================================"
echo " AGMS Enterprise — AG Multi Services Business OS"
echo " Starting..."
echo "================================================================"
echo ""

# Find Python
PYTHON=""
for cmd in python3.11 python3.10 python3 python; do
    if command -v "$cmd" &>/dev/null; then
        ver=$($cmd --version 2>&1 | awk '{print $2}')
        major=$(echo $ver | cut -d. -f1)
        minor=$(echo $ver | cut -d. -f2)
        if [ "$major" -ge 3 ] && [ "$minor" -ge 10 ]; then
            PYTHON="$cmd"
            echo " Python: $ver ($cmd)"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo " [ERROR] Python 3.10+ not found!"
    echo " Install: sudo apt install python3.11 python3.11-venv"
    exit 1
fi

# Create venv
if [ ! -d ".venv" ]; then
    echo " [SETUP] Creating virtual environment..."
    $PYTHON -m venv .venv
fi

# Activate
source .venv/bin/activate

# Install packages
echo " [SETUP] Checking dependencies..."
pip install --quiet --upgrade pip
pip install --quiet PySide6 cryptography Pillow requests 2>/dev/null
pip install --quiet reportlab openpyxl 2>/dev/null
pip install --quiet bcrypt PyJWT psutil schedule qrcode 2>/dev/null

# Verify
python -c "import PySide6; import cryptography" 2>/dev/null
if [ $? -ne 0 ]; then
    echo " [ERROR] Core packages install failed!"
    echo " Run: pip install PySide6 cryptography Pillow requests"
    exit 1
fi

# Launch
echo " [START] Launching AGMS Enterprise..."
echo ""
python launcher.py
