import random
import streamlit as st

st.set_page_config(
    page_title="Detective Mystery",
    page_icon="🕵️‍♀️",
    layout="wide",
)

if "game_initialized" not in st.session_state:
    st.session_state["game_initialized"] = False


class Detective:
    def __init__(self):
        self.score = 0
        self.rank = "Rookie Detective"
        self.inventory = []
        self.clues = []
        self.suspicions = {}

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

    def add_inventory(self, item):
        if item not in self.inventory:
            self.inventory.append(item)

    def add_clue(self, clue):
        if clue not in self.clues:
            self.clues.append(clue)


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


def default_case():
    return {
        "case_type": "High Society Poisoning",
        "victim": {
            "name": "Elena Harrington",
            "location": "Harrington Manor",
            "cause": "Mysterious poison"
        },
        "culprit": "Damien Carter",
        "crime_scene_clues": [
            "Broken glass with powdered residue",
            "A napkin with fingerprints",
            "A spilled guest list with a missing name"
        ],
        "witnesses": [
            {"name": "Grace Bennett", "statement": "I saw Damien argue with Elena over the will."},
            {"name": "Marcus Reed", "statement": "Someone poured a drink near the conservatory table."},
            {"name": "Fiona Cole", "statement": "The lights flickered just before the victim collapsed."}
        ],
        "suspects": [
            {
                "name": "Damien Carter",
                "profession": "Finance Executive",
                "motive": "Inheritance and hidden debt",
                "alibi": "Claimed to be in the library writing notes.",
                "clues": [
                    "Secret transfer from Elena's account",
                    "A torn invitation with Damien's initials"
                ]
            },
            {
                "name": "Lydia Monroe",
                "profession": "Event Planner",
                "motive": "Jealousy over a rejected partnership",
                "alibi": "Said she was organizing the reception in the kitchen.",
                "clues": [
                    "Managerial email about guest seating",
                    "Her perfume was near the service entrance"
                ]
            },
            {
                "name": "Nathan Vale",
                "profession": "Art Dealer",
                "motive": "Blackmail over forged artwork",
                "alibi": "Said he stepped outside to take a phone call.",
                "clues": [
                    "A suspicious receipt for rare poison delivery",
                    "A letter from Elena warning about him"
                ]
            },
            {
                "name": "Olivia Grant",
                "profession": "Celebrity Chef",
                "motive": "Anger at Elena for canceling a restaurant opening",
                "alibi": "Claimed to be in the kitchen prepping dessert.",
                "clues": [
                    "A broken spice jar with traces of toxin",
                    "A guest complaint from dinner service"
                ]
            }
        ],
        "plot_twist": "A hidden will clause reveals the victim planned to spare the entire household from bankruptcy, making the crime more personal than financial."
    }


def initialize_game():
    st.session_state["detective"] = Detective()
    st.session_state["evidence_board"] = EvidenceBoard()
    st.session_state["case_data"] = default_case()
    st.session_state["suspicion"] = {s["name"]: 0 for s in st.session_state["case_data"]["suspects"]}
    st.session_state["twist_revealed"] = False
    st.session_state["solved"] = False
    st.session_state["activity_log"] = []
    st.session_state["game_initialized"] = True


def add_activity(message):
    st.session_state["activity_log"].insert(0, message)


def investigate_crime_scene():
    for clue in st.session_state["case_data"]["crime_scene_clues"]:
        st.session_state["evidence_board"].add_physical(clue)
        st.session_state["detective"].add_clue(clue)
        st.session_state["detective"].add_score(10)
    add_activity("Investigated the crime scene and collected physical evidence.")


def interview_witness(index):
    witness = st.session_state["case_data"]["witnesses"][index]
    st.session_state["evidence_board"].add_statement(witness["statement"])
    st.session_state["detective"].add_score(15)
    add_activity(f"Interviewed witness {witness['name']}.")


def search_suspect(index):
    suspect = st.session_state["case_data"]["suspects"][index]
    evidence = random.choice([
        f"Bank records linked to {suspect['name']}",
        f"Deleted messages found on {suspect['name']}'s phone",
        f"Security keycard owned by {suspect['name']}",
        f"Suspicious receipt belonging to {suspect['name']}",
        f"Photograph connecting {suspect['name']} to the victim"
    ])
    st.session_state["evidence_board"].add_suspect_clue(evidence)
    st.session_state["detective"].add_clue(evidence)
    st.session_state["detective"].add_score(20)
    st.session_state["suspicion"][suspect["name"]] = min(100, st.session_state["suspicion"][suspect["name"]] + 15)
    add_activity(f"Searched {suspect['name']}'s property and found evidence.")


