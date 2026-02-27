# 🚀 AGMS Enterprise v3.0
### AI Powered CSC Business Growth Operating System

> **AGMS is NOT just form filling software.**  
> It is a complete AI-powered CSC Business Operating System for long-term stable business expansion.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 👥 **Customer Intelligence** | AES-256 encrypted Aadhaar/PAN, loyalty tracking, segmentation |
| 📲 **WhatsApp Automation** | QR free mode + Meta API official, templates, campaigns |
| 🤖 **AI Dev Engine** | Self-evolving code with version control + rollback |
| 👁️ **Screen Capture AI** | OCR auto-fill customer forms (Marathi/English) |
| 📊 **Analytics** | Revenue trends, retention, branch ranking, demand forecast |
| 🎯 **Campaign ROI** | Track conversions, calculate ROI per campaign |
| 🔄 **Automation** | Birthday/expiry/followup/loyalty triggers |
| 🌐 **Franchise System** | Multi-branch leaderboard, royalty tracking |
| ☁️ **Cloud Sync** | Firebase real-time + Google Drive backup |
| 📥 **Import Data** | CSV/Excel import with auto column mapping |
| 🔐 **Security** | bcrypt, JWT, rate limiting, device binding |

---

## 🚀 Quick Start

**Windows:** Double-click `run.bat`  
**Linux/Mac:** `./run.sh`

Full setup: See [INSTALL.md](INSTALL.md)

---

## 📁 Structure

```
AGMS_Enterprise/
├── main.py                  ← Entry point
├── run.bat / run.sh         ← Launchers
├── config/                  ← Settings, API keys, roles
├── core/                    ← Auth, security, health, updater
├── modules/                 ← All business modules
│   ├── customers/           ← Customer + AI vision
│   ├── whatsapp_engine/     ← WhatsApp automation
│   ├── automation/          ← Background triggers
│   ├── analytics/           ← Charts + AI prediction
│   ├── marketing_engine/    ← Campaigns + AI images
│   ├── ai_dev_engine/       ← Self-evolving code
│   └── ...                  ← 15+ modules
├── ai_models/               ← NLP, risk scoring, advisor
├── database/                ← Schema, migrations, seeders
└── web_dashboard/           ← FastAPI + HTML dashboard
```

---

## 🔐 Security

- AES-256-GCM encryption for Aadhaar/PAN
- bcrypt password hashing
- JWT authentication (PyJWT + HMAC fallback)
- Rate limiting (5 login attempts/5min)
- Device fingerprinting
- Immutable audit logs
- WAL-mode SQLite

---

## 📊 Tech Stack

| Layer | Technology |
|-------|-----------|
| UI | PySide6 (Qt6) |
| Database | SQLite3 + WAL mode |
| Security | AES-256-GCM + bcrypt + JWT |
| AI | Gemini Pro + Ollama (local) |
| Web API | FastAPI + Uvicorn |
| Automation | QThread + schedule |
| OCR | EasyOCR + Tesseract |
| WhatsApp | Selenium + Meta API |
| Cloud | Firebase + Google Drive |

---

## 📄 License

AG Multi Services — Internal Use License  
© 2026 AGMS Enterprise. All rights reserved.
