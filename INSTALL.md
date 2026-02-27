# 🚀 AGMS Enterprise v3.0 — Installation Guide

## Quick Start (Windows)

```
1. ZIP extract करा → AGMS_Enterprise फोल्डर मध्ये
2. run.bat double-click करा
3. पहिल्यांदा auto-setup होईल (2-3 मिनिट)
4. App open होईल → Super Admin account बनवा
```

## Quick Start (Linux / Mac)

```bash
cd AGMS_Enterprise
chmod +x run.sh
./run.sh
```

---

## 📋 Requirements

| Software | Version | Download |
|----------|---------|---------|
| Python | 3.10+ | python.org/downloads |
| pip | Latest | Auto-included |
| 4 GB RAM | Minimum | — |
| 2 GB Storage | Minimum | — |

---

## 🔧 Manual Install (if run.bat fails)

```bash
# 1. Virtual environment
python -m venv .venv
.venv\Scripts\activate       # Windows
source .venv/bin/activate    # Linux/Mac

# 2. Core packages
pip install PySide6 cryptography bcrypt PyJWT
pip install Pillow requests reportlab openpyxl
pip install psutil schedule

# 3. Optional (AI features)
pip install google-generativeai    # Gemini AI
pip install easyocr               # Screen capture OCR
pip install selenium webdriver-manager  # WhatsApp QR

# 4. Optional (Web Dashboard)
pip install fastapi uvicorn

# 5. Optional (GDrive Backup)
pip install google-auth google-auth-oauthlib google-api-python-client

# 6. Run
python main.py
```

---

## ⚙️ Configuration (config/api_keys.json)

```bash
# api_keys.template.json copy करा:
cp config/api_keys.template.json config/api_keys.json
```

**Required भरा:**

| Key | कुठे मिळेल |
|-----|-----------|
| `gemini_key` | aistudio.google.com/app/apikey |
| `google_client_id` | console.cloud.google.com → OAuth 2.0 |
| `owner_phone` | तुमचा WhatsApp number |

**Optional:**
- `wa_api_token` — Meta Business account
- `firebase_project_id` — Firebase Console
- `github_repo` — Auto-update साठी

---

## 🏗️ First Run Setup

1. **App start** → Onboarding wizard उघडेल
2. **Business info** भरा (नाव, पत्ता, GST)
3. **Super Admin** account बनवा
4. **Services** → 30 default CSC services auto-loaded
5. **WhatsApp** → Mode निवडा (QR free / Meta API paid)
6. Dashboard ready! ✅

---

## 📱 WhatsApp Setup

### Mode 1 — Free QR (Selenium)
```bash
pip install selenium webdriver-manager
```
→ Settings → WhatsApp → QR Scan करा → Done

### Mode 2 — Official Meta API
1. business.facebook.com → WhatsApp Business API
2. Phone number verify करा
3. Settings → WhatsApp → API Token + Phone ID paste करा

---

## 🌐 Web Dashboard

```bash
pip install fastapi uvicorn
uvicorn web_dashboard.backend.app:app --host 0.0.0.0 --port 8080
```
Browser: `http://localhost:8080/docs`

---

## ☁️ Firebase Sync (Optional)

1. console.firebase.google.com → New project
2. Project Settings → Service Accounts → Generate key
3. JSON file → `config/firebase_service_account.json` म्हणून save करा
4. Settings → Firebase Project ID भरा
5. Auto-sync every 15 minutes!

---

## 💾 Google Drive Backup (Optional)

1. console.cloud.google.com → APIs → Drive API enable
2. OAuth2 Credentials create → JSON download
3. `config/gdrive_credentials.json` म्हणून save करा
4. Backup UI → GDrive Enable → Authenticate → Done!

---

## 🔄 Auto Updater

`config/api_keys.json` मध्ये:
```json
"github_repo": "your-username/agms-enterprise"
```
Settings → Check for Updates → Auto-apply

---

## 🛠️ Troubleshooting

| Error | Solution |
|-------|---------|
| `ModuleNotFoundError: PySide6` | `pip install PySide6` |
| `cryptography` error | `pip install cryptography==41.0.0` |
| WhatsApp QR not loading | Chrome install करा + `pip install webdriver-manager` |
| DB locked | App बंद करून reopen करा |
| OCR not working | `pip install easyocr` किंवा Tesseract install |
| Firebase error | `config/firebase_service_account.json` check करा |

---

## 📂 Important Folders

```
data/                    ← Database + keystore (BACKUP करा!)
data/agms_enterprise.db  ← Main database
data/.keystore           ← Encryption keys (कधीही delete करू नका!)
config/api_keys.json     ← Your API keys
backups/                 ← Auto-backups (daily)
logs/                    ← Application logs
```

---

## 🔐 Security Notes

- `data/.keystore` delete केला तर सर्व encrypted data permanently lost!
- `config/api_keys.json` कधीही GitHub वर upload करू नका
- Daily backup automatic होतो `backups/` मध्ये
- Aadhaar/PAN AES-256-GCM encrypted आहे DB मध्ये

---

## 📞 Support

AGMS Enterprise — AG Multi Services  
Email: support@agms.in  
WhatsApp: +91 98765 43210