def forensic_lab(option):
    culprit = st.session_state["case_data"]["culprit"]
    if option == "Fingerprint Analysis":
        result = f"Fingerprint partially matches {culprit}."
        score = 30
        suspicion_gain = 20
    elif option == "DNA Analysis":
        result = f"DNA traces connect to {culprit}."
        score = 35
        suspicion_gain = 25
    elif option == "Footprint Analysis":
        result = f"Footprint size matches {culprit}."
        score = 20
        suspicion_gain = 10
    else:
        result = f"Coffee cup contains fingerprints of {culprit}."
        score = 25
        suspicion_gain = 15

    st.session_state["evidence_board"].add_physical(result)
    st.session_state["detective"].add_score(score)
    st.session_state["suspicion"][culprit] = min(100, st.session_state["suspicion"][culprit] + suspicion_gain)
    add_activity(f"Completed {option.lower()} in forensics.")


def analyze_security_logs():
    logs = [
        "Camera outage occurred at 9:15 PM.",
        f"Shadowy figure resembles {st.session_state['case_data']['culprit']}.",
        "Security access door opened twice.",
        "Motion detected near the vault."
    ]
    for log in logs:
        st.session_state["evidence_board"].add_physical(log)
    st.session_state["detective"].add_score(20)
    add_activity("Reviewed security camera logs.")


def reveal_plot_twist():
    st.session_state["twist_revealed"] = True
    st.session_state["detective"].add_score(40)
    add_activity("Unlocked the plot twist.")


def make_accusation(choice):
    accused = st.session_state["case_data"]["suspects"][choice]
    culprit = st.session_state["case_data"]["culprit"]
    if accused["name"] == culprit:
        st.session_state["detective"].add_score(200)
        st.session_state["solved"] = True
        add_activity(f"Accused {accused['name']} and solved the case.")
        return True
    st.session_state["detective"].add_score(-50)
    st.session_state["suspicion"][accused["name"]] = max(0, st.session_state["suspicion"][accused["name"]] - 10)
    add_activity(f"Accused {accused['name']}. The accusation was incorrect.")
    return False


def show_sidebar():
    st.sidebar.title("🕵️‍♀️ Detective Toolkit")
    st.sidebar.markdown("***")
    st.sidebar.subheader("Current Case")
    st.sidebar.write(st.session_state["case_data"]["case_type"])
    st.sidebar.subheader("Detective Profile")
    st.sidebar.write(f"**Rank:** {st.session_state['detective'].rank}")
    st.sidebar.write(f"**Score:** {st.session_state['detective'].score}")
    st.sidebar.write(f"**Clues:** {len(st.session_state['detective'].clues)}")
    st.sidebar.markdown("***")

    st.sidebar.subheader("Actions")
    if st.sidebar.button("Investigate Crime Scene"):
        investigate_crime_scene()
    if st.sidebar.button("Review Security Logs"):
        analyze_security_logs()
    if st.sidebar.button("Reveal Plot Twist"):
        reveal_plot_twist()

    st.sidebar.markdown("***")
    if st.sidebar.button("Reset Case"):
        initialize_game()
        st.experimental_rerun()

    st.sidebar.markdown("***")
    st.sidebar.caption("A detective-themed murder mystery with suspect cards, evidence display, and interactive investigation.")


def render_suspect_cards():
    st.subheader("Suspect Wall")
    suspects = st.session_state["case_data"]["suspects"]
    cols = st.columns(4)
    for index, suspect in enumerate(suspects):
        with cols[index]:
            st.markdown(f"### {suspect['name']}")
            st.write(f"**Profession:** {suspect['profession']}")
            st.write(f"**Motive:** {suspect['motive']}")
            st.write(f"**Alibi:** {suspect['alibi']}")
            progress_value = st.session_state["suspicion"][suspect['name']]
            st.progress(progress_value / 100)
            st.caption(f"Suspicion {progress_value}%")
            if st.button(f"Search {suspect['name']}", key=f"search_{index}"):
                search_suspect(index)


def render_case_overview():
    case = st.session_state["case_data"]
    st.markdown("## Case File")
    st.write(f"**Victim:** {case['victim']['name']}")
    st.write(f"**Location:** {case['victim']['location']}")
    st.write(f"**Cause:** {case['victim']['cause']}")
    st.write(f"**Case Type:** {case['case_type']}")


