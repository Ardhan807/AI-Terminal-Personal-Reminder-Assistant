from datetime import datetime, timedelta
from plyer import notification
import re
import os

# Google Calendar Imports
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/calendar"]
REMINDER_FILE = "reminders.txt"


# ===== Helper to Avoid Emoji Save Errors =====
def clean_text(text: str):
    """Remove emojis and ensure UTF-8 safe text for saving."""
    return text.encode("ascii", "ignore").decode("ascii")


# ===== Waktu Bahasa Indonesia Parser =====
def parse_indonesian_time(text: str):
    text = text.lower().strip()
    now = datetime.now()

    if "besok" in text:
        target_date = now + timedelta(days=1)
    elif "lusa" in text:
        target_date = now + timedelta(days=2)
    else:
        target_date = now

    match = re.search(r"jam\s*(\d{1,2})", text)
    hour = int(match.group(1)) if match else None

    if "pagi" in text:
        hour = hour or 8
    elif "siang" in text:
        hour = 13 if hour is None else (hour + 12 if hour < 12 else hour)
    elif "sore" in text:
        hour = 16 if hour is None else (hour + 12 if hour < 12 else hour)
    elif "malam" in text:
        hour = 20 if hour is None else (hour + 12 if hour < 12 else hour)
    else:
        hour = hour or 9

    final_time = datetime(target_date.year, target_date.month, target_date.day, hour, 0)
    return final_time.strftime("%Y-%m-%d %H:%M")


# ===== GOOGLE CALENDAR =====
def export_to_google_calendar(title, time):
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)

        with open("token.json", "w", encoding="utf-8") as token_file:
            token_file.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)

    event = {
        "summary": title,
        "start": {"dateTime": time.replace(" ", "T") + ":00", "timeZone": "Asia/Jakarta"},
        "end": {"dateTime": time.replace(" ", "T") + ":00", "timeZone": "Asia/Jakarta"},
    }

    created_event = service.events().insert(calendarId="primary", body=event).execute()
    return created_event.get("id")


# ===== DELETE EVENT GOOGLE CALENDAR =====
def delete_from_google_calendar(event_id: str):
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    service = build("calendar", "v3", credentials=creds)

    try:
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        return True
    except:
        return False


# ===== LOCAL REMINDER MANAGEMENT =====
def delete_reminder(query: str):
    if not os.path.exists(REMINDER_FILE):
        return "! Tidak ada reminder."

    with open(REMINDER_FILE, "r", encoding="utf-8") as file:
        reminders = file.readlines()

    removed = False
    new_list = []

    for line in reminders:
        if query.lower() in line.lower():
            removed = True
            event_match = re.search(r"calendar:(.*)", line)
            if event_match:
                delete_from_google_calendar(event_match.group(1).strip())
        else:
            new_list.append(line)

    if not removed:
        return f"! Tidak ditemukan reminder berisi: '{query}'"

    with open(REMINDER_FILE, "w", encoding="utf-8") as f:
        f.writelines(new_list)

    return f"🗑 Reminder '{query}' berhasil dihapus (lokal + Google Calendar)."


# ===== MAIN TOOL FUNCTION =====
def personal_task_assistant(operation, content=None, time=None):

    if operation == "set_reminder":
        formatted_time = parse_indonesian_time(time)
        event_id = export_to_google_calendar(content, formatted_time)

        safe_entry = clean_text(f"{formatted_time} | {content} | calendar:{event_id}\n")

        with open(REMINDER_FILE, "a", encoding="utf-8") as f:
            f.write(safe_entry)

        return f"""
 Reminder dibuat!
{formatted_time}
{content}
Disinkronkan ke Google Calendar
{event_id}
"""

    elif operation == "delete_reminder":
        return delete_reminder(content)

    return "! Operasi tidak dikenali." 