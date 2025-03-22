from functions import *

import os

def list_automata_files():
    path = "./automatas" #search the automatas in the repo
    try:
        files = next(walk(path), (None, None, []))[2]
        files_txt = keep_right_file(files)
        files_txt.sort()
        return files_txt
    except Exception as e:
        print(f"Error reading automatas folder : {e}")
        return []

def choose_automaton():
    files = list_automata_files()
    if not files:
        print("No automata files found in ./automatas/")
        return None
    while True:
        try:
            choice = int(input("\nWhich FA do you want to use? (Enter number between 01 and 44) : "))
            if 1 <= choice <= len(files):
                return os.path.join("./automatas", files[choice - 1])
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")

def main_menu():
    while True:
        file_path = choose_automaton()
        if file_path is None:
            return
        fa_info = get_info(read_fa(file_path))

        while True:
            print("\n--- SUPER MAIN MENU FOR FINITE AUTOMATA PROJECT ---")
            print("1. Display FA information")
            print("2. Display transition table")
            print("3. Check if standard / deterministic / complete")
            print("4. Standardize automaton")
            print("5. Determinize and/or complete automaton") #need to modified with complete function
            print("6. Minimize automaton") #need to modified with complete function
            print("7. Test word recognition")
            print("8. Choose another FA")
            print("0. Exit")
            choice = input("Enter your choice : ")

            if choice == "1":
                print_fa_info(file_path)
            elif choice == "2":
                table = create_fa_table(fa_info)
                print_fa_table(table)
            elif choice == "3":
                print_fa_status(fa_info)
            elif choice == "4":
                fa_info = standardization(fa_info)
                print("Automaton standardized.")
                print_fa_table(create_fa_table(fa_info))
            elif choice == "5":
                fa_info = determinization_and_completion(fa_info)
                print("Now the automaton is determinized and completed.")
                print_fa_table(create_fa_table(fa_info))
            elif choice == "6":
                print("Minimization result : ")
                partitions = minimization(fa_info)
                for part in partitions:
                    print(part)
            elif choice == "7":
                test_recognize_word(fa_info)
            elif choice == "8":
                break
            elif choice == "0":
                return
            else:
                print("Invalid option.")

if __name__ == "__main__":
    main_menu()