def render_actions():
    tabs = st.tabs(["Evidence Board", "Witnesses", "Forensics", "Timeline", "Accuse"])

    with tabs[0]:
        st.markdown("### Evidence Board")
        board = st.session_state["evidence_board"]
        st.write("**Physical Evidence**")
        for item in board.physical_evidence or ["No physical evidence collected yet."]:
            st.write(f"- {item}")
        st.write("**Witness Statements**")
        for item in board.witness_statements or ["No witness statements collected yet."]:
            st.write(f"- {item}")
        st.write("**Suspect Clues**")
        for item in board.suspect_clues or ["No suspect clues discovered yet."]:
            st.write(f"- {item}")

    with tabs[1]:
        st.markdown("### Witness Interviews")
        witnesses = st.session_state["case_data"]["witnesses"]
        for idx, witness in enumerate(witnesses):
            if st.button(f"Interview {witness['name']}", key=f"wit_{idx}"):
                interview_witness(idx)
        st.markdown("#### Witness Notes")
        for statement in st.session_state["evidence_board"].witness_statements or ["No interviews yet."]:
            st.write(f"- {statement}")

    with tabs[2]:
        st.markdown("### Forensics Lab")
        for option in [
            "Fingerprint Analysis",
            "DNA Analysis",
            "Footprint Analysis",
            "Coffee Cup Analysis"
        ]:
            if st.button(option, key=f"forensic_{option}"):
                forensic_lab(option)
        st.markdown("#### Current Forensic Evidence")
        for item in st.session_state["evidence_board"].physical_evidence or ["No forensic evidence yet."]:
            st.write(f"- {item}")

    with tabs[3]:
        st.markdown("### Timeline Reconstruction")
        events = [
            f"8:30 PM - {st.session_state['case_data']['victim']['name']} arrives.",
            "9:05 PM - Tension grows during dinner.",
            "9:15 PM - Power flickers in the conservatory.",
            "9:20 PM - A conversation erupts near the buffet.",
            "9:30 PM - The victim collapses.",
            "9:45 PM - The body is discovered."
        ]
        for event in events:
            st.write(f"- {event}")

    with tabs[4]:
        st.markdown("### Make an Accusation")
        suspects = st.session_state["case_data"]["suspects"]
        choice = st.radio("Select the guilty party:", [s["name"] for s in suspects])
        if st.button("Accuse"):
            accused_index = next(i for i, s in enumerate(suspects) if s["name"] == choice)
            solved = make_accusation(accused_index)
            if solved:
                st.success(f"Case solved! {choice} is the culprit.")
            else:
                st.error(f"Incorrect accusation against {choice}.")
        if st.session_state["solved"]:
            st.markdown("### Case Summary")
            st.write(f"**Final Score:** {st.session_state['detective'].score}")
            st.write(f"**Rank:** {st.session_state['detective'].rank}")
            st.write(f"**Actual Culprit:** {st.session_state['case_data']['culprit']}")


def render_activity_log():
    st.subheader("Investigation Log")
    for entry in st.session_state["activity_log"][:10] or ["No activity yet."]:
        st.write(f"- {entry}")


def render_inventory():
    st.sidebar.markdown("### Inventory")
    if st.session_state["detective"].inventory:
        for item in st.session_state["detective"].inventory:
            st.sidebar.write(f"- {item}")
    else:
        st.sidebar.write("No items in inventory.")
    st.sidebar.markdown("### Achievements")
    achievements = []
    score = st.session_state["detective"].score
    if score >= 100:
        achievements.append("Junior Investigator")
    if score >= 300:
        achievements.append("Case Cracker")
    if score >= 600:
        achievements.append("Elite Detective")
    if score >= 1000:
        achievements.append("Legendary Investigator")
    if achievements:
        for achievement in achievements:
            st.sidebar.write(f"- {achievement}")
    else:
        st.sidebar.write("No achievements yet.")


def apply_theme():
    st.markdown(
        """
        <style>
        body {background-color: #121212; color: #f5f5f5; }
        .stApp {background-image: linear-gradient(135deg, #1b1b2f 0%, #0f3460 100%); }
        .css-15tx938 {background-color: rgba(0,0,0,0.45);}
        .stButton>button {background-color: #ff4b5c; color: white; border:none; }
        .stButton>button:hover {background-color: #ff7a76; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    if not st.session_state["game_initialized"]:
        initialize_game()

    apply_theme()

    st.markdown("# 🕵️ Detective Mystery Investigation")
    st.markdown("Welcome detective. Use your intuition, evidence board, and suspect cards to crack the case.")

    show_sidebar()
    render_case_overview()
    render_suspect_cards()
    render_actions()
    render_activity_log()
    render_inventory()


if __name__ == "__main__":
    main()
