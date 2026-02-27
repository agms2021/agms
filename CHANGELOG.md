# AGMS Enterprise — Changelog

## v3.0 (2026-02-26) — Production Release

### 🆕 New Features
- **AI Dev Engine** — 4-tab panel (Pipeline / Version History+Rollback / Sandbox / Quick Patches)
- **AI Screen Capture** — 3-tab panel (Manual / Auto Monitor 4s interval / History)
- **Import Data** — CSV/Excel import with column mapping, preview, templates
- **Health Monitor** — CPU/RAM/DB latency tracking, 60s interval, alerts
- **Feature Flags** — Per-feature ON/OFF with rollout percentage
- **Database Seeders** — 30 default CSC services auto-seeded on first run
- **Database Migrations** — 5 versioned migration files (001-005)
- **Campaign ROI** — Conversion tracking, ROI calculation per campaign
- **Customer Retention** — Monthly breakdown, inactive customer list
- **Branch Ranking** — Revenue leaderboard with progress bars
- **Customer Segments** — VIP / Regular / At-Risk / Inactive auto-classification
- **Demand Prediction** — Weighted moving average, next month forecast per service
- **Service Expiry Alert** — WhatsApp reminder N days before expiry
- **Loyalty Reward Engine** — Milestones at 100/250/500/1000 points
- **Firebase Real Sync** — firebase_admin SDK, auto-sync every 15 minutes
- **GDrive Backup** — OAuth2, resumable upload, list/download backups
- **Auto Updater** — GitHub release check, SHA256 verify, pre-update backup, rollback
- **JWT Tokens** — PyJWT + HMAC fallback
- **bcrypt Passwords** — SHA256 fallback for older installations
- **Rate Limiting** — 5 login attempts/5min, hard block on abuse
- **WAL Mode** — SQLite WAL for faster concurrent reads

### 🔧 Security Improvements
- AES-256-GCM encryption for Aadhaar/PAN
- Device fingerprinting
- Immutable audit logging
- File integrity monitoring

### 📊 Analytics
- Revenue trend line charts (pure Qt, no external deps)
- Service popularity bar charts
- Payment mode analysis
- AI demand prediction widget

### 🌐 Web Dashboard
- FastAPI REST API (24 endpoints)
- JWT authentication
- Customer CRUD, transactions, expenses
- Franchise leaderboard API
- OpenAPI docs at /docs

## v2.0 (2026-01) — Phase 2

- WhatsApp QR automation
- Meta API integration
- Marketing campaigns
- Loyalty system

## v1.0 (2025-12) — Initial Release

- Customer management
- Service catalog
- Transaction tracking
- Basic reports
