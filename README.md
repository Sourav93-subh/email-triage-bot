
<div align="center">

<br/>

```
███████╗███╗   ███╗ █████╗ ██╗██╗     
██╔════╝████╗ ████║██╔══██╗██║██║     
█████╗  ██╔████╔██║███████║██║██║     
██╔══╝  ██║╚██╔╝██║██╔══██║██║██║     
███████╗██║ ╚═╝ ██║██║  ██║██║███████╗
╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝
████████╗██████╗ ██╗ █████╗  ██████╗ ███████╗
╚══██╔══╝██╔══██╗██║██╔══██╗██╔════╝ ██╔════╝
   ██║   ██████╔╝██║███████║██║  ███╗█████╗  
   ██║   ██╔══██╗██║██╔══██║██║   ██║██╔══╝  
   ██║   ██║  ██║██║██║  ██║╚██████╔╝███████╗
   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
██████╗  ██████╗ ████████╗
██╔══██╗██╔═══██╗╚══██╔══╝
██████╔╝██║   ██║   ██║   
██╔══██╗██║   ██║   ██║   
██████╔╝╚██████╔╝   ██║   
╚═════╝  ╚═════╝    ╚═╝   
```

### *Your inbox, on autopilot.*

<br/>

[![n8n](https://img.shields.io/badge/Built%20with-n8n-FF6B35?style=for-the-badge&logo=n8n&logoColor=white)](https://n8n.io)
[![Groq](https://img.shields.io/badge/AI-Groq%20%2B%20Qwen%203.6-F54F29?style=for-the-badge)](https://groq.com)
[![Gmail](https://img.shields.io/badge/Gmail-API-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](https://gmail.com)
[![Slack](https://img.shields.io/badge/Slack-Alerts-4A154B?style=for-the-badge&logo=slack&logoColor=white)](https://slack.com)
[![Notion](https://img.shields.io/badge/Notion-Log-000000?style=for-the-badge&logo=notion&logoColor=white)](https://notion.so)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

<br/>

> **An autonomous AI agent that reads every email you receive, decides what matters, replies to the noise, and escalates what's critical — all without you lifting a finger.**

<br/>

---

</div>

## ✦ The Problem

You receive 100 emails a day.
- 60 are noise — newsletters, notifications, low-priority queries
- 35 need a quick acknowledgment
- **5 are urgent — and those are the ones you miss**

This bot handles all of it automatically.

---

## ✦ How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   📧 New Email                                                  │
│        │                                                        │
│        ▼                                                        │
│   ┌─────────────┐                                               │
│   │   Extract   │  → pulls subject, sender, body               │
│   └──────┬──────┘                                               │
│          │                                                      │
│          ▼                                                      │
│   ┌─────────────────────────┐                                   │
│   │   Groq AI Classifier    │  → Llama 3.3 70B                  │
│   │   urgency · category    │  → classifies in <1 second        │
│   │   sentiment · summary   │                                   │
│   └──────────┬──────────────┘                                   │
│              │                                                  │
│       ┌──────┴──────┐                                           │
│       │             │                                           │
│    🔴 HIGH       🟢 LOW                                         │
│    URGENCY      URGENCY                                         │
│       │             │                                           │
│       ▼             ▼                                           │
│  ⚡ Slack Alert  ✉️ Auto-Reply                                   │
│  Notify team    AI drafts &                                     │
│  immediately    sends reply                                     │
│       │             │                                           │
│       └──────┬───────┘                                          │
│              ▼                                                  │
│        📋 Notion Log                                            │
│        Every email tracked                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✦ What Gets Classified

| Field | Values | Example |
|-------|--------|---------|
| **Urgency** | `high` / `low` | Payment dispute → high |
| **Category** | `support` `sales` `billing` `spam` `general` | Invoice query → billing |
| **Sentiment** | `positive` `neutral` `negative` `angry` | Threat of lawsuit → angry |
| **Action Required** | `true` / `false` | Newsletter → false |

---

## ✦ Tech Stack

```
Automation     →  n8n (self-hosted, free)
AI Model       →  Groq API · Llama 3.3 70B (free tier)
Email          →  Gmail API via OAuth2
Alerts         →  Slack Bot API
Database       →  Notion API
```

---

## ✦ Demo

**Scenario 1 — Angry billing email:**
```
📧 Subject: "URGENT: Legal action if not resolved today"

🤖 Groq classifies:
   urgency: HIGH | category: billing | sentiment: angry

⚡ Slack fires:
   🚨 Urgent Email Alert
   From: angry.client@example.com
   Summary: Client threatening legal action over overdue invoice

📋 Notion logs the entry automatically
```

**Scenario 2 — General inquiry:**
```
📧 Subject: "Question about your pricing"

🤖 Groq classifies:
   urgency: LOW | category: sales | sentiment: neutral

✉️ Auto-reply sent:
   "Hi [Name], thank you for reaching out.
    We'll get back to you within 24 hours..."

📋 Notion logs the entry automatically
```

---

## ✦ Quick Start

### Prerequisites
- [n8n](https://n8n.io) installed (`npm install -g n8n`)
- [Groq API key](https://console.groq.com) — free, no credit card
- Gmail account + Google Cloud OAuth
- Slack workspace + Bot token
- Notion account + Integration token

### Setup

```bash
# Clone the repo
git clone https://github.com/Sourav93-subh/email-triage-bot.git
cd email-triage-bot

# Start n8n
n8n start

# Open http://localhost:5678
# Import workflow.json
# Connect credentials
# Publish ✓
```

Full step-by-step guide → [SETUP.md](SETUP.md)

---

## ✦ Cost

| Service | Cost |
|---------|------|
| n8n | Free (self-hosted) |
| Groq API | Free tier |
| Gmail API | Free |
| Slack | Free tier |
| Notion | Free tier |
| **Total** | **$0/month** |

---

## ✦ Project Structure

```
email-triage-bot/
├── workflow.json          ← import this into n8n
├── prompts/
│   └── classifier.txt     ← AI prompt (tweak this)
├── scripts/
│   ├── test_classifier.py ← test AI locally
│   └── setup_notion.py    ← auto-create Notion DB
├── SETUP.md               ← full setup guide
└── .env.example           ← environment variables
```

---

## ✦ Resume Bullet

> Built autonomous AI email triage system using n8n + Groq (Llama 3.3 70B) — classifies urgency, category and sentiment of every incoming email; auto-replies to low-priority emails; alerts Slack for urgent ones; logs all to Notion — processing 100+ emails/day at $0 cost

---

## ✦ License

MIT © [Sourav Subham](https://github.com/Sourav93-subh)

<div align="center">
<br/>
<i>Built with ☕ and too many unread emails</i>
<br/><br/>

⭐ Star this repo if it saved your inbox

</div>
