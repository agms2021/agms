"""
launcher.py
AGMS Enterprise v3.0 — Smart Launcher
  1. Python version check
  2. Auto-install required packages
  3. Qt splash screen with progress
  4. Launch main.py
"""
import sys, os, subprocess, json, time
from pathlib import Path

ROOT   = Path(__file__).resolve().parent
VENV   = ROOT / ".venv"
GREEN  = "\033[92m"; YELLOW = "\033[93m"; RED = "\033[91m"
RESET  = "\033[0m";  BOLD   = "\033[1m";  CYAN = "\033[96m"

# ── Package lists ─────────────────────────────────────────────────────────────
REQUIRED = {
    "PySide6":       "PySide6>=6.6.0",
    "cryptography":  "cryptography>=41.0.0",
    "bcrypt":        "bcrypt>=4.0.0",
    "jwt":           "PyJWT>=2.8.0",
    "PIL":           "Pillow>=10.0.0",
    "requests":      "requests>=2.31.0",
    "reportlab":     "reportlab>=4.0.0",
    "openpyxl":      "openpyxl>=3.1.0",
    "psutil":        "psutil>=5.9.0",
    "qrcode":        "qrcode[pil]>=7.4.0",
}
OPTIONAL = {
    "easyocr":            "easyocr",
    "selenium":           "selenium",
    "webdriver_manager":  "webdriver-manager",
    "firebase_admin":     "firebase-admin",
    "fastapi":            "fastapi",
    "uvicorn":            "uvicorn",
}


def banner():
    print(f"""
{BOLD}{'═'*62}{RESET}
{BOLD}{CYAN}   🏢  AGMS ENTERPRISE  v3.0{RESET}
{BOLD}   AI Business Growth OS — AG Multi Services{RESET}
{BOLD}{'═'*62}{RESET}
""")


def check_python():
    v = sys.version_info
    if v < (3, 10):
        print(f"{RED}❌ Python 3.10+ required. Current: {v.major}.{v.minor}{RESET}")
        sys.exit(1)
    print(f"{GREEN}✅ Python {v.major}.{v.minor}.{v.micro}{RESET}")


def is_installed(pkg_import: str) -> bool:
    try:
        __import__(pkg_import.split(".")[0])
        return True
    except ImportError:
        return False


def install_pkg(pkg_import: str, pkg_install: str) -> bool:
    print(f"   {YELLOW}⬇  Installing {pkg_install}…{RESET}", end="", flush=True)
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", pkg_install, "-q",
         "--break-system-packages"],
        capture_output=True, text=True)
    if result.returncode == 0:
        print(f" {GREEN}✓{RESET}")
        return True
    # Try without --break-system-packages
    result2 = subprocess.run(
        [sys.executable, "-m", "pip", "install", pkg_install, "-q"],
        capture_output=True, text=True)
    if result2.returncode == 0:
        print(f" {GREEN}✓{RESET}")
        return True
    print(f" {RED}✗ failed{RESET}")
    return False


def check_and_install():
    print(f"\n{BOLD}Checking dependencies…{RESET}")
    missing = []
    for imp, pkg in REQUIRED.items():
        if not is_installed(imp):
            missing.append((imp, pkg))

    if missing:
        print(f"  Installing {len(missing)} required packages:")
        failed = []
        for imp, pkg in missing:
            ok = install_pkg(imp, pkg)
            if not ok:
                failed.append(pkg)
        if failed:
            print(f"\n{RED}❌ Failed to install: {failed}{RESET}")
            print(f"Run manually: pip install {' '.join(failed)}")
            input("Press Enter to try anyway, or Ctrl+C to exit…")
    else:
        print(f"  {GREEN}✅ All required packages present{RESET}")

    # Optional packages (silent check)
    optional_missing = [pkg for imp, pkg in OPTIONAL.items() if not is_installed(imp)]
    if optional_missing:
        print(f"  {YELLOW}ℹ  Optional packages not installed: {', '.join(optional_missing)}{RESET}")
        print(f"  {YELLOW}   OCR / WhatsApp QR / Firebase require these. Install via Settings.{RESET}")


