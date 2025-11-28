import json
from colorama import Fore, Style, init
from agent import ask_ai
from tools import personal_task_assistant    

init(autoreset=True)

print(Fore.CYAN + "AI Terminal — Personal Reminder Assistant" + Style.RESET_ALL)

while True:
    user_input = input(Fore.GREEN + "You: " + Style.RESET_ALL)

    if user_input.lower() in ["exit", "quit", "keluar"]:
        print(Fore.CYAN + "Terima kasih, sampai jumpa!" + Style.RESET_ALL)
        break

    print(Fore.YELLOW + "AI Thinking..." + Style.RESET_ALL)
    response = ask_ai(user_input)

    reply = response.get("choices", [{}])[0].get("message", {})

    # Jika AI ingin memanggil tool
    if "tool_calls" in reply:
        call = reply["tool_calls"][0]["function"]
        args = json.loads(call["arguments"])
        tool_result = personal_task_assistant(**args)

        print(Fore.CYAN + tool_result + Style.RESET_ALL)

    else:
        ai_text = reply.get("content", "! Tidak ada respon.")
        print(Fore.CYAN + ai_text + Style.RESET_ALL)