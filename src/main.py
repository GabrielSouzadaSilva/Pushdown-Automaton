from file_handling import FileHandling

def main():
    file_handler = FileHandling("../examples/01")
    dict_raw = file_handler.get_raw_input()
    
    print(dict_raw)

if __name__ == "__main__":
    main()