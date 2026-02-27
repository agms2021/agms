"""
setup.py — AGMS Enterprise Installer
python setup.py install   (or just run launcher.py)
"""
from pathlib import Path
import subprocess, sys, os

ROOT = Path(__file__).resolve().parent

REQUIRED = [
    "PySide6>=6.6.0",
    "cryptography>=42.0.0",
    "Pillow>=10.0.0",
    "requests>=2.31.0",
]

OPTIONAL = {
    "easyocr":            "AI Screen Detection (OCR)",
    "selenium":           "WhatsApp Free Mode",
    "webdriver-manager":  "WhatsApp Free Mode",
    "firebase-admin":     "Cloud Sync",
    "google-auth":        "Google OAuth Login",
    "google-auth-oauthlib":"Google OAuth Login",
    "fastapi":            "Web Dashboard",
    "uvicorn":            "Web Dashboard",
}

def banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║         AGMS Enterprise v3.0 — Setup & Installer            ║
║    AG Multi Services — AI Business Growth OS                 ║
╚══════════════════════════════════════════════════════════════╝
""")

def pip_install(package: str) -> bool:
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package,
             "--break-system-packages", "--quiet"],
            stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False

def check_python():
    v = sys.version_info
    if v < (3, 10):
        print(f"  ❌ Python 3.10+ आवश्यक. तुमचे version: {v.major}.{v.minor}")
        sys.exit(1)
    print(f"  ✅ Python {v.major}.{v.minor}.{v.micro}")

def install_required():
    print("\n📦 Required packages install करत आहे...\n")
    ok = 0
    for pkg in REQUIRED:
        name = pkg.split(">=")[0]
        print(f"  ⏳ {name}...", end=" ", flush=True)
        if pip_install(pkg):
            print("✅"); ok += 1
        else:
            print("❌ FAILED — please install manually")
    return ok == len(REQUIRED)

def install_optional():
    print("\n⚙️  Optional packages (recommended):\n")
    for pkg, desc in OPTIONAL.items():
        ans = input(f"  Install {pkg} ({desc})? [y/N] ").strip().lower()
        if ans == "y":
            print(f"  ⏳ Installing {pkg}...", end=" ", flush=True)
            if pip_install(pkg):
                print("✅")
            else:
                print("⚠️  Failed — skip करत आहे")

def create_dirs():
    print("\n📁 Directories create करत आहे...")
    dirs = ["data","data/marketing","logs","logs/crashes","logs/audit",
            "backups","config"]
    for d in dirs:
        (ROOT / d).mkdir(parents=True, exist_ok=True)
    print("  ✅ Directories ready")

def copy_config():
    template = ROOT / "config" / "api_keys.template.json"
    target   = ROOT / "config" / "api_keys.json"
    if not target.exists() and template.exists():
        import shutil
        shutil.copy(template, target)
        print("  ✅ config/api_keys.json created (कृपया keys भरा)")
    else:
        print("  ℹ️  api_keys.json already exists")

def init_db():
    print("  ⏳ Database initialize करत आहे...", end=" ", flush=True)
    try:
        sys.path.insert(0, str(ROOT))
        import config.settings as s
        s.DB_PATH    = ROOT / "data" / "agms_enterprise.db"
        s.KEY_PATH   = ROOT / "data" / ".keystore"
        s.LOGS_DIR   = ROOT / "logs"
        s.CRASH_DIR  = ROOT / "logs" / "crashes"
        s.BACKUP_DIR = ROOT / "backups"
        s.DATA_DIR   = ROOT / "data"

        from core.security.encryption import EncryptionManager
        from database.db_manager import DatabaseManager
        enc = EncryptionManager(s.KEY_PATH)
        db  = DatabaseManager(enc)
        db.initialise()

        # Create default dev admin
        from core.auth.auth_manager import AuthManager
        auth = AuthManager(db, enc)
        ok, _ = auth.create_local_user(
            "admin@agms.local", "admin123",
            "Dev Admin", "super_admin", "main")
        if ok:
            print("✅")
            print("  📋 Default login: admin@agms.local / admin123")
        else:
            print("✅ (existing)")
        db.close()
    except Exception as e:
        print(f"❌ {e}")

def mark_setup():
    (ROOT / ".setup_done").write_text("1.0")
    print("\n  ✅ Setup complete!")

def main():
    banner()
    print("🔍 System check...\n")
    check_python()
    ok = install_required()
    if not ok:
        print("\n❌ Required packages install झाले नाहीत. Manual install करा:")
        print("   pip install " + " ".join(REQUIRED))
        sys.exit(1)
    install_optional()
    create_dirs()
    copy_config()
    print("\n🗄️  Database setup...\n")
    init_db()
    mark_setup()
    print("""
╔══════════════════════════════════════════════════════════════╗
║  🎉 AGMS Enterprise Setup Complete!                         ║
║                                                              ║
║  Launch करा:                                                 ║
║    Windows: run.bat                                          ║
║    Linux:   ./run.sh                                         ║
║    Manual:  python3 launcher.py                              ║
║                                                              ║
║  API Keys: config/api_keys.json मध्ये fill करा               ║
╚══════════════════════════════════════════════════════════════╝
""")

if __name__ == "__main__":
    main()
