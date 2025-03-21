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
    nb_letters = infos[0]
    nb_states = infos[1]
    nb_entry, pos_entry = split_string(infos[2])
    nb_terminal, pos_terminal = split_string(infos[3])
    nb_transitions = infos[4]
    list_transitions = infos[5:]
    return int(nb_letters), int(nb_states), int(nb_entry), pos_entry, int(nb_terminal), pos_terminal, int(nb_transitions), list_transitions

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


    states = [str(state) for state in range(nb_states)]
    if "i" in pos_entry:
        states.insert(0, "i")

    for state in states:
        row = []
        if state in map(str, pos_entry) and state not in map(str, pos_terminal):
            row.append("E")
        elif state in map(str, pos_terminal) and state not in map(str, pos_entry):
            row.append("T")
        elif state in map(str, pos_entry) and state in map(str, pos_terminal):
            row.append("E / T")
        else:
            row.append("")

        row.append(state)

        for letter in range(nb_letters):
            temp = [transition[2:] for transition in list_transitions if transition[0] == str(state) and transition[1] == alphabet[letter]]
            row.append(", ".join(temp) if temp else "-")

        myTable.add_row(row)

    return myTable

def print_fa_table(table):
    print(table)
    print("-" * 40)



### **Checking FA Properties**
def is_deterministic(fa_info):
    nb_letters, nb_states, nb_entry, pos_entry, nb_terminal, pos_terminal, nb_transitions, list_transitions = fa_info
    set_transitions = set(list_transitions)

    if len(set_transitions) != nb_transitions:
        print("Some of your transition are multiple times in the file")

    for state in range(nb_states):
        determinize = True
        for letter in range(nb_letters):
            transition_count = sum(1 for transition in list_transitions if transition[0] == str(state) and transition[1] == alphabet[letter])
            if transition_count > 1:
                print(f"Not deterministic: State {state} has {transition_count} transitions on symbol '{alphabet[letter]}'.")
                determinize = False
    return determinize

def is_complete(fa_info):
    complete = True
    nb_letters, nb_states, nb_entry, pos_entry, nb_terminal, pos_terminal, nb_transitions, list_transitions = fa_info
    for state in range(nb_states):
        for letter in range(nb_letters):
            if not any(transition[0] == str(state) and transition[1] == alphabet[letter] for transition in list_transitions):
                print(f"Not complete: Missing transition from state {state} with letter '{alphabet[letter]}'")
                complete = False
    return complete

def check_standard(fa_info):
    nb_letters, nb_states, nb_entry, pos_entry, nb_terminal, pos_terminal, nb_transitions, list_transitions = fa_info
    state, temp = True, False
    if nb_entry > 1:
        print(f"Not standard : There are {nb_entry} entries : you must have a unique entry.")
        state = False
    for i in range(nb_transitions):
        if int(list_transitions[i][2]) in pos_entry:
            state, temp = False, True
    if temp:
        print("Not standard : There are some states that have a path leading to the entry state.")
    return state

def print_fa_status(fa_info):
    if is_deterministic(fa_info):
        print("The FA is deterministic.")
    if is_complete(fa_info):
        print("The FA is complete.")
    if check_standard(fa_info):
        print("The FA is standard.")
        
    print("-" * 40)



### **FA change **
def standardization(fa_info):
    nb_letters, nb_states, nb_entry, pos_entry, nb_terminal, pos_terminal, nb_transitions, list_transitions = fa_info

    new_initial_state = "i"
    list_new_transitions = []

    for state_entry in pos_entry:
        for transition in list_transitions:
            if (transition[0] == str(state_entry)) and (new_initial_state + transition[1:] not in list_new_transitions) :
                list_new_transitions.append((new_initial_state + transition[1:]))
    
    for i in list_transitions:
        list_new_transitions.append(i)

    nb_new_states = nb_states + 1
    nb_new_transitions = len(list_new_transitions)

    return nb_letters, nb_new_states, 1, [new_initial_state], nb_terminal, pos_terminal, nb_new_transitions, list_new_transitions

def completion(fa_info):
    if not is_complete(fa_info):
        nb_letters, nb_states, nb_entry, pos_entry, nb_terminal, pos_terminal, nb_transitions, list_transitions = fa_info
        nb_states +=1 #rajout de l'état P
        #rajout de ses transitions
        for i in range(nb_letters):
            transition = f"P{alphabet[i]}P"
            list_transitions.append(transition)
            nb_transitions +=1
        #rajout des transitions incomplete
        for state in range(nb_states-1): #on doit soutraire 1 car sinon cela rajoute un état indésirable 
            for letter in range(nb_letters):
                if not any(transition[0] == str(state) and transition[1] == alphabet[letter] for transition in list_transitions):
                    list_transitions.append(f"{state}{alphabet[letter]}P")
                    nb_transitions+=1
        for transition in list_transitions:
            print(f"  - {transition}")
        print("-" * 40)
        print_fa_table(create_fa_table(fa_info))
    else :
        print("your table is already completed ^^")

