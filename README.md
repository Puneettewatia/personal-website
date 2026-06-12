# personal-website
"The Last Alibi" in this you play as detective and solve mystery cases
import os
import json
import random
from datetime import datetime
import google.generativeai as genai

# =====================================================
# CONFIGURATION
# =====================================================

SAVE_FILE = "detective_save.json"


def setup_gemini():
    """
    Setup Gemini API
    Replace with your API key
    """
    API_KEY = "AQ.Ab8RN6K4-jwWaDAGCghRRGWUkta1T8oNRCKDDOPCxEk_PXYJYg"

    genai.configure(api_key=API_KEY)

    return genai.GenerativeModel("gemini-2.5-flash")


# =====================================================
# DETECTIVE PROFILE
# =====================================================

class Detective:

    def __init__(self):

        self.score = 0
        self.rank = "Rookie Detective"

        self.inventory = []

        self.clues = []

        self.suspicions = {}

        self.case_history = []

    def update_rank(self):

        if self.score >= 1000:
            self.rank = "Master Detective"

        elif self.score >= 600:
            self.rank = "Senior Detective"

        elif self.score >= 300:
            self.rank = "Detective"

        elif self.score >= 100:
            self.rank = "Investigator"

        else:
            self.rank = "Rookie Detective"

    def add_score(self, points):

        self.score += points

        self.update_rank()

    def display(self):

        print("\n" + "=" * 50)
        print("DETECTIVE PROFILE")
        print("=" * 50)

        print(f"Rank: {self.rank}")
        print(f"Score: {self.score}")

        print("=" * 50)


# =====================================================
# SAVE / LOAD SYSTEM
# =====================================================

def save_game(game_data):

    try:

        with open(SAVE_FILE, "w") as file:
            json.dump(game_data, file, indent=4)

        print("\nGame saved successfully!")

    except Exception as e:

        print("Save failed:", e)


def load_game():

    if not os.path.exists(SAVE_FILE):
        return None

    try:

        with open(SAVE_FILE, "r") as file:

            data = json.load(file)

        print("\nSave loaded!")

        return data

    except:

        return None


# =====================================================
# EVIDENCE BOARD
# =====================================================

class EvidenceBoard:

    def __init__(self):

        self.physical_evidence = []
        self.witness_statements = []
        self.suspect_clues = []

    def add_physical(self, clue):

        if clue not in self.physical_evidence:
            self.physical_evidence.append(clue)

    def add_statement(self, statement):

        if statement not in self.witness_statements:
            self.witness_statements.append(statement)

    def add_suspect_clue(self, clue):

        if clue not in self.suspect_clues:
            self.suspect_clues.append(clue)

    def display(self):

        print("\n")
        print("=" * 60)
        print("EVIDENCE BOARD")
        print("=" * 60)

        print("\nPHYSICAL EVIDENCE")

        for clue in self.physical_evidence:
            print("✓", clue)

        print("\nWITNESS STATEMENTS")

        for statement in self.witness_statements:
            print("✓", statement)

        print("\nSUSPECT CLUES")

        for clue in self.suspect_clues:
            print("✓", clue)

        print("=" * 60)


# =====================================================
# SUSPICION SYSTEM
# =====================================================

def initialize_suspicion(suspects):

    suspicion = {}

    for suspect in suspects:

        suspicion[suspect["name"]] = 0

    return suspicion


def increase_suspicion(suspicion, suspect_name, amount):

    suspicion[suspect_name] += amount

    if suspicion[suspect_name] > 100:
        suspicion[suspect_name] = 100