def setup_config():
    """Copy api_keys.template.json → api_keys.json on first run."""
    template = ROOT / "config" / "api_keys.template.json"
    keys_file = ROOT / "config" / "api_keys.json"
    if template.exists() and not keys_file.exists():
        import shutil
        shutil.copy2(template, keys_file)
        print(f"  {YELLOW}⚙  config/api_keys.json created from template{RESET}")
        print(f"  {YELLOW}   Edit it to add your API keys (Gemini, WhatsApp, etc.){RESET}")


def launch_with_splash():
    """Launch main app with Qt splash screen."""
    try:
        from PySide6.QtWidgets import QApplication, QSplashScreen, QLabel
        from PySide6.QtCore    import Qt, QTimer
        from PySide6.QtGui     import QPixmap, QColor, QPainter, QFont, QBrush

        app = QApplication.instance() or QApplication(sys.argv)

        # Build splash pixmap
        pm = QPixmap(520, 300)
        pm.fill(QColor("#0d1117"))
        p  = QPainter(pm)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Dark card background
        p.setBrush(QBrush(QColor("#161b22")))
        p.setPen(QColor("#21262d"))
        p.drawRoundedRect(20, 20, 480, 260, 12, 12)

        # Title
        title_font = QFont("Segoe UI", 22, QFont.Weight.Bold)
        p.setFont(title_font)
        p.setPen(QColor("#58a6ff"))
        p.drawText(pm.rect().adjusted(0, 60, 0, 0), Qt.AlignmentFlag.AlignHCenter, "AGMS Enterprise")

        # Subtitle
        sub_font = QFont("Segoe UI", 10)
        p.setFont(sub_font)
        p.setPen(QColor("#8b949e"))
        p.drawText(pm.rect().adjusted(0, 110, 0, 0), Qt.AlignmentFlag.AlignHCenter,
                   "AI Business Growth OS  •  AG Multi Services")

        # Version badge
        p.setPen(QColor("#3fb950"))
        ver_font = QFont("Segoe UI", 9)
        p.setFont(ver_font)
        p.drawText(pm.rect().adjusted(0, 140, 0, 0), Qt.AlignmentFlag.AlignHCenter, "v3.0.0  |  Production")

        p.end()

        splash = QSplashScreen(pm)
        splash.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        splash.show()

        def _update(msg: str, pct: int):
            bar_w   = int(400 * pct / 100)
            pm2     = QPixmap(pm)
            p2      = QPainter(pm2)
            # Progress bar
            p2.setBrush(QBrush(QColor("#21262d")))
            p2.setPen(QColor("#30363d"))
            p2.drawRoundedRect(60, 230, 400, 16, 8, 8)
            p2.setBrush(QBrush(QColor("#1f6feb")))
            p2.setPen(QColor("#58a6ff"))
            p2.drawRoundedRect(60, 230, max(bar_w, 4), 16, 8, 8)
            # Status text
            sf = QFont("Segoe UI", 9)
            p2.setFont(sf)
            p2.setPen(QColor("#8b949e"))
            p2.drawText(60, 216, msg)
            p2.end()
            splash.setPixmap(pm2)
            app.processEvents()

        _update("Initialising…", 10)
        time.sleep(0.2)
        _update("Loading database…", 35)
        time.sleep(0.2)
        _update("Starting services…", 65)
        time.sleep(0.2)
        _update("Ready!", 100)
        time.sleep(0.3)

        # Import and run main
        if str(ROOT) not in sys.path:
            sys.path.insert(0, str(ROOT))

        import main as _main_mod
        splash.finish(None)
        return _main_mod.main()

    except Exception as e:
        print(f"{RED}Splash failed: {e}{RESET} — launching directly")
        return launch_direct()


def launch_direct():
    """Fallback: launch without splash."""
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    import main as _m
    return _m.main()


def mark_setup():
    marker = ROOT / "data" / ".setup_done"
    marker.parent.mkdir(exist_ok=True)
    marker.write_text("ok")


def main():
    banner()
    check_python()
    check_and_install()
    setup_config()

    marker = ROOT / "data" / ".setup_done"
    if not marker.exists():
        mark_setup()

    print(f"\n{GREEN}{BOLD}Launching AGMS Enterprise…{RESET}\n")
    sys.exit(launch_with_splash())


if __name__ == "__main__":
    main()