def determinization_and_completion(fa_info):
    if is_complete(fa_info) and is_deterministic(fa_info):
        print("your automata is already deterministic and complete")
    else:
        if is_deterministic(fa_info):
            print("your automata is now completed")
            completion(fa_info)
        if is_complete(fa_info):
            determiniaztion(fa_info)
        else:
            completion(fa_info)
            determiniaztion(fa_info)

def determiniaztion(fa_info):
    if not is_deterministic(fa_info):
        nb_letters, nb_states, nb_entry, pos_entry, nb_terminal, pos_terminal, nb_transitions, list_transitions = fa_info
        new_nb_states = 0
        new_nb_entry = 1
        new_pos_entry = []
        new_nb_terminal = 0
        new_pos_terminal = []
        new_nb_transitions = 0
        new_list_transitions = []
        if (nb_entry > 1):
            entry=""
            for i in pos_entry:
                entry +=str(i)
            new_pos_entry.append(entry)
        else:
            new_pos_entry = pos_entry
        new_nb_states +=1

        transition_int = []
        for state in new_pos_entry[0]:
            for transition in list_transitions:
                if state == transition[0]:
                    for letter in range(nb_letters):
                        if transition[1] == alphabet[letter] and transition[2:] not in a:
                            a.append(transition[2:])
                        
                    
        if a != [] and b != [] :
            new_list_transitions.append(f"{new_pos_entry[0]}a{trans_a}")
            new_list_transitions.append(f"{new_pos_entry[0]}b{trans_b}")
        for i in new_list_transitions:
            print(i)

def int_to_roman(num):
    roman_numerals = {
        1000: "M", 900: "CM", 500: "D", 400: "CD",
        100: "C", 90: "XC", 50: "L", 40: "XL",
        10: "X", 9: "IX", 5: "V", 4: "IV", 1: "I"
    }

    roman_string = ""

    for value, symbol in roman_numerals.items():
        while num >= value:
            roman_string += symbol
            num -= value  # Reduce the number

    return roman_string

def minimization(cdfa_info):
    nb_letters, nb_states, nb_entry, pos_entry, nb_terminal, pos_terminal, nb_transitions, list_transitions = cdfa_info
    t = []
    nt = []

    # filling of the terminal and non-terminal lists
    for state in nb_states:
        if str(state) in map(str, pos_terminal):
            t.append(state)
        else:
            nt.append(state)

    term_info = []
    non_term_info = []
    partition_table = []

    # creating transition lists to partition further
    for state in t:
        term_info.append([state])
        for transition in list_transitions:
            if state == transition[0]:
                if transition[2:] in t:
                    term_info[-1].extend([str(transition[2:]), "t"])
                else:
                    term_info[-1].extend([str(transition[2:]), "nt"])
    partition_table.append(term_info)

    for state in nt:
        non_term_info.append([state])
        for transition in list_transitions:
            if state == transition[0]:
                if transition[2:] in t:
                    non_term_info[-1].extend([str(transition[2:]), "t"])
                else:
                    non_term_info[-1].extend([str(transition[2:]), "nt"])
    partition_table.append(non_term_info)

    final_partition = []

    for table in partition_table: #study of each table to create the final repartition
        final_partition.append([str(int_to_roman(len(final_partition)+1)), "", ""])
        for state in table:
            for partition in final_partition:
                if state[2]+state[4] in partition:
                    partition[1] += state[0]
                else:
                    if state == table[0]:
                        partition[1] = state[0]
                        partition[2] = state[2]+state[4]
                    else :
                        final_partition.append([str(int_to_roman(len(final_partition) + 1)), state[0], state[2] + state[4]])

    return final_partition





def recognize_word(fa_info, word):
 
    nb_letters, nb_states, nb_entry, pos_entry, nb_terminal, pos_terminal, nb_transitions, list_transitions = fa_info

    # Convert current states -> into strings
    current_states = [str(state) for state in pos_entry]

    # Travel the word
    for letter in word:
        next_states = []
        for state in current_states:
            for transition in list_transitions:
                if transition[0] == state and transition[1] == letter:
                    if transition[2:] not in next_states:
                        next_states.append(transition[2:])  
        if not next_states:
            return False

        current_states = next_states
    #check if final states
    return any(state in [str(s) for s in pos_terminal] for state in current_states)


def test_recognize_word(fa_info):
    print("\n Type a word to test (or type 'end') :")

    while True:
        word = input() # read the word
        if word.lower() == "end":
            break

        if recognize_word(fa_info, word):
            print(f"Yes, '{word}' is recognizable by the automata")
        else:
            print(f"No, '{word}' is not recognizable by the automata")


### **Usage**
file = "./automatas/39.txt"
fa_info = get_info(read_fa(file))
standardized_fa_info = standardization(fa_info)
table = create_fa_table(fa_info)
standardized_table = create_fa_table(standardized_fa_info)

print_fa_info(file)
print_fa_table(table)
print_fa_status(fa_info)

print_fa_table(standardized_table)
test_recognize_word(fa_info)
