"""
Creates the Notion database with the right schema for the email triage bot.
Usage: python scripts/setup_notion.py
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_PARENT_PAGE_ID = os.getenv("NOTION_PARENT_PAGE_ID")

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}


def create_database():
    url = "https://api.notion.com/v1/databases"

    payload = {
        "parent": {
            "type": "page_id",
            "page_id": NOTION_PARENT_PAGE_ID
        },
        "title": [{"type": "text", "text": {"content": "Email Triage Log"}}],
        "properties": {
            "Subject": {"title": {}},
            "From": {"rich_text": {}},
            "Summary": {"rich_text": {}},
            "Urgency": {
                "select": {
                    "options": [
                        {"name": "high", "color": "red"},
                        {"name": "low", "color": "green"}
                    ]
                }
            },
            "Category": {
                "select": {
                    "options": [
                        {"name": "support", "color": "blue"},
                        {"name": "sales", "color": "purple"},
                        {"name": "billing", "color": "orange"},
                        {"name": "spam", "color": "gray"},
                        {"name": "general", "color": "default"}
                    ]
                }
            },
            "Sentiment": {
                "select": {
                    "options": [
                        {"name": "positive", "color": "green"},
                        {"name": "neutral", "color": "gray"},
                        {"name": "negative", "color": "orange"},
                        {"name": "angry", "color": "red"}
                    ]
                }
            },
            "Action Required": {"checkbox": {}},
            "Date": {"date": {}},
            "Replied": {"checkbox": {}}
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        db = response.json()
        print(f"Database created!")
        print(f"Database ID: {db['id']}")
        print(f"\nAdd this to your n8n workflow:")
        print(f"NOTION_DATABASE_ID={db['id']}")
    else:
        print(f"Error: {response.status_code}")
        print(response.json())


if __name__ == "__main__":
    create_database()