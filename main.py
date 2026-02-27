"""
main.py - AGMS Enterprise v3.0 Production Entry Point
FIXES: correct boot order, single QApp, 're' renamed to 'recovery'
"""
import sys, logging, traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config.settings import LOGS_DIR, ensure_dirs
ensure_dirs()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOGS_DIR / "agms.log", encoding="utf-8"),
    ]
)
logger = logging.getLogger("AGMS.Main")


def _crash_handler(exc_type, exc_value, exc_tb):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_tb); return
    tb_str = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    logger.critical(f"UNHANDLED EXCEPTION:\n{tb_str}")
    try:
        from datetime import datetime
        f = LOGS_DIR / "crashes" / f"crash_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        f.parent.mkdir(exist_ok=True); f.write_text(tb_str, encoding="utf-8")
    except Exception: pass
    try:
        from PySide6.QtWidgets import QApplication, QMessageBox
        if QApplication.instance():
            QMessageBox.critical(None, "Crash", f"Error:\n{exc_value}\n\nSee logs/crashes/")
    except Exception: pass

sys.excepthook = _crash_handler


def main() -> int:
    from PySide6.QtWidgets import QApplication, QMessageBox
    from PySide6.QtCore    import Qt
    from PySide6.QtGui     import QFont

    # [1] Qt Application - created ONCE
    app = QApplication(sys.argv)
    app.setApplicationName("AGMS Enterprise")
    app.setApplicationVersion("3.0.0")
    app.setOrganizationName("AG Multi Services")
    app.setStyle("Fusion")
    theme_file = ROOT / "config" / "theme.qss"
    if theme_file.exists():
        app.setStyleSheet(theme_file.read_text(encoding="utf-8"))
    font = QFont("Segoe UI", 10)
    font.setHintingPreference(QFont.HintingPreference.PreferDefaultHinting)
    app.setFont(font)

    # [2] Core: Encryption -> DB -> AppState (MUST be first)
    try:
        from core.security.encryption import EncryptionManager
        from database.db_manager      import DatabaseManager
        from core.dashboard.app_state import AppState
        enc = EncryptionManager()
        db  = DatabaseManager(enc)
        db.initialise()
        st  = AppState(db)
        logger.info("Core components initialised.")
    except Exception as e:
        QMessageBox.critical(None, "Startup Error",
            f"Core init failed:\n{e}\n\nCheck logs/agms.log")
        return 1

    # [3] DB Migrations (needs db)
    try:
        from database.migrations.run_migrations import run_all
        from config.settings import DB_PATH
        r = run_all(str(DB_PATH))
        if r.get("applied", 0) > 0:
            logger.info(f"Migrations: {r['applied']} applied")
    except Exception as _e: logger.debug(f"Migrations: {_e}")

    # [4] Seed default data on first run (needs db)
    try:
        from database.seeders.default_data import seed_all
        r = seed_all(db)
        if r.get("seeded"):
            logger.info(f"Seeded: {r.get('services', 0)} CSC services")
    except Exception as _e: logger.warning(f"Seeder: {_e}")

    # [5] Health Monitor (needs db)
    try:
        from core.health_monitor.health_monitor import HealthMonitor
        _hm = HealthMonitor(db, interval=60)
        _hm.on_alert = lambda lvl, msg: logger.warning(f"HEALTH [{lvl}]: {msg}")
        _hm.start()
        logger.info("HealthMonitor started")
    except Exception as _e: logger.warning(f"HealthMonitor: {_e}")

    # [6] Feature Flags (needs db)
    try:
        from core.feature_flags.feature_flags import get_flags
        _flags = get_flags(db)
        logger.info(f"FeatureFlags: {len(_flags.get_all())} flags")
    except Exception as _e: logger.warning(f"FeatureFlags: {_e}")

    # [7] Recovery Engine (needs db) - renamed 're' -> 'recovery' to avoid stdlib collision
    try:
        from core.recovery.recovery_engine import RecoveryEngine
        recovery = RecoveryEngine(db)
        rep = recovery.startup_check()
        if rep.get("status") == "healed":
            logger.info(f"Self-heal: {rep.get('restored', 0)} files restored.")
        recovery.start_scheduler(int(db.get_setting("backup_interval_hours") or 24))
    except Exception as _e: logger.warning(f"Recovery: {_e}")

    # [8] Background Update Checker (needs db)
    try:
        from core.updater.update_engine import UpdateEngine
        UpdateEngine(db).start_background_check()
    except Exception as _e: logger.warning(f"Updater: {_e}")

    # [9] Firebase Sync - optional (needs db)
    try:
        from core.cloud.firebase_sync import FirebaseSync
        _fb = FirebaseSync(db)
        if _fb.is_configured() and _fb.connect():
            _fb.start_auto_sync(interval_minutes=15)
            logger.info("Firebase auto-sync started")
    except Exception as _e: logger.debug(f"Firebase: {_e}")

    # [10] Auth + Login
    from core.auth.auth_manager import AuthManager
    from core.auth.login_ui    import LoginDialog
    auth = AuthManager(db, enc)

    # Onboarding wizard (first run)
    try:
        from core.dashboard.onboarding import should_show_onboarding, OnboardingWizard
        if should_show_onboarding(db):
            OnboardingWizard(db, enc).exec()
    except Exception as _e: logger.warning(f"Onboarding: {_e}")

    # Login dialog
    user = None

    def _show_login() -> bool:
        nonlocal user
        dlg = LoginDialog(auth)
        dlg.login_success.connect(lambda u: (user.__setitem__(0, u) if isinstance(user, list) else None))
        # Use a mutable container for closure
        _u = []
        dlg.login_success.connect(lambda u: _u.append(u))
        result = dlg.exec() == dlg.DialogCode.Accepted
        if _u:
            nonlocal user
            user = _u[0]
        return result

    # Simpler closure approach
    _login_result = [None]

    def _do_login() -> bool:
        dlg = LoginDialog(auth)
        dlg.login_success.connect(lambda u: _login_result.__setitem__(0, u))
        return dlg.exec() == dlg.DialogCode.Accepted

    if not _do_login():
        logger.info("Login cancelled.")
        return 0

    user = _login_result[0] or auth.quick_dev_login()
    st.login(user)
    logger.info(f"Logged in: {user.get('name')} [{user.get('role')}]")

    # [11] Main Window
    from core.dashboard.main_window import MainWindow
    window = MainWindow(st, db, enc)

    # [12] Notification Engine
    notifier = None
    try:
        from core.notifications.notification_engine import NotificationEngine, NotificationSignals
        sig      = NotificationSignals()
        sig.show_popup.connect(st.notification.emit)
        notifier = NotificationEngine(db, sig)
        bdays = db.get_birthdays_today(st.branch_id)
        if bdays: notifier.birthday_alert(bdays, st.branch_id)
        dues = db.get_due_reminders(st.branch_id)
        if dues: notifier.due_reminder_alert(len(dues), st.branch_id)
    except Exception as _e: logger.warning(f"Notifications: {_e}")

    # [13] Cloud Sync
    try:
        from modules.cloud_sync.sync_manager import CloudSyncManager
        CloudSyncManager(db).start_sync_scheduler()
    except Exception as _e: logger.warning(f"Cloud sync: {_e}")

    # [14] WhatsApp Manager
    wa_mgr = None
    try:
        from modules.whatsapp_engine.wa_manager import WhatsAppManager
        wa_mgr = WhatsAppManager(db)
        st.wa_manager = wa_mgr
    except Exception as _e: logger.warning(f"WhatsApp: {_e}")

    # [15] AutoScheduler + AutomationEngine (6 background tasks)
    try:
        from core.dashboard.auto_scheduler        import AutoScheduler
        from modules.automation.automation_engine import AutomationEngine
        from modules.whatsapp_engine.wa_templates import WATemplateManager

        scheduler = AutoScheduler(db, st, wa_manager=wa_mgr, notifier=notifier)
        scheduler.start_all()
        st._scheduler = scheduler

        eng = AutomationEngine(db, wa_mgr)
        eng.install_defaults(st.branch_id, getattr(st, "user_id", ""))
        eng.load_rules(st.branch_id)
        eng.start_scheduler()

        WATemplateManager(db).install_defaults(st.branch_id, getattr(st, "user_id", ""))
        logger.info("AutoScheduler + AutomationEngine: 6 tasks running.")
    except Exception as _e: logger.warning(f"Scheduler: {_e}")

    # [16] Show window + event loop
    window.show()
    logger.info("AGMS Enterprise ready.")
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
