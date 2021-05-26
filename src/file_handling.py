from pathlib import Path
import re

class FileHandling():
    
    
    def __init__(self, path_to_file: str):
        
        self.absolute_filename = Path(path_to_file)
        
        if self.absolute_filename.exists():
            self.file = open(self.absolute_filename)
        else:
            raise ValueError("Invalid path to file")
        
        self.raw_input = self.fill_raw_input()
        
        if self.verify_pattern():
            print("File handler created successfully.")
        else:
            raise ValueError("Input does not match pattern. File handler was not created.")
        
    
    def print(self):
        print(self.absolute_filename)
    
    
    def fill_raw_input(self) -> dict:
        dict_input = dict()
        lines = self.file.readlines()
        
        dict_input["Components"] = lines[0][:-1]
        dict_input["Rules"] = [line for line in lines[1:]]
        
        return dict_input
    
    
    def verify_pattern(self) -> bool:
        comp_pattern = re.compile(r"\(\{([a-z],\s*)*[a-z]\},\s*\{(q(\d+|f),\s*)*q(\d+|f)\},\s*D,\s*q\d+,\s*\{(q(\d+|f),\s*)*q(\d+|f)\},\s*\{([A-Z],\s*)*[A-Z]\}\)")
        rule_pattern = re.compile(r"q(\d+|f),\s*[a-z?],\s*[A-Z?-],\s*q(\d+|f),\s*[A-Z-]")
        
        if not re.match(comp_pattern, self.raw_input["Components"]):
            return False
        
        for rule in self.raw_input["Rules"]:
            if not re.match(rule_pattern, rule):
                return False
        
        return True
    
    
    def get_raw_input(self) -> dict:
        return self.raw_input