def display_suspicion(suspicion):

    print("\n")
    print("=" * 50)
    print("SUSPICION METER")
    print("=" * 50)

    for name, value in suspicion.items():

        bars = "█" * (value // 10)
        empty = "░" * (10 - (value // 10))

        print(f"{name:<20} [{bars}{empty}] {value}%")

    print("=" * 50)


# =====================================================
# AI CASE GENERATION
# =====================================================

def generate_case(model):

    print("\nGenerating mystery case...\n")

    prompt = """
Create a detective mystery.

Return ONLY JSON.

{
  "case_type":"",
  "victim":{
      "name":"",
      "location":"",
      "cause":""
  },
  "culprit":"",

  "crime_scene_clues":[
      ""
  ],

  "witnesses":[
      {
         "name":"",
         "statement":""
      }
  ],

  "suspects":[
      {
         "name":"",
         "profession":"",
         "motive":"",
         "alibi":"",
         "clues":[]
      }
  ],

  "plot_twist":""
}

Requirements:

4 suspects
3 witnesses
1 culprit
logical clues
interesting mystery
"""

    try:

        response = model.generate_content(prompt)

        text = response.text

        start = text.find("{")
        end = text.rfind("}") + 1

        json_text = text[start:end]

        return json.loads(json_text)

    except Exception as e:

        print("Generation failed:", e)

        return None


# =====================================================
# WITNESS INTERVIEW SYSTEM
# =====================================================

def interview_witness(case_data, evidence_board):

    witnesses = case_data["witnesses"]

    print("\nWitnesses")

    for i, witness in enumerate(witnesses, start=1):

        print(f"{i}. {witness['name']}")

    try:

        choice = int(input("\nChoose witness: "))

        witness = witnesses[choice - 1]

        print("\n")
        print(f"{witness['name']} says:")
        print(witness["statement"])

        evidence_board.add_statement(
            witness["statement"]
        )

    except:

        print("Invalid selection")


# =====================================================
# CRIME SCENE
# =====================================================

def investigate_crime_scene(case_data,
                            evidence_board,
                            detective):

    clues = case_data["crime_scene_clues"]

    print("\nInvestigating crime scene...\n")

    for clue in clues:

        print("Found:", clue)

        evidence_board.add_physical(clue)

        detective.clues.append(clue)

        detective.add_score(10)

    print("\nCrime scene processed.")


# =====================================================
# DISPLAY FUNCTIONS
# =====================================================

def display_case_intro(case_data):

    victim = case_data["victim"]

    print("\n")
    print("=" * 60)
    print("CASE FILE")
    print("=" * 60)

    print(f"Case Type : {case_data['case_type']}")
    print(f"Victim    : {victim['name']}")
    print(f"Location  : {victim['location']}")
    print(f"Cause     : {victim['cause']}")

    print("=" * 60)


def display_suspects(case_data):

    print("\nSuspects")

    for i, suspect in enumerate(
            case_data["suspects"],
            start=1):

        print(
            f"{i}. {suspect['name']} "
            f"({suspect['profession']})"
        )


# =====================================================
# GAME HEADER
# =====================================================

def title():

    print("\n")
    print("=" * 70)
    print(" AI DETECTIVE: MURDER INVESTIGATION ")
    print("=" * 70)

 # =====================================================
# INVENTORY SYSTEM
# =====================================================

def show_inventory(detective):

    print("\n" + "=" * 50)
    print("INVENTORY")
    print("=" * 50)

    if not detective.inventory:
        print("Inventory is empty.")

    else:

        for item in detective.inventory:
            print("•", item)

    print("=" * 50)


def add_inventory_item(detective, item):

    if item not in detective.inventory:

        detective.inventory.append(item)

        print(f"\nAdded to inventory: {item}")


# =====================================================
# DYNAMIC GEMINI INTERROGATION
# =====================================================

def interrogate_suspect_ai(model,
                           suspect,
                           evidence_board,
                           detective):

    print("\n" + "=" * 60)
    print(f"INTERROGATING {suspect['name'].upper()}")
    print("=" * 60)

    print(f"Profession: {suspect['profession']}")
    print(f"Official Alibi: {suspect['alibi']}")

    while True:

        question = input(
            "\nAsk a question (or type EXIT): "
        ).strip()

        if question.lower() == "exit":
            break

        prompt = f"""
You are a suspect in a detective game.

Name:
{suspect['name']}

Profession:
{suspect['profession']}

Motive:
{suspect['motive']}

Alibi:
{suspect['alibi']}

Known Clues:
{suspect['clues']}

Stay in character.

Do not reveal if you are guilty.

Answer naturally.

Detective Question:
{question}
"""

        try:

            response = model.generate_content(prompt)

            print("\nSuspect:")
            print(response.text)

        except Exception as e:

            print("Gemini Error:", e)

    print("\nInterrogation complete.")

    detective.add_score(15)


# =====================================================
# SEARCH SUSPECT PROPERTY
# =====================================================

def search_suspect(case_data,
                   evidence_board,
                   detective,
                   suspicion):

    display_suspects(case_data)

    try:

        choice = int(
            input("\nSearch which suspect? ")
        )

        suspect = case_data["suspects"][choice - 1]

        possible_evidence = [

            f"Bank records linked to {suspect['name']}",

            f"Deleted messages found on {suspect['name']}'s phone",

            f"Security keycard owned by {suspect['name']}",

            f"Suspicious receipt belonging to {suspect['name']}",

            f"Photograph connecting {suspect['name']} to victim"

        ]

        evidence = random.choice(possible_evidence)

        print("\nFOUND EVIDENCE:")
        print(evidence)

        evidence_board.add_suspect_clue(evidence)

        detective.clues.append(evidence)

        detective.add_score(25)

        increase_suspicion(
            suspicion,
            suspect["name"],
            15
        )

    except:

        print("Invalid selection.")


# =====================================================
# FORENSICS LAB
# =====================================================

def forensic_lab(case_data,
                 detective,
                 evidence_board,
                 suspicion):

    print("\n")
    print("=" * 60)
    print("FORENSICS LAB")
    print("=" * 60)

    print("1. Fingerprint Analysis")
    print("2. DNA Analysis")
    print("3. Footprint Analysis")
    print("4. Coffee Cup Analysis")

    choice = input("\nChoose: ")

    culprit = case_data["culprit"]

    if choice == "1":

        result = (
            f"Fingerprint partially matches "
            f"{culprit}"
        )

        evidence_board.add_physical(result)

        detective.add_score(30)

        increase_suspicion(
            suspicion,
            culprit,
            20
        )

        print("\nResult:", result)

    elif choice == "2":

        result = (
            f"DNA trace found connected to "
            f"{culprit}"
        )

        evidence_board.add_physical(result)

        detective.add_score(35)

        increase_suspicion(
            suspicion,
            culprit,
            25
        )

        print("\nResult:", result)

    elif choice == "3":

        result = (
            f"Footprint size consistent with "
            f"{culprit}"
        )

        evidence_board.add_physical(result)

        detective.add_score(20)

        increase_suspicion(
            suspicion,
            culprit,
            10
        )

        print("\nResult:", result)

    elif choice == "4":

        result = (
            f"Coffee cup contains fingerprints "
            f"of {culprit}"
        )

        evidence_board.add_physical(result)

        detective.add_score(25)

        increase_suspicion(
            suspicion,
            culprit,
            15
        )

        print("\nResult:", result)

    else:

        print("Invalid option")


# =====================================================
# SECURITY CAMERA SYSTEM
# =====================================================

def analyze_security_logs(case_data,
                          detective,
                          evidence_board):

    culprit = case_data["culprit"]

    logs = [

        "Camera outage occurred at 9:15 PM",

        f"Shadowy figure resembles {culprit}",

        "Security access door opened twice",

        "Motion detected near vault"

    ]

    print("\nSECURITY LOG ANALYSIS")

    for log in logs:

        print("•", log)

        evidence_board.add_physical(log)

    detective.add_score(25)


# =====================================================
# TIMELINE RECONSTRUCTION
# =====================================================

def build_timeline(case_data):

    victim = case_data["victim"]

    print("\n")
    print("=" * 60)
    print("TIMELINE RECONSTRUCTION")
    print("=" * 60)

    events = [

        f"8:30 PM - {victim['name']} arrives",

        "9:05 PM - Witness reports argument",

        "9:15 PM - Camera malfunction",

        "9:20 PM - Suspicious movement detected",

        "9:30 PM - Crime occurs",

        "9:45 PM - Body discovered"

    ]

    for event in events:
        print(event)

    print("=" * 60)


# =====================================================
# PLOT TWIST SYSTEM
# =====================================================

def reveal_plot_twist(case_data,
                      detective):

    print("\n")
    print("=" * 70)
    print("PLOT TWIST UNLOCKED")
    print("=" * 70)

    print(case_data["plot_twist"])

    detective.add_score(40)

    print("=" * 70)


# =====================================================
# ADVANCED CASE FILE DISPLAY
# =====================================================

def show_case_file(case_data):

    victim = case_data["victim"]

    print("\n")
    print("=" * 70)
    print("OFFICIAL CASE FILE")
    print("=" * 70)

    print(f"Case Type : {case_data['case_type']}")
    print(f"Victim    : {victim['name']}")
    print(f"Location  : {victim['location']}")
    print(f"Cause     : {victim['cause']}")

    print("\nPRIMARY SUSPECTS")

    for suspect in case_data["suspects"]:

        print(
            f"- {suspect['name']} "
            f"({suspect['profession']})"
        )

    print("=" * 70)


# =====================================================
# CHOOSE SUSPECT FOR INTERROGATION
# =====================================================

def choose_interrogation(case_data,
                         model,
                         evidence_board,
                         detective):

    display_suspects(case_data)

    try:

        choice = int(
            input("\nChoose suspect: ")
        )

        suspect = case_data["suspects"][choice - 1]

        interrogate_suspect_ai(
            model,
            suspect,
            evidence_board,
            detective
        )

    except:

        print("Invalid selection.")

 # =====================================================
# ACHIEVEMENT SYSTEM
# =====================================================

def check_achievements(detective):

    achievements = []

    if detective.score >= 100:
        achievements.append("Junior Investigator")

    if detective.score >= 300:
        achievements.append("Case Cracker")

    if detective.score >= 600:
        achievements.append("Elite Detective")

    if detective.score >= 1000:
        achievements.append("Legendary Investigator")

    return achievements


# =====================================================
# ACCUSATION SYSTEM
# =====================================================

def make_accusation(case_data,
                    detective,
                    suspicion):

    print("\n")
    print("=" * 60)
    print("MAKE AN ACCUSATION")
    print("=" * 60)

    display_suspects(case_data)

    try:

        choice = int(
            input("\nWho is the murderer? ")
        )

        accused = case_data["suspects"][choice - 1]

        culprit = case_data["culprit"]

        if accused["name"] == culprit:

            detective.add_score(200)

            print("\n")
            print("=" * 60)
            print("CASE SOLVED")
            print("=" * 60)

            print(
                f"You correctly identified "
                f"{culprit}!"
            )

            print("\nJustice has been served.")

            return True

        else:

            detective.add_score(-50)

            print("\nWRONG ACCUSATION!")

            print(
                f"{accused['name']} is innocent."
            )

            return False

    except:

        print("Invalid selection.")

        return False


# =====================================================
# CASE SUMMARY
# =====================================================

def show_case_summary(case_data,
                      detective):

    print("\n")
    print("=" * 70)
    print("CASE SUMMARY")
    print("=" * 70)

    print(f"Final Score : {detective.score}")
    print(f"Rank        : {detective.rank}")

    print("\nAchievements:")

    achievements = check_achievements(
        detective
    )

    if achievements:

        for item in achievements:
            print("🏆", item)

    else:
        print("None")

    print("\nActual Culprit:")
    print(case_data["culprit"])

    print("=" * 70)


# =====================================================
# SAVE CURRENT PROGRESS
# =====================================================

def create_save_data(case_data,
                     detective,
                     suspicion):

    return {

        "case_data": case_data,

        "score": detective.score,

        "rank": detective.rank,

        "inventory": detective.inventory,

        "clues": detective.clues,

        "suspicion": suspicion
    }


# =====================================================
# LOAD DETECTIVE DATA
# =====================================================

def restore_save_data(saved_data):

    detective = Detective()

    detective.score = saved_data["score"]

    detective.rank = saved_data["rank"]

    detective.inventory = saved_data["inventory"]

    detective.clues = saved_data["clues"]

    suspicion = saved_data["suspicion"]

    case_data = saved_data["case_data"]

    return detective, case_data, suspicion


# =====================================================
# MAIN INVESTIGATION MENU
# =====================================================

def investigation_menu():

    print("\n")
    print("=" * 70)
    print("INVESTIGATION MENU")
    print("=" * 70)

    print("1. View Case File")
    print("2. Investigate Crime Scene")
    print("3. Interview Witness")
    print("4. Interrogate Suspect")
    print("5. Search Suspect Property")
    print("6. Forensics Lab")
    print("7. Security Log Analysis")
    print("8. Evidence Board")
    print("9. Suspicion Meter")
    print("10. Inventory")
    print("11. Timeline Reconstruction")
    print("12. Reveal Plot Twist")
    print("13. Detective Profile")
    print("14. Save Game")
    print("15. Make Accusation")
    print("16. Quit")

    print("=" * 70)


# =====================================================
# NEW GAME
# =====================================================

def start_new_game(model):

    detective = Detective()

    evidence_board = EvidenceBoard()

    case_data = generate_case(model)

    if not case_data:

        print("Failed to generate case.")

        return

    suspicion = initialize_suspicion(
        case_data["suspects"]
    )

    game_loop(
        model,
        detective,
        evidence_board,
        case_data,
        suspicion
    )


# =====================================================
# LOAD GAME
# =====================================================

def continue_saved_game(model):

    save = load_game()

    if not save:

        print("\nNo save file found.")

        return

    detective, case_data, suspicion = \
        restore_save_data(save)

    evidence_board = EvidenceBoard()

    game_loop(
        model,
        detective,
        evidence_board,
        case_data,
        suspicion
    )


# =====================================================
# GAME LOOP
# =====================================================

def game_loop(model,
              detective,
              evidence_board,
              case_data,
              suspicion):

    twist_revealed = False

    while True:

        investigation_menu()

        choice = input(
            "\nChoose an action: "
        ).strip()

        if choice == "1":

            show_case_file(case_data)

        elif choice == "2":

            investigate_crime_scene(
                case_data,
                evidence_board,
                detective
            )

        elif choice == "3":

            interview_witness(
                case_data,
                evidence_board
            )

        elif choice == "4":

            choose_interrogation(
                case_data,
                model,
                evidence_board,
                detective
            )

        elif choice == "5":

            search_suspect(
                case_data,
                evidence_board,
                detective,
                suspicion
            )

        elif choice == "6":

            forensic_lab(
                case_data,
                detective,
                evidence_board,
                suspicion
            )

        elif choice == "7":

            analyze_security_logs(
                case_data,
                detective,
                evidence_board
            )

        elif choice == "8":

            evidence_board.display()

        elif choice == "9":

            display_suspicion(
                suspicion
            )

        elif choice == "10":

            show_inventory(
                detective
            )

        elif choice == "11":

            build_timeline(
                case_data
            )

        elif choice == "12":

            if not twist_revealed:

                reveal_plot_twist(
                    case_data,
                    detective
                )

                twist_revealed = True

            else:

                print(
                    "\nTwist already revealed."
                )

        elif choice == "13":

            detective.display()

        elif choice == "14":

            save_data = create_save_data(
                case_data,
                detective,
                suspicion
            )

            save_game(save_data)

        elif choice == "15":

            solved = make_accusation(
                case_data,
                detective,
                suspicion
            )

            if solved:

                show_case_summary(
                    case_data,
                    detective
                )

                break

        elif choice == "16":

            print(
                "\nInvestigation terminated."
            )

            break

        else:

            print(
                "\nInvalid option."
            )


# =====================================================
# MAIN MENU
# =====================================================

def main_menu():

    print("\n")
    print("=" * 70)
    print("AI DETECTIVE INVESTIGATION")
    print("=" * 70)

    print("1. New Case")
    print("2. Load Saved Case")
    print("3. Exit")

    print("=" * 70)


# =====================================================
# MAIN FUNCTION
# =====================================================

def main():

    title()

    try:

        print(
            "\nInitializing Gemini..."
        )

        model = setup_gemini()

    except Exception as e:

        print(
            "\nGemini setup failed:"
        )

        print(e)

        return

    while True:

        main_menu()

        choice = input(
            "\nSelect option: "
        ).strip()

        if choice == "1":

            start_new_game(
                model
            )

        elif choice == "2":

            continue_saved_game(
                model
            )

        elif choice == "3":

            print(
                "\nThanks for playing."
            )

            break

        else:

            print(
                "\nInvalid choice."
            )


# =====================================================
# ENTRY POINT
# =====================================================

if __name__ == "__main__":

    main()  
