# AI Email Triage Bot — Complete Setup Guide

## Overview
This bot watches your Gmail, classifies every email using GPT-4o-mini, 
auto-replies to low-priority emails, alerts Slack for urgent ones, 
and logs everything to Notion.

---

## Step 1 — Install n8n

```bash
npm install -g n8n
n8n start
```

Open http://localhost:5678 and create an account.

---

## Step 2 — Get your API credentials

### Gmail (Google OAuth)
1. Go to https://console.cloud.google.com
2. Create a new project
3. Enable Gmail API
4. Go to Credentials → Create OAuth Client ID
5. Application type: Web application
6. Add redirect URI: http://localhost:5678/rest/oauth2-credential/callback
7. Copy Client ID and Client Secret

### OpenAI
1. Go to https://platform.openai.com/api-keys
2. Create new key
3. Copy it

### Slack
1. Go to https://api.slack.com/apps
2. Create new app → From scratch
3. Name: "Email Triage Bot"
4. Add these OAuth scopes under Bot Token Scopes:
   - chat:write
   - channels:read
5. Install app to workspace
6. Copy Bot User OAuth Token (starts with xoxb-)
7. Add bot to your channel: /invite @email-triage-bot
8. Get channel ID: right-click channel → View channel details → Copy ID

### Notion
1. Go to https://www.notion.so/my-integrations
2. Create new integration
3. Copy the Internal Integration Token
4. Create a new page in Notion (this will hold the database)
5. Copy the page ID from the URL:
   https://notion.so/My-Page-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ this part

---

## Step 3 — Create Notion database

```bash
pip install -r requirements.txt
cp .env.example .env
# Fill in your NOTION_TOKEN and NOTION_PARENT_PAGE_ID
python scripts/setup_notion.py
```

Copy the DATABASE_ID it prints out — you'll need it in n8n.

---

## Step 4 — Test the classifier locally

```bash
# Add your OPENAI_API_KEY to .env
python scripts/test_classifier.py
```

You should see 3 test emails classified correctly.

---

## Step 5 — Import workflow into n8n

1. Open http://localhost:5678
2. Click "Add workflow"
3. Click the three dots menu (⋮) → Import from file
4. Select workflow.json
5. The workflow will appear with all nodes

---

## Step 6 — Connect credentials in n8n

Click each node and connect credentials:

### Gmail Trigger node
- Click "Credential for Gmail OAuth2 API" → Create new
- Enter your Google Client ID and Secret
- Click "Sign in with Google" and authorize

### OpenAI Classifier node  
- Click "Credential for OpenAI API" → Create new
- Paste your OpenAI API key

### Slack Alert node
- Click "Credential for Slack API" → Create new
- Paste your Slack Bot Token (xoxb-...)
- Update channelId to your channel ID

### Notion Log node
- Click "Credential for Notion API" → Create new
- Paste your Notion Integration Token
- Update databaseId to the ID from Step 3

---

## Step 7 — Update workflow values

In the Slack Alert node, find:
```
"value": "YOUR_SLACK_CHANNEL_ID"
```
Replace with your actual channel ID (e.g. C0123456789)

In the Notion Log node, find:
```
"value": "YOUR_NOTION_DATABASE_ID"
```
Replace with the database ID from Step 3.

---

## Step 8 — Test the workflow

1. Click "Test workflow" in n8n
2. Send yourself a test email:
   Subject: "URGENT: Payment issue needs immediate attention"
   Body: "Our payment failed and we need this resolved today or we'll cancel."
3. Watch the workflow execute step by step
4. Check Slack for the alert
5. Check Notion for the logged entry

---

## Step 9 — Activate

Click the toggle in the top right to activate the workflow.
It will now run every minute checking for new emails.

---

## Troubleshooting

### Gmail not triggering
- Make sure the Gmail API is enabled in Google Cloud Console
- Re-authorize the OAuth connection

### OpenAI parse error
- The Parse AI Response node handles this gracefully
- Check the raw_response field to see what GPT returned

### Notion fields not matching
- Make sure your database has these exact property names:
  From, Summary, Urgency, Category, Sentiment, Action Required, Date

---

## Cost estimate
- GPT-4o-mini: ~$0.001 per email (very cheap)
- 1000 emails/month ≈ $1
- n8n: free self-hosted
- Notion: free tier works fine
- Slack: free tier works fine