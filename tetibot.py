import webbrowser
import re
import threading
import random

def curriculum_te():
    url = "https://sarjana.jteti.ugm.ac.id/program-sarjana/program-studi-teknik-elektro/kurikulum-2021/"
    webbrowser.open(url)
    return None

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

# Sample course data
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
            
def start_chat():
    print("Welcome to TETI-BOT")
    print("Type 'exit' to stop the conversation.")

def loop_chat():
    start_chat()
    while True:
        user = input("You: ").lower()
        if user in ['exit', 'no', 'no thanks']:
            print("TETI-BOT: Goodbye! Feel free to ask anytime.")
            break
        response = chatbot_response(user)
        if response:
            print("TETI-BOT:", random.choice(response))
        else:
            print("TETI-BOT: I'm opening the web page for you.")

loop_chat()