import webbrowser
import re
import threading
import random
import os
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

load_dotenv()
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")

def curriculum_te():
    url = "https://sarjana.jteti.ugm.ac.id/program-sarjana/program-studi-teknik-elektro/kurikulum-2021/"
    webbrowser.open(url)

def curriculum_ti():
    url = "https://sarjana.jteti.ugm.ac.id/program-sarjana/program-studi-teknologi-informasi/kurikulum-2021/"
    webbrowser.open(url)

def curriculum_tb():
    url = "https://sarjana.jteti.ugm.ac.id/program-sarjana/program-studi-teknik-biomedis/kurikulum-2021/"
    webbrowser.open(url)

def academic_documents():
    url = "https://sarjana.jteti.ugm.ac.id/akademik/dokumen-akademik/"
    webbrowser.open(url)

def beasiswa():
    url = "https://sarjana.jteti.ugm.ac.id/kemahasiswaan/peluang-mahasiswa/beasiswa/"
    webbrowser.open(url)

courses = {
    "electrical engineering": [
        "Circuit Theory",
        "Electromagnetics",
        "Power Systems",
        "Control Systems",
        "Signal Processing"
    ],
    "information engineering": [
        "Data Structures",
        "Algorithms",
        "Operating Systems",
        "Database Systems",
        "Computer Networks"
    ],
    "biomedical engineering": [
        "Anatomy and Physiology",
        "Biomaterials",
        "Biomedical Signal Processing",
        "Medical Imaging",
        "Biostatistics"
    ],
}

def get_courses(major):
    major = major.lower()
    if major in courses:
        return f"The important courses in {major.title()} are:\n" + "\n".join(courses[major])
    else:
        return "Sorry, I don't have information for that major."

patterns = [
    (r'.*(course.*electrical.*engineering|electrical.*engineering.*course).*', [get_courses("electrical engineering")]),
    (r'.*(course.*information.*engineering|information.*engineering.*course).*', [get_courses("information engineering")]),
    (r'.*(course.*biomedical.*engineering|biomedical.*engineering.*course).*', [get_courses("biomedical engineering")]),

    (r'.*(curriculum.*electrical.*engineering|electrical.*engineering.*curriculum).*', [curriculum_te]),
    (r'.*(curriculum.*information.*engineering|information.*engineering.*curriculum).*', [curriculum_ti]),
    (r'.*(curriculum.*biomedical.*engineering|biomedical.*engineering.*curriculum).*', [curriculum_tb]),

    (r'.*(academic.*document|document.*academic).*', [academic_documents]),
    (r'.*(scholarship.*available).*', ["Beasiswa Bayan Peduli 2023", "Beasiswa Chandra Asri 2024", "Beasiswa Paragon 2024"]),
    (r'.*(scholarship.*web|web.*scholarship).*', [beasiswa]),
    (r'.*(internship.*opportunity|internship.*opportunities).*', ["Internship at PT. Telkom Indonesia", "Internship at PT. Astra International", "Internship at PT. Pertamina"]),
    (r'.*(internship.*web|web.*internship).*', ["hhttps://sarjana.jteti.ugm.ac.id/kemahasiswaan/peluang-mahasiswa/kerja-praktik-internship/"]),
    (r'.*(contact.*university|university.*contact|how.*contact).*', ["You can reach the university at +62-123-4567", "You can email us at teti@ugm.ac.id"]),

    (r'^(hey|hello|hi).*', ["Hi there! How may I help you?", "Hey, how can TETI-BOT help you?"]),
    (r'.*(thanks|thank).*', ["You're welcome! Anything else?", "Happy to help! Anything else?", "My pleasure, anything else?"]),
    (r'.*', ["I'm sorry, I don't understand.", "Can you provide more information?", "I'm not sure I understand.", "Can you elaborate on that?"]),
]

def chatbot_response(user):
    for pattern, response in patterns:
        match = re.search(pattern, user, re.IGNORECASE)
        if match:
            if callable(response):
                return response(match)
            elif callable(response[0]):
                thread = threading.Thread(target=response[0])
                thread.start()
                return []
            else:
                return response
    return None
            
# Telegram message handler
def handle_message(update, context):
    user_input = update.message.text.lower()
    response = chatbot_response(user_input)
    if response:
        update.message.reply_text(response)
    else:
        update.message.reply_text("I'm opening the web page for you.")

def start(update, context):
    update.message.reply_text("Welcome to TETI-BOT! How can I assist you?")

def main():
    updater = Updater(TELEGRAM_API_KEY, use_context=True)

    dp = updater.dispatcher

    # Command handler for /start
    dp.add_handler(CommandHandler("start", start))

    # Message handler for regular messages
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()