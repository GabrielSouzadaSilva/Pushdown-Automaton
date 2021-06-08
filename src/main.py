from file_handling import FileHandling
from preprocessing import PreProcessing
from automaton import Automaton

def main():
    file_handler = FileHandling("../examples/02")
    dict_raw = file_handler.get_raw_input()
    
    print(dict_raw)

    pre_process = PreProcessing(dict_raw)
    dict_components = pre_process.components
    list_rules = pre_process.rules
    

    print(dict_components, end='\n\n')
    print(list_rules)
    
    word = 'abba'
    Automaton(word, dict_components,list_rules).execute()

if __name__ == "__main__":
    main()