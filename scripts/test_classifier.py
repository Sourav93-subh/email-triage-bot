"""
Test the OpenAI classifier locally before plugging into n8n.
Usage: python scripts/test_classifier.py
"""
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are an expert email triage assistant. Analyze emails and respond ONLY with valid JSON, no markdown, no explanation.

Output format:
{
  "urgency": "high" or "low",
  "category": "support" or "sales" or "billing" or "spam" or "general",
  "sentiment": "positive" or "neutral" or "negative" or "angry",
  "summary": "one sentence max 15 words",
  "suggested_reply": "professional reply under 80 words",
  "action_required": true or false
}

Rules:
- high urgency: payment issues, angry tone, deadline mentioned, complaint, legal threat
- low urgency: general inquiry, newsletter, FYI emails, follow-ups
- spam: mark action_required false and urgency low
- suggested_reply: start with Hi [Name], be professional and concise"""

TEST_EMAILS = [
    {
        "name": "Urgent billing complaint",
        "from": "angry.client@example.com",
        "from_name": "John Smith",
        "subject": "URGENT: Invoice overdue - threatening legal action",
        "body": "I've been waiting 3 weeks for a response to my invoice dispute. If I don't hear back by tomorrow, I'm contacting my lawyer. This is completely unacceptable.",
        "date": "2025-01-15"
    },
    {
        "name": "General inquiry",
        "from": "potential@startup.com",
        "from_name": "Sarah Lee",
        "subject": "Question about your pricing plans",
        "body": "Hi, I came across your product and I'm interested in learning more about your enterprise pricing. Could you send me more details when you get a chance? No rush.",
        "date": "2025-01-15"
    },
    {
        "name": "Spam newsletter",
        "from": "newsletter@deals.com",
        "from_name": "Deals Weekly",
        "subject": "🎉 50% OFF Everything This Weekend Only!!!",
        "body": "Don't miss out on our biggest sale of the year! Click here to shop now. Unsubscribe at any time.",
        "date": "2025-01-15"
    }
]


def classify_email(email: dict) -> dict:
    user_prompt = f"""Triage this email:

From: {email['from_name']} <{email['from']}>
Subject: {email['subject']}
Date: {email['date']}

Body:
{email['body']}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        max_tokens=500
    )

    raw = response.choices[0].message.content.strip()
    return json.loads(raw)


if __name__ == "__main__":
    print("Testing AI Email Classifier\n" + "="*40)

    for email in TEST_EMAILS:
        print(f"\nTest: {email['name']}")
        print(f"Subject: {email['subject']}")
        print("-" * 30)

        result = classify_email(email)
        print(f"Urgency:  {result['urgency'].upper()}")
        print(f"Category: {result['category']}")
        print(f"Sentiment: {result['sentiment']}")
        print(f"Summary:  {result['summary']}")
        print(f"Action:   {result['action_required']}")
        print(f"Reply:    {result['suggested_reply'][:80]}...")