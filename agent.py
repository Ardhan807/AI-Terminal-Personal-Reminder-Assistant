import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

MODEL = "x-ai/grok-4.1-fast:free"   # model gratis & support tool calling


def ask_ai(user_message):
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Anda adalah AI asisten terminal. "
                    "Jika user meminta membuat reminder, event, waktu, atau meringkas teks, "
                    "gunakan function personal_task_assistant. "
                    "Pastikan mengurai teks menjadi parameter valid:"
                    "{operation: set_reminder/summarize_text, content: string, time: string}. "
                    "Jika user hanya berbicara biasa dan tidak meminta tindakan, jawab seperti asisten normal."
                )
            },
            {"role": "user", "content": user_message}
        ],
        "tool_choice": "auto",  # <-- fitur penting
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "personal_task_assistant",
                    "description": "Kelola reminder, event, dan ringkasan teks.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "operation": {
                                "type": "string",
                                "enum": ["set_reminder", "summarize_text", "delete_reminder"]
                            },
                            "content": {"type": "string"},
                            "time": {"type": "string"},
                        },
                        "required": ["operation"]
                    }
                }
            }
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=HEADERS,
        json=payload
    )

    return response.json()
