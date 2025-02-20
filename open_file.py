from os import walk
from prettytable import PrettyTable 

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]


### **Readind the infos of the FA**
def keep_right_file(fileslist) :
    for i in fileslist :
        if not ".txt" in i:
            fileslist.remove(i)
    return fileslist

def read_fa(file) :
    f = open(file, "r")
    informations = []
    for i in f:
        informations.append(i.replace('\n', ''))
    f.close()
    return informations

def split_string(s):
    parts = s.split()
    count = int(parts[0])
    values = list(map(int, parts[1:1+count]))
    return count, values

def get_info(infos) :
    nb_letters = int(infos[0])
    nb_states = int(infos[1])
    nb_entry, pos_entry = split_string(infos[2])
    nb_terminal, pos_terminal = split_string(infos[3])
    nb_transitions = int(infos[4])
    list_transitions = infos[5:]
    return nb_letters, nb_states, nb_entry, pos_entry, nb_terminal, pos_terminal, nb_transitions, list_transitions

def print_fa_info(file):
    nb_letters, nb_states, nb_entry, pos_entry, nb_terminal, pos_terminal, nb_transitions, list_transitions = get_info(read_fa(file))
    print(f"Number of letters in the alphabet: {nb_letters}")
    print(f"Number of states: {nb_states}")
    print(f"Number of entry states: {nb_entry}")
    print("Entry state(s):")
    for entry in range(nb_entry):
        print(f"  - {pos_entry[entry]}")
    print(f"Number of terminal states: {nb_terminal}")
    print("Terminal state(s):")
    for terminal in range(nb_terminal):
        print(f"  - {pos_terminal[terminal]}")
    print(f"Number of transitions: {nb_transitions}")
    print("Transitions:")
    for transition in list_transitions:
        print(f"  - {transition}")
    print("-" * 40)


### **Displaying the FA informations in a table**
def create_fa_table(fa_info):
    nb_letters, nb_states, nb_entry, pos_entry, nb_terminal, pos_terminal, nb_transitions, list_transitions = fa_info
    col_list = ["", "States"] + alphabet[:nb_letters]
    myTable = PrettyTable(col_list)

    for state in range(nb_states):
        row = []
        if state in pos_entry and state not in pos_terminal:
            row.append("E")
        elif state in pos_terminal and state not in pos_entry:
            row.append("T")
        elif state in pos_entry and state in pos_terminal:
            row.append("E / T")
        else:
            row.append("")

        row.append(str(state))

        for letter in range(nb_letters):
            temp = [transition[2:] for transition in list_transitions if int(transition[0]) == state and transition[1] == alphabet[letter]]
            row.append(", ".join(temp) if temp else "-")

        myTable.add_row(row)

    return myTable

def print_fa_table(table):
    print(table)
    print("-" * 40)

### **Checking FA Properties**
def is_deterministic(fa_info):
    nb_letters, nb_states, _, _, _, _, _, list_transitions = fa_info
    for state in range(nb_states):
        for letter in range(nb_letters):
            transition_count = sum(1 for transition in list_transitions if int(transition[0]) == state and transition[1] == alphabet[letter])
            if transition_count > 1:
                return False
    return True

def is_complete(fa_info):
    nb_letters, nb_states, _, _, _, _, _, list_transitions = fa_info
    for state in range(nb_states):
        for letter in range(nb_letters):
            if not any(int(transition[0]) == state and transition[1] == alphabet[letter] for transition in list_transitions):
                return False
    return True

def check_standard(fa_info):
    return is_deterministic(fa_info) and is_complete(fa_info)

def print_fa_status(fa_info):
    if is_deterministic(fa_info):
        print("The FA is deterministic.")
    else:
        print("The FA is not deterministic.")

    if is_complete(fa_info):
        print("The FA is complete.")
    else:
        print("The FA is not complete.")

    if check_standard(fa_info):
        print("The FA is standard.")
    else:
        print("The FA is not standard.")


### **FA change **


### **Usage**
fa_info = get_info(read_fa("1.txt"))
table = create_fa_table(fa_info)

print_fa_info("1.txt")
print_fa_table(table)
print_fa_status(fa_info)