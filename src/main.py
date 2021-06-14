from file_handling import FileHandling
from preprocessing import PreProcessing
from automaton import Automaton
from interface import Interface

def main():
    
    file = Interface("../examples/").runningGui()
    

    file_handler = FileHandling("../examples/"+file)
    dict_raw = file_handler.get_raw_input()
    

    pre_process = PreProcessing(dict_raw)
    dict_components = pre_process.components
    list_rules = pre_process.rules
    

    print(dict_components, end='\n\n')
    for i in list_rules:
        print(i)


    Automaton(dict_components,list_rules).execute()
    
    input("Press Enter")

if __name__ == "__main__":
    main()