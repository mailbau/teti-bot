import webbrowser
import re
import threading

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

# Sample course data
courses = {
    "electrical engineering": {
        1: ["Introduction to Electrical Engineering", "Calculus I", "Physics I", "Programming Basics"],
        2: ["Circuit Theory", "Calculus II", "Physics II", "Digital Systems"],
        # Add more semesters as needed...
    },
    "information engineering": {
        1: ["Introduction to Information Engineering", "Discrete Mathematics", "Introduction to Programming", "Linear Algebra"],
        2: ["Data Structures", "Computer Organization", "Probability and Statistics", "Calculus II"],
        # Add more semesters as needed...
    },
    "biomedical engineering": {
        1: ["Introduction to Biomedical Engineering", "Biology I", "Chemistry I", "Calculus I"],
        2: ["Anatomy and Physiology", "Biomaterials", "Physics for Engineers", "Biostatistics"],
        # Add more semesters as needed...
    },
}


def get_courses(major, semester):
    major = major.lower()
    semester = int(semester)
    if major in courses and semester in courses[major]:
        return courses[major][semester]
    else:
        return ["Sorry, I don't have information for that semester or major."]

patterns = [
    (r'(?=.*\bcourse\b)(?=.*\bsemester\s*(\d+))(?=.*\b(electrical engineering|information engineering|biomedical engineering)\b).*', 
     lambda match: get_courses(match.group(2), match.group(1))),
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
            if isinstance(response, list):
                print("TETI-BOT:", "\n".join(response))
            else:
                print("TETI-BOT:", response)
        else:
            print("TETI-BOT: I'm not sure how to respond to that. Can you be more specific?")

loop_chat()